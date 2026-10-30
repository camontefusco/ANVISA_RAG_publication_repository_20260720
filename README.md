## Current manuscript revision

The cumulative Reviewer 2 revision, clean and tracked manuscripts, response letter, supplements and selected data are in [the 30 October 2026 snapshot](revisions/reviewer_2_20261030/README.md). This is an ongoing revision: human review is AI-assisted and unblinded, the40-row author-led input set was frozen before generation and all40 answers are now saved with human outcome ratings pending, and independent validation and current-law verification remain open. A further clause-level DR8 audit identified partial-repeal and reference-completeness issues beyond the existing replacement drafts. Earlier release materials below retain their historical context.

# Bilingual ANVISA Regulatory RAG Prototype

This repository contains an unpublished bilingual retrieval-augmented generation (RAG) prototype for Portuguese and English question answering over selected public ANVISA regulatory documents. The system was developed by Carlos Victor Montefusco-Pereira as the primary creator and developer, with manuscript and regulatory-science framing by Howard Lopes Ribeiro Junior.

The project is intended as a technical demonstration and reproducibility package for a regulatory-science manuscript. It is not a regulatory decision system, legal opinion, or substitute for direct review of the official ANVISA text.

## Problem

Regulatory drug-development work often requires locating specific requirements across long, technical documents. This prototype tests whether a closed-corpus RAG system can retrieve article-level ANVISA provisions and generate cited answers for practical questions in Portuguese and English.

The intended users are researchers, regulatory-affairs professionals, dossier-writing teams, and pharmaceutical-development staff who need faster orientation to public ANVISA requirements while preserving traceability to the source document and article.

## Intended Use

Appropriate uses:

- Searching selected ANVISA regulations by practical regulatory question.
- Comparing Portuguese and English questions against the same Portuguese source corpus.
- Supporting early dossier planning, clinical-development orientation, medical-device regulatory review, biological-product registration review, and stability-document checks.
- Producing cited draft answers that must be verified against the official ANVISA source.

Not appropriate uses:

- Making final regulatory decisions without human review.
- Interpreting documents outside the included corpus.
- Treating generated answers as official ANVISA guidance.
- Using the system when the retrieved context does not contain the requested answer.

## Architecture

The final prototype uses a closed, article-aware RAG pipeline:

1. Public ANVISA source pages are listed in a source manifest with URLs and checksums.
2. Raw text is cleaned with a reproducible cleaning script.
3. Documents are split into article-level chunks with regulation, article, section, and language metadata.
4. Retrieval combines dense vector search with keyword/BM25-style lexical retrieval.
5. Candidate chunks are merged and reranked.
6. English questions are optionally rewritten into Portuguese while preserving regulatory terms.
7. Answers are generated only from the retrieved context and must cite the source document and article.
8. If the retrieved context does not contain the requested answer, the system is instructed to refuse.

## Repository Contents

- `src/`: final RAG components, including configuration, ingestion, retrieval, translation, model loading, and response synthesis.
- `app.py`: Streamlit application entry point.
- `rebuild_index.py`: index rebuild entry point.
- `evaluation/`: bilingual benchmark files, evaluation scripts, AI-judge artifacts, development traces, and manuscript evidence artifacts.
- `evaluation/publication_results/.../source_reproducibility/`: public ANVISA source manifest, checksums, cleaning script, and redistribution note.
- `docs/`: public-facing technical demo, example queries, release checklist, and source manifest copy.
- `notebooks/`: development notebooks and notebook-derived materials.
- `tests/`: lightweight code tests.
- `.gitignore`: excludes local corpora, vector stores, credentials, and generated caches.

## Installation

Create the environment:

```bash
conda env create -f environment.yml
conda activate rag-project-env
```

Create a local environment file from the example:

```bash
cp .env.example .env
```

Then edit `.env` locally and add your Gemini API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

The `.env` file is intentionally ignored by git.

## Reproducible Pipeline

The reproducibility package is designed around public source reconstruction rather than redistribution of the full cleaned ANVISA corpus.

1. Review the source manifest:

```bash
docs/ANVISA_SOURCE_LINKS_AND_CHECKSUMS_20260720.csv
```

2. Obtain the official ANVISA source texts from the listed URLs.

3. Clean the raw text using:

