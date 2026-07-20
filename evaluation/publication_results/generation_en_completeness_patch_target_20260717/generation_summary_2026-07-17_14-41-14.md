# Publication RAG Evaluation Summary

Generated: 2026-07-17T14:42:01
Questions: 3
Answerable questions: 3
Unanswerable questions: 0

## Raw Vector Retrieval Metrics

- Source hit rate: 0.6666666666666666
- Mean reciprocal rank: 0.6666666666666666

## BM25 Retrieval Metrics

- Source hit rate: 1
- Mean reciprocal rank: 1.0

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 1
- Mean reciprocal rank: 1.0

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Source MRR after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article Precision@k: 0.267 (95% CI 0.200-0.400; 3 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article nDCG@k: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Mean gold term coverage in retrieved contexts: 1.000 (95% CI 1.000-1.000; 3 pairs)

## Retrieval Metrics By Language

### en

- Questions: 3
- Raw vector source hit rate: 0.6666666666666666
- Raw vector MRR: 0.6666666666666666
- BM25 source hit rate: 1
- BM25 MRR: 1.0
- Fused source hit rate: 1
- Fused MRR: 1.0
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Mean gold term coverage: 1.000 (95% CI 1.000-1.000; 3 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): not available
- Source MRR (PT - EN): not available
- Article Recall@k (PT - EN): not available
- Article MRR@k (PT - EN): not available
- Gold-term coverage (PT - EN): not available

## Retrieval Metrics By Question Type

### direct_article

- Questions: 1
- Source hit rate: 1.000 (95% CI 1.000-1.000; 1 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 1 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 1 pairs)

### exception

- Questions: 1
- Source hit rate: 1.000 (95% CI 1.000-1.000; 1 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 1 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 1 pairs)

### multi_article

- Questions: 1
- Source hit rate: 1.000 (95% CI 1.000-1.000; 1 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 1 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 1 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.899 (95% CI 0.871-0.929; 3 pairs)
- Refusal accuracy on unanswerable questions: not available
- Citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Article citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 3 pairs)
- Retrieved-citation validity: 1.000 (95% CI 1.000-1.000; 3 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
