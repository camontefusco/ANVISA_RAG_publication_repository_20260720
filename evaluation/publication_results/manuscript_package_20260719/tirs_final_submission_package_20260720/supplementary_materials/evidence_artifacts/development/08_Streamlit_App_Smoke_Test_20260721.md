# Streamlit App Smoke Test, 2026-07-21

Purpose: document that the recovered local Streamlit implementation could load and that the backend RAG components could answer a simple traceable regulatory question.

Environment: `/opt/anaconda3/envs/rag-project-env`, Python 3.10.

Local project used for runtime test: `the recovered ANVISA RAG project folder`.

Startup result: `Translator`, Gemini answer wrapper, vector index, hybrid retriever, reranker, and `RetrieverQueryEngine` loaded successfully.

Interface result: Streamlit launched locally, and an evidence view displaying the RAG answer and retrieved sources is provided as Supplementary Figure S4.

Backend query smoke test:

- User question: What does RDC 945/2024 regulate?
- Retrieval rewrite: O que a RDC 945/2024 regulamenta?
- Generated answer: A RDC 945/2024 regulamenta as diretrizes e os procedimentos para a realização de ensaios clínicos com medicamentos no país, incluindo a submissão do Dossiê de Desenvolvimento Clínico de Medicamento (DDCM), visando a posterior concessão de registro de medicamentos [RDC 945/2024, Art. 1].
- Source nodes returned: 5.
- First retrieved source: RDC 945/2024, Art. 1.

Interpretation: this is a local smoke test of the application runtime and backend wiring. It is not counted as an additional benchmark row.
