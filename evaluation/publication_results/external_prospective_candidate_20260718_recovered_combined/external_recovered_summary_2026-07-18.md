# External Prospective Candidate Recovered Summary

This is an artifact-recovery summary. The first external run completed in the terminal, but after the Codex output folder was moved only a 40-row checkpoint remained. The missing 10 unanswerable/adversarial rows were regenerated once with the same frozen settings and merged with the preserved checkpoint. No retrieval, prompt, judge, threshold, or benchmark changes were made.

## Overall Metrics

- question_count: 50
- pair_count: 25
- answerable_count: 40
- unanswerable_count: 10
- source_hit: 0.800
- source_mrr: 0.988
- raw_runner_article_recall_at_k_answerable: 0.000
- normalized_article_recall_at_5_answerable: 0.967
- normalized_article_mrr_at_5_answerable: 0.912
- retrieved_term_coverage_answerable: 0.806
- answer_term_coverage_answerable: 0.761
- citation_present_answerable: 0.975
- article_citation_present_answerable: 0.975
- citation_retrieved_validity_answerable: 0.975
- judge_faithfulness_answerable: 1.000
- judge_citation_correctness_answerable: 0.975
- judge_completeness_answerable: 0.943
- refusal_detected_unanswerable: 0.600
- judge_refusal_correctness_unanswerable: 0.700

## By Language

### en
- n: 25
- source_hit: 0.800
- normalized_article_recall_at_5_answerable: 0.950
- answer_term_coverage_answerable: 0.744
- judge_faithfulness_answerable: 1.000
- judge_completeness_answerable: 0.930
- judge_refusal_correctness_unanswerable: 0.800
### pt
- n: 25
- source_hit: 0.800
- normalized_article_recall_at_5_answerable: 0.983
- answer_term_coverage_answerable: 0.778
- judge_faithfulness_answerable: 1.000
- judge_completeness_answerable: 0.955
- judge_refusal_correctness_unanswerable: 0.600

## Weak/Review Rows
- Rows flagged for review: 24
- Review CSV: `external_recovered_failure_review_2026-07-18.csv`

## Interpretation
The external stress test mostly supports robustness of the final system, especially for source retrieval, citation validity, faithfulness, and refusal correctness. However, the recovered result should be reported with the artifact-recovery caveat, and the deterministic raw article-recall fields from the runner should not be used for this external set because the external gold article labels were formatted differently from the internal benchmark. Use the normalized article audit columns for article-level retrieval reporting.
