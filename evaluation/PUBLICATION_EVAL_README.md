# Publication Evaluation Protocol

This folder contains the reproducible evaluation harness for the bilingual ANVISA
RAG system. The current study design is an automated technical validation using
deterministic retrieval/generation metrics plus an AI judge over frozen generated
answers. It is not expert-consensus, human-expert, clinical, or legal validation.

## Frozen Evaluation Assets

- `publication_benchmark_200.jsonl`: 200 questions in 100 bilingual pairs with
  document-, article-, and passage-level gold evidence.
- `benchmark_200_split_manifest.json`: pair-level calibration, development, and
  held-out assignments. Portuguese and English counterparts never cross splits.
- `ANVISA_RAG_Solo_Validation.xlsx`: blinded benchmark review and delayed repeat
  review workbook.
- `publication_eval.py`: retrieval and optional generation evaluation runner.
- `judge_existing_generation.py`: AI-judge runner for already generated answers.
- `analyze_judge_agreement.py`: intra-rater, human-AI, and AI-AI agreement analysis.

Do not edit the frozen benchmark after final evaluation begins. Record its SHA-256
checksum and every system configuration in the manuscript supplement.

## Prospective External Test

Because the final curated-benchmark scores include targeted post-error-analysis
repairs, create a new untouched external test set before making any
generalization claim. Use:

- `PROSPECTIVE_EXTERNAL_TEST_PROTOCOL.md`
- `external_test_authoring_template_50.csv`
- `external_test_authoring_candidate_50.csv`
- `build_external_benchmark_from_template.py`

After the current pipeline is frozen, fill the template without inspecting RAG
outputs, convert it to JSONL, then evaluate that JSONL once. Do not tune the
pipeline on those failures unless you create another untouched external set.

A candidate 50-question bilingual external set has been drafted in
`external_test_authoring_candidate_50.csv` and converted to
`prospective_external_benchmark_candidate_50.jsonl`.

- Manifest: `prospective_external_benchmark_candidate_50_manifest.json`
- SHA-256: `40a01b48ce016ccc81e5dae082724ffb4a49392726084276e3997ce70bc1f79d`
- Status: `pending_human_review`

Treat this candidate as a prospective stress test after final pipeline freeze,
not as independent expert validation. If you tune the system after seeing its
failures, create a new untouched external set for the next prospective report.

Completed external/refusal evaluation artifacts:

- First external stress test recovered interpretation:
  `publication_results/external_prospective_candidate_20260718_recovered_combined/EXTERNAL_VALIDATION_INTERPRETATION_20260718.md`
- Refusal calibration development report:
  `publication_results/refusal_calibration_dev_after_prompt_20260718/REFUSAL_CALIBRATION_DEV_REPORT_20260718.md`
- Second refusal-focused external benchmark:
  `external_refusal_focus_candidate_30.jsonl`
- Second refusal-focused external interpretation:
  `publication_results/external_refusal_focus_after_prompt_20260718/EXTERNAL_REFUSAL_FOCUS_INTERPRETATION_20260718.md`

Reporting rule: the first external test diagnoses prospective weakness; the
refusal-development set supports engineering changes; the second refusal-focused
external test is post-calibration external evidence. Keep these layers separate.

## 1. Retrieval Evaluation

Run the complete cleaning, transactional index rebuild, verification, and held-out
retrieval evaluation pipeline:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B scripts/run_publication_pipeline.py
```

Run only the frozen 75-pair held-out split without API generation:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py \
  --split held_out_test_75
```

Run a smoke test during development:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py --limit 3
```

If files were restored from cloud storage and local model files are marked
`dataless`, point the evaluator at the materialized HuggingFace cache:

```bash
export RAG_EMBEDDING_MODEL_PATH=/Users/cmontefusco/.cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf
export RAG_RERANKER_MODEL_PATH=/Users/cmontefusco/.cache/huggingface/hub/models--cross-encoder--mmarco-mMiniLMv2-L12-H384-v1/snapshots/1427fd652930e4ba29e8149678df786c240d8825
```

Omitting `--split` evaluates all 100 pairs and is suitable for corpus diagnostics,
not the primary held-out performance claim.

The runner reports source hit rate and MRR plus article-level Recall@k,
Precision@k, MRR@k, and nDCG@k. Confidence intervals use 2,000 pair-clustered
bootstrap resamples so bilingual counterparts are not treated as independent.

## 2. Generation Evaluation

Freeze the corpus, index, retrieval settings, prompts, and model versions before
generating answers:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py --generate
```

