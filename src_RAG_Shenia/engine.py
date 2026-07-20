#imports
#________________________________________________________________________________   
from llama_index.core import (
    StorageContext,
    SimpleDirectoryReader,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.chat_engine.condense_plus_context import CondensePlusContextChatEngine
# from llama_index.core.memory import ChatMemoryBuffer
# from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.schema import Document
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.retrievers.transform_retriever import TransformRetriever
from llama_index.core.retrievers import TransformRetriever
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core.memory import ChatSummaryMemoryBuffer
#________________________________________________________________________________   
#import configs
from src.config import (
    # CHUNK_OVERLAP,
    # CHUNK_SIZE, # use these for basic splitting --- IGNORE ---
    DATA_PATH,
    LLM_SYSTEM_PROMPT,
    SIMILARITY_TOP_K,
    VECTOR_STORE_PATH,
    CHAT_MEMORY_TOKEN_LIMIT,
    RERANKER_TOP_N,    
    RERANKER_MODEL_NAME,
    # CONDENSE_PROMPT_TMPL, # <--- IGNORE ---for now, unless you want to have more control over a query condenser
    # EMBEDDING_CACHE_PATH,
    # EMBEDDING_MODEL_NAME,
    BUFFER_SIZE,
    BREAKPOINT_PERCENTILE_THRESHOLD
)
from src.model_loader import (
    get_embedding_model,
    get_splitter_embedding_model,
    # initialise_llm,
    initialise_hyde_llm
)
#________________________________________________________________________________   
#________________________________________________________________________________   
# ***--- DEFINING FUNCTIONS ---***
#________________________________________________________________________________   
#________________________________________________________________________________   
# --- CREATING NEW VECTOR STORE ---
def _create_new_vector_store(
        embed_model: HuggingFaceEmbedding
) -> VectorStoreIndex:
    """Creates, saves, and returns a new vector store from documents."""
    print(
        "Creating new vector store from all files in the 'data' directory..."
    )

    # This reads all the text files in the specified directory.
    documents: list[Document] = SimpleDirectoryReader(
        input_dir=DATA_PATH
    ).load_data()

    if not documents:
        raise ValueError(
            f"No documents found in {DATA_PATH}. Cannot create vector store."
        )

    # # This breaks the long document into smaller, more manageable chunks.
    # text_splitter: SentenceSplitter = SentenceSplitter(
    #     chunk_size=CHUNK_SIZE,
    #     chunk_overlap=CHUNK_OVERLAP
    # )

    ## This is the core of the vector store. It takes the text chunks,
    ## uses the embedding model to convert them to vectors, and stores them.
    # index: VectorStoreIndex = VectorStoreIndex.from_documents(
    #     documents,
    #     transformations=[text_splitter],
    #     embed_model=embed_model
    # )

#for symantic splitting: 
    semantic_splitter_embedding_model = get_splitter_embedding_model()
    # This breaks the documents into chunks wherever there is a semantic shift between sentences
    semantic_splitter: SemanticSplitterNodeParser = SemanticSplitterNodeParser( # <--- new splitter with new params
        buffer_size=BUFFER_SIZE, 
        breakpoint_percentile_threshold=BREAKPOINT_PERCENTILE_THRESHOLD,
        embed_model=semantic_splitter_embedding_model
    )

    # This is the core of the vector store. It takes the text chunks,
    # uses the embedding model to convert them to vectors, and stores them.
    index: VectorStoreIndex = VectorStoreIndex.from_documents(
        documents,
        transformations=[semantic_splitter], # <--- swapped
        embed_model=embed_model
    )
    # This saves the newly created index to disk for future use.
    index.storage_context.persist(persist_dir=VECTOR_STORE_PATH.as_posix())
    print("Vector store created and saved.")
    return index
#________________________________________________________________________________   
# --- EMBEDDING  ---
def get_vector_store(embed_model: HuggingFaceEmbedding) -> VectorStoreIndex:
    """
    Loads the vector store from disk if it exists;
    otherwise, creates a new one.
    """
    # Create the parent directory if it doesn't exist.
    VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)

    # Check if the directory contains any files.
    if any(VECTOR_STORE_PATH.iterdir()):
        print("Loading existing vector store from disk...")
        storage_context: StorageContext = StorageContext.from_defaults(
            persist_dir=VECTOR_STORE_PATH.as_posix()
        )
        # We must provide the embed_model when loading the index.
        return load_index_from_storage(
            storage_context,
            embed_model=embed_model
        )
    else:
        # If the directory is empty,
        # call our internal function to build the index.
        return _create_new_vector_store(embed_model)
