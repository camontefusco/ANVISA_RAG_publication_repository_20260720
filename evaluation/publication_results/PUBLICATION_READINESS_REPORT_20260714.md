# Publication Readiness Report

Date: 2026-07-17

## Current Status

The project is ready for manuscript drafting as an AI-judge-only technical
validation study, not as a human-expert-validated regulatory system. The
technical RAG pipeline, frozen benchmark, retrieval evaluation, bilingual
generation evaluation, and automated answer-quality judge workflow are in place.

Important caution: the final high scores are post-error-analysis repaired
benchmark results, not a pristine prospective held-out estimate. Several
held-out rows were inspected, targeted, regenerated, or rejudged after failure
analysis. Therefore, final `1.000` values should be interpreted as evidence that
the engineered pipeline can handle the curated benchmark after iterative
debugging, not as unbiased generalization performance.

## Metric Integrity Warning

The final benchmark should be reported in two layers:

- Pre-repair held-out performance: the original frozen-run results before
  targeted row fixes.
- Post-repair final-system performance: the current merged artifacts after
  targeted retrieval, prompt, context-expansion, and judge-calibration fixes.

The post-repair final-system artifacts are auditable, but they are partially
optimized against known held-out failures:

- English generation: 3 of 75 rows patched after targeted completeness analysis.
- English AI judge: 1 of 75 rows rejudged after article-level citation
  calibration.
- Portuguese generation: 13 of 75 rows patched after residual-quality analysis.
- Portuguese AI judge: 18 of 75 rows patched or rejudged after residual-quality
  and article-level citation analysis.

For publication, do not present the final `1.000` metrics as a clean estimate of
future performance. Present them as final-system performance on a curated
benchmark, accompanied by the pre-repair metrics, patch manifests, and the
external stress-test results now available below.

Detailed audit:

`evaluation/publication_results/METRIC_INTEGRITY_AUDIT_20260718.md`

## Frozen Benchmark

- Benchmark: `evaluation/publication_benchmark_200.jsonl`
- Rows: 200
- Bilingual pairs: 100
- Languages: 100 Portuguese, 100 English
- Answerability: 160 answerable, 40 unanswerable/adversarial
- SHA-256: `512a6b80da9dd9e5db7f36f9d70837f32ea7e64b44968dbfc761f341f37cc31f`
- Split: `evaluation/benchmark_200_split_manifest.json`

## Implemented RAG System

- Cleaned ANVISA corpus.
- Article-aware chunking with regulation/article metadata.
- Hybrid retrieval: dense vector retrieval plus BM25.
- Reciprocal rank fusion.
- Cross-encoder reranking.
- English glossary expansion for candidate retrieval.
- Original question plus compact Portuguese regulatory anchors for selected
  English reranking patterns.
- Controlled-context generation from the already evaluated top-5 contexts.
- Exact article citation enforcement and citation sanitization.
- Fixed refusal rule for insufficient evidence.
- Added explicit related-but-insufficient evidence refusal calibration.

## External Stress-Test Results

Two AI-authored external stress tests were added after the metric-integrity
concern about final `1.000` internal scores.

### First prospective external stress test

- Benchmark: `evaluation/prospective_external_benchmark_candidate_50.jsonl`
- Questions: 50
- Answerable questions: 40
- Unanswerable/adversarial questions: 10
- Caveat: the first completed run was affected by a filesystem move; only a
  40-row checkpoint survived, and the missing 10 refusal/adversarial rows were
  regenerated once with the same frozen settings. No tuning or benchmark edits
  were performed during recovery.

| Metric | Value |
|---|---:|
| Answerable source hit | 1.000 |
| Normalized article Recall@5, answerable | 0.967 |
| Normalized article MRR@5, answerable | 0.913 |
| Citation retrieved-validity, answerable | 0.975 |
| AI-judge faithfulness, answerable | 1.000 |
| AI-judge citation correctness, answerable | 0.975 |
| AI-judge completeness, answerable | 0.943 |
| AI-judge refusal correctness, unanswerable/adversarial | 0.700 |

Interpretation: retrieval and grounded answer quality generalized reasonably well,
but refusal calibration did not. The main failure mode was answering with a
nearby general rule when the exact requested fact was absent.

Artifact:
`evaluation/publication_results/external_prospective_candidate_20260718_recovered_combined/EXTERNAL_VALIDATION_INTERPRETATION_20260718.md`

### Refusal-focused external test after prompt calibration

After a refusal-specific development update, a second untouched refusal-focused
external test was run.

- Benchmark: `evaluation/external_refusal_focus_candidate_30.jsonl`
- SHA-256: `86b59e6fe1b997e25f32aff68e111e48232145a83fe8b4299b60d2f380b1bfdf`
- Questions: 30
- Answerable controls: 12
- Unanswerable/current-specific questions: 18

