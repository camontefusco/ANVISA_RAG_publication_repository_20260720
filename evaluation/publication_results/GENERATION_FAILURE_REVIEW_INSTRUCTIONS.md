# Generation Failure Manual Review Instructions

Review file:

`evaluation/publication_results/generation_failure_manual_review_20260714.csv`

This file contains the 36 generated-answer rows flagged by automated screening:
25 English and 11 Portuguese. Rows are randomized with a fixed seed.

## How To Score Pass 1

Fill only the `pass1_*` columns first. Use `1` for acceptable/correct and `0` for
not acceptable/incorrect.

- `pass1_retrieval_correct_0_1`: retrieved evidence is sufficient for the answer.
- `pass1_answer_grounded_0_1`: generated answer does not add unsupported claims.
- `pass1_answer_complete_0_1`: generated answer covers the expected essential points.
- `pass1_citation_correct_0_1`: citations are exact and support the cited claim.
- `pass1_refusal_correct_0_1`: answerable questions are answered; unanswerable questions are refused.
- `pass1_overall_acceptable_0_1`: answer would be acceptable for the intended regulatory assistant use.
- `pass1_root_cause`: use a short category such as `retrieval`, `incomplete_answer`, `citation`, `false_refusal`, `benchmark_issue`, or `acceptable_false_positive`.
- `pass1_notes`: brief rationale.

## Delayed Pass 2

Wait at least seven days, then fill the `pass2_*` columns without consulting pass
1. The summary script reports intra-rater repeatability; do not describe it as
inter-rater agreement.

## Summarize Labels

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B \
  evaluation/summarize_manual_generation_review.py \
  evaluation/publication_results/generation_failure_manual_review_20260714.csv
```

Outputs:

- `manual_generation_review_summary.md`
- `manual_generation_review_summary.json`
