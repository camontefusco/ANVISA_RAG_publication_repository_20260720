# Complete submission evidence: read first

This is the locally completed supplementary-data package prepared on 4 November 2026. It is distributed with GitHub v0.3.2 and supersedes the earlier organized archive for evidence completeness. The published v0.3.1 release and its archive are preserved unchanged. No new Zenodo version DOI is claimed. Scientific results and human judgments have not been changed.

## Find a study

1. **Historical benchmark and 94-output human review**: [data/historical_S1_S2](data/historical_S1_S2/), [data/historical_author_review](data/historical_author_review/).
2. **DR11 tokenizer and 300-answer comparison**: [data/DR11](data/DR11/).
3. **Retrieval and rule ablations**: [data/DR12_retrieval_ablation_sources](data/DR12_retrieval_ablation_sources/), [data/DR13](data/DR13/).
4. **Sibling-context experiment and 44 human ratings**: [data/sibling_context](data/sibling_context/).
5. **Frozen 40-answer test and Howard review**: [data/Howard40_review](data/Howard40_review/).
6. **Mechanism and repair diagnostics**: [data/partial_prompt_pilot](data/partial_prompt_pilot/), [data/partial_mechanism_factorial](data/partial_mechanism_factorial/), [data/combined_repair_comparison](data/combined_repair_comparison/), [data/automatic_evidence_followup](data/automatic_evidence_followup/), [data/residual_mechanisms](data/residual_mechanisms/), [data/four_question_context_controls](data/four_question_context_controls/), [data/ethics_length_and_prompt_controls](data/ethics_length_and_prompt_controls/).
7. **Integrated validation and 80-answer author assessment**: [data/integrated_validation_completed_20261101](data/integrated_validation_completed_20261101/), [data/integrated_scope_resolved_20261101](data/integrated_scope_resolved_20261101/), [data/author_review_completion_80_20261101](data/author_review_completion_80_20261101/).
8. **Hybrid, BM25 and model-only comparison with 118 distinct human ratings**: [data/comparative_baselines_20261102](data/comparative_baselines_20261102/), [data/author_review_completed_20261103](data/author_review_completed_20261103/).
9. **Dated-corpus comparison and regulatory dependencies**: [Supplementary_Data_S16](Supplementary_Data_S16/).
10. **Shared code, source provenance and run-date ledger**: [data/reproducibility_code](data/reproducibility_code/), [data/source_provenance](data/source_provenance/), [data/model_provenance](data/model_provenance/).

## How to use the files

Within each study, read the current guide before using historical summary or provenance files. Frozen inputs, individual outputs, original human returns and derived results are separate. MANUSCRIPT_DATA_MAP.csv maps manuscript topics to existing evidence paths; STUDY_INDEX.csv is the shorter study-level index. FILE_INDEX.csv records every payload file, its size and SHA-256. ADDED_EVIDENCE_MANIFEST.csv identifies local originals restored in this patch. COMPLETENESS_QA.json documents verification. VERIFY_PACKAGE.py verifies hashes, row counts and DR11 scoring arithmetic without model calls or network access.

Original study paths are retained so existing scientific citations and frozen manifests remain interpretable. This is why the package uses named study folders under data/ rather than renumbering all original paths. Historical scripts may require their original execution layout; preserved code is not automatically a portable reproduction command. S16 retains its separately documented portable count recalculation.

## Scope and limitations

Restored files close distribution gaps, not scientific limitations. Independent external validation and measured human workflow benefit remain absent. DR11 and dated-corpus component assessments retain their documented automated/provisional status. The original and corrected human-review provenance must be read separately by cohort; draft labels in original returns are preserved. Credentials, full source/index corpora and concealed coordinator keys are excluded deliberately.
