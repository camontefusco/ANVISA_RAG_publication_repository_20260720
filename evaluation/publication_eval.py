from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.engine import load_index
from src.config import (
    BM25_TOP_K,
    HYBRID_FUSION_TOP_K,
    HYBRID_RRF_K,
    RERANKER_BATCH_SIZE,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_N,
    SIMILARITY_TOP_K,
    GEMINI_ANSWER_MODEL,
    DATA_PATH,
    EMBEDDING_MAX_LENGTH,
    HUGGINGFACE_EMBEDDING_MODEL_ID,
    VECTOR_STORE_PATH,
)
from evaluation.answer_quality import (
    AnswerQualityJudge,
    citation_validity,
    extract_citations,
    sanitize_answer_citations,
)
from evaluation.evaluation_statistics import (
    clustered_bootstrap_mean_ci,
    ndcg_at_k,
    paired_language_difference_ci,
    precision_at_k,
    recall_at_k,
    reciprocal_rank_at_k,
)
from src.model_loader import GlossaryQueryRewriter, Translator, load_answer_llm
from src.prompts import REGULATORY_QA_TEMPLATE
from src.retrieval import HybridRetriever
from llama_index.core.schema import MetadataMode


DEFAULT_BENCHMARK = ROOT / "evaluation" / "publication_benchmark_200.jsonl"
DEFAULT_RESULTS_DIR = ROOT / "evaluation" / "publication_results"
DEFAULT_SPLIT_MANIFEST = ROOT / "evaluation" / "benchmark_200_split_manifest.json"
CONTEXT_EXPANSION_RE = re.compile(
    r"\b("
    r"what (?:specific )?documents|what information|must be included|"
    r"which .*excluded|which .*exempt|exempt from|"
    r"quais .*documentos|quais .*informacoes|deve conter|"
    r"exclu[ií]d\w*|isent\w*"
    r")\b",
    re.IGNORECASE,
)

REFUSAL_PATTERNS = [
    "nao encontrei",
    "nao ha informacao",
    "nao esta disponivel",
    "nao posso determinar",
    "nao e possivel determinar",
    "nao tenho informacao",
    "not enough information",
    "do not provide enough information",
    "do not provide sufficient information",
    "nao fornecem informacao suficiente",
    "cannot determine",
    "not available",
    "not found",
]

ANSWER_TERM_STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "any",
    "are",
    "attached",
    "been",
    "case",
    "clinical",
    "country",
    "days",
    "for",
    "from",
    "has",
    "have",
    "into",
    "may",
    "must",
    "not",
    "or",
    "process",
    "provided",
    "related",
    "respective",
    "should",
    "submit",
    "the",
    "their",
    "they",
    "this",
    "trial",
    "when",
    "with",
}


@dataclass
class BenchmarkItem:
    id: str
    question: str
    language: str
    category: str
    answerable: bool
    gold_sources: list[str]
    gold_terms: list[str]
    expected_answer: str
    notes: str = ""
    pair_id: str = ""
    difficulty: str = ""
    gold_articles: list[str] = field(default_factory=list)
    gold_citations: list[str] = field(default_factory=list)
    gold_evidence: list[str] = field(default_factory=list)
    provenance: str = ""
    validation_status: str = ""


def normalize_text(text: str) -> str:
    """Lowercase, strip accents, and collapse whitespace for robust matching."""
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    ascii_text = ascii_text.lower()
    ascii_text = re.sub(r"\s+", " ", ascii_text)
    return ascii_text.strip()


def load_benchmark(path: Path) -> list[BenchmarkItem]:
    items: list[BenchmarkItem] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            raw = json.loads(line)
            try:
                items.append(BenchmarkItem(**raw))
            except TypeError as exc:
                raise ValueError(f"Invalid benchmark row {line_number}: {exc}") from exc
    return items


def filter_benchmark_split(
    items: list[BenchmarkItem], manifest_path: Path, split: str | None
) -> list[BenchmarkItem]:
    if split is None:
        return items
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assignments = manifest.get("assignments", {})
    filtered = [
        item for item in items if assignments.get(item.pair_id or item.id) == split
    ]
    if not filtered:
        raise ValueError(f"No benchmark items found for split {split!r}.")
    return filtered


def source_name_from_node(node: Any) -> str:
    metadata = getattr(node.node, "metadata", {}) or {}
    return (
        metadata.get("source_document")
        or metadata.get("file_name")
        or Path(metadata.get("file_path", "")).name
    )


