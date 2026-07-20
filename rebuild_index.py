from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.article_chunking import build_article_nodes
from src.config import (
    ARTICLE_LONG_CHUNK_OVERLAP,
    ARTICLE_LONG_CHUNK_SIZE,
    ARTICLE_SINGLE_CHUNK_MAX_TOKENS,
    BASE_PATH,
    DATA_PATH,
    EMBEDDING_MAX_LENGTH,
    EMBEDDING_MODEL_NAME,
    VECTOR_STORE_PATH,
)
from src.regulatory_documents import load_regulatory_documents


def verify_persisted_index(path: Path, expected_chunks: int) -> dict[str, Any]:
    required_files = {
        "default__vector_store.json",
        "docstore.json",
        "graph_store.json",
        "image__vector_store.json",
        "index_store.json",
    }
    present_files = {file.name for file in path.glob("*.json")}
    missing = required_files - present_files
    if missing:
        raise RuntimeError(f"Persisted index is missing files: {sorted(missing)}")

    docstore_text = (path / "docstore.json").read_text(encoding="utf-8")
    strategy_markers = docstore_text.count("article_aware_v1")
    if strategy_markers < expected_chunks:
        raise RuntimeError(
            "Persisted index failed article-aware metadata verification: "
            f"expected at least {expected_chunks} markers, found {strategy_markers}."
        )
    return {
        "required_files_present": True,
        "article_aware_metadata_markers": strategy_markers,
        "expected_chunk_count": expected_chunks,
    }


def promote_index(build_path: Path, target_path: Path) -> None:
    backup_path = target_path.with_name(f"{target_path.name}.backup")
    shutil.rmtree(backup_path, ignore_errors=True)
    if target_path.exists():
        target_path.rename(backup_path)
    try:
        build_path.rename(target_path)
    except Exception:
        if backup_path.exists() and not target_path.exists():
            backup_path.rename(target_path)
        raise
    else:
        shutil.rmtree(backup_path, ignore_errors=True)


def rebuild_index(
    data_path: Path = DATA_PATH,
    target_path: Path = VECTOR_STORE_PATH,
    audit_path: Path | None = None,
) -> dict[str, Any]:
    build_path = target_path.with_name(f"{target_path.name}.building")
    shutil.rmtree(build_path, ignore_errors=True)
    build_path.mkdir(parents=True, exist_ok=True)

    print("Loading cleaned article-level regulatory documents...", flush=True)
    documents = load_regulatory_documents(data_path)
    source_count = len({doc.metadata["source_document"] for doc in documents})
    print(f"Loaded {len(documents)} article records from {source_count} regulations.")

    print("Loading embedding model...", flush=True)
    embed_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL_NAME,
        max_length=EMBEDDING_MAX_LENGTH,
    )

    print("Building article-aware chunks...", flush=True)
    nodes, chunk_report = build_article_nodes(
        documents,
        single_chunk_max_tokens=ARTICLE_SINGLE_CHUNK_MAX_TOKENS,
        long_chunk_size=ARTICLE_LONG_CHUNK_SIZE,
        long_chunk_overlap=ARTICLE_LONG_CHUNK_OVERLAP,
    )
    print(
        f"Created {chunk_report['chunk_count']} chunks: "
        f"{chunk_report['single_chunk_article_count']} intact articles and "
        f"{chunk_report['long_article_count']} split long articles."
    )

    print("Building vector index...", flush=True)
    index = VectorStoreIndex(nodes, embed_model=embed_model)
    index.storage_context.persist(persist_dir=build_path)
    verification = verify_persisted_index(build_path, len(nodes))

    audit = {
        "strategy": "article_aware_v1",
        "data_path": str(data_path),
        "single_chunk_max_tokens": ARTICLE_SINGLE_CHUNK_MAX_TOKENS,
        "long_chunk_size": ARTICLE_LONG_CHUNK_SIZE,
        "long_chunk_overlap": ARTICLE_LONG_CHUNK_OVERLAP,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "embedding_max_length": EMBEDDING_MAX_LENGTH,
        **chunk_report,
        "persistence_verification": verification,
    }

    print("Promoting verified index...", flush=True)
    promote_index(build_path, target_path)
    audit_path = audit_path or BASE_PATH / "reports" / "article_chunk_audit.json"
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_path.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Verified index saved to {target_path}")
    print(f"Chunk audit saved to {audit_path}")
    return audit


if __name__ == "__main__":
    rebuild_index()
