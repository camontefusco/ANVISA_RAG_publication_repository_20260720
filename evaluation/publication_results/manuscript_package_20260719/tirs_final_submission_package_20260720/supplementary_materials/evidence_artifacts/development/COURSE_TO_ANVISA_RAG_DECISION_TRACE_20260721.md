# Course-to-ANVISA RAG Decision Trace

Prepared: 2026-07-21

This note records the traceable development path from the course notebooks to the final ANVISA RAG pipeline.

## Local files located

- Course notebooks were found in `/Users/cmontefusco/Downloads/1_LLM.ipynb`, `/Users/cmontefusco/Downloads/2_chatbot.ipynb`, and `/Users/cmontefusco/Downloads/3_rag.ipynb`.
- Copies of those notebooks are also present in the publication repository under `notebooks/`.
- The original path reported at the start of the project, `/Users/cmontefusco/Documents/DSAI2/Rag_project`, is no longer present.
- A moved/recovered project was found at `/Users/cmontefusco/Coding_projects/Rag_project`.
- A Codex recovered copy was found at `/Users/cmontefusco/projects/Codex/2026-06-16/files-mentioned-by-the-user-rag/Rag_project`.

## Interpretation

The recovered `Coding_projects/Rag_project` folder is the best local evidence for the first ANVISA RAG implementation. It contains the ANVISA Streamlit app, ANVISA `data/` and `cleaned_data/` files, `src_RAG_Shenia/`, current `src/`, notebooks 1 through 7, evaluation scripts, vector stores, and publication-result files. Its git history records one archive commit on 2026-07-17, so file modification times mainly document recovery rather than original authorship dates.

## Development decisions

1. The course notebooks established the Python project layout, environment file, `.env` configuration, model loader, engine module, and command-line chat loop.
2. The chatbot notebook introduced a system prompt and conversational interface.
3. The RAG notebook introduced LlamaIndex document loading, HuggingFace embeddings, persistent vector storage, and retrieval before answering.
4. The ANVISA idea replaced the generic teaching corpus with selected Brazilian regulatory documents.
5. Shenia's source was kept as a comparison and source of implementation ideas, especially semantic splitting, HyDE, reranking, and chat memory.
6. The final publication system did not keep the Shenia architecture as-is. It moved to article-aware chunks, hybrid dense/BM25 retrieval, reciprocal-rank fusion, cross-encoder reranking, bilingual retrieval anchors, article-level citations, refusal rules, and AI-judge evaluation.
7. The high internal scores were treated as a diagnostic risk. The project therefore ran an AI-authored prospective stress test before additional tuning.
8. The prospective stress test showed that refusal calibration, not ordinary source retrieval, was the main weak point.
9. Refusal was repaired on separate development data and checked on a new refusal-focused AI-authored set.
10. The final claim is limited to traceable, closed-corpus information access. It is not a validation of regulatory advice.

