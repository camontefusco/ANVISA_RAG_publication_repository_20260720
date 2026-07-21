# Quality Review and Comparison with RAG Papers

Date: 20 July 2026

## Bottom line

The project is credible as a technical regulatory-science RAG evaluation, especially for Therapeutic Innovation & Regulatory Science. It is not ready to claim regulatory validation or deployment readiness. The strongest paper angle is not "high RAG scores." The stronger angle is a bilingual, article-level ANVISA case study showing why regulatory RAG evaluation must include citation checking, completeness, refusal behavior, and per-question error analysis.

## Current package status

Main manuscript:

- File: `manuscript_TIRS_reader_focused_20260720.md`
- Word count: 4,820 in the working manuscript; 4,291 in the text-only upload manuscript after removing table bodies and embedded figures.
- Scope: selected closed corpus of six ANVISA documents
- Main claim level: technical evaluation with audit trails

Supplementary package:

- Expanded methods and prompts are present.
- Per-question evaluation CSVs are present.
- Benchmark manifest and corpus audits are present.
- Development decision history is present.
- Figure package is present with a traceable source table and checksums.
- Supplementary tables are present for expanded decision history, representative outcomes, and evaluation-stage summary.

## Main strengths

1. The corpus boundary is explicit.

The system used a closed collection of six ANVISA documents. This is a strength for evaluation because unsupported questions have a defined correct behavior: refusal.

2. The unit of retrieval is appropriate for regulation.

Article-level chunking is more defensible than arbitrary chunks for regulatory resolutions because answers can be tied to a document and article.

3. The evaluation includes bilingual access.

The benchmark includes Portuguese and English questions. This adds value beyond many RAG papers that test only English or only one source-language setting.

4. The evaluation includes unanswerable and adversarial questions.

This is important. Many RAG demonstrations overestimate usefulness because they test only answerable questions.

5. The manuscript reports failure types.

The paper now discusses incomplete answers, false refusals, and refusal failures. This is aligned with how regulatory readers judge usefulness.

6. The new figure package is traceable.

Every plotted value is tied to `figure_metrics_source_table.csv`, with source file, filter, calculation, numerator sum, and denominator.

7. The real-world use boundary is explicit.

The Discussion now identifies likely users, development and dossier stages where the tool may be useful, and high-, moderate-, and low-confidence question types.

## Main weaknesses

1. No independent expert validation.

Automated judging is acceptable for a technical evaluation, but it is not equivalent to independent regulatory expert review. This must remain a limitation, not a buried detail.

2. The internal benchmark may be inflated.

The system was improved after error review. Internal post-repair values should be presented as development evidence, not independent validation.

3. External evaluation is still small.

The first AI-authored prospective stress test had 50 questions. The refusal-focused AI-authored prospective test had 30 questions. These are useful, but not large enough for strong generalization claims.

4. Development-stage figures compare different sets.

Figure 3A and Figure 3B show the project history, not paired repeated measurements on the same frozen question set. Captions must state this clearly.

5. No prospective user study.

The paper does not show whether regulatory-affairs users locate evidence faster, avoid errors, or trust the system appropriately.

6. Source corpus is narrow.

Six documents are enough for a case study, but not enough to claim broad ANVISA regulatory coverage.

## Comparison with relevant RAG papers

| Comparison point | Other RAG literature | Current ANVISA RAG project | Assessment |
|---|---|---|---|
| Regulatory-domain RAG | The FDA guidance RAG paper in TIRS tested a RAG application over clinically oriented FDA guidance documents and used SME scoring. It reported correct citation of the source document 89.2% of the time, but fully correct and complete answers only 69.6% of the time. | This project uses a smaller ANVISA corpus but tests article-level citation, bilingual access, refusal, and completeness. | Good fit for TIRS, but should be framed as complementary and smaller-scale. |
| Evaluation dimensions | RAGAs separates retrieval quality, faithfulness, and generation quality. | The project reports source hit, source MRR, normalized article recall, faithfulness, citation correctness, completeness, and refusal correctness. | Aligned with core RAG evaluation practice. |
| Automated judging | ARES uses automated RAG evaluation but still incorporates a small human-annotated set for prediction-powered inference. | This project uses AI judge only. | Acceptable if described as technical scoring, weaker than ARES-style validation. |
| Answer completeness | TREC RAG emphasizes nugget coverage and support, including whether answer facts are supported by cited passages. | This project evaluates completeness and reports omissions such as active-search obligation, ICH E2F condition, and deadline omissions. | Good alignment. Could be strengthened by adding explicit information-nugget scoring. |
| Citation support | TREC RAG evaluates sentence-level citation support. Medical citation-evaluation work also shows that references often fail to support all statements. | This project evaluates citation correctness and retrieved-citation validity, but not sentence-by-sentence support. | Good for a first study; sentence-level support would improve rigor. |
| Human evaluation | Healthcare RAG reviews generally treat human or clinician review as important for safety, usefulness, and domain appropriateness. | No independent human panel is available. | This is the largest validation gap. |
| Unanswerable questions | Many benchmark papers emphasize robustness and hallucination control, but not all domain papers test refusals. | This project directly tests refusal and shows calibration failure then repair. | Strong feature. This should be a central paper contribution. |

