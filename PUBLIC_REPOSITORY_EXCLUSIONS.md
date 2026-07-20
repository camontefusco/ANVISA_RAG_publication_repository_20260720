# Repository Exclusions

This publication repository snapshot intentionally excludes secrets, caches, local vector stores, temporary files, and full ANVISA source-text corpora. The excluded source texts can be regenerated from official ANVISA links using the checksums and cleaning script in the final submission package.

Excluded top-level directories: `data/`, `cleaned_data/`, `embedding_cache/`, `local_storage/`, `vector_store/`, `vector_store_live_candidate/`, `.tmp/`, `.vscode/`, `.ipynb_checkpoints/`, and Python cache folders.

Excluded files include `.env`, `data.zip`, macOS `.DS_Store`, Python bytecode, notebook checkpoints, and LibreOffice lock files.
