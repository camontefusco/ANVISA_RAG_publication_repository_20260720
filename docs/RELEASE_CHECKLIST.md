# Release Checklist

Use this checklist before using the GitHub repository as a public technical-demo artifact.

## Required Before Public Release

- README explains the problem, architecture, intended use, and limitations.
- Installation instructions are present.
- `.env.example` exists and `.env` is ignored.
- Reproducible ingestion, indexing, and evaluation commands are documented.
- Streamlit app entry point and screenshot are documented.
- Example queries with cited outputs are documented.
- Evaluation results and benchmark files are present.
- ANVISA source manifest includes official URLs and SHA-256 checksums.
- Raw and cleaned full-text corpora are not redistributed unless permission is confirmed.
- API keys, credentials, local vector stores, and private files are absent.
- License file is present.
- `CITATION.cff` is present.
- Carlos Victor Montefusco-Pereira is identified as primary creator and developer.

## Recommended Before Proposal or Manuscript Submission

- Create a git tag, for example `v0.1.0`.
- Push the tag to GitHub.
- Create a GitHub release from the tag.
- Archive the release through Zenodo.
- Add the Zenodo DOI to `README.md` and `CITATION.cff`.

## Checks To Run

```bash
git status --short
rg -n --hidden -g '!.git/**' -g '!*.jsonl' -g '!*.csv' -g '!*.ipynb' 'API_KEY|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9]' .
find . -maxdepth 3 -type d \( -name data -o -name cleaned_data -o -name vector_store -o -name local_storage -o -name embedding_cache \)
```

## Current DOI Status

No Zenodo DOI is recorded in this repository yet. This should be completed after the release is tagged.
