Bilingual Article-Aware Retrieval-Augmented Generation for ANVISA Regulatory Document Interpretation

Authors: Carlos Victor Montefusco-Pereira1*, Howard Lopes Ribeiro Junior2

1 Independent Researcher in Data Science and Artificial Intelligence in Industrial Pharmaceutics, Berlin, Germany

2 Center for Research and Drug Development (NPDM), Federal University of Ceara, Fortaleza 60430-275, Brazil; Post-Graduate Program in Pathology, Federal University of Ceara, Fortaleza, Brazil; Post-Graduate Program in Translational Medicine, Federal University of Ceara, Fortaleza, Brazil

ORCID: Carlos Victor Montefusco-Pereira, 0000-0003-4167-4653; Howard Lopes Ribeiro Junior, 0000-0003-2431-4779

Corresponding author: Carlos Victor Montefusco-Pereira. Friedrich-Wilhelm 28, 12103 Berlin, Germany. Email: cmontefusco@gmail.com. Phone: +49 15168108538.

Institutional email addresses: cmontefusco@gmail.com (C.V.M.-P.); howard@ufc.br (H.L.R.J.)

Keywords: regulatory science; retrieval-augmented generation; ANVISA; pharmaceutical regulation; bilingual information retrieval; large language models

Abstract

Background. Regulatory agencies publish long, terminology-dense documents that are difficult to search across languages. Retrieval-augmented generation may improve access, but regulatory use requires source traceability and refusal when evidence is insufficient.

Objective. To develop and technically evaluate a bilingual Portuguese-English retrieval-augmented generation system for selected ANVISA pharmaceutical and health-product regulatory documents.

Methods. Regulatory files were cleaned and indexed as article-aware chunks with document, article, and citation metadata. Retrieval combined dense search, BM25, reciprocal rank fusion, reranking, and answer generation from the top five contexts. English questions were expanded with a fixed Portuguese-English glossary. A 200-question bilingual benchmark tested answerable, exception, multi-article, unanswerable, and adversarial questions. Automated evaluation measured retrieval, citation validity, completeness, faithfulness, and refusal behavior.

Results. The final index contained 382 articles and 481 chunks from six ANVISA documents. On the post-repair internal held-out benchmark, article Recall@5 was 1.000 in both languages. AI-judge completeness was 0.995 in English and 1.000 in Portuguese. A 50-question external stress test showed article Recall@5 of 0.967 and completeness of 0.943, but refusal correctness was 0.700. After refusal calibration, a 30-question refusal-focused test achieved refusal correctness of 0.944, with no over-refusal on answerable controls.

Conclusion. Article-aware indexing, hybrid retrieval, reranking, query expansion, and refusal rules supported technical validation of a bilingual ANVISA regulatory-document RAG system. The findings do not establish regulatory advice.

Introduction

Regulatory agencies publish information that guides pharmaceutical and health-product development, submission, monitoring, and post-authorization obligations. These materials are often long, article-structured, and dependent on exact terminology. A user may need to locate a specific article, distinguish a general rule from an exception, or determine whether a requirement applies to a clinical trial, biological product, medical device, or pharmacovigilance obligation. In Brazil, many health-product regulatory documents are published in Portuguese. This creates a practical barrier for international scientists, sponsors, and companies that need to work with Portuguese source material but may ask questions in English.

The information-access problem is practical rather than theoretical. Regulatory staff and scientists often search across several documents to answer a narrow operational question, such as which documents must accompany a submission, whether a category is excluded from a rule, or what obligation applies after a trial event. In these cases, a document-level search result is not enough. The user needs the article that supports the answer, and the system must separate an answer that is explicitly present from a related passage that only discusses the same topic. This distinction is central for regulatory use because nearby but incomplete evidence can produce a plausible answer that is still unsupported.

Retrieval-augmented generation (RAG) combines document retrieval with language-model generation and has been proposed as a way to reduce unsupported responses in knowledge-intensive question answering [1]. In regulatory use, however, the question is not only whether an answer is fluent. A useful system must retrieve the correct source document, preserve article-level provenance, cite the evidence used, and refuse questions that cannot be answered from the indexed corpus. These requirements are stricter than ordinary chatbot behavior because unsupported answers can mislead users who are trying to interpret regulatory obligations.

