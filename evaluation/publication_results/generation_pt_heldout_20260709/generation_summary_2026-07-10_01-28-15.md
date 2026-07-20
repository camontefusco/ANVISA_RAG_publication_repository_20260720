# Publication RAG Evaluation Summary

Generated: 2026-07-10T01:33:57
Questions: 75
Answerable questions: 60
Unanswerable questions: 15

## Raw Vector Retrieval Metrics

- Source hit rate: 0.9
- Mean reciprocal rank: 0.7327777777777778

## BM25 Retrieval Metrics

- Source hit rate: 0.9833333333333333
- Mean reciprocal rank: 0.9097222222222222

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 0.9833333333333333
- Mean reciprocal rank: 0.8472222222222222

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Source MRR after cross-encoder reranking: 0.958 (95% CI 0.925-0.992; 60 pairs)
- Article Recall@k: 0.933 (95% CI 0.867-0.983; 60 pairs)
- Article Precision@k: 0.190 (95% CI 0.177-0.200; 60 pairs)
- Article MRR@k: 0.861 (95% CI 0.789-0.925; 60 pairs)
- Article nDCG@k: 0.871 (95% CI 0.803-0.929; 60 pairs)
- Mean gold term coverage in retrieved contexts: 0.956 (95% CI 0.916-0.984; 60 pairs)

## Retrieval Metrics By Language

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

- Source hit rate (PT - EN): not available
- Source MRR (PT - EN): not available
- Article Recall@k (PT - EN): not available
- Article MRR@k (PT - EN): not available
- Gold-term coverage (PT - EN): not available

## Retrieval Metrics By Question Type

### direct_article

- Questions: 53
- Source hit rate: 1.000 (95% CI 1.000-1.000; 53 pairs)
- Article Recall@k: 0.943 (95% CI 0.868-1.000; 53 pairs)
- Article MRR@k: 0.843 (95% CI 0.758-0.915; 53 pairs)

### exception

- Questions: 5
- Source hit rate: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 5 pairs)

### multi_article

- Questions: 2
- Source hit rate: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article Recall@k: 0.500 (95% CI 0.500-0.500; 2 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 2 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.749 (95% CI 0.676-0.812; 60 pairs)
- Refusal accuracy on unanswerable questions: 1.000 (95% CI 1.000-1.000; 15 pairs)
- Citation presence on answerable questions: 0.983 (95% CI 0.950-1.000; 60 pairs)
- Article citation presence on answerable questions: 0.983 (95% CI 0.950-1.000; 60 pairs)
- Retrieved-citation validity: 0.983 (95% CI 0.950-1.000; 60 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
