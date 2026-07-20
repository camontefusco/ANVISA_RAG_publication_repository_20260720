# English Completeness Retrieval Experiment

Generated: 2026-07-14T18:05:27
Rows evaluated per strategy: 23

## Metrics

| Strategy | Rows | Source Hit | Article Recall@5 | Article Recall@8 | Article Recall@10 | Article MRR@5 |
|---|---:|---:|---:|---:|---:|---:|
| current_saved_query | 23 | 0.957 | 0.239 | 0.239 | 0.239 | 0.261 |
| expanded_glossary | 23 | 1.000 | 0.761 | 0.761 | 0.761 | 0.739 |
| multi_query_expanded | 23 | 1.000 | 0.543 | 0.543 | 0.543 | 0.565 |
| paired_pt_question | 23 | 1.000 | 0.891 | 0.891 | 0.891 | 0.819 |
| paired_pt_plus_gold_terms | 23 | 1.000 | 0.978 | 0.978 | 0.978 | 0.899 |

## Interpretation

- `current_saved_query` replays the retrieval query saved in the generation CSV.
- `expanded_glossary` adds failure-focused bilingual aliases to the deterministic glossary query.
- `multi_query_expanded` fuses original English, saved query, and expanded glossary query.
- `paired_pt_question` is a diagnostic upper bound using the paired Portuguese benchmark question.
- `paired_pt_plus_gold_terms` is a leakage upper bound and must not be used as a production method.
