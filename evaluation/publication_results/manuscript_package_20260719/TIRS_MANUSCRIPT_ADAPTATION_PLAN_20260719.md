# TIRS manuscript adaptation plan

Date: 2026-07-19

Target journal: Therapeutic Innovation & Regulatory Science

Recommended article type: Research Article

Reason: The project reports original technical evaluation data for a regulatory-document question-answering system. This fits better than Commentary or Review. Analytical Report is possible, but its 3,000-word limit is tight and it is better suited to working-group or methodologic consensus reports.

Main constraint from TIRS instructions: 5,000 words including abstract and main text, excluding references, figures, and tables. Abstract maximum 250 words. References in Vancouver style. Figures and tables can be separate. Supplementary files are expected for material that supports conclusions but is too detailed for print.

Companion file: `TIRS_DECISION_RATIONALE_AND_VALIDATION_HISTORY_20260719.md` records the project decision history, quality-review steps, pipeline repairs, and validation sequence. Use it to support the Methods subsection on development history and as the basis for an additional supplementary file.

## Core framing

Current framing is acceptable but should be sharpened.

Use this frame:

"This study evaluates a bilingual article-aware retrieval-augmented generation system for interpretation support over selected ANVISA pharmaceutical and health-product regulatory documents. The focus is not clinical decision support, but regulatory information access, source traceability, article-level provenance, and refusal when retrieved evidence is insufficient."

Avoid:

- Claims of regulatory advice.
- Claims of ANVISA endorsement.
- Claims of deployment readiness.
- Claims that AI judgment replaces expert regulatory review.
- Language implying that perfect internal scores prove general performance.

## Suggested title

Bilingual Article-Aware Retrieval-Augmented Generation for ANVISA Regulatory Document Interpretation

Alternative:

Technical Validation of a Bilingual Retrieval-Augmented Generation System for Article-Level ANVISA Regulatory Documents

## Main-text structure

### Title page

Include:

- Full title.
- Author name and affiliation.
- Corresponding author full postal address and email.
- Five to six keywords.

Suggested keywords:

- Regulatory science
- Retrieval-augmented generation
- ANVISA
- Pharmaceutical regulation
- Bilingual information retrieval
- Large language models

### Abstract

Use structured abstract because Research Articles require a structured abstract.

Suggested headings:

- Background
- Objective
- Methods
- Results
- Conclusion

Keep under 250 words.

### Introduction

Target length: 600-800 words.

Must do three things:

1. Explain the regulatory-science problem: long article-structured regulatory texts, dense terminology, multilingual access needs, and need for traceable answers.
2. Connect to prior TIRS work on generative AI/RAG for FDA guidance documents.
3. State the specific contribution: ANVISA corpus, Portuguese-English retrieval, article-level chunking, hybrid retrieval, reranking, refusal calibration, and staged automated validation.

Recommended opening logic:

- Regulatory agencies publish guidance and rules that support pharmaceutical and health-product development.
- Existing keyword search is limited for article-level interpretation and cross-language queries.
- RAG can improve access, but regulatory use requires source citation, exact document retrieval, and refusal on insufficient evidence.
- Prior FDA-guidance RAG work showed promise but also incomplete or incorrect answers, motivating task-specific validation.
- This study evaluates a bilingual ANVISA-focused implementation.

### Materials and Methods

Target length: 1,400-1,700 words.

Needs expansion. TIRS requires enough detail to reproduce the procedures.

Subsections:

1. Corpus and document inclusion
2. Text cleaning and article-aware chunking
3. Retrieval architecture
4. English query expansion
5. Answer generation and refusal policy
6. Benchmark construction
7. Evaluation metrics
8. Automated judging protocol
9. Statistical analysis
10. Software, code, and data availability

Add a corpus table in the main text:

Columns:

- Document
- Regulatory topic
- Year
- Included source file
- Number of cleaned articles/chunks
- Main relevance to pharmaceutical or health-product regulation

Add a clear statement:

"The indexed corpus was closed. The system was not allowed to answer from current web pages, private submission systems, forms, fees, or documents not included in the index."

### Results

Target length: 900-1,100 words.

Use staged reporting:

1. Corpus and index characteristics
2. Internal held-out benchmark
3. Prospective external stress test
4. Refusal-focused external test
5. Error analysis

Important: Do not let the 1.000 internal scores dominate the story. Report them, then immediately qualify them as post-repair internal performance.

Main table:

Table 1. Corpus and index characteristics.

Table 2. Internal held-out and external benchmark performance.

Table 3. Error categories from external testing.

Recommended figure:

Figure 1. RAG pipeline flow: raw text, cleaning, article-aware chunking, hybrid retrieval, reranking, answer generation, citation/refusal, evaluation.

Optional figure:

Figure 2. Staged validation design: internal benchmark, prospective external test, refusal-development update, refusal-focused external test.

### Discussion

Target length: 1,000-1,300 words.

Recommended sections:

- Principal findings
- Comparison with prior FDA-guidance generative AI/RAG work
- Regulatory-science implications
- Refusal calibration and safety boundary
- Limitations
- Future work

Most important comparison:

Use the prior TIRS FDA guidance paper as the closest comparator. The discussion should say that both studies support the value of retrieval and citation, but both show that regulatory-document AI must be validated for correctness, completeness, and unsupported-answer behavior before operational use.

### Conclusion

Target length: 120-180 words.

Conservative conclusion:

"The system showed strong technical performance on selected ANVISA documents when evaluated for retrieval, citation validity, answer faithfulness, completeness, and refusal behavior. The findings support further development of bilingual regulatory information-access systems, but not unsupervised regulatory decision-making."

