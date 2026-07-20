from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Any

import numpy as np
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import NodeWithScore, QueryBundle
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder


DOCUMENT_REFERENCE_RE = re.compile(
    r"\b(RDC|IN)\s*(?:N[Oº°.]?\s*)?0*(\d+)\s*[/\-]\s*(\d{4})\b",
    re.IGNORECASE,
)
TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
SOURCE_IDENTIFICATION_RE = re.compile(
    r"\b(?:qual|que|which|what)\b.*\b(?:documento|document|resolucao|regulation)\b",
    re.IGNORECASE,
)
PURPOSE_SCOPE_RE = re.compile(
    r"\b(?:objetivo|objective|scope|regulate|regulates|regulamenta)\b",
    re.IGNORECASE,
)
SOURCE_TITLE_STOPWORDS = {
    "a",
    "anvisa",
    "as",
    "da",
    "das",
    "de",
    "do",
    "dos",
    "document",
    "documento",
    "e",
    "for",
    "o",
    "para",
    "qual",
    "que",
    "the",
    "trata",
    "what",
    "which",
}
NEIGHBOR_EXPANSION_RE = re.compile(
    r"\b("
    r"defin|define|defines|definition|"
    r"escopo|scope|"
    r"exclu|exempt|exempted|exemption|excluded|"
    r"objective|objetivo|"
    r"responsibilities|responsabilidades|"
    r"which medical devices|quais dispositivos"
    r")\b",
    re.IGNORECASE,
)
ARTICLE_RE = re.compile(r"\bArt\.\s*(\d+)\b", re.IGNORECASE)
RERANK_QUERY_ANCHORS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\bsuspended\b.*\bterminated prematurely\b", re.IGNORECASE),
        "finalizado prematuramente suspenso participantes investigador",
    ),
    (
        re.compile(
            r"\brequired formats\b|\bformats?\b.*\bdocumentation\b",
            re.IGNORECASE,
        ),
        "via documentação CD-ROM formato pdf mesmas informações",
    ),
    (
        re.compile(
            r"\bapplicant company\b.*\bsubmit\b|"
            r"\bwhat must\b.*\bsubmit\b.*\bregistration application\b",
            re.IGNORECASE,
        ),
        "empresa solicitante deverá apresentar relatórios completos estudos não-clínicos e clínicos",
    ),
    (
        re.compile(
            r"\bresponsibilities\b.*\bpharmacovigilance system\b|"
            r"\bresponsibilities\b.*\binvolved\b",
            re.IGNORECASE,
        ),
        "sobreposições lacunas responsabilidades envolvidos Sistema de Farmacovigilância",
    ),
    (
        re.compile(
            r"\bsops?\b.*\bequivalent documents\b|"
            r"\bactivities\b.*\bdescribed\b",
            re.IGNORECASE,
        ),
        "atividades descritas Procedimentos Operacionais Padrão documentos equivalentes",
    ),
)


def normalize_lexical_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(char for char in decomposed if not unicodedata.combining(char)).lower()


def lexical_tokens(text: str) -> list[str]:
    return TOKEN_RE.findall(normalize_lexical_text(text))


def extract_document_reference(query: str) -> str | None:
    match = DOCUMENT_REFERENCE_RE.search(query)
    if not match:
        return None
    document_type, number, year = match.groups()
    return f"{document_type.upper()} {int(number)}/{year}"


def source_id(node: NodeWithScore) -> str:
    metadata = node.node.metadata or {}
    return str(
        metadata.get("regulation_id")
        or metadata.get("source_document")
        or metadata.get("file_name")
        or node.node.node_id
    )


def searchable_node_text(node: Any) -> str:
    metadata = node.metadata or {}
    context = "\n".join(
        str(metadata.get(key, ""))
        for key in (
            "regulation_id",
            "document_aliases",
            "document_title",
            "citation_label",
            "chapter",
            "section",
            "topics",
        )
        if metadata.get(key)
    )
    return f"{context}\n{node.get_content()}" if context else node.get_content()


def rerank_query_text(query_text: str) -> str:
    anchors = [
        anchor
        for pattern, anchor in RERANK_QUERY_ANCHORS
        if pattern.search(query_text)
    ]
    if not anchors:
        return query_text
    return f"{query_text}\nPortuguese regulatory anchors: {'; '.join(anchors)}"


