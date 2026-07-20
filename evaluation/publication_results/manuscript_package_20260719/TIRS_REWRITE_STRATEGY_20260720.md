# TIRS rewrite strategy, 2026-07-20

## Main decision

The current manuscript should not be submitted in its present form. It is technically defensible but too engineering-forward for Therapeutic Innovation & Regulatory Science. The main paper should be rewritten around regulatory information access in drug development and health-product development. The engineering details should be moved to supplementary material.

## New central story

The study is not mainly about whether a RAG pipeline can produce high retrieval scores. The stronger story is:

Regulatory teams working with ANVISA documents often need fast, traceable answers to specific development questions. These questions may concern clinical-trial submissions, SUSAR reporting, DSUR obligations, biological-product registration, medical-device labelling, pharmacovigilance databases, or reliance pathways. A bilingual RAG system can help when it retrieves the correct document and article, but it must also show when it is incomplete or when the documents do not contain the requested operational fact.

This is a better TIRS story because it connects the method to regulatory affairs work.

## What moves out of the main paper

Move these details to Supplementary Information:

- embedding model names
- BM25 parameters
- reciprocal rank fusion details
- reranker model details
- chunk-length distribution
- prompt text
- JSON judge schema
- full benchmark manifests
- per-question metric files
- checksum tables
- development decision log

The main paper can say only that the system used article-level indexing, combined semantic and keyword retrieval, reranking, bilingual query support, source citation, and refusal rules. Full implementation detail belongs in Supplementary File 1 or 2.

## What moves into the main paper

Add concrete regulatory examples:

1. Clinical-trial safety reporting
   - SUSAR notification and blinding questions.
   - DSUR annual submission question.

2. Clinical-trial submission management
   - DDCM or clinical-trial suspension/cancellation by sponsor.
   - Technical requirement during ANVISA review and effect on deadlines.

3. Pharmacovigilance operations
   - Minimum information for a valid reportable notification.
   - Retention period for pharmacovigilance database records.

4. Biological products
   - Registration of a foreign-manufactured biological product when it is not registered in the manufacturing country.

5. Medical devices
   - Non-printed instructions for use and home-use or lay-user restrictions.

6. Refusal cases
   - Current phone number for an ANVISA support system.
   - Current MedDRA version.
   - Petition subject code for reliance.
   - Current electronic form model for SUSAR notification.

## New Results structure

Use a story-driven Results section:

1. The system answered direct regulatory questions when the answer was in the corpus.
2. The system handled some false-premise questions by correcting the premise.
3. The system still made clinically and regulatory-relevant completeness errors.
4. The external test changed the interpretation: the main residual risk was not retrieval, but refusal calibration.
5. Refusal calibration improved, but did not remove the need for audit.

## Needed table changes

Replace the current metric-heavy tables with:

Table 1. Regulatory use cases represented in the benchmark.

Table 2. Representative examples of correct answers, incomplete answers, false refusals, and correct refusals.

Table 3. Summary performance by evaluation stage.

Detailed technical metrics can be supplementary.

## Tone

Use direct, plain sentences. Avoid phrases such as:

- "article-aware legal-regulatory structure rather than generic passage chunks"
- "staged validation pattern"
- "citation-constrained answer generation"
- "retrieved gold-term coverage"
- "normalized article nDCG"

These terms may remain in supplementary methods, but the main paper should explain what they mean in ordinary regulatory terms.

## Revised claim level

The paper should claim:

"A bilingual RAG prototype was able to support traceable retrieval and answering for selected ANVISA regulatory questions, but error analysis showed that usefulness depends on article-level evidence, completeness checks, and conservative refusal when the documents do not contain the requested fact."

The paper should not claim:

- regulatory validation
- expert consensus
- deployment readiness
- legal advice
- general ANVISA coverage
- proof that AI-judge scores equal human regulatory review

