# Metric Integrity Audit

Date: 2026-07-18

## Bottom Line

The final `1.000` values should not be interpreted as clean prospective
generalization. They are post-error-analysis final-system results on a curated
benchmark after targeted repairs and rejudging.

This is still useful engineering evidence, but it must be separated from
pre-repair held-out results and from any future untouched external test.

## Why The Final Scores Are High

The final artifacts are merged artifacts. They preserve most original held-out
rows but replace known failure rows after targeted debugging.

### English

- Generation patched rows: 3 of 75
  - `COMPLEX_02_EN`
  - `COMPLEX_09_EN`
  - `DIRECT_13_EN`
- AI-judge rejudged rows: 1 of 75
  - `DIRECT_25_EN`

### Portuguese

- Generation patched rows: 13 of 75
  - `COMPLEX_09_PT`
  - `COMPLEX_10_PT`
  - `DIRECT_04_PT`
  - `DIRECT_12_PT`
  - `DIRECT_13_PT`
  - `DIRECT_16_PT`
  - `DIRECT_17_PT`
  - `DIRECT_18_PT`
  - `DIRECT_24_PT`
  - `DIRECT_37_PT`
  - `DIRECT_43_PT`
  - `DIRECT_47_PT`
  - `DIRECT_69_PT`
- AI-judge patched or rejudged rows: 18 of 75
  - `COMPLEX_05_PT`
  - `COMPLEX_09_PT`
  - `COMPLEX_10_PT`
  - `DIRECT_04_PT`
  - `DIRECT_05_PT`
  - `DIRECT_12_PT`
  - `DIRECT_13_PT`
  - `DIRECT_16_PT`
  - `DIRECT_17_PT`
  - `DIRECT_18_PT`
  - `DIRECT_20_PT`
  - `DIRECT_24_PT`
  - `DIRECT_25_PT`
  - `DIRECT_27_PT`
  - `DIRECT_37_PT`
  - `DIRECT_43_PT`
  - `DIRECT_47_PT`
  - `DIRECT_69_PT`

## Interpretation For Manuscript

Use this framing:

> After error analysis and targeted repairs, the final system achieved strong
> post-repair performance on the curated ANVISA benchmark.

Avoid this framing:

> The system achieved perfect held-out performance and therefore generalizes to
> future regulatory questions.

## Required Additional Test

Before claiming prospective performance, freeze the pipeline and run a new
external benchmark that has not been used for prompt, retrieval, chunking,
judge, or threshold tuning.

Prepared files:

- `evaluation/PROSPECTIVE_EXTERNAL_TEST_PROTOCOL.md`
- `evaluation/external_test_authoring_template_50.csv`
- `evaluation/external_test_authoring_candidate_50.csv`
- `evaluation/prospective_external_benchmark_candidate_50.jsonl`
- `evaluation/prospective_external_benchmark_candidate_50_manifest.json`
- `evaluation/build_external_benchmark_from_template.py`

The candidate external set contains 25 bilingual pairs (50 questions) and has
SHA-256 `40a01b48ce016ccc81e5dae082724ffb4a49392726084276e3997ce70bc1f79d`.
It is marked `pending_human_review` and should be reported as AI-authored unless
manually reviewed before freeze.

## Recommended Reporting Table

Report all three layers:

| Layer | Purpose | Can Support Generalization Claim? |
|---|---|---|
| Pre-repair held-out | Baseline after original freeze | Limited |
| Post-repair final system | Engineering evidence after targeted fixes | No, not by itself |
| Prospective external test | New untouched benchmark after final freeze | Yes, with caveats |
