# ANVISA Regulatory RAG Evaluation Project

This repository snapshot contains the code, evaluation scripts, benchmark files, result summaries, manuscript materials, figures, tables, and reproducibility metadata for a closed-corpus retrieval-augmented generation project focused on selected ANVISA regulatory documents.

## Contents

- `src/`: RAG application components, retrieval logic, prompts, document metadata, and language utilities.
- `scripts/`: corpus cleaning, benchmark construction, review preparation, and pipeline scripts.
- `evaluation/`: bilingual benchmark files, evaluation code, result summaries, publication result folders, and final TIRS submission package.
- `notebooks/`: development notebooks used during RAG diagnosis and improvement.
- `reports/`: audits and final project reports.
- `tests/`: available unit tests.
- `app.py`, `main.py`, `rebuild_index.py`: Streamlit app and index-building entry points.
- `environment.yml`: conda environment definition.

## Data Availability

The full ANVISA regulatory source text is not redistributed in this repository snapshot. Instead, the final submission package includes official ANVISA source links, SHA-256 checksums for raw and cleaned local files, and the cleaning script used to regenerate cleaned text locally:

`evaluation/publication_results/manuscript_package_20260719/tirs_final_submission_package_20260720/submission_upload_files_20260720/source_reproducibility/`

This choice avoids accidental redistribution of full regulatory text while preserving reproducibility through official source URLs, checksums, and cleaning code.

## Excluded From This Snapshot

- `.env` and local configuration files.
- Raw and cleaned full-text regulatory corpora: `data/`, `cleaned_data/`, `data.zip`.
- Local embedding/model caches: `embedding_cache/`.
- LlamaIndex/local vector-store artifacts: `local_storage/`, `vector_store/`, `vector_store_live_candidate/`.
- Python caches, notebook checkpoints, macOS metadata, temporary files, and LibreOffice lock files.

## Rebuild Outline

1. Recreate the conda environment from `environment.yml`.
2. Download official ANVISA documents listed in the source reproducibility CSV.
3. Run the cleaning script listed in the source reproducibility folder.
4. Rebuild article-level chunks and the vector index using the project scripts.
5. Rerun the bilingual benchmark and AI-judge evaluation scripts in `evaluation/`.

Snapshot date: 2026-07-20.
