# Publication RAG Evaluation Summary

Generated: 2026-07-18T17:02:46
Questions: 24
Answerable questions: 8
Unanswerable questions: 16

## Raw Vector Retrieval Metrics

- Source hit rate: 0.5
- Mean reciprocal rank: 0.5

## BM25 Retrieval Metrics

- Source hit rate: 1
- Mean reciprocal rank: 1.0

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 1
- Mean reciprocal rank: 1.0

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Source MRR after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article Precision@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article nDCG@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Mean gold term coverage in retrieved contexts: 0.771 (95% CI 0.667-0.917; 4 pairs)

## Retrieval Metrics By Language

### en

- Questions: 4
- Raw vector source hit rate: 0.5
- Raw vector MRR: 0.5
- BM25 source hit rate: 1
- BM25 MRR: 1.0
- Fused source hit rate: 1
- Fused MRR: 1.0
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Mean gold term coverage: 0.771 (95% CI 0.667-0.917; 4 pairs)

### pt

- Questions: 4
- Raw vector source hit rate: 0.5
- Raw vector MRR: 0.5
- BM25 source hit rate: 1
- BM25 MRR: 1.0
- Fused source hit rate: 1
- Fused MRR: 1.0
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Operational MRR: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Mean gold term coverage: 0.771 (95% CI 0.667-0.917; 4 pairs)

## Paired Language Differences

Positive values favor Portuguese; intervals are paired over bilingual facts.

- Source hit rate (PT - EN): 0.000 (95% CI 0.000-0.000; 4 pairs)
- Source MRR (PT - EN): 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article Recall@k (PT - EN): 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article MRR@k (PT - EN): 0.000 (95% CI 0.000-0.000; 4 pairs)
- Gold-term coverage (PT - EN): 0.000 (95% CI 0.000-0.000; 4 pairs)

## Retrieval Metrics By Question Type

### false_premise_answerable

- Questions: 8
- Source hit rate: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Article Recall@k: 0.000 (95% CI 0.000-0.000; 4 pairs)
- Article MRR@k: 0.000 (95% CI 0.000-0.000; 4 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.625 (95% CI 0.489-0.760; 4 pairs)
- Refusal accuracy on unanswerable questions: 1.000 (95% CI 1.000-1.000; 8 pairs)
- Citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Article citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Retrieved-citation validity: 1.000 (95% CI 1.000-1.000; 4 pairs)

## Automated Answer-Quality Judge

- Faithfulness: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Citation correctness: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Completeness: 1.000 (95% CI 1.000-1.000; 4 pairs)
- Refusal accuracy: 0.938 (95% CI 0.812-1.000; 8 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