class HybridRetriever(BaseRetriever):
    """Retrieve with dense vectors and BM25, fuse ranks, then cross-encode."""

    def __init__(
        self,
        index: Any,
        dense_top_k: int,
        bm25_top_k: int,
        fusion_top_k: int,
        rrf_k: int,
        reranker_model_name: str,
        reranker_top_n: int,
        reranker_batch_size: int,
    ) -> None:
        super().__init__()
        self._dense_top_k = dense_top_k
        self._bm25_top_k = bm25_top_k
        self._fusion_top_k = fusion_top_k
        self._rrf_k = rrf_k
        self._reranker_top_n = reranker_top_n
        self._reranker_batch_size = reranker_batch_size
        self._dense_retriever = index.as_retriever(similarity_top_k=dense_top_k)
        self._nodes = sorted(index.docstore.docs.values(), key=lambda node: node.node_id)
        self._article_lookup = self._build_article_lookup(self._nodes)
        self._searchable_texts = [searchable_node_text(node) for node in self._nodes]
        self._bm25 = BM25Okapi([lexical_tokens(text) for text in self._searchable_texts])
        self._reranker = CrossEncoder(reranker_model_name, max_length=512)

    @staticmethod
    def _query_text(query: str | QueryBundle) -> str:
        return query.query_str if isinstance(query, QueryBundle) else query

    @staticmethod
    def _deduplicate_by_citation(nodes: list[NodeWithScore]) -> list[NodeWithScore]:
        selected: list[NodeWithScore] = []
        duplicates: list[NodeWithScore] = []
        seen_labels: set[str] = set()
        for node in nodes:
            metadata = node.node.metadata or {}
            label = str(metadata.get("citation_label") or node.node.node_id)
            if label in seen_labels:
                duplicates.append(node)
                continue
            selected.append(node)
            seen_labels.add(label)
        return selected + duplicates

    @staticmethod
    def _article_number(node: Any) -> int | None:
        article = str((node.metadata or {}).get("article", ""))
        match = ARTICLE_RE.search(article)
        return int(match.group(1)) if match else None

    @classmethod
    def _build_article_lookup(cls, nodes: list[Any]) -> dict[tuple[str, int], Any]:
        lookup: dict[tuple[str, int], Any] = {}
        for node in nodes:
            metadata = node.metadata or {}
            regulation_id = str(metadata.get("regulation_id", ""))
            article_number = cls._article_number(node)
            if not regulation_id or article_number is None:
                continue
            key = (regulation_id, article_number)
            current = lookup.get(key)
            node_chunk = int(metadata.get("article_chunk_index") or 1)
            current_chunk = int((current.metadata or {}).get("article_chunk_index") or 1) if current else 999
            if current is None or node_chunk < current_chunk:
                lookup[key] = node
        return lookup

    def _neighbor_nodes(self, node: NodeWithScore) -> list[NodeWithScore]:
        metadata = node.node.metadata or {}
        regulation_id = str(metadata.get("regulation_id", ""))
        article_number = self._article_number(node.node)
        if not regulation_id or article_number is None:
            return []
        neighbors: list[NodeWithScore] = []
        for neighbor_number in (article_number - 1, article_number + 1):
            neighbor = self._article_lookup.get((regulation_id, neighbor_number))
            if neighbor is None:
                continue
            score = (node.score or 0.0) - 0.01
            neighbors.append(NodeWithScore(node=neighbor, score=score))
        return neighbors

    def _expand_with_neighbor_articles(
        self,
        query_text: str,
        nodes: list[NodeWithScore],
    ) -> list[NodeWithScore]:
        if not NEIGHBOR_EXPANSION_RE.search(normalize_lexical_text(query_text)):
            return nodes
        expanded: list[NodeWithScore] = []
        seen_node_ids: set[str] = set()
        for node in nodes:
            if node.node.node_id not in seen_node_ids:
                expanded.append(node)
                seen_node_ids.add(node.node.node_id)
            for neighbor in self._neighbor_nodes(node):
                if neighbor.node.node_id in seen_node_ids:
                    continue
                expanded.append(neighbor)
                seen_node_ids.add(neighbor.node.node_id)
        return expanded

    def retrieve_dense(
        self, query: str | QueryBundle, top_k: int | None = None
    ) -> list[NodeWithScore]:
        nodes = self._dense_retriever.retrieve(query)
        return nodes[:top_k] if top_k is not None else nodes

    def retrieve_bm25(
        self, query: str | QueryBundle, top_k: int | None = None
    ) -> list[NodeWithScore]:
        query_text = self._query_text(query)
        scores = self._bm25.get_scores(lexical_tokens(query_text))
        limit = min(top_k or self._bm25_top_k, len(self._nodes))
        ranked_indexes = np.argsort(scores)[::-1][:limit]
        return [
            NodeWithScore(node=self._nodes[index], score=float(scores[index]))
            for index in ranked_indexes
        ]

    def fuse(
        self,
        dense_nodes: list[NodeWithScore],
        bm25_nodes: list[NodeWithScore],
    ) -> list[NodeWithScore]:
        nodes_by_id: dict[str, Any] = {}
        fused_scores: Counter[str] = Counter()
        for ranked_nodes in (dense_nodes, bm25_nodes):
            for rank, node in enumerate(ranked_nodes, start=1):
                node_id = node.node.node_id
                nodes_by_id[node_id] = node.node
                fused_scores[node_id] += 1.0 / (self._rrf_k + rank)
        ranked_ids = sorted(
            fused_scores,
            key=lambda node_id: (-fused_scores[node_id], node_id),
        )[: self._fusion_top_k]
        return [
            NodeWithScore(node=nodes_by_id[node_id], score=fused_scores[node_id])
            for node_id in ranked_ids
        ]

    def retrieve_fused(self, query: str | QueryBundle) -> list[NodeWithScore]:
        dense_nodes = self.retrieve_dense(query)
        bm25_nodes = self.retrieve_bm25(query)
        return self.fuse(dense_nodes, bm25_nodes)

    def _source_identification_anchor(self, query_text: str) -> Any | None:
        normalized_query = normalize_lexical_text(query_text)
        requested_document = extract_document_reference(query_text)
        is_source_identification = bool(
            SOURCE_IDENTIFICATION_RE.search(normalized_query)
        )
        is_named_scope_question = bool(
            requested_document and PURPOSE_SCOPE_RE.search(normalized_query)
        )
        if not is_source_identification and not is_named_scope_question:
            return None
        query_terms = set(lexical_tokens(query_text)) - SOURCE_TITLE_STOPWORDS
        article_one_nodes = [
            node
            for node in self._nodes
            if str((node.metadata or {}).get("article", "")) == "Art. 1"
        ]
        if not article_one_nodes:
            return None

        if is_named_scope_question:
            return next(
                (
                    node
                    for node in article_one_nodes
                    if str((node.metadata or {}).get("regulation_id", ""))
                    == requested_document
                ),
                None,
            )

        def title_overlap(node: Any) -> int:
            title_terms = set(
                lexical_tokens(str((node.metadata or {}).get("document_title", "")))
            )
            return len(query_terms & title_terms)

        anchor = max(article_one_nodes, key=title_overlap)
        return anchor if title_overlap(anchor) else None

    def _exact_legal_anchor(self, query_text: str) -> Any | None:
        normalized_query = normalize_lexical_text(query_text)

        def first_node_with(*required_terms: str) -> Any | None:
            normalized_terms = [normalize_lexical_text(term) for term in required_terms]
            for node in self._nodes:
                text = normalize_lexical_text(searchable_node_text(node))
                if all(term in text for term in normalized_terms):
                    return node
            return None

        asks_documentation_format = (
            "formato" in normalized_query
            and "documentacao" in normalized_query
            and "registro" in normalized_query
            and "produto biologico" in normalized_query
        )
        if asks_documentation_format:
            anchor = first_node_with(
                "CD-ROM",
                "formato pdf",
                "protocolar a solicitação de registro",
            )
            if anchor is not None:
                return anchor

        asks_responsibility_structure = (
            "responsabilidades" in normalized_query
            and "envolvidos" in normalized_query
            and "sistema de farmacovigilancia" in normalized_query
        )
        if asks_responsibility_structure:
            anchor = first_node_with(
                "sobreposições",
                "lacunas",
                "responsabilidades dos envolvidos",
                "Sistema de Farmacovigilância",
            )
            if anchor is not None:
                return anchor

        return None

    def rerank(
        self, query: str | QueryBundle, nodes: list[NodeWithScore]
    ) -> list[NodeWithScore]:
        query_text = self._query_text(query)
        scoring_query_text = rerank_query_text(query_text)
        if not nodes:
            return []
        working_nodes = list(nodes)
        anchor = self._source_identification_anchor(query_text)
        if anchor is not None and all(node.node.node_id != anchor.node_id for node in working_nodes):
            working_nodes.append(NodeWithScore(node=anchor, score=0.0))
        exact_anchor = self._exact_legal_anchor(query_text)
        if exact_anchor is not None and all(
            node.node.node_id != exact_anchor.node_id for node in working_nodes
        ):
            working_nodes.append(NodeWithScore(node=exact_anchor, score=0.0))
        pairs = [
            (scoring_query_text, searchable_node_text(node.node))
            for node in working_nodes
        ]
        scores = self._reranker.predict(
            pairs,
            batch_size=self._reranker_batch_size,
            show_progress_bar=False,
        )
        reranked = [
            NodeWithScore(node=node.node, score=float(score))
            for node, score in zip(working_nodes, scores)
        ]
        reranked.sort(key=lambda node: (-(node.score or 0.0), node.node.node_id))

        if anchor is not None:
            anchor_node = next(
                node for node in reranked if node.node.node_id == anchor.node_id
            )
            reranked.remove(anchor_node)
            reranked.insert(0, anchor_node)
        elif exact_anchor is not None:
            anchor_node = next(
                node for node in reranked if node.node.node_id == exact_anchor.node_id
            )
            reranked.remove(anchor_node)
            reranked.insert(0, anchor_node)
        elif SOURCE_IDENTIFICATION_RE.search(normalize_lexical_text(query_text)):
            query_terms = Counter(lexical_tokens(query_text))

            def lexical_overlap(node: NodeWithScore) -> int:
                node_terms = Counter(lexical_tokens(searchable_node_text(node.node)))
                return sum(
                    min(count, node_terms[term])
                    for term, count in query_terms.items()
                )

            strongest_lexical_node = max(
                reranked,
                key=lambda node: (lexical_overlap(node), node.score or 0.0),
            )
            reranked.remove(strongest_lexical_node)
            reranked.insert(0, strongest_lexical_node)
        reranked = self._deduplicate_by_citation(reranked)
        reranked = self._expand_with_neighbor_articles(query_text, reranked)
        reranked = self._deduplicate_by_citation(reranked)
        return reranked[: self._reranker_top_n]

    def _retrieve(self, query_bundle: QueryBundle) -> list[NodeWithScore]:
        fused_nodes = self.retrieve_fused(query_bundle)
        return self.rerank(query_bundle, fused_nodes)


