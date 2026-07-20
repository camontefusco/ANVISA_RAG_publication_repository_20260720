# Bilingual Held-Out Generation Comparison

Generated from the frozen `held_out_test_75` split after repairing cloud-placeholder
files and running controlled-context answer generation.

| Metric | English | Portuguese |
|---|---:|---:|
| Rows | 75 | 75 |
| Answerable questions | 60 | 60 |
| Unanswerable questions | 15 | 15 |
| Source hit rate | 0.933 | 1.000 |
| Article Recall@5 | 0.600 | 0.933 |
| Generated-answer term coverage | 0.553 | 0.749 |
| Citation presence | 0.800 | 0.983 |
| Article citation presence | 0.800 | 0.983 |
| Retrieved-citation validity | 0.800 | 0.983 |
| Refusal accuracy on unanswerable questions | 1.000 | 1.000 |

## Interpretation

- Portuguese held-out generation is publication-ready as an internal technical result, pending human review.
- English held-out generation improved with glossary candidate expansion plus original-question reranking, but answer quality is still limited by article-level retrieval.
- Unanswerable/refusal behavior is strong in both languages on this held-out split.
- These are automated screening metrics. Final claims still need manual review of the generated answers and failure audit rows.

## Run Files

- English: `evaluation/publication_results/generation_en_heldout_20260709/generation_summary_2026-07-10_01-03-11.md`
- Portuguese: `evaluation/publication_results/generation_pt_heldout_20260709/generation_summary_2026-07-10_01-28-15.md`
