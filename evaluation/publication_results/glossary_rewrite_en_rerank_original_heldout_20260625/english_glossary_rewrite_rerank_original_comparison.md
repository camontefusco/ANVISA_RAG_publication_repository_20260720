# English Query Rewrite Comparison

Questions: 60 answerable English questions
Baseline: `retrieval_evaluation_2026-06-22_17-48-54.csv`
Rewritten: `retrieval_evaluation_2026-06-25_17-49-45.csv`

| Metric | Without rewrite | With rewrite | Delta |
|---|---:|---:|---:|
| Raw vector source hit | 0.667 | 0.850 | +0.183 |
| Raw vector MRR | 0.521 | 0.593 | +0.071 |
| BM25 MRR | 0.440 | 0.644 | +0.203 |
| Fused MRR | 0.642 | 0.689 | +0.047 |
| Operational top-5 MRR | 0.835 | 0.868 | +0.033 |
| Article Recall@5 | 0.558 | 0.600 | +0.042 |
| Article MRR@5 | 0.533 | 0.562 | +0.029 |
| Article nDCG@5 | 0.536 | 0.564 | +0.028 |
| Top-5 gold-term coverage | 0.736 | 0.740 | +0.004 |

## Interpretation

- Positive deltas indicate that English query rewriting improved that metric.
- Negative deltas indicate that the rewrite changed retrieval in an unfavorable direction for that metric.
- This comparison uses only answerable English questions so it measures the intended bilingual retrieval effect.
- Keep the paired run manifests with any manuscript supplement so the rewrite method is explicit.