```bash
python evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/source_reproducibility/clean_regulatory_texts.py
```

4. Rebuild the article-aware index:

```bash
python rebuild_index.py
```

5. Run retrieval and answer-quality evaluation:

```bash
python evaluation/publication_eval.py --help
```

Some evaluation modes call the Gemini API for answer generation, query rewriting, or AI-judge scoring. Deterministic retrieval-only runs can be performed without answer generation.

## Streamlit Demo

Run the app locally:

```bash
streamlit run app.py
```

The repository includes a smoke-test screenshot of a RAG answer with retrieved source evidence:

`evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/figures_for_upload/Figure_S4_streamlit_app_rag_answer_smoke_test.png`

Smoke-test question:

> What does RDC 945/2024 regulate?

Generated answer:

> A RDC 945/2024 regulamenta as diretrizes e os procedimentos para a realização de ensaios clínicos com medicamentos no país, incluindo a submissão do Dossiê de Desenvolvimento Clínico de Medicamento (DDCM), visando a posterior concessão de registro de medicamentos [RDC 945/2024, Art. 1].

This smoke test confirms local app loading and backend wiring. It is not counted as a benchmark row.

## Evaluation Summary

The manuscript package includes a 200-question bilingual article-level benchmark and later stress-test artifacts. Question categories included Portuguese answerable, English answerable, multi-article or exception questions, and unanswerable/adversarial questions.

Key internal results reported in the manuscript evidence package:

| Evaluation stage | Main finding |
| --- | --- |
| Prospective 500-question retrieval stress test | Source hit rate 1.000 and source MRR 0.988; article Recall@5 0.967. |
| AI-judge answer-quality evaluation | Faithfulness 1.000, citation correctness 0.975, completeness 0.943, refusal correctness 0.700. |
| Refusal-focused follow-up test | Refusal correctness improved to 0.944; answerable-control completeness was 0.908. |
| Streamlit smoke test | App loaded and produced a cited answer from RDC 945/2024, Art. 1. |

The internal 1.000 scores are treated as a warning sign, not proof of perfect reliability. They may reflect benchmark construction, closed-corpus constraints, source-level rather than article-level scoring, and proximity between development decisions and evaluation data. The manuscript therefore emphasizes article-level scoring, external/adversarial checks, refusal calibration, and full release of benchmark artifacts.

## Benchmark and Evidence Files

Representative locations:

- `evaluation/benchmark_200_bilingual_article_level_gold.jsonl`
- `evaluation/publication_results/`
- `evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/supplementary_data/`
- `evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/supplementary_materials/`

See `docs/TECHNICAL_DEMO.md` and `docs/EXAMPLE_QUERIES.md` for a shorter entry point.

## Source Documents and Redistribution

The full ANVISA raw and cleaned corpus is not redistributed in this public repository. Instead, the repository provides official source links, SHA-256 checksums, and cleaning code so the corpus can be reconstructed from public sources.

Manifest:

`docs/ANVISA_SOURCE_LINKS_AND_CHECKSUMS_20260720.csv`

Redistribution note:

`evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/source_reproducibility/SOURCE_REPRODUCIBILITY_AND_REDISRIBUTION_NOTE_20260720.md`

## Security and Private Files

The repository should not contain API keys, `.env` files, local vector stores, raw full-text corpora, cleaned full-text corpora, or private files. The `.gitignore` excludes these paths:

- `.env`, `.env.*`
- `data/`
- `cleaned_data/`
- `vector_store/`
- `local_storage/`
- `embedding_cache/`

Before each public release, run a credential and corpus audit.

## License

Code and repository-authored documentation are released under the MIT License. Public ANVISA source documents, third-party materials, and any files governed by external licenses are not relicensed by this repository.

## Citation

Please cite the repository metadata in `CITATION.cff`. A tagged GitHub release and Zenodo DOI should be created before using this repository as a formal technical-demo artifact.

## Creator Statement

Carlos Victor Montefusco-Pereira is the primary creator and developer of this ANVISA RAG prototype. The system was derived from course-based RAG learning materials and then substantially adapted into an ANVISA-specific regulatory prototype with article-aware chunking, bilingual retrieval evaluation, hybrid retrieval, reranking, refusal calibration, AI-judge evaluation, and manuscript evidence packaging.