Recent work in Therapeutic Innovation & Regulatory Science evaluated a RAG-based generative AI tool for semantic search of FDA guidance documents [2]. That study showed potential for accelerating access to guidance information, but also reported incomplete answers and answers containing incorrect information. The authors concluded that correct source citation may help users locate relevant documents, while further refinement of chunking, embeddings, prompt engineering, and validation would be needed before such systems could be relied on to answer regulatory questions. This prior work provides a relevant regulatory-science precedent and highlights the need for task-specific validation.

The present study evaluates a bilingual RAG system for selected ANVISA regulatory documents. The contribution is technical and bounded. The system was designed for a closed document collection, with article-aware chunking, hybrid lexical and dense retrieval, cross-encoder reranking, Portuguese-English query expansion, citation-constrained answer generation, and refusal behavior when evidence was insufficient. The objective was to test whether this design could support article-level retrieval and answer generation for Portuguese and English questions while maintaining transparent limits.

The study also records the development decisions that led to the final pipeline. This is relevant because RAG performance can look better than it is when evaluation follows repeated prompt and retrieval adjustments. For that reason, the manuscript separates development findings from external testing. Internal results are reported as post-repair technical checks. External results are used to assess whether the repaired system remained reliable on questions not used to guide the preceding changes.

Materials and Methods

Study design

This was a technical validation study of a closed-corpus RAG system. The project followed a staged development and validation sequence. Initial testing identified environment, corpus-cleaning, retrieval, answer-completeness, citation, and refusal failures. Repairs were made using development data and followed by re-evaluation. Because internal held-out metrics became very high after targeted repairs, a prospective external stress test was run once before further tuning. That test showed strong answerable-question performance but weaker refusal behavior. Refusal calibration was then updated using a separate development set, and a new refusal-focused external test was run. The final pipeline was frozen after this step.

The staged design was chosen to make the role of each dataset explicit. Development data were used to diagnose failures and adjust the pipeline. Held-out internal data were used to check whether the final internal benchmark was passed after those repairs. External tests were used to examine generalization beyond the internal benchmark. The external stress test was intentionally run before tuning from its errors. When that test identified refusal as the main remaining weakness, the refusal prompt was adjusted using separate development examples, and a new refusal-focused test was used to evaluate the repair.

Corpus

The corpus consisted of six selected ANVISA regulatory text files relevant to clinical trials, biological products, medical devices, pharmacovigilance, and reliance-based clinical-trial review [11-16]. The indexed corpus was treated as closed. The system was not allowed to answer from current web pages, private submission systems, forms, fee schedules, unpublished information, or documents outside the index.

The corpus was selected to cover several common regulatory-affairs domains rather than a single narrow document family. It included clinical-trial regulations, biological-product registration material, medical-device risk classification material, and pharmacovigilance requirements. This selection allowed the benchmark to include both document-specific questions and questions that required the system to distinguish between related regulatory domains. The system was not designed to determine whether the selected documents were the current complete legal basis for any real submission.

Each source file was checked against its document identifier and topic before final indexing. This step was added after development review showed that file names alone could be misleading. The final corpus table therefore reports the official regulation and main topic rather than local file names. The check was important for reproducibility because an evaluation question may be counted as correct only if the retrieved document and article correspond to the intended regulation. It also prevents a common error in regulatory RAG projects: treating an inherited text file as reliable metadata without verifying that the document content, document number, and study topic agree.

Table 1. Indexed ANVISA corpus.

| Regulation | Main topic | Cleaned characters | Chunks |
|---|---:|---:|---:|
| IN 338/2024: optimized review, AREE, reliance, and risk/complexity criteria [11] | Reliance and clinical-trial petition review | 14,450 | 19 |
| RDC 406/2020: good pharmacovigilance practices for human medicines [12] | Pharmacovigilance | 39,879 | 61 |
| RDC 55/2010: registration of new biological products and biological products [13] | Biological products | 43,062 | 69 |
| RDC 751/2022: medical-device risk classification, notification, registration, labelling, and instructions for use [14] | Medical devices | 80,024 | 102 |
| RDC 945/2024: clinical trials for later medicine registration [15] | Clinical trials | 71,857 | 123 |
| RDC 9/2015: clinical trials with medicines in Brazil [16] | Clinical trials | 53,346 | 107 |

Text cleaning and article-aware chunking

