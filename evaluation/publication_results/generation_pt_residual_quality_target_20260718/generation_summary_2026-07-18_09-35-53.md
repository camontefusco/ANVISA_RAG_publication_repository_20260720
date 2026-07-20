# Publication RAG Evaluation Summary

Generated: 2026-07-18T09:36:40
Questions: 11
Answerable questions: 11
Unanswerable questions: 0

## Raw Vector Retrieval Metrics

- Source hit rate: 0.9090909090909091
- Mean reciprocal rank: 0.7227272727272728

## BM25 Retrieval Metrics

- Source hit rate: 1
- Mean reciprocal rank: 0.9393939393939394

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 1
- Mean reciprocal rank: 0.803030303030303

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Source MRR after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Article Precision@k: 0.236 (95% CI 0.200-0.291; 11 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Article nDCG@k: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Mean gold term coverage in retrieved contexts: 0.987 (95% CI 0.961-1.000; 11 pairs)

## Retrieval Metrics By Language

### pt

- Questions: 11
- Raw vector source hit rate: 0.9090909090909091
- Raw vector MRR: 0.7227272727272728
- BM25 source hit rate: 1
- BM25 MRR: 0.9393939393939394
- Fused source hit rate: 1
- Fused MRR: 0.803030303030303
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Mean gold term coverage: 0.987 (95% CI 0.961-1.000; 11 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): not available
- Source MRR (PT - EN): not available
- Article Recall@k (PT - EN): not available
- Article MRR@k (PT - EN): not available
- Gold-term coverage (PT - EN): not available

## Retrieval Metrics By Question Type

### direct_article

- Questions: 9
- Source hit rate: 1.000 (95% CI 1.000-1.000; 9 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 9 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 9 pairs)

### multi_article

- Questions: 2
- Source hit rate: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 2 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.643 (95% CI 0.510-0.782; 11 pairs)
- Refusal accuracy on unanswerable questions: not available
- Citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Article citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 11 pairs)
- Retrieved-citation validity: 1.000 (95% CI 1.000-1.000; 11 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
