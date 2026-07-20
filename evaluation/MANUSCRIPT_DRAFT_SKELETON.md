# Manuscript Draft Skeleton

## Working Title

Bilingual Retrieval-Augmented Generation for Brazilian Health Regulatory
Documents: Article-Aware Evaluation on ANVISA Clinical and Product Regulations

## Abstract

### Background

Regulatory documents are long, article-structured, and terminology-dense. These
properties make retrieval-augmented generation (RAG) attractive but also create
risks of incomplete retrieval, unsupported answers, and incorrect citations.

### Objective

To develop and technically validate a bilingual Portuguese-English RAG system for
selected ANVISA regulatory documents, with article-level retrieval and grounded
answer evaluation.

### Methods

We constructed a cleaned corpus from selected ANVISA regulations and indexed it
using article-aware chunks with regulation and article metadata. Retrieval used a
hybrid dense and BM25 strategy, reciprocal rank fusion, and cross-encoder
reranking. English queries were expanded with a deterministic regulatory glossary
for candidate retrieval while using the original question plus compact Portuguese
regulatory anchors for selected English reranking patterns. A frozen
200-question bilingual benchmark was created with answerable,
multi-article/exception, and unanswerable/adversarial questions. Evaluation used
a held-out split of 75 bilingual pairs. Metrics included source hit rate,
article Recall@5, MRR, nDCG, generated-answer term coverage, citation validity,
and refusal accuracy, with pair-clustered bootstrap confidence intervals.
Generated answers were also scored by an LLM-based AI judge for faithfulness,
citation correctness, completeness, and refusal correctness. No human expert
adjudication was performed.

### Results

On the post-repair held-out split, Portuguese generation achieved source hit
rate 1.000, article Recall@5 1.000, generated-answer term coverage 0.828,
retrieved-citation validity 1.000, and refusal accuracy 1.000. After English
retrieval optimization, English retrieval achieved source hit rate 1.000 and
article Recall@5 1.000; final English generation achieved generated-answer term
coverage 0.849, retrieved-citation validity 1.000, and refusal accuracy 1.000.
AI-judge faithfulness was 0.997 in English and 1.000 in Portuguese; citation
correctness was 1.000 in both languages; completeness was 0.995 in English and
1.000 in Portuguese.

Because these near-perfect internal metrics followed targeted error analysis, a
50-question AI-authored prospective external stress test was run. It showed
strong answerable-question performance (source hit 1.000, normalized article
Recall@5 0.967, faithfulness 1.000, citation correctness 0.975, completeness
0.943), but unanswerable/adversarial refusal correctness dropped to 0.700. After
a refusal-specific development update, a second untouched 30-question
refusal-focused external test achieved unanswerable-question refusal correctness
0.944, with no over-refusal on answerable controls.

### Conclusions

Article-aware hybrid retrieval with reranking produced strong Portuguese and
English performance on a frozen ANVISA benchmark. However, the first external
stress test showed that perfect internal refusal metrics overstated prospective
abstention behavior. Refusal calibration improved after an explicit
related-but-insufficient evidence rule, but residual boundary cases remain. The
study should be framed as technical validation using automated metrics,
AI-judge scoring, and AI-authored external stress tests, not expert consensus or
clinical/regulatory validation.

## Introduction

- Regulatory decision support requires grounded, citation-bearing answers.
- Legal and regulatory RAG differs from open-domain RAG because exact terms,
  article numbers, exceptions, and source provenance matter.
- Bilingual retrieval is challenging when source documents are Portuguese but
  users may ask in English.
- This project evaluates whether document-aware chunking and hybrid retrieval
  improve grounded ANVISA question answering.

## Materials And Methods

### Corpus

Describe the selected ANVISA documents and why they were included. State that
the corpus is limited to the indexed files and does not represent all ANVISA
regulations.

### Cleaning And Article-Aware Chunking

Describe:

- raw text extraction;
- cleaned text files;
- article parsing;
- one-article-per-chunk target;
- metadata fields: source document, regulation ID, article, citation label,
  topics;
- long-article splitting.

### Retrieval Pipeline

Describe:

- dense vector retrieval;
- BM25 keyword retrieval;
- reciprocal rank fusion;
- cross-encoder reranking;
- top-5 context selection;
- English glossary expansion for candidate retrieval;
- original English query plus compact Portuguese regulatory anchors used for
  selected reranking patterns.

### Generation Pipeline

Describe:

- generated answers use only the evaluated top-5 retrieved contexts;
- answer language follows question language;
- refusal rule when evidence is insufficient;
- exact article citation requirement;
- citation sanitization to retrieved article labels.

### Benchmark

Describe:

- 200 questions;
- 100 bilingual pairs;
- 70 Portuguese answerable;
- 70 English answerable;
- 20 multi-article or exception questions;
- 40 unanswerable/adversarial questions;
- frozen checksum;
- held-out split design.

### Evaluation Metrics

Retrieval:

- source hit rate;
- source MRR;
- article Recall@5;
- article Precision@5;
- article MRR@5;
- article nDCG@5;
- retrieved gold-term coverage.

Generation:

- answer term coverage;
- citation presence;
- article citation presence;
- retrieved-citation validity;
- refusal accuracy.

AI-judge answer quality:

- faithfulness;
- citation correctness;
- completeness;
- refusal correctness.

Uncertainty:

- pair-clustered bootstrap confidence intervals.

### AI-Judge Validation

State:

