# ANVISA RAG v0.3.1 Organized supplementary data

This organization-only patch improves the supplementary archives accompanying the finalized revision. All 32 supplied reviewer responses remain approved. No question, reference, answer, assessment, metric, figure, manuscript or reviewer-response wording changed. Journal submission has not occurred.

## Start here

- journal_upload/ contains the 14 journal-facing files. Its Supplementary_Data_S16.zip now opens into clearly labeled folders and a read-first guide.
- evidence/Supplementary_Data_S16_READ_ME_FIRST.md explains the standalone S16 archive.
- evidence/00_READ_ME_FIRST.md and evidence/MANUSCRIPT_DATA_MAP.csv guide readers through the larger revision_data.zip by manuscript section, table and figure.
- FILE_INDEX.csv inside each archive identifies contents and purpose. ORIGINAL_PATH_MAP.csv inside S16 maps the former flat layout to the organized folders and records unchanged hashes.
- release_audit/ORGANIZATION_QA.json records byte preservation; S16_RECALCULATED_COUNTS.json independently reproduces the existing headline counts and intervals.

## S16 structure

1. Protocol: frozen plan, subgroups, prompts and hashes.
2. Questions, references and evidence: inputs, exclusions, sources and selected contexts.
3. Answers and results: saved answers, provisional AI assessments, counts and paired comparisons.
4. Regulatory dependency audit: linked instruments, successor evidence and unresolved items.
5. Provenance and limitations: model/source records, hypotheses and negative findings.
6. Reproduction code: portable count recalculation plus original scripts clearly identified by scope.
7. Historical validation: dated completion-stage records, not current editorial status.

The active results guide now correctly states that these results are integrated into the manuscript and response letter. Its earlier not-yet-integrated sentence was stale. The original guide remains explicitly historical; the earlier release remains available unchanged.

The larger evidence archive retains existing data/ paths so manuscript references, code and frozen manifests remain usable. Its topic map and full file index provide navigation. The duplicated S16 subset inside it uses the same organized structure as the standalone archive.

## Version and scientific status

The unchanged scientific documents cite v0.3.0, which preserves their original evidence snapshot. v0.3.1 is a navigation and packaging patch, not a new scientific analysis. Earlier releases are not overwritten. No new Zenodo DOI is claimed.

The dated-corpus component ratings remain provisional AI assessments. Howard's corrected historical score-exposure provenance and AI-draft assistance remain disclosed. Current-law accuracy, fresh independent external validation and measured workflow benefit remain unestablished.

GitHub release: https://github.com/camontefusco/ANVISA_RAG_publication_repository_20260720/releases/tag/v0.3.1
