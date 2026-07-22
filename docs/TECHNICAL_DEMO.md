# Technical Demo

## Purpose

This repository demonstrates a bilingual closed-corpus RAG system for retrieving and answering questions about selected ANVISA regulatory documents. The prototype is intended for regulatory-science research and for practical orientation during drug-development and dossier-writing workflows.

## Primary Creator

Carlos Victor Montefusco-Pereira is the primary creator and developer of the prototype. The repository documents the transition from course-based RAG notebooks to an ANVISA-specific regulatory RAG system.

## System Architecture

The final system uses:

- public ANVISA source manifest with URLs and checksums;
- reproducible cleaning script;
- article-level chunks with metadata;
- dense vector retrieval;
- keyword/BM25-style retrieval;
- merged candidate retrieval;
- reranking;
- Portuguese rewrite for English questions;
- cited answer generation;
- refusal when retrieved context is insufficient;
- AI-judge evaluation of answer quality.

## Working Demonstration

Local command:

```bash
streamlit run app.py
```

Included screenshot:

`evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/figures_for_upload/Figure_S4_streamlit_app_rag_answer_smoke_test.png`

Smoke-test question:

> What does RDC 945/2024 regulate?

Output:

> A RDC 945/2024 regulamenta as diretrizes e os procedimentos para a realização de ensaios clínicos com medicamentos no país, incluindo a submissão do Dossiê de Desenvolvimento Clínico de Medicamento (DDCM), visando a posterior concessão de registro de medicamentos [RDC 945/2024, Art. 1].

This confirms app loading, retrieval, answer generation, and citation display. It is not counted as a benchmark result.

## Evaluation Evidence

The evaluation package includes:

- a bilingual article-level gold benchmark;
- prospective retrieval stress-test files;
- AI-judge scoring outputs;
- refusal-focused follow-up tests;
- representative error/fix tables;
- manuscript figures and supplementary files.

Internal high scores, including source hit rate of 1.000 and faithfulness of 1.000, are explicitly interpreted as potentially inflated and not as proof of perfect reliability.

## Data Boundary

The repository does not redistribute the full raw or cleaned ANVISA corpus. It provides source URLs, checksums, and cleaning code so the corpus can be reconstructed from official public sources.