- generated answers were frozen before judging;
- the judge reconstructed retrieved evidence using the saved retrieval and
  rerank queries;
- one Gemini model was used as the automated judge;
- AI-judge scores are automated labels, not human expert validation;
- no inter-rater reliability or expert consensus claim is made.

## Results

### Retrieval Performance

Summarize Portuguese vs English retrieval performance.

### Generation Performance

Use the bilingual held-out table:

| Metric | English | Portuguese |
|---|---:|---:|
| Source hit rate | 1.000 | 1.000 |
| Article Recall@5 | 1.000 | 1.000 |
| Generated-answer term coverage | 0.849 | 0.828 |
| Citation presence | 1.000 | 1.000 |
| Article citation presence | 1.000 | 1.000 |
| Retrieved-citation validity | 1.000 | 1.000 |
| Refusal accuracy | 1.000 | 1.000 |

### AI-Judge Answer Quality

| Metric | English | Portuguese | Overall |
|---|---:|---:|---:|
| Judged rows | 75 | 75 | 150 |
| Faithfulness, answerable rows | 0.997 | 1.000 | 0.998 |
| Citation correctness, answerable rows | 1.000 | 1.000 | 1.000 |
| Completeness, answerable rows | 0.995 | 1.000 | 0.997 |
| Refusal correctness, unanswerable rows | 1.000 | 1.000 | 1.000 |
| Judge errors | 0 | 0 | 0 |

### External Stress Tests

| Evaluation layer | Questions | Main purpose | Key result |
|---|---:|---|---|
| Post-repair internal held-out benchmark | 150 | Final-system performance on curated benchmark | Near-perfect retrieval, citation validity, and AI-judge scores |
| External prospective stress test | 50 | Test whether internal perfection generalized | Answerable source hit 1.000, normalized article Recall@5 0.967, AI-judge completeness 0.943; refusal correctness 0.700 |
| Refusal-focused external test after prompt calibration | 30 | Test updated refusal behavior on new refusal-heavy questions | Unanswerable refusal correctness 0.944; no over-refusal on answerable controls |

The first external stress test is the key diagnostic check against overfitting:
it showed that the internal perfect refusal score did not fully generalize. The
second refusal-focused external test is post-calibration evidence that a stricter
related-but-insufficient evidence rule improved abstention behavior.

### Failure Analysis

Internal post-repair benchmark screening failures were mostly conservative
term-coverage flags: English had 1 generation-screening failure and Portuguese
had 3; the final AI judge did not identify remaining low-completeness cases.

The first external stress test changed the failure picture. Retrieval and
faithfulness remained strong, but refusal calibration failed on specific
unanswerable/adversarial questions where retrieved documents contained a nearby
general rule but not the exact requested fact. The clearest example was a SUSAR
question asking for the current electronic form model: the system answered with
the general electronic-notification requirement rather than refusing the absent
specific form model.

After prompt calibration, the second refusal-focused external test reduced this
failure pattern. The remaining refusal error involved a boundary case asking for
an exact penalty where the corpus contained a general enforcement provision but
not a case-specific penalty.

## Discussion

### Principal Findings

- Article-aware chunking and hybrid retrieval are useful for regulatory RAG.
- Exact article citation remains a critical bottleneck.
- English query handling improves substantially with expanded glossary retrieval,
  article-deduplicated reranking, neighbor-article expansion, and compact
  Portuguese reranking anchors.
- Refusal behavior is not solved by high internal benchmark scores alone;
  external stress testing is needed to expose related-but-insufficient evidence
  failures.
- A stricter refusal rule improved abstention on a second refusal-focused
  external test without causing broad over-refusal.

### Comparison With Prior Work

Add literature on RAG evaluation, legal/regulatory retrieval, citation
faithfulness, LLM-as-judge limitations, and human adjudication.

### Limitations

- limited corpus;
- benchmark and expected answers were authored by one investigator;
- final internal metrics include post-error-analysis targeted repairs on held-out rows;
- external stress tests were AI-authored and should be interpreted as automated
  prospective stress tests, not independent expert validation;
- the first external stress-test artifacts required recovery because the Codex
  output folder was moved and only a 40-row checkpoint remained; the missing
  refusal/adversarial block was regenerated once with the same frozen settings;
- no human expert adjudication;
- no independent expert consensus;
- AI judge may share biases with answer-generation models and should be treated
  as automated screening rather than ground truth;
- automated answer-term coverage is approximate;
- the remaining English automated generation-screening flag should be manually
  reviewed as a likely heuristic false positive;
- not clinical or legal advice validation.

### Future Work

- adjudicate conservative automated generation-screening flags separately from
  true answer-quality failures;
- add query translation or bilingual sparse index;
- evaluate additional rerankers;
- add independent expert review if available;
- expand corpus and benchmark;
- design more boundary-case refusal tests for questions where the corpus has a
  general enforcement rule but not the exact requested case-specific fact;
- compare multiple independent AI judges and calibrate against human review if
  resources become available.

## Conclusion

The system demonstrates a technically reproducible, article-aware RAG workflow
for selected ANVISA documents, with strong bilingual retrieval, citation
grounding, and answer faithfulness. External stress testing showed that refusal
calibration was the main residual weakness; a refusal-focused prompt update
substantially improved this behavior on a second external test. The project is
publication-ready as a technical feasibility manuscript if automated-only
validation, AI-authored external tests, artifact recovery, and residual boundary
failure cases are presented transparently.
