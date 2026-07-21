# Supplementary Data S1. Per-question audit table

This folder contains a consolidated per-question audit table for the evaluation rows reported in the manuscript and supplementary materials.

The consolidated table contains 404 evaluated rows, not 500. The 404 rows are the reported per-question evaluation outputs from six stages: 150 internal held-out rows, 75 English completeness-repair rows, 75 Portuguese residual-quality rows, 50 AI-authored prospective stress-test rows, 24 refusal-calibration development rows, and 30 refusal-focused AI-authored test rows.

The authored question files contain 304 rows: the 200-question bilingual benchmark, the 50-row AI-authored prospective stress-test set, the 30-row refusal-focused AI-authored set, and the 24-row refusal-calibration development set. Some questions or question categories appear across development and test stages, so the evaluated-row count and unique authored-question count are not the same.

Files:

- `Supplementary_Data_S1_per_question_audit_404_rows_20260721.csv`: consolidated row-level table with question, answer, expected answer, retrieval outputs, citation fields, deterministic metrics, AI-judge scores, detected error flags, and fix/action linked to each row.
- `Supplementary_Data_S1_stage_counts_20260721.csv`: counts by evaluation stage and source file.

Error flags are operational audit flags used during development. They are not regulatory acceptance criteria. AI-judge scores are technical reproducibility indicators and not expert validation.