def metadata_value_from_node(node: Any, key: str) -> str:
    metadata = getattr(node.node, "metadata", {}) or {}
    return str(metadata.get(key, ""))


def node_text(node: Any) -> str:
    return node.node.get_content(metadata_mode=MetadataMode.LLM)


def should_expand_article_context(question: str) -> bool:
    return bool(CONTEXT_EXPANSION_RE.search(question))


def expanded_context_pairs(
    retriever: HybridRetriever,
    retrieved_nodes: list[Any],
    question: str,
) -> list[tuple[str, str]]:
    """Include sibling chunks for long retrieved articles when list completeness matters."""
    if not should_expand_article_context(question):
        return [
            (metadata_value_from_node(node, "citation_label"), node_text(node))
            for node in retrieved_nodes
        ]

    nodes_by_label: dict[str, list[Any]] = {}
    for indexed_node in getattr(retriever, "_nodes", []):
        metadata = indexed_node.metadata or {}
        label = str(metadata.get("citation_label") or "")
        if not label:
            continue
        nodes_by_label.setdefault(label, []).append(indexed_node)

    for siblings in nodes_by_label.values():
        siblings.sort(
            key=lambda node: int((node.metadata or {}).get("article_chunk_index") or 1)
        )

    expanded: list[tuple[str, str]] = []
    seen_node_ids: set[str] = set()
    for retrieved_node in retrieved_nodes:
        metadata = retrieved_node.node.metadata or {}
        label = str(metadata.get("citation_label") or "")
        siblings = nodes_by_label.get(label, [])
        if len(siblings) <= 1:
            if retrieved_node.node.node_id not in seen_node_ids:
                expanded.append((label, node_text(retrieved_node)))
                seen_node_ids.add(retrieved_node.node.node_id)
            continue
        for sibling in siblings:
            if sibling.node_id in seen_node_ids:
                continue
            expanded.append((label, sibling.get_content(metadata_mode=MetadataMode.LLM)))
            seen_node_ids.add(sibling.node_id)
    return expanded


def expanded_context_texts(
    retriever: HybridRetriever,
    retrieved_nodes: list[Any],
    question: str,
) -> list[str]:
    return [
        context
        for _citation, context in expanded_context_pairs(
            retriever,
            retrieved_nodes,
            question,
        )
    ]


def coverage(needles: list[str], haystack: str) -> tuple[float | None, list[str], list[str]]:
    if not needles:
        return None, [], []
    normalized_haystack = normalize_text(haystack)
    matched = [term for term in needles if normalize_text(term) in normalized_haystack]
    missed = [term for term in needles if term not in matched]
    return len(matched) / len(needles), matched, missed


def expected_answer_terms(expected_answer: str) -> list[str]:
    tokens = re.findall(r"\b[A-Za-z0-9][A-Za-z0-9/-]*\b", expected_answer)
    terms: list[str] = []
    seen: set[str] = set()
    for token in tokens:
        normalized = normalize_text(token)
        if normalized in ANSWER_TERM_STOPWORDS:
            continue
        if len(normalized) < 5 and not normalized.isupper() and not normalized.isdigit():
            continue
        if normalized in seen:
            continue
        seen.add(normalized)
        terms.append(token)
    return terms


def answer_coverage_needles(item: BenchmarkItem) -> list[str]:
    if item.language == "en":
        return expected_answer_terms(item.expected_answer)
    return item.gold_terms


def source_hit(gold_sources: list[str], retrieved_sources: list[str]) -> bool | None:
    if not gold_sources:
        return None
    normalized_retrieved = {normalize_text(source) for source in retrieved_sources}
    return any(normalize_text(source) in normalized_retrieved for source in gold_sources)


def reciprocal_rank(gold_sources: list[str], retrieved_sources: list[str]) -> float | None:
    if not gold_sources:
        return None
    normalized_gold = {normalize_text(source) for source in gold_sources}
    for index, source in enumerate(retrieved_sources, start=1):
        if normalize_text(source) in normalized_gold:
            return 1.0 / index
    return 0.0