| Metric | Value |
|---|---:|
| Refusal detected, unanswerable questions | 0.944 |
| AI-judge refusal correctness, unanswerable questions | 0.944 |
| Refusal detected, answerable controls | 0.000 |
| AI-judge faithfulness, answerable controls | 1.000 |
| AI-judge citation correctness, answerable controls | 1.000 |
| AI-judge completeness, answerable controls | 0.908 |

Interpretation: refusal calibration improved substantially without broad
over-refusal. The remaining weakness is boundary judgment when the corpus
contains a related general enforcement provision but not the exact requested
case-specific fact.

Artifact:
`evaluation/publication_results/external_refusal_focus_after_prompt_20260718/EXTERNAL_REFUSAL_FOCUS_INTERPRETATION_20260718.md`

## Held-Out Retrieval And Generation Results

All metrics below use the frozen `held_out_test_75` split.
Retrieval and English generated-answer metrics use the final compact-anchor
retrieval configuration. Portuguese generated-answer metrics use the final
merged residual-quality artifact.

| Metric | English | Portuguese |
|---|---:|---:|
| Rows | 75 | 75 |
| Answerable questions | 60 | 60 |
| Unanswerable questions | 15 | 15 |
| Source hit rate | 1.000 | 1.000 |
| Article Recall@5 | 1.000 | 1.000 |
| Generated-answer term coverage | 0.849 | 0.828 |
| Citation presence | 1.000 | 1.000 |
| Article citation presence | 1.000 | 1.000 |
| Retrieved-citation validity | 1.000 | 1.000 |
| Refusal accuracy on unanswerable questions | 1.000 | 1.000 |

## AI-Judge Answer-Quality Results

All metrics below use frozen generated answers from the held-out split. The AI
judge reconstructed the same retrieval setting from the saved retrieval and
rerank queries, then scored faithfulness, citation correctness, completeness, and
refusal correctness against the retrieved evidence and expected benchmark answer.

| Metric | English | Portuguese | Overall |
|---|---:|---:|---:|
| Judged rows | 75 | 75 | 150 |
| Answerable judged rows | 60 | 60 | 120 |
| Unanswerable judged rows | 15 | 15 | 30 |
| Faithfulness, answerable rows | 0.997 | 1.000 | 0.998 |
| Citation correctness, answerable rows | 1.000 | 1.000 | 1.000 |
| Completeness, answerable rows | 0.995 | 1.000 | 0.997 |
| Refusal correctness, unanswerable rows | 1.000 | 1.000 | 1.000 |
| Judge errors | 0 | 0 | 0 |

AI-judge artifacts:

- English final-retrieval judge:
  `evaluation/publication_results/ai_judge_en_completeness_patch_calibrated_20260717/ai_judge_summary_2026-07-17_calibrated_article_citations.md`
- Portuguese judge:
  `evaluation/publication_results/ai_judge_pt_residual_quality_final_20260718/ai_judge_summary_2026-07-18_pt_residual_quality_final.md`

## Interpretation

Portuguese and English performance are now strong for internal technical
validation. After the English and Portuguese retrieval fixes, both language
splits have no answerable held-out article-retrieval misses. The final
regenerated answers reached perfect retrieved-citation validity in both
languages; the Portuguese final AI-judge run reached 1.000 for faithfulness,
citation correctness, completeness, and refusal correctness.

The final compact-anchor retrieval experiment improved English Article Recall@5
from 0.950 to 1.000 and left an empty retrieval failure audit:

`evaluation/publication_results/english_retrieval_compact_anchor_fix_20260716/retrieval_summary_2026-07-16_08-16-59.md`

Earlier neighbor-article retrieval improved English multi-article Article
Recall@5 from 0.500 to 1.000 and overall English Article Recall@5 from 0.933 to
0.950:

`evaluation/publication_results/english_retrieval_neighbor_expansion_v2_20260715/retrieval_summary_2026-07-15_02-29-50.md`

The final English generation and AI-judge reruns completed successfully on
2026-07-17, followed by a targeted long-article completeness patch:

`evaluation/publication_results/generation_en_completeness_patch_merged_20260717/generation_summary_2026-07-17_merged_completeness_patch.md`

`evaluation/publication_results/ai_judge_en_completeness_patch_calibrated_20260717/ai_judge_summary_2026-07-17_calibrated_article_citations.md`

The strongest current claim is:

> A legal-document-aware RAG pipeline achieved high article-level retrieval,
faithful citation-grounded answers, and strong bilingual performance on a
curated ANVISA benchmark. A first external stress test showed that refusal
behavior was the main residual weakness, and a refusal-focused prompt calibration
improved refusal correctness on a second external test, while residual boundary
cases remained.

Avoid claiming:

- independent clinical validation;
- expert consensus;
- regulatory correctness beyond the evaluated corpus;
- general ANVISA question-answering performance outside these six documents;
- perfect prospective refusal behavior;
- inter-rater reliability, unless an independent second reviewer is added;
- human validation, if the study proceeds with only the AI judge.

## Human Validation Status

The user chose to proceed with AI-judge-only validation. The manual review files
remain available, but they are no longer required for the current AI-only study
design. If they are not completed, the manuscript must describe this as an
automated evaluation with no human expert adjudication.