Raw files contained a mix of plain text and HTML-derived material. The cleaning pipeline removed markup and boilerplate where possible, normalized text, and saved cleaned files before indexing. The cleaned corpus was then segmented using article-aware rules. The target unit was one regulatory article per chunk, with nearby section or chapter headings preserved when available. Long articles were split into smaller subchunks while retaining the same article citation metadata.

Article-aware chunking was used because it preserves the unit that a regulatory reader expects to verify. A fixed token window may retrieve words from the correct document while joining unrelated articles or separating a requirement from its exception. That behavior is difficult to audit and can weaken citation correctness. The article-level approach made the retrieved evidence easier to inspect and allowed article Recall@5 and article citation validity to be measured directly.

The final article-aware index used `sentence-transformers/all-MiniLM-L6-v2` embeddings with maximum length 512. The chunking configuration used a maximum of 500 tokens for single-article chunks. Long articles were split into 400-token chunks with 60-token overlap. The final index contained 382 articles and 481 chunks. Of these, 359 articles were represented as a single chunk and 23 long articles were split into multiple chunks. Median chunk length was 155 tokens, maximum length was 503 tokens, and no chunk exceeded 700 tokens.

Retrieval architecture

The retrieval pipeline used four stages. First, dense vector retrieval selected semantic candidates. Second, BM25 selected lexical candidates over passage text and regulatory metadata. Third, reciprocal rank fusion merged dense and BM25 results. Fourth, a multilingual cross-encoder reranker sorted the fused candidates. The system retrieved 100 dense candidates and 100 BM25 candidates, retained 100 fused candidates, and passed the top five reranked contexts to answer generation. Reciprocal rank fusion used a smoothing constant of 60. The reranker was `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`.

Hybrid retrieval was used because regulatory questions often depend on exact terms, acronyms, document numbers, and article labels. Examples include DDCM, RDC 945, IN 338, Art. 33, sponsor, clinical trial, biological product, medical device, and pharmacovigilance. Dense retrieval can match meaning across paraphrases, but lexical retrieval is important when a specific regulatory term or document number determines the correct answer.

English query expansion

English questions were expanded for retrieval using a fixed Portuguese-English regulatory glossary. The original English question was preserved for user intent and answer language. Portuguese retrieval anchors were added only to improve matching against Portuguese source documents. The glossary preserved terms such as clinical trial/ensaio clinico, sponsor/patrocinador, biological product/produto biologico, medical device/dispositivo medico, and pharmacovigilance/farmacovigilancia. Query expansion was evaluated during development with and without rewrite to confirm that it improved English retrieval.

The rewrite step was deterministic and conservative. It was not used to broaden the question or add regulatory facts. Its purpose was to reduce a known mismatch between English user wording and Portuguese source wording. This distinction matters because a free generative rewrite could change the legal meaning of a question. The retrieval query could include Portuguese anchors, but the generation step still received the original user question and was required to answer in the same language as the question.

Answer generation and refusal policy

Generated answers were constrained to the top five retrieved contexts. The answer language followed the user question. The prompt required every material statement to cite the retrieved source document and article using the stored citation label. The prompt also prohibited invented document numbers, articles, sections, deadlines, or requirements.

A strict refusal rule was added after failure analysis. If retrieved context was related but did not contain the specific requested answer, the system was instructed to return a refusal sentence without citation. English refusals used: "The retrieved documents do not provide enough information to answer." Portuguese refusals used: "Os documentos recuperados nao fornecem informacao suficiente para responder." The rule explicitly covered current forms, exact URLs, current fees, private contract terms, company-specific submission status, personal contact information, market prices, reimbursement, taxes, patents, future approvals, and advice not stated in the retrieved regulatory text.

Answer generation used `models/gemini-flash-lite-latest` with temperature 0.2. Query rewriting used the same model identifier with temperature 0.0. Prompts and retrieval traces were saved with the evaluation outputs.

Benchmark

The main benchmark contained 200 bilingual, article-level questions: 70 Portuguese answerable questions, 70 English answerable questions, 20 multi-article or exception questions, and 40 unanswerable or adversarial questions. Questions were designed to test source retrieval, article retrieval, completeness, citation behavior, and refusal behavior. The held-out evaluation used 75 English rows and 75 Portuguese rows. Benchmark manifests and checksums were saved to support reproducibility.

