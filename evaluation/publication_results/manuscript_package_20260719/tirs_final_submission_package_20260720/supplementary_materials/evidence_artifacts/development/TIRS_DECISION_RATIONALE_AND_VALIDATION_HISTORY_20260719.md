# Decision rationale and validation history

Date: 2026-07-19

Target journal: Therapeutic Innovation & Regulatory Science

Purpose: This document records the major engineering, evaluation, and publication-framing decisions made during development of the ANVISA bilingual RAG project. It is intended to support manuscript Methods, Limitations, supplementary material, and response-to-review.

## Summary

The project began as a non-working Streamlit RAG application with dependency and source-code issues. It was converted into a technical validation study for a closed corpus of selected ANVISA regulatory documents. The final project direction was not chosen in one step. It resulted from repeated diagnosis, quality review, failure analysis, and re-decisions after benchmark results showed weaknesses.

The final manuscript should present this as a staged development and validation process:

1. Repair the application and environment.
2. Clean and structure the regulatory corpus.
3. Replace arbitrary chunks with article-aware chunks.
4. Add hybrid retrieval to support exact regulatory terms.
5. Add reranking to reduce noisy retrieval.
6. Add English-to-Portuguese regulatory query expansion.
7. Add citation-constrained answer generation.
8. Add refusal behavior for insufficient evidence.
9. Build a bilingual article-level benchmark.
10. Use automated AI judging because expert-panel validation was not available.
11. Run internal held-out evaluation.
12. Run an external stress test once without tuning.
13. Repair refusal calibration only after documenting the external weakness.
14. Run a new refusal-focused external test.
15. Freeze the pipeline and avoid further tuning from test results.

## Decision log

### 1. Environment and app repair

Problem observed: The app failed with `ModuleNotFoundError: No module named 'llama_index'`.

Decision: Treat dependency repair as the first engineering task before evaluating model behavior.

Rationale: Retrieval and generation results are not interpretable if the application environment is broken or inconsistent.

Quality check: The environment needed explicit package management and reproducible setup rather than relying on whatever packages were present in the base Anaconda environment.

Consequence: The project moved from an informal app-debugging task toward a reproducible RAG pipeline with scripts, environment files, and evaluation outputs.

### 2. Source-code comparison with borrowed working code

Problem observed: The user had local `src` files and borrowed `src_RAG_Shenia` files from a working but different project.

Decision: Use the borrowed code as a reference pattern, not as a direct replacement.

Rationale: The friend's project worked in another context, but this project needed ANVISA-specific document handling, article citation, bilingual retrieval, and refusal behavior.

Quality check: Code changes were judged against this project's corpus and evaluation requirements, not only whether the Streamlit app opened.

Consequence: The final pipeline kept project-specific modules for regulatory documents, language handling, retrieval, prompts, and evaluation.

### 3. Cleaning pipeline before benchmark interpretation

Problem observed: Raw text files were noisy and inconsistent. Some chunks mixed unrelated content or split regulatory articles poorly.

Decision: Build a cleaning and indexing pipeline:

`raw data/*.txt -> cleaned_data/*.txt -> article-level chunks with metadata -> rebuilt vector store -> rerun benchmark`

Rationale: Low RAG scores can result from noisy corpus structure rather than weak language models. Regulatory text is organized by articles, chapters, sections, and annexes, so cleaning and article-aware indexing are foundational.

Quality check: Corpus outputs were audited through cleaned-data reports and article-chunk audits.

Consequence: Evaluation became more meaningful because retrieval targets were aligned with regulatory citation units.

### 4. Article-aware chunking

Problem observed: Token-based chunks mixed too much content and sometimes split article-level meaning.

Decision: Use article-aware chunking as the primary indexing unit.

Rationale: In legal and regulatory texts, the article is the natural citation and interpretation unit. A useful answer should cite the document and article, not only a text span.

Implementation target:

- One article per chunk when possible.
- Preserve nearby section heading.
- Use approximately 300-700 tokens when possible.
- Split long articles only when necessary while preserving article metadata.

Quality check: Article citation validity and article Recall@5 were added as core metrics.

Consequence: Retrieval and generation could be evaluated at the level reviewers will care about: whether the correct regulation and article were found and cited.

### 5. Hybrid retrieval

Problem observed: Dense retrieval alone was weak for exact regulatory terms such as DDCM, RDC 945, Art. 33, IN 338, sponsor, biological product, medical device, and stability study.

Decision: Add hybrid retrieval using vector retrieval plus BM25 keyword retrieval, then merge candidate lists.

