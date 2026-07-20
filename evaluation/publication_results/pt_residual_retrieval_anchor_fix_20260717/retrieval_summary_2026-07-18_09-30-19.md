# Publication RAG Evaluation Summary

Generated: 2026-07-18T09:30:37
Questions: 6
Answerable questions: 6
Unanswerable questions: 0

## Raw Vector Retrieval Metrics

- Source hit rate: 0.8333333333333334
- Mean reciprocal rank: 0.7

## BM25 Retrieval Metrics

- Source hit rate: 1
- Mean reciprocal rank: 0.9166666666666666

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 1
- Mean reciprocal rank: 0.8888888888888888

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Source MRR after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Article Recall@k: 0.667 (95% CI 0.333-1.000; 6 pairs)
- Article Precision@k: 0.200 (95% CI 0.067-0.333; 6 pairs)
- Article MRR@k: 0.667 (95% CI 0.333-1.000; 6 pairs)
- Article nDCG@k: 0.667 (95% CI 0.333-1.000; 6 pairs)
- Mean gold term coverage in retrieved contexts: 0.765 (95% CI 0.530-0.976; 6 pairs)

## Retrieval Metrics By Language

### pt

- Questions: 6
- Raw vector source hit rate: 0.8333333333333334
- Raw vector MRR: 0.7
- BM25 source hit rate: 1
- BM25 MRR: 0.9166666666666666
- Fused source hit rate: 1
- Fused MRR: 0.8888888888888888
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 6 pairs)
- Article Recall@k: 0.667 (95% CI 0.333-1.000; 6 pairs)
- Article MRR@k: 0.667 (95% CI 0.333-1.000; 6 pairs)
- Mean gold term coverage: 0.765 (95% CI 0.530-0.976; 6 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): not available
- Source MRR (PT - EN): not available
- Article Recall@k (PT - EN): not available
- Article MRR@k (PT - EN): not available
- Gold-term coverage (PT - EN): not available

## Retrieval Metrics By Question Type

### direct_article

- Questions: 4
- Source hit rate: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Article Recall@k: 0.500 (95% CI 0.000-1.000; 4 pairs)
- Article MRR@k: 0.500 (95% CI 0.000-1.000; 4 pairs)

### multi_article

- Questions: 2
- Source hit rate: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 2 pairs)


## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
