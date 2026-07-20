from __future__ import annotations

import hashlib
from collections import Counter
from statistics import median
from typing import Any

from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode
from llama_index.core.utils import get_tokenizer


def _heading_context(metadata: dict[str, Any]) -> str:
    return "\n".join(
        heading
        for heading in (metadata.get("chapter", ""), metadata.get("section", ""))
        if heading
    )


def _node_id(metadata: dict[str, Any], part_index: int, text: str) -> str:
    identity = "|".join(
        (
            str(metadata.get("source_document", "")),
            str(metadata.get("citation_label", "")),
            str(part_index),
            text,
        )
    )
    return hashlib.sha1(identity.encode("utf-8")).hexdigest()


def build_article_nodes(
    documents: list[Document],
    single_chunk_max_tokens: int = 500,
    long_chunk_size: int = 400,
    long_chunk_overlap: int = 60,
) -> tuple[list[TextNode], dict[str, Any]]:
    """Keep articles intact when possible and split only long articles."""
    if long_chunk_size > single_chunk_max_tokens:
        raise ValueError("long_chunk_size must not exceed single_chunk_max_tokens")
    if not 0 <= long_chunk_overlap < long_chunk_size:
        raise ValueError("long_chunk_overlap must be smaller than long_chunk_size")

    tokenizer = get_tokenizer()
    long_splitter = SentenceSplitter(
        chunk_size=long_chunk_size,
        chunk_overlap=long_chunk_overlap,
    )
    nodes: list[TextNode] = []
    long_article_count = 0
    article_part_counts: Counter[str] = Counter()
    chunks_by_source: Counter[str] = Counter()
    long_articles: list[dict[str, Any]] = []

    for document in documents:
        article_token_count = len(tokenizer(document.text))
        is_long_article = article_token_count > single_chunk_max_tokens
        if is_long_article:
            text_parts = long_splitter.split_text(document.text)
            long_article_count += 1
        else:
            text_parts = [document.text]

        part_count = len(text_parts)
        citation_label = str(document.metadata["citation_label"])
        article_part_counts[citation_label] += part_count
        chunks_by_source[str(document.metadata["source_document"])] += part_count
        if is_long_article:
            long_articles.append(
                {
                    "citation_label": citation_label,
                    "article_token_count": article_token_count,
                    "chunk_count": part_count,
                }
            )
        heading_context = _heading_context(document.metadata)

        for part_index, text_part in enumerate(text_parts, start=1):
            content = f"{heading_context}\n{text_part}" if heading_context else text_part
            metadata = {
                **document.metadata,
                "chunking_strategy": "article_aware_v1",
                "article_token_count": article_token_count,
                "article_chunk_index": part_index,
                "article_chunk_count": part_count,
                "is_long_article": is_long_article,
                "chunk_token_count": len(tokenizer(content)),
                "chunk_overlap_tokens": long_chunk_overlap if is_long_article else 0,
            }
            llm_metadata_keys = {
                "regulation_id",
                "citation_label",
                "article",
                "chapter",
                "section",
            }
            if metadata.get("article") in {"Preamble", "Art. 1"}:
                llm_metadata_keys.add("document_title")
            nodes.append(
                TextNode(
                    id_=_node_id(metadata, part_index, content),
                    text=content,
                    metadata=metadata,
                    excluded_embed_metadata_keys=list(metadata),
                    excluded_llm_metadata_keys=[
                        key
                        for key in metadata
                        if key not in llm_metadata_keys
                    ],
                )
            )

    token_counts = [int(node.metadata["chunk_token_count"]) for node in nodes]
    report = {
        "article_count": len(documents),
        "chunk_count": len(nodes),
        "single_chunk_article_count": len(documents) - long_article_count,
        "long_article_count": long_article_count,
        "split_chunk_count": sum(
            count for count in article_part_counts.values() if count > 1
        ),
        "min_chunk_tokens": min(token_counts) if token_counts else 0,
        "median_chunk_tokens": median(token_counts) if token_counts else 0,
        "max_chunk_tokens": max(token_counts) if token_counts else 0,
        "chunks_300_to_700_tokens": sum(300 <= count <= 700 for count in token_counts),
        "chunks_under_300_tokens": sum(count < 300 for count in token_counts),
        "chunks_over_700_tokens": sum(count > 700 for count in token_counts),
        "chunks_by_source": dict(sorted(chunks_by_source.items())),
        "long_articles": long_articles,
    }
    return nodes, report
