# ANVISA RAG review release v0.3.0-rc.1

This 4 November 2026 review snapshot supersedes the v0.2.1 submission files for ongoing revision. It is a prerelease: DR33-DR34 remain pending author discussion. See REVIEW_STATUS.md before using it for submission.

## Files and their purpose

| Folder or file | Purpose |
| --- | --- |
| journal_upload/ | Clean and cumulative tracked Word manuscripts, justified reviewer response, tables, figure legends, supplementary PDF, Data S16 and seven 600-dpi TIFFs. These are candidate journal-facing files; submission has not occurred. |
| documents/ | Editable documents and rendered PDFs for reading and review. |
| figures/ | PDF/vector versions of Figures 1-6 and Supplementary Figure S1. TIFFs are in journal_upload/figures/. |
| evidence/revision_data.zip | Curated code, original outputs, separate assessments, source checksums, dated-corpus analysis, restored run ledger and rule audit. |
| evidence/Supplementary_Data_S16.zip | Dated-corpus experiment and linked-instrument dependency audit. Also copied in journal_upload/. |
| release_audit/ | Inventories, line map, reviewer crosswalk and validation results. Do not upload these audit files as manuscript supplements. |
| inventory.csv | File-by-file purpose, size and SHA-256. |
| SHA256_MANIFEST.csv | Checksums for all release files except the manifest itself. |

## Changes from v0.2.1

Adds the 188-question dated-corpus comparison, Figure 6 and Data S16; source-dependency audit; S13 run-date ledger and Table S26; S14 full glossary/rule audit; tokenizer evidence; consolidated concern-by-concern responses; explicit patient-identification scoring discrepancy and prompt-aligned refusal limitation; corrected score-exposure provenance; all seven 600-dpi figure exports.

Existing reported scores are preserved. Common-prompt coauthor success remains hybrid 39/40, BM25 38/40 and model-only 9/40. Hybrid superiority over BM25 remains unproven. The additional dated-corpus result is provisional AI assessment: 144/188 versus 172/188, difference +14.9 points (95% paired interval 7.4 to 22.9). Source updating and structural curation were bundled, development questions reused, and human confirmation of component ratings remains incomplete.

## Reproducibility entry points

Inside evidence/revision_data.zip: data/reproducibility_code/scripts/clean_regulatory_texts.py; data/source_provenance/historical_raw_and_clean_source_checksums.csv; data/source_provenance/official_sources_and_snapshot_checksums.csv; data/model_provenance/reported_stage_run_dates.csv; data/DR13/rule_audit_restored_20261104/; Supplementary_Data_S16/.

Full source/index corpora, credentials and concealed coordinator keys are excluded. Official links and snapshot hashes support source reconstruction. A dated snapshot does not certify current law. Use initial AI judgments, author overlays and adjudications according to the active evidence guide, not historical pending-review labels.

GitHub release: https://github.com/camontefusco/ANVISA_RAG_publication_repository_20260720/releases/tag/v0.3.0-rc.1

The previous v0.2.1 Zenodo DOI https://doi.org/10.5281/zenodo.23925532 identifies the earlier snapshot, not this release. No new Zenodo DOI is claimed. Earlier tags and release assets remain unchanged.
