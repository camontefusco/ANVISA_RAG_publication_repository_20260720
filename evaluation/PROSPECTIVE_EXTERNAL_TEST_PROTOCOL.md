# Prospective External Test Protocol

Purpose: create a new untouched bilingual test set after the current RAG
pipeline is frozen. This protects the publication from overclaiming the repaired
benchmark scores as unbiased generalization performance.

## Why This Is Needed

The current final metrics include post-error-analysis repairs on held-out rows.
Those results are useful final-system evidence, but they are not a clean
prospective test. A new external set should be created only after no more
retrieval, prompt, chunking, judge, or benchmark-threshold changes are allowed.

## Recommended Size

- Minimum: 15 bilingual pairs, 30 questions.
- Better: 25 bilingual pairs, 50 questions.
- Include Portuguese and English versions of each question.
- Keep both languages of each pair together in the external test set.

## Suggested Composition For 25 Pairs

- 12 direct article questions.
- 5 multi-article or exception questions.
- 4 list/completeness questions with long articles.
- 4 unanswerable or adversarial questions.

## Authoring Rules

1. Freeze the code, corpus, vector store, prompts, judge prompt, and model names
   before writing the external questions.
2. Do not inspect RAG outputs while writing questions or expected answers.
3. For answerable questions, cite exact source document, regulation, article,
   and supporting passage.
4. For unanswerable questions, leave source/article/citation/evidence empty and
   explain why the corpus does not answer it.
5. Keep the expected answer short enough to judge, but complete enough to include
   all material conditions, exceptions, deadlines, and categories.
6. Do not tune code, prompts, retrieval anchors, or judge rules after seeing
   external-test failures. If a fix is necessary, freeze it and create a second
   untouched external set.

## Files

- Author questions in `evaluation/external_test_authoring_template_50.csv`.
- A prefilled AI-authored candidate is available at
  `evaluation/external_test_authoring_candidate_50.csv`.
- Convert and freeze them with:

```bash
/opt/anaconda3/envs/rag-project-env/bin/python -B evaluation/build_external_benchmark_from_template.py \
  --input evaluation/external_test_authoring_template_50.csv \
  --output evaluation/external_benchmark_50.jsonl \
  --manifest evaluation/external_benchmark_50_manifest.json
```

The current candidate conversion output is:

- `evaluation/prospective_external_benchmark_candidate_50.jsonl`
- `evaluation/prospective_external_benchmark_candidate_50_manifest.json`
- SHA-256:
  `40a01b48ce016ccc81e5dae082724ffb4a49392726084276e3997ce70bc1f79d`

Because this candidate was authored by AI inside the project workflow, report it
as an AI-authored prospective stress test unless you manually review and revise
it before freezing. It should not be described as independent expert validation.

## Reporting

Report three layers separately:

- Original held-out results before targeted repairs.
- Post-repair final-system results on the curated benchmark.
- Prospective external-test results after the final pipeline was frozen.

The third layer is the only defensible estimate of prospective generalization.
