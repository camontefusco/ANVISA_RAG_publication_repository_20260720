# Current revision and release

Version v0.2.1 contains the [checked GPEC and table revision](revisions/reviewer_2_20261103_v021/README.md), with the complete submission ZIP, updated response, all figure/table alignment checks, and recovered S14/S15 numeric sources. Scientific scores are unchanged from v0.2.0. Earlier snapshots remain intact. The verified v0.2.1 DOI is https://doi.org/10.5281/zenodo.23925532. The [current DOI-linked submission](revisions/v021_linked_20261103/README.md) adds that citation without changing scientific results.

The [citation-linked submission variant](revisions/release_linked_20261103/README.md) adds the verified DOI and refreshed response line references after archival; scientific data and figures are unchanged. The tagged v0.2.0 snapshot remains intact.

The current coauthor-reviewed revision is [3 November 2026](revisions/reviewer_2_20261103/README.md). It contains the clean and cumulative tracked manuscripts, full reviewer response, supporting documents, figures and curated evidence. The [complete package](revisions/reviewer_2_20261103/submission_ready_20261103.zip) also contains the high-resolution TIFF files. Earlier dated revisions are historical snapshots and may contain superseded scores or review-status descriptions.

The new common-prompt study has 118 distinct coauthor-rated answers representing 120 condition records. Hybrid, BM25 and model-only content success is 39/40, 38/40 and 9/40 answers, or 19/20, 18/20 and 4/20 bilingual pairs. Hybrid superiority over BM25 is unproven (+5 percentage points; descriptive 95% paired interval -10 to +20; exact p = 1.000). Review date: 2 November; prior project/question exposure and limited condition masking are disclosed. Original AI scores and disagreements remain separate. Current-law accuracy and fresh independent validation are not established.

The preceding release is version v0.2.0. Prior version v0.1.2 is archived at https://doi.org/10.5281/zenodo.21504214; the all-versions DOI is https://doi.org/10.5281/zenodo.21504181. Version v0.2.0 is published at https://doi.org/10.5281/zenodo.23909097. Cite this version-specific DOI for the completed November results; the prior version does not contain them.

# Bilingual ANVISA Regulatory RAG Prototype

This repository contains a bilingual archived-corpus retrieval-augmented generation (RAG) prototype for Portuguese and English question answering over selected public ANVISA regulatory documents. The system was developed by Carlos Victor Montefusco-Pereira as the primary creator and developer, with manuscript and regulatory-science framing by Howard Lopes Ribeiro Junior.

The project is intended as a technical demonstration and reproducibility package for a regulatory-science manuscript. It is not a regulatory decision system, legal opinion, or substitute for direct review of the official ANVISA text.

## Problem

Regulatory drug-development work often requires locating specific requirements across long, technical documents. This prototype tests whether a closed-corpus RAG system can retrieve article-level ANVISA provisions and generate cited answers for practical questions in Portuguese and English.

The intended users are researchers, regulatory-affairs professionals, dossier-writing teams, and pharmaceutical-development staff who need faster orientation to public ANVISA requirements while preserving traceability to the source document and article.

## Intended Use

Appropriate uses:

- Searching selected ANVISA regulations by practical regulatory question.
- Comparing Portuguese and English questions against the same Portuguese source corpus.
- Supporting early dossier planning, clinical-development orientation, medical-device regulatory review, biological-product registration review, and archived regulatory-document checks; current applicability must be established separately.
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

## Evaluation summary and provenance

The constructed historical benchmark had 200 questions in 100 bilingual pairs; six overlapping evaluation stages produced 404 outputs with 254 distinct IDs. Repair and calibration reuse precludes independent generalization or a causal before/after calibration claim. The diagnostic stress set contained 50 outputs, not 500 questions. Original labels, problematic revoked-source references and historical Gemini-judge scores remain available as evidence, separately from corrections and author review.

| Assessment | Main result |
| --- | --- |
| Frozen 40-answer coauthor assessment | 10/20 bilingual pairs passed; 6/12 answerable, 0/4 partly answerable, 4/4 unanswerable. |
| Earlier 80-answer repair comparison, completed author review | 14/20 baseline versus 17/20 repair; exact paired p = 0.375. Initial AI scores are separate. |
| Common-prompt three-condition coauthor comparison | Hybrid 19/20, BM25 18/20, model-only 4/20 pairs; no established hybrid advantage over BM25. |
| Matched retrieval coverage | BM25/hybrid all required articles at five: 30/32 versus 32/32. Structural coverage is not answer quality. |

Historical saturated faithfulness scores are not proof of reliability. Source validity, reference completeness, selected evidence, language and refusal behavior require separate checks. Regulatory status checks are targeted; the corpus is not maintained as consolidated current law. The older Streamlit demonstration is not bilingual deployment-validation evidence. No workflow time or decision benefit was measured. See the current revision, not older reports, for the active interpretation.

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

Please cite the specific tagged evidence release using `CITATION.cff`. The concept DOI identifies the complete version family; a version-specific DOI identifies the exact archived snapshot. See the release section above for current identifiers.

## Creator Statement

Carlos Victor Montefusco-Pereira is the primary creator and developer of this ANVISA RAG prototype. The system was derived from course-based RAG learning materials and then substantially adapted into an ANVISA-specific regulatory prototype with article-aware chunking, bilingual retrieval evaluation, hybrid retrieval, reranking, refusal calibration, AI-judge evaluation, and manuscript evidence packaging.