def citation_metrics(
    gold_citations: list[str], retrieved_citations: list[str], top_k: int
) -> dict[str, float | None]:
    return {
        "article_recall_at_k": recall_at_k(gold_citations, retrieved_citations, top_k),
        "article_precision_at_k": precision_at_k(
            gold_citations, retrieved_citations, top_k
        ),
        "article_mrr_at_k": reciprocal_rank_at_k(
            gold_citations, retrieved_citations, top_k
        ),
        "article_ndcg_at_k": ndcg_at_k(gold_citations, retrieved_citations, top_k),
    }


def detect_refusal(answer: str) -> bool:
    normalized_answer = normalize_text(answer)
    return any(pattern in normalized_answer for pattern in REFUSAL_PATTERNS)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("No rows to write.")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def directory_checksums(path: Path, pattern: str = "*") -> dict[str, str]:
    return {
        str(file.relative_to(path)): sha256_file(file)
        for file in sorted(path.glob(pattern))
        if file.is_file()
    }


def package_versions() -> dict[str, str]:
    packages = [
        "llama-index-core",
        "sentence-transformers",
        "rank-bm25",
        "google-generativeai",
    ]
    versions: dict[str, str] = {}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = "not-installed"
    return versions


def numeric_mean(rows: list[dict[str, Any]], key: str) -> float | None:
    values = [
        row[key]
        for row in rows
        if isinstance(row.get(key), (float, int)) and row.get(key) is not None
    ]
    return mean(values) if values else None


def metric_with_ci(rows: list[dict[str, Any]], key: str) -> str:
    estimate, lower, upper, clusters = clustered_bootstrap_mean_ci(rows, key)
    if estimate is None:
        return "not available"
    return f"{estimate:.3f} (95% CI {lower:.3f}-{upper:.3f}; {clusters} pairs)"


def paired_language_metric(rows: list[dict[str, Any]], key: str) -> str:
    estimate, lower, upper, pairs = paired_language_difference_ci(rows, key)
    if estimate is None:
        return "not available"
    return f"{estimate:.3f} (95% CI {lower:.3f}-{upper:.3f}; {pairs} pairs)"