## Supplementary material package

TIRS allows online supplementary material. This project should use it heavily.

### Supplementary File 1. Corpus and preprocessing

Content:

- Full source-document inventory.
- Raw-to-cleaned transformation description.
- Cleaning rules.
- Article-detection rules.
- Chunk metadata schema.
- Counts by document.
- Examples of raw text, cleaned text, and resulting article chunk.

Purpose: proves the indexing corpus and chunking are auditable.

### Supplementary File 2. Retrieval and generation configuration

Content:

- Embedding model.
- BM25 configuration.
- Rank-fusion method.
- Candidate retrieval depth.
- Reranker model and top-k settings.
- Query expansion glossary.
- Generation model settings.
- Final answer prompt.
- Refusal prompt.

Purpose: reproducibility.

### Supplementary File 3. Benchmark dataset documentation

Content:

- Benchmark design.
- Category counts: 70 Portuguese answerable, 70 English answerable, 20 multi-article or exception, 40 unanswerable/adversarial.
- Inclusion/exclusion rules.
- Question fields and answer key fields.
- SHA-256 checksums.
- Split manifest.
- Full question list if legally and ethically acceptable.

Purpose: makes the evaluation credible despite no two-expert panel.

### Supplementary File 4. Evaluation metrics and AI-judge rubric

Content:

- Definitions for source hit, MRR, article Recall@5, Precision@5, nDCG@5, term coverage, citation validity, refusal accuracy.
- AI-judge rubric for faithfulness, citation correctness, completeness, and refusal correctness.
- Judge prompt.
- Model used for judging.
- Temperature/settings.
- Evidence passed to judge.
- Known limits of AI-as-judge.

Purpose: transparent automated validation.

### Supplementary File 5. Full evaluation results

Content:

- Per-question retrieval results.
- Per-question generated answers.
- Retrieved contexts.
- Citation validity labels.
- AI-judge scores.
- Error category labels.

Purpose: lets reviewers inspect whether averages hide failures.

### Supplementary File 6. External stress tests

Content:

- Prospective external benchmark protocol.
- First external test manifest.
- First external test results.
- Refusal calibration development set, clearly separated from testing.
- Second refusal-focused external test manifest.
- Second refusal-focused test results.
- Statement that no tuning was performed from the external test before first reporting.

Purpose: addresses reviewer concern about overfitting.

### Supplementary File 7. Statistical analysis

Content:

- Pair-clustered bootstrap procedure.
- Confidence intervals.
- Language-stratified results.
- Answerable vs unanswerable stratification.
- Sensitivity analysis excluding post-repair internal results.

Purpose: makes the performance claims more publication-grade.

### Supplementary File 8. Source code and reproducibility manifest

Content:

- Environment file.
- Package versions.
- Script execution order.
- Random seeds if applicable.
- Input and output file manifest.
- Hashes for frozen artifacts.
- Instructions to rebuild cleaned data, index, retrieval evaluation, generation evaluation, and AI-judge evaluation.

Purpose: satisfies research-data expectations and reduces reviewer skepticism.

## Main manuscript changes needed from current draft

High priority:

1. Add direct comparison to the prior TIRS FDA guidance generative AI/RAG paper.
2. Convert references from name-year style to Vancouver numbered style.
3. Add exact corpus table with document names and chunk counts.
4. Add a reproducibility paragraph with code, data, and artifact availability.
5. Replace "LLM-based evaluator" with a more explicit automated judging protocol.
6. Add confidence intervals for main metrics where available.
7. Add a short ethics/IRB statement: no human participants, no patient data, no clinical trial.
8. Add a data availability statement.
9. Add funding, conflict of interest, and author contribution statements.
10. Add a stronger limitation that the benchmarks were not independently authored by regulatory experts.

Medium priority:

1. Add a pipeline figure.
2. Add a validation-flow figure.
3. Add error-analysis table.
4. Add representative examples of answerable, multi-article, and unanswerable questions.
5. Add a paragraph explaining why Cohen's kappa is not reported.
6. Add one sentence explaining why no clinical trial registration applies.

Low priority:

1. Add optional appendix with Portuguese-English glossary.
2. Add optional appendix with refused-answer examples.
3. Add optional appendix comparing retrieval with and without English query expansion.

## Recommended claim level

Acceptable:

- Technical validation.
- Regulatory information access.
- Article-level traceability.
- Bilingual retrieval support.
- Automated evaluation with transparent limitations.

Not acceptable:

- Regulatory decision support readiness.
- Legal correctness.
- Expert-level regulatory interpretation.
- Replacement of regulatory professionals.
- Current ANVISA guidance coverage.

## Cover letter angle

The cover letter should be short.

Key message:

"This manuscript extends recent work on generative AI semantic search of FDA guidance documents by evaluating a bilingual Portuguese-English, article-aware RAG pipeline over selected ANVISA regulatory documents. The study emphasizes source and article citation, refusal behavior, and transparent automated validation rather than deployment claims."

## Submission readiness checklist

Before submission:

- Main manuscript under 5,000 words.
- Structured abstract under 250 words.
- Vancouver references.
- 5-6 keywords.
- Title page complete.
- Funding statement included.
- Conflict of interest statement included.
- Author contributions included.
- Data availability statement included.
- Ethics statement included.
- Tables cited in order.
- Figures uploaded separately or placed at end as required.
- Supplementary files numbered and cited in text.
- All benchmark files checksummed.
- External test described separately from development tuning.
- No claim of ANVISA endorsement.
- No claim of expert validation.
