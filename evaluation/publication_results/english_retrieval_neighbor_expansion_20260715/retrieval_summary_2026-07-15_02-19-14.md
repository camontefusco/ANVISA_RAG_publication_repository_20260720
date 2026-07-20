# Publication RAG Evaluation Summary

Generated: 2026-07-15T02:28:57
Questions: 75
Answerable questions: 60
Unanswerable questions: 15

## Raw Vector Retrieval Metrics

- Source hit rate: 0.85
- Mean reciprocal rank: 0.6377777777777778

## BM25 Retrieval Metrics

- Source hit rate: 0.9166666666666666
- Mean reciprocal rank: 0.7555555555555555

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 0.9833333333333333
- Mean reciprocal rank: 0.7836111111111111

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Source MRR after cross-encoder reranking: 0.958 (95% CI 0.925-0.992; 60 pairs)
- Article Recall@k: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Article Precision@k: 0.193 (95% CI 0.177-0.207; 60 pairs)
- Article MRR@k: 0.844 (95% CI 0.761-0.920; 60 pairs)
- Article nDCG@k: 0.866 (95% CI 0.789-0.933; 60 pairs)
- Mean gold term coverage in retrieved contexts: 0.961 (95% CI 0.926-0.987; 60 pairs)

## Retrieval Metrics By Language

### en

- Questions: 60
- Raw vector source hit rate: 0.85
- Raw vector MRR: 0.6377777777777778
- BM25 source hit rate: 0.9166666666666666
- BM25 MRR: 0.7555555555555555
- Fused source hit rate: 0.9833333333333333
- Fused MRR: 0.7836111111111111
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Operational MRR: 0.958 (95% CI 0.925-0.992; 60 pairs)
- Article Recall@k: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Article MRR@k: 0.844 (95% CI 0.761-0.920; 60 pairs)
- Mean gold term coverage: 0.961 (95% CI 0.926-0.987; 60 pairs)

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
- Source hit rate: 1.000 (95% CI 1.000-1.000; 53 pairs)
- Article Recall@k: 0.925 (95% CI 0.849-0.981; 53 pairs)
- Article MRR@k: 0.842 (95% CI 0.748-0.924; 53 pairs)

### exception

- Questions: 5
- Source hit rate: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article MRR@k: 0.800 (95% CI 0.600-1.000; 5 pairs)

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
