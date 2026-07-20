# Publication RAG Evaluation Summary

Generated: 2026-07-10T01:09:24
Questions: 75
Answerable questions: 60
Unanswerable questions: 15

## Raw Vector Retrieval Metrics

- Source hit rate: 0.85
- Mean reciprocal rank: 0.5925

## BM25 Retrieval Metrics

- Source hit rate: 0.8
- Mean reciprocal rank: 0.6436111111111111

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 0.9
- Mean reciprocal rank: 0.6894444444444444

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Source MRR after cross-encoder reranking: 0.868 (95% CI 0.787-0.938; 60 pairs)
- Article Recall@k: 0.600 (95% CI 0.475-0.717; 60 pairs)
- Article Precision@k: 0.123 (95% CI 0.100-0.147; 60 pairs)
- Article MRR@k: 0.562 (95% CI 0.438-0.679; 60 pairs)
- Article nDCG@k: 0.564 (95% CI 0.441-0.678; 60 pairs)
- Mean gold term coverage in retrieved contexts: 0.740 (95% CI 0.649-0.824; 60 pairs)

## Retrieval Metrics By Language

### en

- Questions: 60
- Raw vector source hit rate: 0.85
- Raw vector MRR: 0.5925
- BM25 source hit rate: 0.8
- BM25 MRR: 0.6436111111111111
- Fused source hit rate: 0.9
- Fused MRR: 0.6894444444444444
- Operational source hit rate: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Operational MRR: 0.868 (95% CI 0.787-0.938; 60 pairs)
- Article Recall@k: 0.600 (95% CI 0.475-0.717; 60 pairs)
- Article MRR@k: 0.562 (95% CI 0.438-0.679; 60 pairs)
- Mean gold term coverage: 0.740 (95% CI 0.649-0.824; 60 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): not available
- Source MRR (PT - EN): not available
- Article Recall@k (PT - EN): not available
- Article MRR@k (PT - EN): not available
- Gold-term coverage (PT - EN): not available

## Retrieval Metrics By Question Type

### direct_article

- Questions: 53
- Source hit rate: 0.925 (95% CI 0.849-0.981; 53 pairs)
- Article Recall@k: 0.585 (95% CI 0.453-0.717; 53 pairs)
- Article MRR@k: 0.533 (95% CI 0.401-0.660; 53 pairs)

### exception

- Questions: 5
- Source hit rate: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article Recall@k: 0.800 (95% CI 0.400-1.000; 5 pairs)
- Article MRR@k: 0.700 (95% CI 0.300-1.000; 5 pairs)

### multi_article

- Questions: 2
- Source hit rate: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article Recall@k: 0.500 (95% CI 0.500-0.500; 2 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 2 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.553 (95% CI 0.462-0.643; 60 pairs)
- Refusal accuracy on unanswerable questions: 1.000 (95% CI 1.000-1.000; 15 pairs)
- Citation presence on answerable questions: 0.800 (95% CI 0.700-0.900; 60 pairs)
- Article citation presence on answerable questions: 0.800 (95% CI 0.700-0.900; 60 pairs)
- Retrieved-citation validity: 0.800 (95% CI 0.700-0.900; 60 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