Answerable questions were linked to expected source documents, article labels, and key terms. English and Portuguese questions were paired where possible so that language effects could be examined without treating translated counterparts as independent facts. Multi-article and exception questions were included because regulatory interpretation often depends on a rule and its qualifying condition. Unanswerable and adversarial questions were included because a system that always answers can score well on answerable questions while remaining unsafe for regulatory use.

The benchmark was built as an article-level gold set rather than a free-text answer-only set. For answerable rows, the primary label was the article or articles expected to support the answer. Key terms were used as secondary checks for answer completeness, not as a substitute for article retrieval. For unanswerable rows, the expected behavior was refusal unless the retrieved corpus contained the specific requested fact. This design made the benchmark more conservative than simple semantic similarity scoring because a plausible answer without the expected article support was not sufficient.

Because the project was conducted without a two-expert panel, benchmark construction used explicit traceability controls. Each question was tied to source metadata, expected article labels, and expected terms, and the generated outputs were preserved for audit. This does not replace independent expert validation. It is a reproducibility strategy for a solo technical study: readers can inspect whether the question, gold article, retrieved evidence, answer, and automated score are aligned.

External testing used two additional benchmarks. The first was a 50-question prospective stress test with 25 bilingual pairs, including 40 answerable and 10 unanswerable or adversarial questions. The second was a 30-question refusal-focused external test with 18 unanswerable or current-specific questions and 12 answerable controls.

Evaluation metrics

Retrieval was evaluated with source hit rate, source mean reciprocal rank (MRR), article Recall@5, article Precision@5, article MRR@5, article nDCG@5, and retrieved gold-term coverage. Generation was evaluated with answer gold-term coverage, citation presence, article citation presence, retrieved-citation validity, and refusal accuracy. Automated answer-quality judging scored faithfulness, citation correctness, completeness, and refusal correctness.

Pair-clustered bootstrap confidence intervals were used where applicable so bilingual counterpart questions were not treated as independent observations. For the external prospective test, normalized article metrics were used because article labels in the external gold file used a different format from the internal runner fields.

Automated judging

Generated answers and retrieval traces were frozen before judging. The automated judge evaluated each answer against the saved retrieved evidence and did not regenerate the answer. Judge outputs were treated as automated labels, not human expert validation. No inter-rater reliability statistic was calculated because there was no independent second human rater. Cohen's kappa was therefore not applicable.

The judging rubric separated four dimensions. Faithfulness assessed whether the answer was supported by the retrieved evidence. Citation correctness assessed whether cited documents and articles matched the evidence used. Completeness assessed whether the answer covered the material parts of the question when the evidence was sufficient. Refusal correctness assessed whether the system refused when the retrieved corpus did not contain the answer and answered when sufficient evidence was present.

The automated judge used `models/gemini-flash-lite-latest` with temperature 0.0 and returned JSON scores from 0 to 1. The same model family was used for answer generation and automated judging, which may increase shared-model bias. This was handled by limiting the claim to automated technical evaluation and by preserving retrieved contexts, expected answers, generated answers, judge prompts, and judge outputs for audit.

Ethics and regulatory status

The study used public regulatory text files and generated benchmark questions. It did not involve human participants, patient data, animal studies, or a clinical trial. No ANVISA, regulatory authority, or journal endorsement is implied. The system is not intended to provide legal, clinical, or regulatory advice.

Results

Corpus and index characteristics

Cleaning reduced raw source files from large HTML-derived text exports to structured cleaned text files suitable for article-level indexing. The final index contained 382 detected articles and 481 chunks. Most articles were represented by one chunk; long articles were split while preserving article metadata. Chunk counts varied by source document, from 19 chunks for IN 338/2024 to 123 chunks for RDC 945/2024.

The audit confirmed that all required vector-store files were present and that 481 chunks contained article-aware metadata markers. The cleaned-data audit also showed that five source files came from HTML-derived exports and one was plain text. This supported the decision to report cleaning as a separate Methods step rather than treating the corpus as already normalized input.

Internal held-out benchmark before final repairs

The first frozen held-out AI-judge evaluation included 150 rows, with 120 answerable and 30 unanswerable questions. Overall faithfulness on answerable rows was 0.997, citation correctness was 0.965, completeness was 0.807, and refusal correctness on unanswerable rows was 1.000. Language-stratified results showed a clear weakness in English completeness. English completeness was 0.645, while Portuguese completeness was 0.970. This result led to targeted review of English retrieval and answer completeness.

