import os
from pathlib import Path

# ----------------------------------------------------
# GEMINI API KEY
# ----------------------------------------------------
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")


# ----------------------------------------------------
# GEMINI MODELS
# (you confirmed these exist via genai.list_models())
# ----------------------------------------------------
GEMINI_REWRITE_MODEL = "models/gemini-flash-lite-latest"     # translations + rewriting
GEMINI_ANSWER_MODEL = "models/gemini-flash-lite-latest"      # final generated answers


# ----------------------------------------------------
# PATHS
# ----------------------------------------------------
BASE_PATH = Path(__file__).resolve().parent.parent
CLEANED_DATA_PATH = BASE_PATH / "cleaned_data"
RAW_DATA_PATH = BASE_PATH / "data"
DATA_PATH = Path(
    os.getenv(
        "RAG_DATA_PATH",
        str(CLEANED_DATA_PATH if CLEANED_DATA_PATH.exists() else RAW_DATA_PATH),
    )
)
VECTOR_STORE_PATH = Path(
    os.getenv("RAG_VECTOR_STORE_PATH", str(BASE_PATH / "vector_store"))
)
EMBEDDING_CACHE_PATH = BASE_PATH / "embedding_cache"


# ----------------------------------------------------
# EMBEDDINGS
# ----------------------------------------------------
# Using SentenceTransformer HF embeddings (local, no OpenAI)
HUGGINGFACE_EMBEDDING_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_EMBEDDING_MODEL_PATH = (
    EMBEDDING_CACHE_PATH
    / "models--sentence-transformers--all-MiniLM-L6-v2"
    / "snapshots"
    / "c9745ed1d9f207416be6d2e6f8de32d1f16199bf"
)
EMBEDDING_MODEL_NAME = (
    os.getenv(
        "RAG_EMBEDDING_MODEL_PATH",
        str(LOCAL_EMBEDDING_MODEL_PATH)
        if LOCAL_EMBEDDING_MODEL_PATH.exists()
        else HUGGINGFACE_EMBEDDING_MODEL_ID,
    )
)
EMBEDDING_MAX_LENGTH = 512


# ----------------------------------------------------
# ARTICLE-AWARE CHUNKING
# ----------------------------------------------------
ARTICLE_SINGLE_CHUNK_MAX_TOKENS = 500
ARTICLE_LONG_CHUNK_SIZE = 400
ARTICLE_LONG_CHUNK_OVERLAP = 60


# ----------------------------------------------------
# SEMANTIC SPLITTER (for rebuild_index + experiments)
# ----------------------------------------------------
# These are the ones your notebook is trying to import
SEMANTIC_SPLITTER_EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
BUFFER_SIZE = 1                       # neighbour window for semantic splitter
BREAKPOINT_PERCENTILE_THRESHOLD = 90  # topic-change sensitivity (1–100)


# ----------------------------------------------------
# RETRIEVAL CONFIG
# ----------------------------------------------------
SIMILARITY_TOP_K = 100                # broad vector candidate search
BM25_TOP_K = 100                      # exact-term candidate search
HYBRID_FUSION_TOP_K = 100             # candidates retained after rank fusion
HYBRID_RRF_K = 60                     # reciprocal-rank-fusion smoothing constant
SOURCE_DIVERSITY_TOP_N = 5            # optional evaluation experiment
MAX_CHUNKS_PER_SOURCE = 2             # optional evaluation experiment
RERANKER_MODEL_ID = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
LOCAL_RERANKER_MODEL_PATH = (
    EMBEDDING_CACHE_PATH
    / "models--cross-encoder--mmarco-mMiniLMv2-L12-H384-v1"
    / "snapshots"
    / "1427fd652930e4ba29e8149678df786c240d8825"
)
RERANKER_MODEL_NAME = os.getenv(
    "RAG_RERANKER_MODEL_PATH",
    str(LOCAL_RERANKER_MODEL_PATH)
    if LOCAL_RERANKER_MODEL_PATH.exists()
    else RERANKER_MODEL_ID,
)
RERANKER_TOP_N = 5                    # final passages sent to the answering LLM
RERANKER_BATCH_SIZE = 8


# ----------------------------------------------------
# APP SETTINGS
# ----------------------------------------------------
DEFAULT_LANGUAGE_PREF = "Bilingual"   # or: "Portuguese Only" / "English Only"
DEBUG_MODE_DEFAULT = False