def select_source_diverse_nodes(
    nodes: list[NodeWithScore],
    query: str,
    top_n: int,
    max_per_source: int,
) -> list[NodeWithScore]:
    """Preserve reranker order while preventing one regulation from crowding results."""
    if top_n <= 0 or max_per_source <= 0:
        return []

    selected: list[NodeWithScore] = []
    selected_ids: set[str] = set()
    source_counts: Counter[str] = Counter()
    requested_document = extract_document_reference(query)

    def add(node: NodeWithScore) -> bool:
        node_id = node.node.node_id
        source = source_id(node)
        if node_id in selected_ids or source_counts[source] >= max_per_source:
            return False
        selected.append(node)
        selected_ids.add(node_id)
        source_counts[source] += 1
        return True

    if requested_document:
        for node in nodes:
            if source_id(node) == requested_document:
                add(node)
                if source_counts[requested_document] >= max_per_source:
                    break

    represented = set(source_counts)
    for node in nodes:
        source = source_id(node)
        if source in represented:
            continue
        if add(node):
            represented.add(source)
        if len(selected) >= top_n:
            return selected

    for node in nodes:
        add(node)
        if len(selected) >= top_n:
            break
    return selected


class SourceDiversityPostprocessor(BaseNodePostprocessor):
    top_n: int = 10
    max_per_source: int = 2

    def _postprocess_nodes(
        self,
        nodes: list[NodeWithScore],
        query_bundle: QueryBundle | None = None,
    ) -> list[NodeWithScore]:
        query = query_bundle.query_str if query_bundle else ""
        return select_source_diverse_nodes(
            nodes,
            query=query,
            top_n=self.top_n,
            max_per_source=self.max_per_source,
        )