The English completeness gap was important because the source corpus was primarily Portuguese. Failure review showed that some English answers retrieved the correct document but omitted required list elements, conditions, or exceptions. This pattern suggested that the main problem was not only source retrieval. It also involved retrieval of the complete article context and answer prompting that required all material parts of a question to be addressed.

Post-repair internal held-out benchmark

After retrieval and completeness repairs, the English held-out run included 75 rows, with 60 answerable and 15 unanswerable questions. Operational source hit rate after reranking was 1.000, source MRR was 0.950, article Recall@5 was 1.000, article MRR@5 was 0.898, article nDCG@5 was 0.924, and retrieved gold-term coverage was 0.994. Answer gold-term coverage was 0.849, citation presence was 1.000, article citation presence was 1.000, retrieved-citation validity was 1.000, and refusal accuracy was 1.000. AI-judge faithfulness was 0.997, citation correctness was 0.983, completeness was 0.995, and refusal correctness was 1.000.

The final Portuguese held-out run included 75 rows, with 60 answerable and 15 unanswerable questions. AI-judge faithfulness, citation correctness, completeness, and refusal correctness were all 1.000. These values should be interpreted cautiously. They were obtained after targeted repairs and therefore show that the final system passed the curated internal benchmark, not that general regulatory performance is perfect.

Table 2. Main post-repair internal held-out results.

| Metric | English | Portuguese |
|---|---:|---:|
| Source hit after reranking | 1.000 | 1.000 |
| Article Recall@5 | 1.000 | 1.000 |
| Answer term coverage | 0.849 | 0.828 |
| Retrieved-citation validity | 1.000 | 1.000 |
| Refusal accuracy | 1.000 | 1.000 |
| AI-judge faithfulness | 0.997 | 1.000 |
| AI-judge citation correctness | 0.983 | 1.000 |
| AI-judge completeness | 0.995 | 1.000 |
| AI-judge refusal correctness | 1.000 | 1.000 |

Prospective external stress test

Because the internal metrics were high after repair, a 50-question prospective external stress test was run once before further tuning. The test contained 25 bilingual pairs, 40 answerable questions, and 10 unanswerable or adversarial questions. During artifact recovery, 40 preserved rows were combined with 10 regenerated unanswerable/adversarial rows using the same frozen settings. No retrieval, prompt, judge, threshold, or benchmark changes were made during recovery.

The external test supported answerable-question performance but exposed refusal weakness. Normalized article Recall@5 on answerable questions was 0.967 and normalized article MRR@5 was 0.912. Retrieved term coverage was 0.806, answer term coverage was 0.761, citation presence was 0.975, article citation presence was 0.975, and retrieved-citation validity was 0.975. AI-judge faithfulness was 1.000, citation correctness was 0.975, and completeness was 0.943. Refusal detection on unanswerable questions was 0.600 and AI-judge refusal correctness was 0.700.

By language, normalized article Recall@5 was 0.950 for English and 0.983 for Portuguese. AI-judge completeness was 0.930 for English and 0.955 for Portuguese. Refusal correctness was 0.800 for English and 0.600 for Portuguese. Error review showed that the system sometimes answered with nearby general rules when the corpus did not contain the exact requested fact.

The external stress test therefore changed the main risk assessment. Before this test, the project appeared to be limited mainly by answer completeness. After this test, the main weakness was refusal calibration. This distinction matters for publication because completeness errors and refusal errors have different implications. An incomplete answer may omit a relevant condition, while a refusal error may present an unsupported claim as if it were grounded in the corpus.

Refusal-focused external test

After the first external test, refusal calibration was repaired using a separate development set. A new 30-question refusal-focused external test was then run. This test included 18 unanswerable or current-specific questions and 12 answerable controls.

On answerable controls, operational source hit after reranking was 1.000 and source MRR was 1.000. Retrieved gold-term coverage was 0.799. Citation presence, article citation presence, and retrieved-citation validity were all 1.000. AI-judge faithfulness and citation correctness were 1.000. Completeness was 0.908.

On unanswerable questions, refusal accuracy was 0.944, with a 95% confidence interval of 0.833 to 1.000. AI-judge refusal correctness was also 0.944. No over-refusal occurred on answerable controls. The remaining boundary case involved questions where the retrieved corpus provided a general enforcement consequence but did not provide the exact requested penalty.