## How our results compare numerically

The FDA TIRS paper reported that its RAG application cited the correct source document 89.2% of the time, while all relevant information was present in 69.6% of answers and 13.4% contained incorrect information.

Our AI-authored prospective-test retrieval values are strong:

- Source hit: 1.000, n=40 answerable questions
- Source MRR: 0.988, n=40
- Normalized article Recall@5: 0.967, n=40
- Normalized article MRR@5: 0.912, n=40

Our answer-quality values should be interpreted more cautiously because they come from AI-judge scoring:

- AI-authored prospective-test completeness: 0.943, n=40 answerable questions
- AI-authored prospective-test refusal correctness: 0.700, n=10 unanswerable/adversarial questions
- Refusal-focused AI-authored refusal correctness after calibration: 0.944, n=18
- Answerable-control completeness after refusal tuning: 0.908, n=12

Interpretation: retrieval appears strong in the tested corpus. Refusal calibration was the main safety weakness. The stricter refusal prompt improved refusal behavior but may have slightly reduced completeness on answerable controls. That trade-off is scientifically useful and should be shown, not hidden.

## Publication readiness

Ready enough for serious manuscript development:

- Yes, as a technical evaluation / case study.
- Yes, for a TIRS-style regulatory science audience.
- Yes, if limitations remain explicit.

Not ready for stronger claims:

- Not ready to claim regulatory decision support.
- Not ready to claim broad ANVISA coverage.
- Not ready to claim expert-validated accuracy.
- Not ready to claim generalizable improvement from development-stage figures.

## Most important remaining checks before submission

1. Confirm journal table placement during final formatting.

The main manuscript now keeps three compact tables and moves the expanded development and evaluation-stage material to Supplementary Tables S1-S3. In the rendered DOCX, Tables 1 and 3 continue across pages without clipping. Final journal formatting may require repeated table headers.

2. Add one sentence in Results that explicitly compares with the FDA TIRS paper.

Suggested wording:

"Compared with the prior TIRS evaluation of generative AI search over FDA guidance documents, the present study used a smaller corpus but added bilingual ANVISA questions, article-level evidence labels, and explicit refusal testing for questions outside the indexed documents."

3. Add one paragraph on AI-judge limits.

Suggested wording:

"The automated judge reduced the burden of scoring a large bilingual benchmark, but it was not treated as an independent regulatory expert. Scores should therefore be interpreted as structured technical evaluation with audit trails. The per-question outputs are provided so that readers can inspect disagreements, omissions, and refusal behavior."

4. Add an information-nugget table for selected examples.

For 8-12 representative questions, list the expected material elements and mark which were present, missing, or unsupported. This would make the completeness analysis more transparent and closer to TREC-style nugget evaluation.

5. Keep the per-question CSVs in supplementary material.

This is essential because the paper relies on AI judging. Auditability partly compensates for the absence of two expert reviewers.

## Suggested figure set

Main manuscript:

- Figure 1: closed-corpus RAG workflow and evaluation boundary.
- Figure 2: representative answer/failure examples or question-category/error map.
- Figure 3: targeted weak-point repairs from real development metrics.

Supplement:

- Figure S1: AI-authored prospective-test retrieval validity.
- Figure S2: 200-question benchmark composition.
- Figure S3: article-aware chunk distribution.
- Full source table for all plotted values.

## Decision

The manuscript is close to submission-quality as a regulatory RAG technical evaluation. The remaining work is not more model tuning. The remaining work is claim control, clearer comparison with prior RAG evaluation papers, and stronger transparency around AI-judge-only validation.

## Sources used for comparison

1. Proestel S, Jeng LJB, Smith C, et al. Semantic Search of FDA Guidance Documents Using Generative AI. Therapeutic Innovation & Regulatory Science. 2025;59:1148-1159. doi:10.1007/s43441-025-00798-8. https://pmc.ncbi.nlm.nih.gov/articles/PMC12446095/
2. Es S, James J, Espinosa Anke L, Schockaert S. RAGAs: Automated Evaluation of Retrieval Augmented Generation. EACL 2024. doi:10.18653/v1/2024.eacl-demo.16. https://aclanthology.org/2024.eacl-demo.16/
3. Saad-Falcon J, Khattab O, Potts C, Zaharia M. ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems. NAACL 2024. doi:10.18653/v1/2024.naacl-long.20. https://aclanthology.org/2024.naacl-long.20/
4. TREC 2024 RAG Evaluation Overview. https://trec-rag.github.io/annoucements/evaluation/
5. TREC 2024 RAG Track Guidelines. https://trec-rag.github.io/annoucements/2024-track-guidelines/
6. Retrieval augmented generation for large language models in healthcare: A systematic review. PLOS Digital Health. https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0000877
7. Guinet G, Omidvar-Tehrani B, Deoras A, Callot L. Automated Evaluation of Retrieval-Augmented Language Models with Task-Specific Exam Generation. ICML 2024. https://proceedings.mlr.press/v235/guinet24a.html
