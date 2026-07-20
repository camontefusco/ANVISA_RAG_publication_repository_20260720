# Publication RAG Evaluation Summary

Generated: 2026-06-22T17:51:39
Questions: 150
Answerable questions: 120
Unanswerable questions: 30

## Raw Vector Retrieval Metrics

- Source hit rate: 0.7833333333333333
- Mean reciprocal rank: 0.6270833333333333

## BM25 Retrieval Metrics

- Source hit rate: 0.8583333333333333
- Mean reciprocal rank: 0.675

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 0.9166666666666666
- Mean reciprocal rank: 0.7445833333333334

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 0.967 (95% CI 0.933-0.992; 60 pairs)
- Source MRR after cross-encoder reranking: 0.897 (95% CI 0.849-0.943; 60 pairs)
- Article Recall@k: 0.746 (95% CI 0.667-0.821; 60 pairs)
- Article Precision@k: 0.152 (95% CI 0.135-0.167; 60 pairs)
- Article MRR@k: 0.697 (95% CI 0.619-0.769; 60 pairs)
- Article nDCG@k: 0.703 (95% CI 0.626-0.774; 60 pairs)
- Mean gold term coverage in retrieved contexts: 0.846 (95% CI 0.793-0.891; 60 pairs)

## Retrieval Metrics By Language

### en

- Questions: 60
- Raw vector source hit rate: 0.6666666666666666
- Raw vector MRR: 0.5213888888888889
- BM25 source hit rate: 0.7333333333333333
- BM25 MRR: 0.44027777777777777
- Fused source hit rate: 0.85
- Fused MRR: 0.6419444444444444
- Operational source hit rate: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Operational MRR: 0.835 (95% CI 0.749-0.914; 60 pairs)
- Article Recall@k: 0.558 (95% CI 0.425-0.683; 60 pairs)
- Article MRR@k: 0.533 (95% CI 0.408-0.650; 60 pairs)
- Mean gold term coverage: 0.736 (95% CI 0.647-0.815; 60 pairs)

### pt

- Questions: 60
- Raw vector source hit rate: 0.9
- Raw vector MRR: 0.7327777777777778
- BM25 source hit rate: 0.9833333333333333
- BM25 MRR: 0.9097222222222222
- Fused source hit rate: 0.9833333333333333
- Fused MRR: 0.8472222222222222
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Operational MRR: 0.958 (95% CI 0.925-0.992; 60 pairs)
- Article Recall@k: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Article MRR@k: 0.861 (95% CI 0.789-0.925; 60 pairs)
- Mean gold term coverage: 0.956 (95% CI 0.916-0.984; 60 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): 0.067 (95% CI 0.017-0.133; 60 pairs)
- Source MRR (PT - EN): 0.123 (95% CI 0.044-0.214; 60 pairs)
- Article Recall@k (PT - EN): 0.375 (95% CI 0.250-0.500; 60 pairs)
- Article MRR@k (PT - EN): 0.328 (95% CI 0.203-0.461; 60 pairs)
- Gold-term coverage (PT - EN): 0.220 (95% CI 0.140-0.306; 60 pairs)

## Retrieval Metrics By Question Type

### direct_article

- Questions: 106
- Source hit rate: 0.962 (95% CI 0.925-0.991; 53 pairs)
- Article Recall@k: 0.745 (95% CI 0.660-0.821; 53 pairs)
- Article MRR@k: 0.681 (95% CI 0.596-0.764; 53 pairs)

### exception

- Questions: 10
- Source hit rate: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article Recall@k: 0.900 (95% CI 0.700-1.000; 5 pairs)
- Article MRR@k: 0.850 (95% CI 0.650-1.000; 5 pairs)

### multi_article

- Questions: 4
- Source hit rate: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article Recall@k: 0.375 (95% CI 0.250-0.500; 2 pairs)
- Article MRR@k: 0.750 (95% CI 0.500-1.000; 2 pairs)


## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