Table 3. External testing results.

| Metric | Prospective stress test | Refusal-focused external test |
|---|---:|---:|
| Questions | 50 | 30 |
| Answerable questions | 40 | 12 |
| Unanswerable/adversarial questions | 10 | 18 |
| Normalized article Recall@5, answerable | 0.967 | Not applicable |
| Retrieved-citation validity, answerable | 0.975 | 1.000 |
| AI-judge faithfulness, answerable | 1.000 | 1.000 |
| AI-judge citation correctness, answerable | 0.975 | 1.000 |
| AI-judge completeness, answerable | 0.943 | 0.908 |
| AI-judge refusal correctness, unanswerable | 0.700 | 0.944 |
| Over-refusal on answerable controls | Not reported | 0.000 |

Article-level metrics were not reported for the refusal-focused external test because its article labels were not normalized for that analysis; source retrieval and answer-quality metrics were retained.

Discussion

Principal findings

This study developed and evaluated a bilingual article-aware RAG system for selected ANVISA regulatory documents. The final pipeline performed well on article-level retrieval, citation validity, answer faithfulness, completeness, and refusal behavior in internal testing. More importantly, external testing changed the interpretation of the project. The first prospective external test confirmed strong answerable-question behavior but showed that refusal calibration remained the main weakness. After a separate refusal-development repair, the refusal-focused external test showed improved refusal correctness without over-refusal on answerable controls.

The main result is therefore not the presence of 1.000 internal scores. Those scores are useful only as evidence that the repaired system passed the curated internal benchmark. The more credible finding is the staged validation pattern: internal repair, untouched external stress testing, documented refusal failure, separate calibration, and a new external refusal test.

This interpretation is also more useful for readers who want to build similar systems. The development history shows that high retrieval scores do not remove the need to test answer completeness and refusal separately. It also shows that source citation alone is not sufficient. A system may cite a real article and still answer a more specific question than the article supports.

Comparison with prior regulatory RAG work

The closest published comparator is the TIRS study of semantic search of FDA guidance documents using generative AI [2]. That study evaluated a RAG application for FDA guidance questions and reported that correct source citation may help users find relevant guidance, but incorrect or incomplete answers remained a concern. The present study is aligned with that conclusion. It treats source and article citation as a primary endpoint and evaluates refusal behavior as a separate safety boundary.

This study differs in three main ways. First, the corpus was based on selected ANVISA regulatory documents rather than FDA guidance documents. Second, the evaluation was bilingual, with English questions over Portuguese source material. Third, the system was designed around article-level legal-regulatory structure rather than generic passage chunks. These differences make the work relevant to international regulatory affairs settings where users may need to search non-English health-authority documents while preserving source traceability.

The results also suggest a different evaluation emphasis for regulatory RAG than for general question answering. Correctness should be divided into retrieval correctness, citation correctness, answer completeness, and refusal correctness. These endpoints are related but not interchangeable. A system can retrieve the correct document but miss the article, cite the correct article but omit a condition, or retrieve related evidence and still need to refuse.

Regulatory-science implications

The results support a limited use case: technical support for locating and summarizing evidence within a closed regulatory corpus. In that role, the system may help users identify relevant ANVISA documents and articles faster than manual search alone. The strongest design features for this use case were article-aware chunking, hybrid retrieval, reranking, bilingual query expansion, and citation-constrained generation.

The results do not support unsupervised regulatory decision-making. A RAG system can retrieve and summarize indexed text, but it does not determine current legal status, apply regulatory judgment to a full product dossier, or replace professional review. The closed-corpus design is important. Questions about current forms, fees, submission portals, private company status, future regulatory changes, or documents outside the index should be refused.

The most realistic near-term use is assisted navigation of a defined document collection. In that setting, the user remains responsible for checking the cited article and applying professional judgment. The system can reduce search burden by ranking likely evidence and drafting a concise answer, but the citation remains the control point. This is why article-level citation was treated as a design requirement rather than a cosmetic addition.

Refusal calibration

Refusal behavior was the main safety boundary. The first external test showed that the system sometimes treated related context as sufficient even when the exact requested fact was absent. This is a common regulatory risk. A nearby article may discuss the same topic but not answer the specific question. In such cases, a fluent answer can be more harmful than a refusal because it may appear authoritative.

