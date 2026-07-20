# Solo Validation Protocol for the ANVISA RAG Benchmark

## What Can Be Claimed

This benchmark can support a publication by a solo researcher if its provenance,
manual checks, automated-judge calibration, and limitations are reported clearly.
Do not describe an LLM as a regulatory expert or claim inter-rater reliability when
only one human annotator participated.

## Artifacts

- `publication_benchmark_200.jsonl`: frozen benchmark data.
- `benchmark_200_manifest.json`: construction metadata and target counts.
- `benchmark_200_audit.json`: deterministic corpus and structure audit.
- `benchmark_200_review.csv`: human-review worksheet.

## Stage 1: Freeze Before System Evaluation

1. Record a SHA-256 checksum of the benchmark.
2. Do not tune retrieval, prompts, or thresholds on the full benchmark.
3. Select 25 bilingual pair IDs for development and retain 75 pair IDs as a
   held-out test set. Keep both languages of a pair in the same split.
4. Stratify the split across direct, complex/exception, and unanswerable items.

## Stage 2: First Human Pass

Review one bilingual pair at a time without looking at RAG outputs. Use the source
excerpt and regulation file to label:

- Question clarity: answerable as written, without hidden assumptions.
- Answer support: every expected-answer claim is present in the evidence.
- Citation accuracy: source, regulation, and article are exact.
- Bilingual equivalence: Portuguese and English ask the same substantive question.
- Decision: keep, revise, or drop.

Write a short reason for every revision or deletion. A benchmark item is accepted
only when all four binary checks equal 1.

## Stage 3: Repeatability Check

After at least seven days, blindly re-review a seeded random sample of 20 bilingual
pairs. Hide the first-pass labels. Report raw agreement and Cohen's kappa between
your two passes as intra-rater repeatability, not inter-rater agreement.

Resolve disagreements by returning to the cited article and recording the final
rationale. Preserve both original ratings in the research archive.

## Stage 4: Automated Judges

Use automated judges only after human gold labels are frozen.

- Prefer a judge from a different model family than the answer generator.
- Use two judges when feasible and retain their raw JSON decisions.
- Give judges the question, expected answer, answer, citation labels, and evidence.
- Require claim-level support decisions, not only a global 0-1 score.
- Calibrate each judge against at least 40 manually reviewed items.
- Report judge-human agreement, sensitivity, specificity, and common error types.

Automated judges may expand evaluation coverage, but they do not replace the human
validation of gold questions, answers, or legal citations.

ARES is not treated as a no-label substitute here. Its published experiments found
that approximately 150 human annotations were needed for reliable prediction-powered
calibration, and replacing the human validation set entirely with GPT-4 generations
performed worse. With this project's resources, transparent deterministic metrics
plus calibrated general-purpose judges are more defensible than training an ARES
judge on insufficient labels.

## Stage 5: Final RAG Evaluation

Report retrieval and generation separately:

- Recall@1, Recall@5, MRR, and article-level evidence recall.
- Faithfulness and completeness at claim level.
- Citation precision, citation recall, and unsupported-citation rate.
- Correct refusal, false refusal, and unsafe-answer rates.
- Portuguese and English metrics with paired differences.
- Bootstrap 95% confidence intervals over bilingual pair IDs.
- Latency, API cost, model version, retrieval configuration, and run date.

Compare dense-only, BM25-only, hybrid, reranked, and rewritten-query variants on
the same held-out pairs. Use paired bootstrap intervals or a paired randomization
test rather than interpreting small raw score differences as meaningful.

## Required Limitation Statement

State that benchmark validation was performed by one researcher and that regulatory
interpretations were not independently reviewed by legal or ANVISA specialists.
Frame conclusions as system performance on the curated corpus, not proof of legal
correctness or fitness for clinical or regulatory decision-making.

## Methodological Basis

- Es et al. (2024), RAGAS: https://doi.org/10.18653/v1/2024.eacl-demo.16
- Saad-Falcon et al. (2024), ARES: https://aclanthology.org/2024.naacl-long.20/
- Ru et al. (2024), RAGChecker: https://arxiv.org/abs/2408.08067
- Zheng et al. (2023), LLM-as-a-judge bias and calibration:
  https://arxiv.org/abs/2306.05685
- Thomas et al. (2025), TREC human versus LLM support assessment:
  https://arxiv.org/abs/2504.15205
