# Publication RAG Evaluation Summary

Generated: 2026-07-18T17:14:13
Questions: 30
Answerable questions: 12
Unanswerable questions: 18

## Raw Vector Retrieval Metrics

- Source hit rate: 0.5833333333333334
- Mean reciprocal rank: 0.4166666666666667

## BM25 Retrieval Metrics

- Source hit rate: 1
- Mean reciprocal rank: 1.0

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 1
- Mean reciprocal rank: 0.8916666666666667

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Source MRR after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article Precision@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article nDCG@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Mean gold term coverage in retrieved contexts: 0.799 (95% CI 0.507-1.000; 6 pairs)

## Retrieval Metrics By Language

### en

- Questions: 6
- Raw vector source hit rate: 0.5
- Raw vector MRR: 0.5
- BM25 source hit rate: 1
- BM25 MRR: 1.0
- Fused source hit rate: 1
- Fused MRR: 1.0
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Mean gold term coverage: 0.778 (95% CI 0.444-1.000; 6 pairs)

### pt

- Questions: 6
- Raw vector source hit rate: 0.6666666666666666
- Raw vector MRR: 0.3333333333333333
- BM25 source hit rate: 1
- BM25 MRR: 1.0
- Fused source hit rate: 1
- Fused MRR: 0.7833333333333333
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 6 pairs)
- Mean gold term coverage: 0.819 (95% CI 0.569-1.000; 6 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): 0.000 (95% CI 0.000-0.000; 6 pairs)
- Source MRR (PT - EN): 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article Recall@k (PT - EN): 0.000 (95% CI 0.000-0.000; 6 pairs)
- Article MRR@k (PT - EN): 0.000 (95% CI 0.000-0.000; 6 pairs)
- Gold-term coverage (PT - EN): 0.042 (95% CI 0.000-0.125; 6 pairs)

## Retrieval Metrics By Question Type

### answerable_boundary

- Questions: 6
- Source hit rate: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 3 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 3 pairs)

### false_premise_answerable

- Questions: 6
- Source hit rate: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 3 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 3 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.776 (95% CI 0.680-0.881; 6 pairs)
- Refusal accuracy on unanswerable questions: 0.944 (95% CI 0.833-1.000; 9 pairs)
- Citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Article citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Retrieved-citation validity: 1.000 (95% CI 1.000-1.000; 6 pairs)

## Automated Answer-Quality Judge

- Faithfulness: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Citation correctness: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Completeness: 0.908 (95% CI 0.792-1.000; 6 pairs)
- Refusal accuracy: 0.944 (95% CI 0.833-1.000; 9 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