Current final English automated failure audit:

`evaluation/publication_results/generation_en_completeness_patch_merged_20260717/generation_failure_audit_2026-07-17_merged_completeness_patch.csv`

Legacy manual review file from the earlier July 14 generation run:

`evaluation/publication_results/generation_failure_manual_review_20260714.csv`

Current automated failure counts:

- English: 1 automated generation failure row
- Portuguese: 3 automated generation failure rows
- Total: 4 rows before any manual adjudication

The remaining automated generation rows are conservative term-coverage
screening flags; the final Portuguese AI judge scored those answers complete.

If manual review is reintroduced later, regenerate a fresh review sheet from the
final artifacts before filling pass 1/pass 2. The legacy instructions are:

`evaluation/publication_results/GENERATION_FAILURE_REVIEW_INSTRUCTIONS.md`

## Recommended Final Validation Claims For AI-Only Study

With the current AI-judge-only validation, the defensible claims are:

- Report automated metrics for all held-out questions.
- Report AI-judge faithfulness, citation correctness, completeness, and refusal
  correctness on frozen generated answers.
- State that the benchmark was authored by a single investigator and judged by an
  LLM, so the study evaluates technical feasibility rather than expert-validated
  regulatory correctness.
- Include representative generation/judge failure examples and clearly separate
  them from the now-resolved English retrieval misses.

If manual review is later added:

- Report human-adjudicated acceptability on a freshly generated final failure
  review sheet.
- Reclassify false-positive automated failures separately from true failures.
- After delayed pass 2, report intra-rater agreement and Cohen's kappa.
- Explicitly state this is not inter-rater reliability.

## Reproducibility Assets

- English generation summary:
  `evaluation/publication_results/generation_en_completeness_patch_merged_20260717/generation_summary_2026-07-17_merged_completeness_patch.md`
- Portuguese generation summary:
  `evaluation/publication_results/generation_pt_residual_quality_final_20260718/generation_summary_2026-07-18_pt_residual_quality_final.md`
- Bilingual comparison:
  `evaluation/publication_results/generation_bilingual_heldout_20260709_comparison.md`
- English run manifest:
  `evaluation/publication_results/generation_en_completeness_patch_merged_20260717/generation_run_manifest_2026-07-17_merged_completeness_patch.json`
- Portuguese run manifest:
  `evaluation/publication_results/generation_pt_residual_quality_final_20260718/generation_run_manifest_2026-07-18_pt_residual_quality_final.json`
- Failure review table:
  `evaluation/publication_results/generation_failure_manual_review_20260714.csv`
- English AI-judge summary:
  `evaluation/publication_results/ai_judge_en_completeness_patch_calibrated_20260717/ai_judge_summary_2026-07-17_calibrated_article_citations.md`
- English AI-judge detailed results:
  `evaluation/publication_results/ai_judge_en_completeness_patch_calibrated_20260717/ai_judge_evaluation_2026-07-17_calibrated_article_citations.csv`
- English AI-judge manifest:
  `evaluation/publication_results/ai_judge_en_completeness_patch_calibrated_20260717/ai_judge_manifest_2026-07-17_calibrated_article_citations.json`
- Portuguese AI-judge summary:
  `evaluation/publication_results/ai_judge_pt_residual_quality_final_20260718/ai_judge_summary_2026-07-18_pt_residual_quality_final.md`
- Portuguese AI-judge detailed results:
  `evaluation/publication_results/ai_judge_pt_residual_quality_final_20260718/ai_judge_evaluation_2026-07-18_pt_residual_quality_final.csv`
- Portuguese AI-judge manifest:
  `evaluation/publication_results/ai_judge_pt_residual_quality_final_20260718/ai_judge_manifest_2026-07-18_pt_residual_quality_final.json`
- First external stress-test interpretation:
  `evaluation/publication_results/external_prospective_candidate_20260718_recovered_combined/EXTERNAL_VALIDATION_INTERPRETATION_20260718.md`
- First external recovered summary:
  `evaluation/publication_results/external_prospective_candidate_20260718_recovered_combined/external_recovered_summary_2026-07-18.md`
- Refusal-development report:
  `evaluation/publication_results/refusal_calibration_dev_after_prompt_20260718/REFUSAL_CALIBRATION_DEV_REPORT_20260718.md`
- Refusal-focused external test summary:
  `evaluation/publication_results/external_refusal_focus_after_prompt_20260718/generation_summary_2026-07-18_17-10-42.md`
- Refusal-focused external interpretation:
  `evaluation/publication_results/external_refusal_focus_after_prompt_20260718/EXTERNAL_REFUSAL_FOCUS_INTERPRETATION_20260718.md`

## Final Decision

Publication-ready as a technical feasibility and engineering case study after
the methods, limitations, and failure analysis are written carefully. The study
now includes external AI-authored stress tests, so it can discuss prospective
stress-test behavior, but it is still not ready for claims of expert regulatory
validation, clinical/legal correctness, or operational deployment.
