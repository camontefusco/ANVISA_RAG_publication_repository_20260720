# Publication RAG Evaluation Summary

Generated: 2026-07-17T11:54:40
Questions: 75
Answerable questions: 60
Unanswerable questions: 15

## Raw Vector Retrieval Metrics

- Source hit rate: 0.85
- Mean reciprocal rank: 0.6377777777777778

## BM25 Retrieval Metrics

- Source hit rate: 0.9166666666666666
- Mean reciprocal rank: 0.8027777777777778

## Fused Retrieval Metrics Before Reranking

- Source hit rate: 0.9833333333333333
- Mean reciprocal rank: 0.7752777777777777

## Operational Retrieval Metrics

- Source hit rate after cross-encoder reranking: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Source MRR after cross-encoder reranking: 0.950 (95% CI 0.908-0.983; 60 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Article Precision@k: 0.207 (95% CI 0.200-0.217; 60 pairs)
- Article MRR@k: 0.898 (95% CI 0.838-0.954; 60 pairs)
- Article nDCG@k: 0.924 (95% CI 0.879-0.966; 60 pairs)
- Mean gold term coverage in retrieved contexts: 0.984 (95% CI 0.968-0.997; 60 pairs)

## Retrieval Metrics By Language

### en

- Questions: 60
- Raw vector source hit rate: 0.85
- Raw vector MRR: 0.6377777777777778
- BM25 source hit rate: 0.9166666666666666
- BM25 MRR: 0.8027777777777778
- Fused source hit rate: 0.9833333333333333
- Fused MRR: 0.7752777777777777
- Operational source hit rate: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Operational MRR: 0.950 (95% CI 0.908-0.983; 60 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Article MRR@k: 0.898 (95% CI 0.838-0.954; 60 pairs)
- Mean gold term coverage: 0.984 (95% CI 0.968-0.997; 60 pairs)

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
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 53 pairs)
- Article MRR@k: 0.894 (95% CI 0.829-0.957; 53 pairs)

### exception

- Questions: 5
- Source hit rate: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 5 pairs)
- Article MRR@k: 0.900 (95% CI 0.700-1.000; 5 pairs)

### multi_article

- Questions: 2
- Source hit rate: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article Recall@k: 1.000 (95% CI 1.000-1.000; 2 pairs)
- Article MRR@k: 1.000 (95% CI 1.000-1.000; 2 pairs)


## Generation Metrics

- Mean gold term coverage in generated answers: 0.825 (95% CI 0.784-0.864; 60 pairs)
- Refusal accuracy on unanswerable questions: 1.000 (95% CI 1.000-1.000; 15 pairs)
- Citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Article citation presence on answerable questions: 1.000 (95% CI 1.000-1.000; 60 pairs)
- Retrieved-citation validity: 1.000 (95% CI 1.000-1.000; 60 pairs)

## Notes

- Automated scores are screening metrics, not final evidence.
- Raw vector metrics measure the embedding retriever without routing or source diversification.
- BM25 metrics measure exact-term retrieval over passage text and regulatory metadata.
- Fused metrics use reciprocal rank fusion before cross-encoder reranking.
- Operational metrics use the five highest-scoring passages from multilingual cross-encoder reranking.
- Confidence intervals use pair-clustered bootstrap resampling so bilingual counterparts are not treated as independent.
- LLM-judge scores are supplementary and require calibration against the blinded human review subset.
- Single-reviewer repeat scoring estimates intra-rater reliability, not inter-rater agreement.