Rationale: Regulatory questions often depend on exact terms, acronyms, article numbers, and named resolutions. Dense retrieval improves semantic matching, but lexical retrieval protects exact-term recall.

Quality check: Retrieval was evaluated with source hit rate, source MRR, article Recall@5, article MRR@5, nDCG@5, and gold-term coverage.

Consequence: Retrieval became better aligned with legal-document search requirements.

### 6. Reranking

Problem observed: Retrieval could find relevant chunks but not always rank the best evidence high enough for generation.

Decision: Retrieve a broader set of candidate chunks, then rerank down to the top contexts used for answer generation.

Rationale: Broad retrieval maximizes recall; reranking improves final evidence selection. This is important when the generator receives only a small number of contexts.

Implementation target:

- Retrieve approximately top 20-30 chunks.
- Rerank candidates.
- Generate from top five contexts.

Quality check: Reranked retrieval was evaluated before focusing on answer quality.

Consequence: The system reduced cases where the answer generator missed the relevant article despite the article existing somewhere in the candidate set.

### 7. English query expansion

Problem observed: English source hit rate was lower than Portuguese source hit rate.

Decision: Translate or rewrite English questions into Portuguese retrieval anchors while preserving the original English question for intent and answer language.

Rationale: The source documents are Portuguese. English questions such as "clinical trial," "sponsor," "biological product," "medical device," and "stability study" need retrieval anchors such as "ensaio clinico," "patrocinador," "produto biologico," "dispositivo medico," and "estudo de estabilidade."

Quality check: English retrieval was evaluated with and without glossary rewrite.

Consequence: English retrieval improved without changing the user-facing answer language.

### 8. Citation-constrained generation

Problem observed: Answer quality cannot be evaluated only by whether an answer sounds plausible.

Decision: Require generated answers to cite source document and article.

Rationale: Regulatory usefulness depends on traceability. Readers need to know which regulation and article support the answer.

Quality check: Citation presence, article citation presence, retrieved-citation validity, and AI-judge citation correctness were added.

Consequence: The answer layer became auditable instead of purely conversational.

### 9. Refusal rule

Problem observed: The system sometimes answered unanswerable or adversarial questions using nearby general rules.

Decision: Add a strict refusal rule: if the retrieved context does not contain the specific requested answer, the system should say the indexed documents do not provide enough information.

Rationale: In regulatory contexts, unsupported specificity is a safety risk. A related article is not enough if it does not answer the exact question.

Quality check: Unanswerable/adversarial questions were included in benchmark design and scored separately.

Consequence: Refusal behavior became a main validation endpoint rather than an afterthought.

### 10. Bilingual 200-question benchmark

Problem observed: Small ad hoc tests could not support a publication-style validation claim.

Decision: Build a 200-question bilingual, article-level gold benchmark:

- 70 Portuguese answerable questions.
- 70 English answerable questions.
- 20 multi-article or exception questions.
- 40 unanswerable or adversarial questions.

Rationale: The benchmark needed to test normal retrieval, cross-language retrieval, complex regulatory interpretation, and refusal behavior.

Quality check: Benchmark audits and split manifests were created. Question categories were tracked separately.

Consequence: The project became suitable for technical validation reporting, although not for expert-consensus claims.

### 11. Automated AI judge instead of two human experts

Problem observed: The user was working alone and could not assemble two independent regulatory experts.

Decision: Use AI judging as the formal answer-quality evaluator, with explicit limitations.

Rationale: LLM-as-judge evaluation is scalable and can provide consistent labels for faithfulness, citation correctness, completeness, and refusal correctness. However, it is not a substitute for human expert validation.

Quality check: The manuscript explicitly avoids claims of inter-rater agreement or expert consensus. Cohen's kappa is not reported because there was no independent second human rater.

Consequence: The study is framed as automated technical validation, not as definitive regulatory validation.

### 12. Internal held-out evaluation

Problem observed: The internal benchmark eventually produced very high or perfect scores, including some 1.000 values.

Decision: Treat internal results as a post-repair benchmark, not as unbiased generalization evidence.

Rationale: The system had been improved after error analysis. Perfect internal scores can suggest overfitting, benchmark leakage, or overly easy evaluation.

Quality check: The user explicitly raised concern about trusting 1.000 metrics. The interpretation was revised to report internal scores cautiously.

Consequence: The manuscript emphasizes the staged evaluation sequence rather than relying on the internal benchmark alone.

### 13. Prospective external stress test

Problem observed: Internal scores were suspiciously high.

Decision: Run an external benchmark once and do not tune from it before reporting.

Rationale: A prospective external test is needed to estimate whether performance is robust or inflated by internal development.

