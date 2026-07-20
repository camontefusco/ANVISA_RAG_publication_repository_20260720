# Publication RAG Evaluation Summary

Generated: 2026-07-18T16:42:23
Questions: 10
Answerable questions: 0
Unanswerable questions: 10

## Raw Vector Retrieval Metrics

- Source hit rate: None
- Mean reciprocal rank: None

## BM25 Retrieval Metrics

- Source hit rate: None
- Mean reciprocal rank: None

## Fused Retrieval Metrics Before Reranking

- Source hit rate: None
- Mean reciprocal rank: None

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: not available
- Source MRR after cross-encoder reranking: not available
- Article Recall@k: not available
- Article Precision@k: not available
- Article MRR@k: not available
- Article nDCG@k: not available
- Mean gold term coverage in retrieved contexts: not available

## Retrieval Metrics By Language

### en

- Questions: 0
- Raw vector source hit rate: None
- Raw vector MRR: None
- BM25 source hit rate: None
- BM25 MRR: None
- Fused source hit rate: None
- Fused MRR: None
- Operational source hit rate: not available
- Operational MRR: not available
- Article Recall@k: not available
- Article MRR@k: not available
- Mean gold term coverage: not available

### pt

- Questions: 0
- Raw vector source hit rate: None
- Raw vector MRR: None
- BM25 source hit rate: None
- BM25 MRR: None
- Fused source hit rate: None
- Fused MRR: None
- Operational source hit rate: not available
- Operational MRR: not available
- Article Recall@k: not available
- Article MRR@k: not available
- Mean gold term coverage: not available

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): not available
- Source MRR (PT - EN): not available
- Article Recall@k (PT - EN): not available
- Article MRR@k (PT - EN): not available
- Gold-term coverage (PT - EN): not available

## Retrieval Metrics By Question Type


## Generation Metrics

- Mean gold term coverage in generated answers: not available
- Refusal accuracy on unanswerable questions: 0.600 (95% CI 0.200-1.000; 5 pairs)
- Citation presence on answerable questions: not available
- Article citation presence on answerable questions: not available
- Retrieved-citation validity: not available

## Automated Answer-Quality Judge

- Faithfulness: not available
- Citation correctness: not available
- Completeness: not available
- Refusal accuracy: 0.700 (95% CI 0.300-1.000; 5 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
