# Publication RAG Evaluation Summary

Generated: 2026-06-25T16:52:57
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

- Source hit rate after cross-encoder reranking: 0.883 (95% CI 0.800-0.950; 60 pairs)
- Source MRR after cross-encoder reranking: 0.751 (95% CI 0.653-0.839; 60 pairs)
- Article Recall@k: 0.333 (95% CI 0.217-0.450; 60 pairs)
- Article Precision@k: 0.067 (95% CI 0.043-0.090; 60 pairs)
- Article MRR@k: 0.130 (95% CI 0.077-0.191; 60 pairs)
- Article nDCG@k: 0.180 (95% CI 0.114-0.252; 60 pairs)
- Mean gold term coverage in retrieved contexts: 0.574 (95% CI 0.488-0.658; 60 pairs)

## Retrieval Metrics By Language

### en

- Questions: 60
- Raw vector source hit rate: 0.85
- Raw vector MRR: 0.5925
- BM25 source hit rate: 0.8
- BM25 MRR: 0.6436111111111111
- Fused source hit rate: 0.9
- Fused MRR: 0.6894444444444444
- Operational source hit rate: 0.883 (95% CI 0.800-0.950; 60 pairs)
- Operational MRR: 0.751 (95% CI 0.653-0.839; 60 pairs)
- Article Recall@k: 0.333 (95% CI 0.217-0.450; 60 pairs)
- Article MRR@k: 0.130 (95% CI 0.077-0.191; 60 pairs)
- Mean gold term coverage: 0.574 (95% CI 0.488-0.658; 60 pairs)

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
- Source hit rate: 0.906 (95% CI 0.830-0.981; 53 pairs)
- Article Recall@k: 0.302 (95% CI 0.189-0.434; 53 pairs)
- Article MRR@k: 0.124 (95% CI 0.067-0.192; 53 pairs)

### exception

- Questions: 5
- Source hit rate: 0.800 (95% CI 0.400-1.000; 5 pairs)
- Article Recall@k: 0.800 (95% CI 0.400-1.000; 5 pairs)
- Article MRR@k: 0.250 (95% CI 0.100-0.400; 5 pairs)

### multi_article

- Questions: 2
- Source hit rate: 0.500 (95% CI 0.000-1.000; 2 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 2 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 2 pairs)


## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