def build_summary(rows: list[dict[str, Any]], generate: bool) -> str:
    answerable_rows = [row for row in rows if row["answerable"]]
    unanswerable_rows = [row for row in rows if not row["answerable"]]
    languages = sorted({row["language"] for row in rows})

    lines = [
        "# Publication RAG Evaluation Summary",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Questions: {len(rows)}",
        f"Answerable questions: {len(answerable_rows)}",
        f"Unanswerable questions: {len(unanswerable_rows)}",
        "",
        "## Raw Vector Retrieval Metrics",
        "",
        f"- Source hit rate: {numeric_mean(answerable_rows, 'raw_vector_source_hit')}",
        f"- Mean reciprocal rank: {numeric_mean(answerable_rows, 'raw_vector_source_mrr')}",
        "",
        "## BM25 Retrieval Metrics",
        "",
        f"- Source hit rate: {numeric_mean(answerable_rows, 'bm25_source_hit')}",
        f"- Mean reciprocal rank: {numeric_mean(answerable_rows, 'bm25_source_mrr')}",
        "",
        "## Fused Retrieval Metrics Before Reranking",
        "",
        f"- Source hit rate: {numeric_mean(answerable_rows, 'fused_source_hit')}",
        f"- Mean reciprocal rank: {numeric_mean(answerable_rows, 'fused_source_mrr')}",
        "",
        "## Operational Retrieval Metrics",
        "",
        f"- Source hit rate after cross-encoder reranking: {metric_with_ci(answerable_rows, 'source_hit')}",
        f"- Source MRR after cross-encoder reranking: {metric_with_ci(answerable_rows, 'source_mrr')}",
        f"- Article Recall@k: {metric_with_ci(answerable_rows, 'article_recall_at_k')}",
        f"- Article Precision@k: {metric_with_ci(answerable_rows, 'article_precision_at_k')}",
        f"- Article MRR@k: {metric_with_ci(answerable_rows, 'article_mrr_at_k')}",
        f"- Article nDCG@k: {metric_with_ci(answerable_rows, 'article_ndcg_at_k')}",
        f"- Mean gold term coverage in retrieved contexts: {metric_with_ci(answerable_rows, 'retrieved_term_coverage')}",
        "",
        "## Retrieval Metrics By Language",
        "",
    ]

    for language in languages:
        language_rows = [
            row
            for row in answerable_rows
            if row["language"] == language
        ]
        lines.extend(
            [
                f"### {language}",
                "",
                f"- Questions: {len(language_rows)}",
                f"- Raw vector source hit rate: {numeric_mean(language_rows, 'raw_vector_source_hit')}",
                f"- Raw vector MRR: {numeric_mean(language_rows, 'raw_vector_source_mrr')}",
                f"- BM25 source hit rate: {numeric_mean(language_rows, 'bm25_source_hit')}",
                f"- BM25 MRR: {numeric_mean(language_rows, 'bm25_source_mrr')}",
                f"- Fused source hit rate: {numeric_mean(language_rows, 'fused_source_hit')}",
                f"- Fused MRR: {numeric_mean(language_rows, 'fused_source_mrr')}",
                f"- Operational source hit rate: {metric_with_ci(language_rows, 'source_hit')}",
                f"- Operational MRR: {metric_with_ci(language_rows, 'source_mrr')}",
                f"- Article Recall@k: {metric_with_ci(language_rows, 'article_recall_at_k')}",
                f"- Article MRR@k: {metric_with_ci(language_rows, 'article_mrr_at_k')}",
                f"- Mean gold term coverage: {metric_with_ci(language_rows, 'retrieved_term_coverage')}",
                "",
            ]
        )

    lines.extend(
        [
            "## Paired Language Differences",
            "",
            "Positive values favor Portuguese; intervals are paired over bilingual facts.",
            "",
            f"- Source hit rate (PT - EN): {paired_language_metric(answerable_rows, 'source_hit')}",
            f"- Source MRR (PT - EN): {paired_language_metric(answerable_rows, 'source_mrr')}",
            f"- Article Recall@k (PT - EN): {paired_language_metric(answerable_rows, 'article_recall_at_k')}",
            f"- Article MRR@k (PT - EN): {paired_language_metric(answerable_rows, 'article_mrr_at_k')}",
            f"- Gold-term coverage (PT - EN): {paired_language_metric(answerable_rows, 'retrieved_term_coverage')}",
            "",
            "## Retrieval Metrics By Question Type",
            "",
        ]
    )
    for category in sorted({row["category"] for row in answerable_rows}):
        category_rows = [row for row in answerable_rows if row["category"] == category]
        lines.extend(
            [
                f"### {category}",
                "",
                f"- Questions: {len(category_rows)}",
                f"- Source hit rate: {metric_with_ci(category_rows, 'source_hit')}",
                f"- Article Recall@k: {metric_with_ci(category_rows, 'article_recall_at_k')}",
                f"- Article MRR@k: {metric_with_ci(category_rows, 'article_mrr_at_k')}",
                "",
            ]
        )

    if generate:
        lines.extend(
            [
                "",
                "## Generation Metrics",
                "",
                f"- Mean gold term coverage in generated answers: {metric_with_ci(answerable_rows, 'answer_term_coverage')}",
                f"- Refusal accuracy on unanswerable questions: {metric_with_ci(unanswerable_rows, 'refusal_detected')}",
                f"- Citation presence on answerable questions: {metric_with_ci(answerable_rows, 'citation_present')}",
                f"- Article citation presence on answerable questions: {metric_with_ci(answerable_rows, 'article_citation_present')}",
                f"- Retrieved-citation validity: {metric_with_ci(answerable_rows, 'citation_retrieved_validity')}",
            ]
        )
        if any("judge_faithfulness" in row for row in rows):
            lines.extend(
                [
                    "",
                    "## Automated Answer-Quality Judge",
                    "",
                    f"- Faithfulness: {metric_with_ci(answerable_rows, 'judge_faithfulness')}",
                    f"- Citation correctness: {metric_with_ci(answerable_rows, 'judge_citation_correctness')}",
                    f"- Completeness: {metric_with_ci(answerable_rows, 'judge_completeness')}",
                    f"- Refusal accuracy: {metric_with_ci(unanswerable_rows, 'judge_refusal_correctness')}",
                ]
            )

    lines.extend(
        [
            "",
            "## Notes",
            "",
            "- Automated scores are screening metrics, not final evidence.",
            "- Raw vector metrics measure the embedding retriever without routing or source diversification.",
            "- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.",
            "- Fused metrics use reciprocal rank fusion before cross-encoder reranking.",
            "- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.",
            "- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.",
            "- LLM-judge scores are supplementary and require calibration against the blinded human review subset.",
            "- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.",
        ]
    )
    return "\n".join(lines) + "\n"


