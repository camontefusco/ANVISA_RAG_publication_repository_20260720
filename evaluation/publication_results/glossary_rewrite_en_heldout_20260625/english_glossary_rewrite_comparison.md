# English Query Rewrite Comparison

Questions: 60 answerable English questions
Baseline: `retrieval_evaluation_2026-06-22_17-48-54.csv`
Rewritten: `retrieval_evaluation_2026-06-25_16-52-56.csv`

| Metric | Without rewrite | With rewrite | Delta |
|---|---:|---:|---:|
| Raw vector source hit | 0.667 | 0.850 | +0.183 |
| Raw vector MRR | 0.521 | 0.593 | +0.071 |
| BM25 MRR | 0.440 | 0.644 | +0.203 |
| Fused MRR | 0.642 | 0.689 | +0.047 |
| Operational top-5 MRR | 0.835 | 0.751 | -0.085 |
| Article Recall@5 | 0.558 | 0.333 | -0.225 |
| Article MRR@5 | 0.533 | 0.130 | -0.403 |
| Article nDCG@5 | 0.536 | 0.180 | -0.356 |
| Top-5 gold-term coverage | 0.736 | 0.574 | -0.163 |

## Interpretation

- Positive deltas indicate that English query rewriting improved that metric.
- Negative deltas indicate that the rewrite changed retrieval in an unfavorable direction for that metric.
- This comparison uses only answerable English questions so it measures the intended bilingual retrieval effect.
- Keep the paired run manifests with any manuscript supplement so the rewrite method is explicit.