The refusal-focused repair improved refusal correctness from 0.700 in the first external stress test to 0.944 in the second refusal-focused external test. The repair also preserved answerability, with no over-refusal on answerable controls. This does not prove that refusal is solved. It shows that refusal should be evaluated separately from answer correctness and should remain a monitored endpoint in future work.

Automated evaluation

The project used an AI judge because a two-expert panel was not available. This choice makes the study feasible as a solo technical validation project, but it limits the claim level. Automated judging can consistently apply a rubric for faithfulness, citation correctness, completeness, and refusal correctness. It can also score larger benchmarks than a single manual reviewer can practically assess. However, it may miss domain-specific legal nuance, may favor answers that match its preferred style, and cannot establish expert consensus.

For that reason, the manuscript should describe AI-judge scores as automated technical labels. It should not report inter-rater reliability, expert agreement, or regulatory correctness. Future validation should compare automated scores against independent regulatory reviewers and include disagreement analysis.

The practical value of the AI judge in this study was failure detection, not proof of regulatory truth. It helped identify repeated patterns, especially incomplete English answers and over-answering of unanswerable questions. Those patterns then guided separate repairs and external tests. The final interpretation therefore depends on the full audit trail: retrieved contexts, cited articles, refusal decisions, and preserved outputs, rather than on the judge score alone.

Limitations

The study has several limitations. First, the corpus was closed and selected. It does not represent all ANVISA regulations, current web pages, forms, fees, submission systems, or future regulatory updates. Second, the benchmark was created without an independent regulatory expert panel. Third, answer-quality scoring used one automated judge rather than multiple human reviewers. Fourth, internal results may be inflated because the pipeline was repaired after error analysis. Fifth, the first external stress test required artifact recovery after output files were moved; the recovery preserved settings, but the caveat should be reported. Sixth, the system may still fail on boundary questions where the retrieved text is related but incomplete. Seventh, the system was tested as a technical prototype, not as a deployed regulatory affairs tool.

Future work

Future work should expand the corpus, add version tracking for regulatory updates, test additional languages, and compare AI-judge scores with independent regulatory reviewers. External benchmarks should be authored by people not involved in system development. Evaluation should include time-to-answer studies, user trust calibration, and controlled comparisons against keyword search. Refusal testing should remain separate from ordinary answerable-question testing.

Future studies should also test alternative retrieval and evaluation designs. Larger multilingual embedding models, stronger rerankers, and document-structure parsers may improve retrieval of long articles and annexes. Human evaluation could use blinded article-level answer keys and separate scoring for legal sufficiency, practical usefulness, and risk of misleading interpretation. A prospective study with regulatory-affairs users could measure whether cited RAG answers reduce time to locate evidence without increasing overconfidence.

Conclusion

A bilingual article-aware RAG pipeline can retrieve and summarize selected ANVISA regulatory documents with source and article citation when the corpus contains the answer. Hybrid retrieval, reranking, Portuguese-English query expansion, citation constraints, and refusal calibration were all needed to reach stable technical performance. The system should be presented as a regulatory information-access prototype with transparent limits, not as regulatory advice or expert validation.

Funding

The authors received no specific funding for this work.

Conflict of Interest

The authors declare no competing financial interests.

Author Contributions

C.V.M.-P. conceived and designed the study, developed the software pipeline, prepared the corpus, constructed the benchmark, performed the analyses, interpreted the results, and drafted the manuscript. H.L.R.J. contributed to the regulatory and pharmaceutical framing, interpretation of results, and critical revision of the manuscript. Both authors approved the final manuscript and agree to be accountable for the work.

Data Availability

The cleaned corpus files, benchmark manifests, evaluation outputs, prompts, and code used for the technical validation are available in the project repository or can be provided as supplementary material, subject to any redistribution limits for source regulatory text. Benchmark and output files were saved with manifests and checksums to support reproducibility.

Ethics Approval

Ethics approval was not required because the study used public regulatory documents and generated benchmark questions. No human participants, patient data, animal data, or clinical trial data were used.

Clinical Trial Registration

Not applicable.

References

1. Lewis P, Perez E, Piktus A, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems. 2020;33:9459-9474.

2. Proestel S, Jeng LJB, Smith C, et al. Semantic Search of FDA Guidance Documents Using Generative AI. Ther Innov Regul Sci. 2025;59:1148-1159. doi:10.1007/s43441-025-00798-8.