Quality check: The external test was treated as untouched at first run. It exposed a meaningful weakness: refusal calibration.

Consequence: The strongest evidence became the external test pattern, not the internal perfect scores.

### 14. Refusal calibration repair

Problem observed: The first external stress test showed refusal correctness around 0.700 on unanswerable/adversarial questions.

Decision: Repair refusal calibration using a separate development set, not by tuning directly on the external test.

Rationale: The failure was important enough to fix, but tuning directly from the external test would compromise its value as an external assessment.

Quality check: A separate refusal-focused development set was used, followed by a new external refusal-focused test.

Consequence: The second refusal-focused external test showed improved refusal behavior while preserving answerable-control performance.

### 15. Pipeline freeze

Problem observed: Repeated tuning can inflate metrics and weaken publication credibility.

Decision: Freeze the pipeline after refusal calibration and report later results as validation, not development.

Rationale: A publication-ready study needs a clear boundary between development data and test data.

Quality check: The manuscript should describe which datasets were used for development, which were held out, and which external tests were run after freezing.

Consequence: Further changes should be limited to manuscript writing, supplement preparation, formatting, and reproducibility packaging unless a critical bug is discovered.

### 16. Journal selection

Problem observed: Many RAG and informatics journals either charge APCs, are not PubMed/MEDLINE indexed, are too high impact, or are not regulatory/pharma focused.

Decision: Target Therapeutic Innovation & Regulatory Science first.

Rationale: TIRS matches regulatory science and medical-product regulation, is not a super-high-impact target, offers a non-APC subscription publication route, and has already published closely related work on generative AI semantic search of FDA guidance documents.

Quality check: Alternative journals were filtered against scope, PubMed/MEDLINE status, and no mandatory APC/no waiver dependence.

Consequence: The manuscript should be adapted specifically for TIRS rather than written as a generic AI paper.

## Current final pipeline rationale

The final pipeline is justified by the failure modes observed during development:

- Article-aware chunks address regulatory citation and article-level meaning.
- Hybrid retrieval addresses exact regulatory terminology.
- Reranking addresses candidate-ordering errors after broad retrieval.
- English query expansion addresses Portuguese source documents queried in English.
- Citation-constrained generation addresses traceability.
- Refusal calibration addresses unsupported answers when related but insufficient context is retrieved.
- AI judging addresses practical solo-author evaluation constraints while requiring transparent limitations.
- External stress testing addresses concern that internal 1.000 scores are inflated.

## What to include in the manuscript

The main manuscript should include a short subsection called "Development and validation sequence" or "Pipeline development and validation design."

Suggested text:

"Pipeline development followed a staged procedure. Initial testing identified environment, corpus-cleaning, retrieval, answer-completeness, citation, and refusal failures. Each repair was made on development data and followed by re-evaluation. Because internal held-out metrics became very high after targeted repairs, the final system was assessed with a prospective external stress test that was run once before additional tuning. That test showed strong answerable-question performance but weaker refusal behavior. Refusal calibration was then updated using a separate development set, and a new refusal-focused external test was run to assess the repaired boundary condition. The final pipeline was frozen after this step."

## What to include in supplementary material

This document can become Supplementary File 9 or be merged into Supplementary File 8.

Recommended title:

Supplementary File 9. Development decisions, quality review, and validation history

Recommended contents:

- Full decision log.
- Development vs test dataset separation.
- Reasons for each pipeline component.
- Quality-review findings that changed the project direction.
- Journal-targeting rationale.
- Statement that no further tuning should be performed on reported external tests.

## Reviewer concerns addressed by this document

Concern: The system was overfit to the benchmark.

Response: Internal results are explicitly reported as post-repair. External stress testing was added because internal scores were suspiciously high.

Concern: There was no expert panel.

Response: The study is framed as automated technical validation, not expert regulatory validation. AI judging is disclosed and limited.

Concern: RAG is outside TIRS scope.

Response: The paper is framed around regulatory information access, medical-product regulation, source traceability, and ANVISA document interpretation. A prior TIRS FDA-guidance generative AI/RAG paper provides direct scope precedent.

Concern: The system may hallucinate.

Response: Refusal behavior is an explicit endpoint. The first external test exposed refusal weakness, calibration was repaired on development data, and a second external refusal test assessed the fix.

Concern: The system is not current regulatory advice.

Response: The corpus is closed and selected. The system is not allowed to answer questions about current web pages, future changes, forms, fees, or private submission status.

## Recommended next step

Revise the manuscript into the TIRS Research Article structure, then cite this development history in Methods and place the full version in supplementary material.
