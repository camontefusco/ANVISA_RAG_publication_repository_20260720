# Quality check and no-APC journal target list

Date: 2026-07-19

## Manuscript quality check

Current draft: manuscript_draft_plain_20260719.md
Current length: about 2,051 words.

### Strengths

- The paper has a clear technical contribution: article-aware RAG for bilingual ANVISA regulatory documents.
- The evaluation story is honest: internal benchmark, external stress test, refusal weakness, refusal-focused retest.
- The manuscript avoids claiming expert validation or regulatory readiness.
- The methods are publishable if the benchmark, code, prompts, and corpus processing are documented as supplementary material.
- The refusal calibration result is useful because it reports a failure mode instead of hiding it.

### Main weaknesses before submission

- The current manuscript is too short for most full research article formats.
- The Results section needs compact tables, not only prose metrics.
- The corpus must be described more concretely: exact ANVISA documents, versions, dates, number of cleaned files, number of articles, number of chunks.
- The benchmark construction needs a reproducibility table: question classes, languages, answerability labels, article labels, checksum, and split logic.
- The AI-judge protocol needs stronger reporting: model, prompt, temperature, evidence passed to judge, blinded/frozen status, failure handling, and limitations.
- The external benchmark recovery caveat must be transparent: 40-row checkpoint plus regenerated missing 10 rows, no tuning during recovery.
- The paper needs at least one figure: pipeline diagram from raw text to cleaned data to chunks to hybrid retrieval to rerank to answer/judge.
- The paper needs supplementary artifacts: benchmark JSONL, prompts, metric scripts, retrieval traces, and manifest of source documents.

### Recommendation

Do not submit the current 2,051-word draft as-is. Use it as the base for a Brief Communication only if the target journal allows focused system evaluations. For a full paper, expand to about 3,800-4,500 words and add 3-4 tables plus one pipeline figure.

## No-APC target journals

Interpretation of no APC: publication must be possible without paying an APC and without relying on a waiver. For hybrid/subscription journals, this means choosing the standard subscription route, not gold open access.

### Best fit

1. Journal of Biomedical Informatics

- Route: subscription publication, no publication fee charged to authors; optional open access has an APC.
- Fit: strong if framed as biomedical/health informatics methodology for regulatory document QA.
- Why plausible: the journal accepts informatics methods and evaluation papers, and its guide allows up to 6,000 words.
- Risk: expects stronger biomedical informatics significance and rigorous reporting.
- Needed adaptation: use structured abstract with Objective, Methods, Results, Conclusion; add Statement of Significance.

2. JAMIA

- Route: standard subscription-based access, no charge if open access is not selected.
- Fit: possible but ambitious.
- Why plausible: JAMIA accepts implementation or evaluation of informatics-based studies and brief communications.
- Risk: likely wants broader biomedical informatics contribution, not only one local regulatory corpus.
- Needed adaptation: submit as Brief Communication or Research and Applications only after adding stronger methodology detail and public artifacts.

3. Research Methods in Medicine & Health Sciences

- Route: journal states no article processing fees for authors.
- Fit: good if framed as a methods paper on RAG validation when expert panels are unavailable.
- Why plausible: the paper is mainly about evaluation design and validation methods.
- Risk: less obviously AI/RAG-specific; needs emphasis on research-methods contribution.
- Needed adaptation: strengthen methods, benchmark design, AI-judge limitations, and reproducibility.

4. Artificial Intelligence and Law

- Route: hybrid journal; standard subscription route should avoid APC under Springer hybrid policy.
- Fit: strong on legal/regulatory AI if framed as AI for legal/regulatory texts, not health informatics.
- Why plausible: journal seeks computational models, tools, datasets, and empirical AI systems for legal knowledge and reasoning.
- Risk: ANVISA health regulation may be seen as regulatory informatics rather than core AI and Law unless the legal reasoning/citation aspect is emphasized.
- Needed adaptation: emphasize legal/regulatory retrieval, article-level citation, refusal under incomplete legal evidence, and benchmark contribution.

### Secondary fit

5. International Journal of Medical Informatics

- Route: subscription publication appears available; optional open access has APC.
- Fit: possible if framed as medical informatics decision-support infrastructure.
- Risk: may expect clinical, organizational, or user-facing health system relevance beyond a technical RAG benchmark.

6. Information Processing & Management

- Route: subscription publication, no publication fee charged to authors; optional open access has APC.
- Fit: possible if reframed as information retrieval / question answering evaluation.
- Risk: current corpus and evaluation may be too application-specific unless the article contributes a reusable benchmark or method.

7. Information Systems Frontiers

- Route: hybrid journal; subscription route should avoid APC under Springer hybrid policy.
- Fit: possible for an AI-enabled information access system in a regulatory setting.
- Risk: less natural than JBI, JAMIA, or AI and Law.

8. Knowledge-Based Systems

- Route: subscription publication, no publication fee charged to authors; optional open access has APC.
- Fit: possible if the paper is reframed around knowledge-based AI and robust evidence-grounded generation.
- Risk: likely expects stronger algorithmic novelty than the current pipeline.

## Journals to avoid for this no-APC constraint

- Health Informatics Journal: open access with APC.
- JAMIA Open: fully open access with APC.
- JAMA Network Open: fully open access with APC.
- Discover Computing: fully open access with APC.
- npj Artificial Intelligence: fully open access with APC.
- BMC/Springer fully open access journals unless an institutional agreement covers the charge; that would not meet the no-waiver requirement.

## Best submission strategy

First choice: Journal of Biomedical Informatics, if we expand the manuscript to a full technical evaluation paper.

Second choice: Artificial Intelligence and Law, if we reposition the paper as regulatory/legal AI with article-level citation and refusal behavior.

Lower-risk no-fee route: Research Methods in Medicine & Health Sciences, if we frame it as a methodology paper about validating RAG systems with single-researcher plus AI-judge constraints.

## Work needed before submission

- Add Table 1: corpus and index statistics.
- Add Table 2: benchmark composition.
- Add Table 3: internal, external, and refusal-focused metrics.
- Add Table 4: target journal compliance checklist.
- Add Figure 1: pipeline diagram.
- Add an AI-use disclosure and conflict/funding/data/code availability statements.
- Add supplementary files with prompts, benchmark schema, and evaluation scripts.
- Convert references to the target journal style.
