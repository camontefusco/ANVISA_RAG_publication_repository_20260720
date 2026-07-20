import os
from llama_index.core import (
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.config import (
    VECTOR_STORE_PATH,
    BM25_TOP_K,
    EMBEDDING_MAX_LENGTH,
    EMBEDDING_MODEL_NAME,
    HYBRID_FUSION_TOP_K,
    HYBRID_RRF_K,
    SIMILARITY_TOP_K,
    RERANKER_BATCH_SIZE,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_N,
)
from src.model_loader import load_answer_llm
from src.prompts import REGULATORY_QA_TEMPLATE
from src.retrieval import HybridRetriever


# ------------------------------
# Load Vector Index
# ------------------------------
def load_index():
    """Load a previously built index from /vector_store."""
    if not VECTOR_STORE_PATH.exists():
        raise RuntimeError("❌ No vector index found. Run rebuild_index.py first.")

    embed_model = HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL_NAME,
        max_length=EMBEDDING_MAX_LENGTH,
    )
    storage_ctx = StorageContext.from_defaults(persist_dir=str(VECTOR_STORE_PATH))

    try:
        index = load_index_from_storage(storage_ctx, embed_model=embed_model)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to load index: {e}")

    return index, embed_model


# ------------------------------
# Main Query Engine
# ------------------------------
def get_chat_engine():
    """Return a LlamaIndex query engine with local embeddings + Gemini answer LLM."""

    # Load vector index with the same local embedding model used at query time.
    index, embed_model = load_index()

    # Load answering model (Gemini flash-lite)
    llm = load_answer_llm()

    # Build query engine
    retriever = HybridRetriever(
        index=index,
        dense_top_k=SIMILARITY_TOP_K,
        bm25_top_k=BM25_TOP_K,
        fusion_top_k=HYBRID_FUSION_TOP_K,
        rrf_k=HYBRID_RRF_K,
        reranker_model_name=RERANKER_MODEL_NAME,
        reranker_top_n=RERANKER_TOP_N,
        reranker_batch_size=RERANKER_BATCH_SIZE,
    )
    query_engine = RetrieverQueryEngine.from_args(
        retriever,
        llm=llm,
        text_qa_template=REGULATORY_QA_TEMPLATE,
    )

    return query_engine
