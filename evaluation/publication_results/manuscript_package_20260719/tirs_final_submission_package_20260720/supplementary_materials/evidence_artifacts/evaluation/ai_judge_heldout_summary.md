# AI-Judge Evaluation of Frozen Held-Out RAG Answers

Generated: 2026-07-14T17:29:50
Input rows: 150
Successfully judged rows: 150
Rows with judge errors: 0
Answerable judged rows: 120
Unanswerable judged rows: 30

## Inputs

- evaluation/publication_results/generation_en_heldout_20260709/generation_evaluation_2026-07-10_01-03-11.csv
- evaluation/publication_results/generation_pt_heldout_20260709/generation_evaluation_2026-07-10_01-28-15.csv

## Overall AI-Judge Metrics

- Faithfulness, answerable rows: 0.997
- Citation correctness, answerable rows: 0.965
- Completeness, answerable rows: 0.807
- Refusal correctness, unanswerable rows: 1.000

## By Language

### en

- Judged rows: 75
- Faithfulness: 1.000
- Citation correctness: 0.967
- Completeness: 0.645
- Refusal correctness: 1.000

### pt

- Judged rows: 75
- Faithfulness: 0.993
- Citation correctness: 0.963
- Completeness: 0.970
- Refusal correctness: 1.000

## Publication Use

- These scores are automated LLM-judge labels over frozen generated answers.
- They should be reported as AI-judge validation, not as human expert validation.
- The retrieved evidence was reconstructed with the saved retrieval and rerank queries from the original generation CSVs.
- The generation outputs were not regenerated during this judge-only run.