3. Robertson S, Zaragoza H. The Probabilistic Relevance Framework: BM25 and Beyond. Found Trends Inf Retr. 2009;3:333-389. doi:10.1561/1500000019.

4. Karpukhin V, Oguz B, Min S, et al. Dense Passage Retrieval for Open-Domain Question Answering. Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing. 2020:6769-6781. doi:10.18653/v1/2020.emnlp-main.550.

5. Nogueira R, Cho K. Passage Re-ranking with BERT. arXiv. 2019. doi:10.48550/arXiv.1901.04085.

6. Gao Y, Xiong Y, Gao X, et al. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv. 2023. doi:10.48550/arXiv.2312.10997.

7. Es S, James J, Espinosa-Anke L, Schockaert S. RAGAS: Automated Evaluation of Retrieval Augmented Generation. arXiv. 2023. doi:10.48550/arXiv.2309.15217.

8. Zheng L, Chiang WL, Sheng Y, et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. Advances in Neural Information Processing Systems. 2023;36.

9. Guha N, Nyarko J, Ho DE, et al. LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models. Advances in Neural Information Processing Systems. 2023;36.

10. Chalkidis I, Fergadiotis M, Malakasiotis P, Aletras N, Androutsopoulos I. LEGAL-BERT: The Muppets straight out of Law School. Findings of the Association for Computational Linguistics: EMNLP 2020. 2020:2898-2904. doi:10.18653/v1/2020.findings-emnlp.261.

11. Agencia Nacional de Vigilancia Sanitaria. Instrucao Normativa - IN No. 338, de 29 de novembro de 2024. Establishes the list of equivalent foreign regulatory authorities and criteria for optimized review under RDC 945/2024. AnvisaLegis. https://anvisalegis.datalegis.net/action/UrlPublicasAction.php?acao=abrirAtoPublico&cod_menu=8542&cod_modulo=310&num_ato=00000338&seq_ato=000&sgl_orgao=DC%2FANVISA%2FMS&sgl_tipo=INM&vlr_ano=2024. Accessed 19 July 2026.

12. Agencia Nacional de Vigilancia Sanitaria. Resolucao de Diretoria Colegiada - RDC No. 406, de 22 de julho de 2020. Good pharmacovigilance practices for holders of human medicine registrations. AnvisaLegis. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=8542&cod_modulo=310&link=S&numeroAto=00000406&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2020. Accessed 19 July 2026.

13. Agencia Nacional de Vigilancia Sanitaria. Resolucao - RDC No. 55, de 16 de dezembro de 2010. Registration of new biological products and biological products. AnvisaLegis. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&codTipo=&cod_menu=1696&cod_modulo=134&desItem=&desItemFim=&numeroAto=00000055&orgao=RDC%2FDC%2FANVISA%2FMS&pesquisa=true&seqAto=000&tipo=RDC&valorAno=2010. Accessed 19 July 2026.

14. Agencia Nacional de Vigilancia Sanitaria. Resolucao - RDC No. 751, de 15 de setembro de 2022. Medical-device risk classification, notification and registration regimes, labelling, and instructions for use. AnvisaLegis. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=1696&cod_modulo=134&numeroAto=00000751&orgao=RDC%2FDC%2FANVISA%2FMS&pesquisa=true&seqAto=000&tipo=RDC&valorAno=2022. Accessed 19 July 2026.

15. Agencia Nacional de Vigilancia Sanitaria. Resolucao da Diretoria Colegiada Anvisa No. 945, de 29 de novembro de 2024. Guidelines and procedures for clinical trials for later medicine registration. AnvisaLegis. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=abrirTextoAto&cod_menu=8542&cod_modulo=310&link=S&numeroAto=00000945&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2024. Accessed 19 July 2026.

16. Agencia Nacional de Vigilancia Sanitaria. Resolucao RDC No. 9, de 20 de fevereiro de 2015. Regulation for clinical trials with medicines in Brazil. AnvisaLegis. https://anvisalegis.datalegis.net/action/ActionDatalegis.php?acao=detalharAto&cod_menu=9431&cod_modulo=310&desItem=&desItemFim=&nomeTitulo=codigos&numeroAto=00000009&orgao=RDC%2FDC%2FANVISA%2FMS&seqAto=000&tipo=RDC&valorAno=2015. Accessed 19 July 2026.