def classify_failures(row: dict[str, Any], generate: bool) -> list[str]:
    failures: list[str] = []
    if row["answerable"]:
        if not row.get("source_hit"):
            failures.append("wrong_or_missing_source")
        article_recall = row.get("article_recall_at_k")
        if isinstance(article_recall, (int, float)) and article_recall < 1:
            failures.append("incomplete_article_retrieval")
        term_coverage = row.get("retrieved_term_coverage")
        if isinstance(term_coverage, (int, float)) and term_coverage < 0.5:
            failures.append("low_evidence_term_coverage")
    if not generate:
        return failures
    if row["answerable"]:
        if row.get("refusal_detected"):
            failures.append("incorrect_refusal")
        if not row.get("citation_present"):
            failures.append("missing_citation")
        elif (row.get("citation_retrieved_validity") or 0) < 1:
            failures.append("unsupported_or_unretrieved_citation")
        if (row.get("answer_term_coverage") or 0) < 0.5:
            failures.append("incomplete_answer")
        if "judge_faithfulness" in row and row.get("judge_faithfulness", 1) < 0.8:
            failures.append("judge_flagged_unfaithful")
    elif not row.get("refusal_detected"):
        failures.append("failed_to_refuse")
    return failures


def build_failure_rows(
    rows: list[dict[str, Any]], generate: bool
) -> list[dict[str, Any]]:
    failures: list[dict[str, Any]] = []
    for row in rows:
        failure_types = classify_failures(row, generate)
        if not failure_types:
            continue
        failures.append(
            {
                "id": row["id"],
                "pair_id": row["pair_id"],
                "language": row["language"],
                "category": row["category"],
                "answerable": row["answerable"],
                "failure_types": ";".join(failure_types),
                "question": row["question"],
                "gold_citations": row["gold_citations"],
                "retrieved_citations": row["retrieved_citations"],
                "answer": row.get("answer", ""),
                "human_adjudication": "",
                "human_root_cause": "",
                "human_notes": "",
            }
        )
    return failures


