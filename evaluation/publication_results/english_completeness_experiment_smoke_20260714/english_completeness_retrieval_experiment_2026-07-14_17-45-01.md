# English Completeness Retrieval Experiment

Generated: 2026-07-14T17:45:01
Rows evaluated per strategy: 3

## Metrics

| Strategy | Rows | Source Hit | Article Recall@5 | Article Recall@8 | Article Recall@10 | Article MRR@5 |
|---|---:|---:|---:|---:|---:|---:|
| current_saved_query | 3 | 1.000 | 0.333 | 0.333 | 0.333 | 0.333 |
| expanded_glossary | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.833 |
| multi_query_expanded | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| paired_pt_question | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.667 |
| paired_pt_plus_gold_terms | 3 | 1.000 | 1.000 | 1.000 | 1.000 | 0.833 |

## Interpretation

- `current_saved_query` replays the retrieval query saved in the generation CSV.
- `expanded_glossary` adds failure-focused bilingual aliases to the deterministic glossary query.
- `multi_query_expanded` fuses original English, saved query, and expanded glossary query.
- `paired_pt_question` is a diagnostic upper bound using the paired Portuguese benchmark question.
- `paired_pt_plus_gold_terms` is a leakage upper bound and must not be used as a production method.
