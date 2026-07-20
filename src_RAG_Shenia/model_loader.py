# import necessary modules
import os
from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms import LLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
#________________________________________________________________________________   
from src.config import (
    EMBEDDING_MODEL_NAME,
    LLM_MODEL,
    LLM_MAX_NEW_TOKENS,
    LLM_TEMPERATURE,
    LLM_TOP_P,
    LLM_REPETITION_PENALTY,
    SEMANTIC_SPLITTER_EMBEDDING_MODEL_NAME,
    EMBEDDING_CACHE_PATH
)
#________________________________________________________________________________   
# Load environment
load_dotenv()
#________________________________________________________________________________   
#________________________________________________________________________________   
# ***--- DEFINING FUNCTIONS ---***
#________________________________________________________________________________   
#________________________________________________________________________________   
#________________________________________________________________________________   
# --- LLM Initialisation ---
# without hyde
# def initialise_llm() -> GoogleGenAI:
#     """Initialises the GoogleGenAI LLM with core parameters from config."""

#     api_key: str | None = os.getenv("GOOGLE_API_KEY")

#     if not api_key:
#         raise ValueError(
#             "GOOGLE_API_KEY not found. Make sure it's set in your .env file."
#         )

#     return GoogleGenAI(
#         api_key=api_key,
#         model=LLM_MODEL,
#         repetition_penalty=LLM_REPETITION_PENALTY,
#         max_new_tokens=LLM_MAX_NEW_TOKENS,
#         temperature=LLM_TEMPERATURE,
#         top_p=LLM_TOP_P,
#     )
# using hyde 
def initialise_hyde_llm() -> GoogleGenAI:
    """Initialises the GoogleGenAI LLM with core parameters from config."""

    api_key: str | None = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Make sure it's set in your .env file."
        )

    return GoogleGenAI(
        api_key=api_key,
        model=LLM_MODEL,
        repetition_penalty=LLM_REPETITION_PENALTY,
        max_new_tokens=LLM_MAX_NEW_TOKENS,
        temperature=LLM_TEMPERATURE,
        top_p=LLM_TOP_P,
    )
#________________________________________________________________________________   
# # --- EMBEDDING ---
def get_embedding_model() -> HuggingFaceEmbedding:
    """Initialises and returns the HuggingFace embedding model"""
    # Create the cache directory if it doesn't exist
    EMBEDDING_CACHE_PATH.mkdir(parents=True, exist_ok=True)

    return HuggingFaceEmbedding(
        model_name=EMBEDDING_MODEL_NAME, 
        cache_folder=EMBEDDING_CACHE_PATH.as_posix()
    )
# #________________________________________________________________________________   
# # --- SPLITTER EMBEDDING  ---
def get_splitter_embedding_model() -> HuggingFaceEmbedding:
    """Initialises and returns the HuggingFace embedding model for sentence embedding"""
    
    # Create the cache directory if it doesn't exist
    EMBEDDING_CACHE_PATH.mkdir(parents=True, exist_ok=True)

    return HuggingFaceEmbedding(
        model_name=SEMANTIC_SPLITTER_EMBEDDING_MODEL_NAME, # <--- these different params must be set in the config file and imported in the model_loader.py file
        cache_folder=EMBEDDING_CACHE_PATH.as_posix()
    )
# #________________________________________________________________________________   
# --- LOADING LLM ---
def load_llm_model(model_name: str = "gemini-2.5-flash") -> LLM:
    """
    Loads and returns the desired Google GenAI LLM instance. 
    The API key is expected to be managed by the runtime environment.

    Args:
        model_name: The name of the Gemini model to use.

    Returns:
        LLM: The initialized LLM instance.
    """
    print(f"Loading LLM model for Query Condensation: {model_name}...")
    # Using GoogleGenAI as the default LLM
    llm = GoogleGenAI(model=model_name)
    return llm
#________________________________________________________________________________   