def run_evaluation(
    benchmark_path: Path,
    results_dir: Path,
    top_k: int,
    generate: bool,
    rewrite: bool,
    rewrite_mode: str,
    rerank_query_mode: str,
    judge: bool,
    limit: int | None,
    language: str | None = None,
    ids: set[str] | None = None,
    split: str | None = None,
    split_manifest_path: Path = DEFAULT_SPLIT_MANIFEST,
) -> tuple[Path, Path, Path, Path, Path]:
    items = load_benchmark(benchmark_path)
    items = filter_benchmark_split(items, split_manifest_path, split)
    if language is not None:
        items = [item for item in items if item.language == language]
        if not items:
            raise ValueError(f"No benchmark items found for language {language!r}.")
    if ids is not None:
        items = [item for item in items if item.id in ids]
        if not items:
            raise ValueError(f"No benchmark items found for ids {sorted(ids)!r}.")
    if limit is not None:
        items = items[:limit]

    index, _embed_model = load_index()
    retriever = HybridRetriever(
        index=index,
        dense_top_k=max(SIMILARITY_TOP_K, top_k),
        bm25_top_k=max(BM25_TOP_K, top_k),
        fusion_top_k=max(HYBRID_FUSION_TOP_K, top_k),
        rrf_k=HYBRID_RRF_K,
        reranker_model_name=RERANKER_MODEL_NAME,
        reranker_top_n=RERANKER_TOP_N,
        reranker_batch_size=RERANKER_BATCH_SIZE,
    )
    answer_llm = load_answer_llm() if generate else None
    translator = Translator() if rewrite and rewrite_mode == "gemini" else None
    query_rewriter = (
        translator if rewrite and rewrite_mode == "gemini"
        else GlossaryQueryRewriter() if rewrite and rewrite_mode == "glossary"
        else None
    )
    quality_judge = AnswerQualityJudge(GEMINI_ANSWER_MODEL) if judge else None

    rows: list[dict[str, Any]] = []
    manual_rows: list[dict[str, Any]] = []
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mode = "generation" if generate else "retrieval"
    checkpoint_path = results_dir / f"{mode}_checkpoint_{timestamp}.jsonl"

    for item_number, item in enumerate(items, start=1):
        print(f"[{item_number}/{len(items)}] {item.id}: {item.question}", flush=True)
        rewrite_applied = bool(query_rewriter and item.language == "en")
        retrieval_query = (
            query_rewriter.rewrite(item.question)
            if rewrite_applied and query_rewriter
            else item.question
        )
        raw_vector_nodes = retriever.retrieve_dense(retrieval_query, top_k=top_k)
        raw_vector_sources = [source_name_from_node(node) for node in raw_vector_nodes]
        raw_vector_citations = [
            metadata_value_from_node(node, "citation_label") for node in raw_vector_nodes
        ]
        bm25_nodes = retriever.retrieve_bm25(retrieval_query, top_k=top_k)
        bm25_sources = [source_name_from_node(node) for node in bm25_nodes]
        bm25_citations = [
            metadata_value_from_node(node, "citation_label") for node in bm25_nodes
        ]
        fused_nodes = retriever.retrieve_fused(retrieval_query)
        fused_sources = [source_name_from_node(node) for node in fused_nodes[:top_k]]
        fused_citations = [
            metadata_value_from_node(node, "citation_label")
            for node in fused_nodes[:top_k]
        ]
        rerank_query = (
            item.question
            if rewrite_applied and rerank_query_mode == "original"
            else retrieval_query
        )
        candidate_nodes = retriever.rerank(rerank_query, fused_nodes)
        retrieved_nodes = candidate_nodes[:top_k]
        retrieved_sources = [source_name_from_node(node) for node in retrieved_nodes]
        retrieved_citations = [
            metadata_value_from_node(node, "citation_label") for node in retrieved_nodes
        ]
        retrieved_articles = [
            metadata_value_from_node(node, "article") for node in retrieved_nodes
        ]
        retrieved_topics = [
            metadata_value_from_node(node, "topics") for node in retrieved_nodes
        ]
        retrieved_context_pairs = expanded_context_pairs(
            retriever,
            retrieved_nodes,
            item.question,
        )
        retrieved_contexts = [context for _citation, context in retrieved_context_pairs]
        combined_context = "\n\n".join(retrieved_contexts)
        retrieved_term_coverage, retrieved_terms_matched, retrieved_terms_missed = coverage(
            item.gold_terms,
            combined_context,
        )

        row: dict[str, Any] = {
            "id": item.id,
            "pair_id": item.pair_id or item.id,
            "question": item.question,
            "retrieval_query": retrieval_query,
            "rerank_query": rerank_query,
            "rewrite_applied": rewrite_applied,
            "rewrite_mode": rewrite_mode if rewrite else "none",
            "rerank_query_mode": rerank_query_mode,
            "language": item.language,
            "category": item.category,
            "answerable": item.answerable,
            "difficulty": item.difficulty,
            "gold_sources": ";".join(item.gold_sources),
            "gold_articles": ";".join(item.gold_articles),
            "gold_citations": ";".join(item.gold_citations),
            "raw_vector_sources": ";".join(raw_vector_sources),
            "raw_vector_citations": ";".join(raw_vector_citations),
            "raw_vector_source_hit": source_hit(item.gold_sources, raw_vector_sources),
            "raw_vector_source_mrr": reciprocal_rank(item.gold_sources, raw_vector_sources),
            "bm25_sources": ";".join(bm25_sources),
            "bm25_citations": ";".join(bm25_citations),
            "bm25_source_hit": source_hit(item.gold_sources, bm25_sources),
            "bm25_source_mrr": reciprocal_rank(item.gold_sources, bm25_sources),
            "fused_sources": ";".join(fused_sources),
            "fused_citations": ";".join(fused_citations),
            "fused_source_hit": source_hit(item.gold_sources, fused_sources),
            "fused_source_mrr": reciprocal_rank(item.gold_sources, fused_sources),
            "retrieved_sources": ";".join(retrieved_sources),
            "retrieved_citations": ";".join(retrieved_citations),
            "retrieved_articles": ";".join(retrieved_articles),
            "retrieved_topics": " | ".join(retrieved_topics),
            "source_hit": source_hit(item.gold_sources, retrieved_sources),
            "source_mrr": reciprocal_rank(item.gold_sources, retrieved_sources),
            "gold_terms": ";".join(item.gold_terms),
            "retrieved_terms_matched": ";".join(retrieved_terms_matched),
            "retrieved_terms_missed": ";".join(retrieved_terms_missed),
            "retrieved_term_coverage": retrieved_term_coverage,
            "top_k": top_k,
            "rewrite": rewrite,
            "expected_answer": item.expected_answer,
            "notes": item.notes,
        }
        row.update(citation_metrics(item.gold_citations, retrieved_citations, top_k))
        for prefix, citations in (
            ("raw_vector", raw_vector_citations),
            ("bm25", bm25_citations),
            ("fused", fused_citations),
        ):
            for metric_name, metric_value in citation_metrics(
                item.gold_citations, citations, top_k
            ).items():
                row[f"{prefix}_{metric_name}"] = metric_value

        answer = ""
        if generate and answer_llm is not None:
            prompt = REGULATORY_QA_TEMPLATE.format(
                context_str=combined_context,
                query_str=item.question,
            )
            response = answer_llm.complete(prompt)
            raw_answer = str(response)
            answer = sanitize_answer_citations(raw_answer, retrieved_citations)
            answer_terms_expected = answer_coverage_needles(item)
            answer_term_coverage, answer_terms_matched, answer_terms_missed = coverage(
                answer_terms_expected,
                answer,
            )
            row.update(
                {
                    "raw_rag_answer": raw_answer,
                    "answer": answer,
                    "answer_terms_expected": ";".join(answer_terms_expected),
                    "answer_terms_matched": ";".join(answer_terms_matched),
                    "answer_terms_missed": ";".join(answer_terms_missed),
                    "answer_term_coverage": answer_term_coverage,
                    "refusal_detected": detect_refusal(answer),
                }
            )
            answer_citations = extract_citations(answer)
            citation_present, citation_retrieved_validity = citation_validity(
                answer,
                retrieved_citations,
            )
            row.update(
                {
                    "answer_citations": ";".join(answer_citations),
                    "citation_present": citation_present,
                    "article_citation_present": any(
                        ", Art." in citation for citation in answer_citations
                    ),
                    "citation_retrieved_validity": citation_retrieved_validity,
                }
            )
            if quality_judge is not None:
                judged = quality_judge.evaluate(
                    question=item.question,
                    answer=answer,
                    expected_answer=item.expected_answer,
                    answerable=item.answerable,
                    contexts=retrieved_context_pairs,
                )
                row.update(
                    {
                        "judge_faithfulness": judged.faithfulness,
                        "judge_citation_correctness": judged.citation_correctness,
                        "judge_completeness": judged.completeness,
                        "judge_refusal_correctness": judged.refusal_correctness,
                        "judge_rationale": judged.rationale,
                    }
                )

        rows.append(row)
        manual_rows.append(
            {
                "id": item.id,
                "pair_id": item.pair_id or item.id,
                "language": item.language,
                "category": item.category,
                "answerable": item.answerable,
                "question": item.question,
                "expected_answer": item.expected_answer,
                "gold_citations": ";".join(item.gold_citations),
                "gold_evidence": "\n\n".join(item.gold_evidence),
                "answer": answer,
                "retrieved_sources": ";".join(retrieved_sources),
                "retrieved_citations": ";".join(retrieved_citations),
                "retrieved_context_1": retrieved_contexts[0] if retrieved_contexts else "",
                "retrieved_context_2": retrieved_contexts[1] if len(retrieved_contexts) > 1 else "",
                "human_source_correct_0_1": "",
                "human_answer_grounded_0_1": "",
                "human_answer_complete_0_1": "",
                "human_citation_correct_0_1": "",
                "human_safety_or_refusal_correct_0_1": "",
                "human_error_type": "",
                "human_comments": "",
            }
        )
        append_jsonl(checkpoint_path, row)

    detailed_path = results_dir / f"{mode}_evaluation_{timestamp}.csv"
    manual_path = results_dir / f"manual_review_template_{timestamp}.csv"
    summary_path = results_dir / f"{mode}_summary_{timestamp}.md"
    failure_path = results_dir / f"{mode}_failure_audit_{timestamp}.csv"
    manifest_path = results_dir / f"{mode}_run_manifest_{timestamp}.json"

    write_csv(detailed_path, rows)
    write_csv(manual_path, manual_rows)
    summary_path.write_text(build_summary(rows, generate), encoding="utf-8")
    failure_rows = build_failure_rows(rows, generate)
    if failure_rows:
        write_csv(failure_path, failure_rows)
    else:
        failure_path.write_text(
            "id,pair_id,language,category,answerable,failure_types,question,"
            "gold_citations,retrieved_citations,answer,human_adjudication,"
            "human_root_cause,human_notes\n",
            encoding="utf-8",
        )
    manifest = {
        "timestamp": timestamp,
        "benchmark": str(benchmark_path.resolve()),
        "benchmark_sha256": sha256_file(benchmark_path),
        "question_count": len(rows),
        "pair_count": len({row["pair_id"] for row in rows}),
        "split": split or "all",
        "language": language or "all",
        "split_manifest": str(split_manifest_path.resolve()) if split else None,
        "split_manifest_sha256": sha256_file(split_manifest_path) if split else None,
        "top_k": top_k,
        "generate": generate,
        "rewrite": rewrite,
        "rewrite_mode": rewrite_mode if rewrite else "none",
        "rerank_query_mode": rerank_query_mode,
        "judge": judge,
        "retrieval": {
            "embedding_model": HUGGINGFACE_EMBEDDING_MODEL_ID,
            "embedding_max_length": EMBEDDING_MAX_LENGTH,
            "dense_top_k": max(SIMILARITY_TOP_K, top_k),
            "bm25_top_k": max(BM25_TOP_K, top_k),
            "fusion_top_k": max(HYBRID_FUSION_TOP_K, top_k),
            "rrf_k": HYBRID_RRF_K,
            "reranker": RERANKER_MODEL_NAME,
            "reranker_top_n": RERANKER_TOP_N,
        },
        "answer_model": GEMINI_ANSWER_MODEL if generate else None,
        "judge_model": GEMINI_ANSWER_MODEL if judge else None,
        "corpus_checksums": directory_checksums(DATA_PATH, "*.txt"),
        "vector_store_checksums": directory_checksums(VECTOR_STORE_PATH, "*.json"),
        "package_versions": package_versions(),
        "confidence_intervals": {
            "method": "pair-clustered percentile bootstrap",
            "confidence": 0.95,
            "resamples": 2000,
            "seed": 20260619,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Detailed results: {detailed_path}")
    print(f"Manual review template: {manual_path}")
    print(f"Summary: {summary_path}")
    print(f"Failure audit: {failure_path}")
    print(f"Run manifest: {manifest_path}")
    return detailed_path, manual_path, summary_path, failure_path, manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run publication-oriented RAG evaluation."
    )
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--split",
        choices=["calibration_20", "dev_remaining_5", "held_out_test_75"],
        default=None,
        help="Evaluate only one frozen bilingual pair split.",
    )
    parser.add_argument(
        "--split-manifest", type=Path, default=DEFAULT_SPLIT_MANIFEST
    )
    parser.add_argument(
        "--language",
        choices=["pt", "en"],
        default=None,
        help="Evaluate only one benchmark language.",
    )
    parser.add_argument(
        "--ids",
        default=None,
        help="Comma-separated benchmark IDs to evaluate.",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Also generate answers with the RAG system. This uses the Gemini API.",
    )
    parser.add_argument(
        "--rewrite",
        action="store_true",
        help="Rewrite each question to Portuguese before retrieval. This uses the Gemini API.",
    )
    parser.add_argument(
        "--rewrite-mode",
        choices=["gemini", "glossary"],
        default="gemini",
        help="Query rewrite method. 'glossary' is deterministic and does not use an API.",
    )
    parser.add_argument(
        "--rerank-query-mode",
        choices=["retrieval", "original"],
        default="retrieval",
        help="Use the rewritten retrieval query or the original question for reranking.",
    )
    parser.add_argument(
        "--judge",
        action="store_true",
        help="Use a structured Gemini judge for answer-quality scoring; requires --generate.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.judge and not args.generate:
        raise SystemExit("--judge requires --generate")
    run_evaluation(
        benchmark_path=args.benchmark,
        results_dir=args.results_dir,
        top_k=args.top_k,
        generate=args.generate,
        rewrite=args.rewrite,
        rewrite_mode=args.rewrite_mode,
        rerank_query_mode=args.rerank_query_mode,
        judge=args.judge,
        limit=args.limit,
        language=args.language,
        ids=set(args.ids.split(",")) if args.ids else None,
        split=args.split,
        split_manifest_path=args.split_manifest,
    )


if __name__ == "__main__":
    main()