#________________________________________________________________________________  
# # --- CHAT ENGINE  ---
# basic version without reranker and condense plus context 
# def get_chat_engine(
#         llm: GoogleGenAI,
#         embed_model: HuggingFaceEmbedding
# ) -> CondensePlusContextChatEngine:
#     """Initialises and returns the main conversational RAG chat engine."""
#     vector_index: VectorStoreIndex = get_vector_store(embed_model)
#     memory: ChatMemoryBuffer = ChatMemoryBuffer.from_defaults(
#         token_limit=CHAT_MEMORY_TOKEN_LIMIT
#     )

#     ## Assemble the RAG chat engine
#     # chat_engine: BaseChatEngine = vector_index.as_chat_engine(
#         # memory=memory,
#         # llm=llm,
#         # system_prompt=LLM_SYSTEM_PROMPT,
#         # similarity_top_k=SIMILARITY_TOP_K,
#     # )
#     # return chat_engine

#     retriever = vector_index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)

#     reranker: SentenceTransformerRerank = SentenceTransformerRerank( 
#         top_n=RERANKER_TOP_N,         
#         model=RERANKER_MODEL_NAME     
#     )
#     chat_engine: CondensePlusContextChatEngine = CondensePlusContextChatEngine( 
#         retriever=retriever,
#         llm=llm,
#         memory=memory,
#         system_prompt=LLM_SYSTEM_PROMPT,
#         node_postprocessors=[reranker]
#     )
#     return chat_engine
#________________________________________________________________________________   
# hyde version with reranker and condense plus context
def get_chat_engine(
    llm: GoogleGenAI,
    embed_model: HuggingFaceEmbedding
) -> CondensePlusContextChatEngine:
    """Initialises and returns the main conversational RAG chat engine."""

    # Access index (vector database)
    vector_index: VectorStoreIndex = get_vector_store(embed_model)

    # Set up chunk retriever
    base_retriever: BaseRetriever = vector_index.as_retriever(similarity_top_k=SIMILARITY_TOP_K)

    # Set up HyDE system
    hyde: HyDEQueryTransform = HyDEQueryTransform(
        include_original=True, 
        llm=initialise_hyde_llm()
    )

    # Combine HyDE with retriever
    hyde_retriever: TransformRetriever = TransformRetriever(
        retriever=base_retriever, 
        query_transform=hyde
    )

    # Set up chunk reranker
    reranker: SentenceTransformerRerank = SentenceTransformerRerank( 
        top_n=RERANKER_TOP_N, 
        model=RERANKER_MODEL_NAME
    )

    # Set up chat memory (summary memory condenses chat history)
    memory: ChatSummaryMemoryBuffer = ChatSummaryMemoryBuffer.from_defaults(
        token_limit=CHAT_MEMORY_TOKEN_LIMIT
    )

    # Set up chat engine with memory, retriever, and reranker
    chat_engine: CondensePlusContextChatEngine = CondensePlusContextChatEngine( 
        retriever=hyde_retriever,
        llm=llm,
        memory=memory,
        system_prompt=LLM_SYSTEM_PROMPT,
        node_postprocessors=[reranker]
    )

    return chat_engine
#________________________________________________________________________________   
# --- DEFINING THE CHAT LOOP ---
def main_chat_loop() -> None:
    """Main application loop to run the RAG chatbot."""
    print("--- Initialising models... ---")
    llm: GoogleGenAI = initialise_hyde_llm()
    embed_model: HuggingFaceEmbedding = get_embedding_model()
    # The get_chat_engine now returns a ContextChatEngine that uses
    # the CondenseQuestionQueryEngine for better contextual understanding.
    chat_engine: CondensePlusContextChatEngine = get_chat_engine(
        llm=llm,
        embed_model=embed_model
    )
    print("--- RAG Chatbot Initialised (Using Condensed Querying). ---")
    
    # # Run the chat loop
    chat_engine.chat_repl()
#________________________________________________________________________________   