Add the configured Gemini screening judge:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py --generate --judge
```

For the English query-rewrite ablation, run both conditions and retain both run
manifests:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py --generate
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py --generate --rewrite
```

For an offline retrieval-only English rewrite ablation, use deterministic glossary
expansion to collect candidates, but rerank with the original English question:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/publication_eval.py \
  --split held_out_test_75 \
  --language en \
  --rewrite \
  --rewrite-mode glossary \
  --rerank-query-mode original
```

Avoid reranking directly with a verbose expanded glossary query unless it is being
tested as a negative control; it can improve candidate recall while hurting
article-level reranking.

Each run writes detailed results, a human-review template, a structured failure
ledger, a Markdown summary, and a JSON manifest containing the benchmark checksum
and retrieval/model settings.

Generation runs also write `generation_checkpoint_*.jsonl` incrementally so
completed answers are not lost if a long API run is interrupted.

## 3. Single-Reviewer Validation

This section is optional for the current AI-only manuscript design. Complete it
only if you decide to add human intra-rater validation later.

1. Complete the first blinded review without seeing system scores.
2. Freeze those labels.
3. Wait at least seven days.
4. Complete the independently randomized second pass without consulting pass 1.
5. Report percentage agreement and Cohen's kappa with bootstrap confidence intervals.

This is intra-rater repeatability. Do not call it inter-rater agreement.

## 4. AI-Judge Triangulation

For the current AI-only evaluation, judge the frozen held-out generated answers
without regenerating them:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/judge_existing_generation.py \
  --output-dir evaluation/publication_results/ai_judge_heldout_20260714 \
  --continue-on-error
```

This reconstructs top-5 evidence with the saved retrieval and rerank queries from
the generation CSVs, then scores faithfulness, citation correctness,
completeness, and refusal correctness. Report these as AI-judge labels, not
human validation.

Use at least two fixed judges from different model families when resources permit.
Do not use an AI judge as a nominal second human expert. Keep temperature, prompts,
model identifiers, evidence order, and score thresholds fixed and publish them.

Each judge-results CSV must include `id` and these numeric columns:

- `judge_faithfulness`
- `judge_citation_correctness`
- `judge_completeness`
- `judge_refusal_correctness`

After filling two human-review CSVs, calculate repeatability and judge calibration:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/analyze_judge_agreement.py \
  --human-pass-1 evaluation/publication_results/human_pass_1.csv \
  --human-pass-2 evaluation/publication_results/human_pass_2.csv \
  --judge gemini=evaluation/publication_results/gemini_judge.csv \
  --judge independent=evaluation/publication_results/independent_judge.csv \
  --output-dir evaluation/publication_results/agreement
```

The analyzer reports every pairwise comparison and exports disagreements for human
adjudication. AI scores are thresholded at 0.5 by default; declare and sensitivity-
test any different threshold.

## 5. Required Reporting

Report Portuguese, English, direct, multi-article/exception, and unanswerable
results separately, followed by pooled estimates. Include:

- article-level retrieval metrics with 95% confidence intervals;
- groundedness, completeness, citation correctness, and refusal accuracy;
- AI-judge faithfulness, citation correctness, completeness, and refusal
  correctness;
- human intra-rater repeatability only if manual repeat review is completed;
- human-AI and AI-AI agreement only if those comparison datasets are completed;
- counts and examples for every failure category;
- the frozen benchmark checksum and run manifests;
- all prompts, model identifiers, and judge thresholds;
- the limitation that no independent second human expert was available;
- for an AI-only study, the limitation that no human expert adjudication was
  performed.

Valid framing: the system achieved internal retrieval and grounded-answer
performance on a transparent locked benchmark. Invalid framing: expert consensus,
clinical validation, or safety for autonomous regulatory decision-making.
