# GitHub package inventory audit 4 November 2026

## Previously published package

Audited public main commit 459e68879931cebc469533312b1227455ca2f76e and downloaded the actual v0.2.1 submission_ready_20261103_v021.zip release asset. Its SHA-256 matched GitHub: 078cfaa6bfc4af6b42630d764470c59a257f02cef8fe0adc01a5ce1b0a65c693. All 51 listed manifest files passed, with no missing entries or mismatches. Code, cleaning script, both source checksum CSVs and the Table S14/S15 numeric sources were present.

Gaps: Figure 6/Data S16, S13 run ledger and full restored S14 rule audit were absent; reader documents and data guide retained the superseded score-exposure account; main Figures 1-4 TIFFs were 400 dpi and Figure 5/S1 300 dpi. Three README benchmark/supplement paths did not exist. QA/history files were mixed with journal-facing files.

## New review release

The v0.3.0 package adds the missing materials and corrected provenance, all seven TIFF figures at 600 dpi, and consolidated concern-by-concern responses with rendered manuscript locations. Folder separation distinguishes journal-upload candidates, reading/editable documents, evidence and release-audit records. inventory.csv identifies every file by purpose, size and checksum. SHA256_MANIFEST.csv validates the package; evidence_archive_inventory.csv enumerates the nested evidence ZIP. The cleaning script and both source checksum CSVs are explicitly checked in release_audit/VALIDATION.json.

Tracked-change accept/reject projections match the current clean manuscript and September submission, respectively. Thirty-two reviewer comments remain verbatim; DR21/DR23 are absent from the source PDF. DR33/DR34 are approved and integrated. This is a finalized revision release, not a final submission or proof that every scientific concern is resolved. Earlier tags and release assets are preserved.

The new release has no claimed Zenodo DOI. The preceding version DOI identifies v0.2.1 only. All old snapshots should be treated as historical evidence rather than mixed with the new active package.

Package guide: ../revisions/reviewer_2_20261104_final/README.md
Inventory: ../revisions/reviewer_2_20261104_final/inventory.csv
Release: https://github.com/camontefusco/ANVISA_RAG_publication_repository_20260720/releases/tag/v0.3.0
