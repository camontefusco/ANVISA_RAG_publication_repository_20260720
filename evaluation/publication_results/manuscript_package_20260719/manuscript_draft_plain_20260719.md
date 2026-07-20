Bilingual article-aware retrieval-augmented generation for ANVISA regulatory documents: technical validation with automated judging

Abstract

Background. Regulatory documents are long, article-structured, and terminology-dense. In this setting, a useful retrieval-augmented generation system must retrieve the correct document and article, answer only from retrieved evidence, and refuse questions that are outside the indexed corpus.

Objective. This study developed and technically evaluated a bilingual Portuguese-English RAG system for selected ANVISA regulatory documents, with emphasis on article-level retrieval, citation correctness, answer completeness, and refusal behavior.

Methods. The corpus was cleaned from raw text files and indexed as article-aware chunks with document, regulation, article, and citation metadata. Retrieval combined dense vector search and BM25 keyword search, merged candidates with rank fusion, retrieved 20 to 30 candidate chunks, reranked them, and generated answers from the top five contexts. English questions were expanded with a deterministic regulatory glossary while preserving terms such as clinical trial/ensaio clinico, sponsor/patrocinador, biological product/produto biologico, medical device/dispositivo medico, and stability study/estudo de estabilidade. The benchmark contained 200 bilingual article-level questions: 70 Portuguese answerable, 70 English answerable, 20 multi-article or exception questions, and 40 unanswerable or adversarial questions. The main held-out evaluation used 75 bilingual pairs. Generated answers were judged by an LLM-based evaluator for faithfulness, citation correctness, completeness, and refusal correctness. No human expert panel was used.

Results. On the post-repair internal held-out benchmark, English and Portuguese source hit rate and article Recall@5 were 1.000. Generated-answer term coverage was 0.849 in English and 0.828 in Portuguese. Retrieved-citation validity and refusal accuracy were 1.000 in both languages. AI-judge faithfulness was 0.997 in English and 1.000 in Portuguese. AI-judge citation correctness was 1.000 in both languages. AI-judge completeness was 0.995 in English and 1.000 in Portuguese. Because these internal results were obtained after error analysis, a 50-question prospective external stress test was run once without tuning. It showed strong answerable-question performance: source hit rate 1.000, normalized article Recall@5 0.967, faithfulness 1.000, citation correctness 0.975, and completeness 0.943. Refusal correctness on unanswerable and adversarial questions was lower at 0.700. After refusal calibration on a separate development set, a second untouched 30-question refusal-focused external test achieved unanswerable-question refusal correctness of 0.944 with no over-refusal on answerable controls.

Conclusion. Article-aware chunking, hybrid retrieval, reranking, bilingual query expansion, and stricter refusal rules produced strong technical performance for the selected ANVISA corpus. The main remaining limitation is validation: the results support a technical validation manuscript, not a claim of regulatory, clinical, or expert-consensus readiness.

Introduction

Retrieval-augmented generation was proposed to improve factual question answering by combining parametric language models with retrieved external documents (Lewis et al., 2020). For regulatory use, the central problem is narrower than open-domain question answering. The system must find the correct source, preserve article-level provenance, and avoid answering when the indexed documents do not contain the requested information.

Dense retrieval is useful for semantic matching, but regulatory questions often depend on exact strings: DDCM, RDC 945, Art. 33, IN 338, sponsor, clinical trial, biological product, medical device, and stability study. For that reason, this project used hybrid retrieval. Dense retrieval was combined with BM25, which remains a standard lexical retrieval method, and the merged candidates were reranked before answer generation (Robertson and Zaragoza, 2009; Karpukhin et al., 2020; Nogueira and Cho, 2019).

The bilingual setting adds another constraint. Users may ask in English while source rules and article labels are in Portuguese. The system therefore needs query expansion that maps English regulatory language to Portuguese regulatory terms without changing the legal meaning of the question.

This study evaluates the system as a technical RAG pipeline. It does not claim that automated judgment replaces expert legal or regulatory review. LLM-as-judge methods can provide scalable scoring, but their use must be reported as automated evaluation with known limitations (Zheng et al., 2023). This framing is especially important because no two-expert validation panel was available.

Materials and methods

Corpus

The corpus consisted of selected ANVISA regulatory text files relevant to clinical trials, product regulation, medical devices, biological products, and stability requirements. The indexed corpus was treated as a closed document collection. Answers were required to cite the retrieved source document and article. Questions outside the indexed documents were expected to receive a refusal.

Cleaning and chunking

The indexing pipeline transformed raw data text into cleaned text and then into article-level chunks. The target chunk was one article per chunk, with nearby section headings preserved when available. Long articles were split into smaller subchunks while preserving the article citation. This design was chosen because regulatory meaning is usually organized at the article level rather than by arbitrary token windows.

Retrieval

The retrieval pipeline used four stages. First, dense vector retrieval selected semantic candidates. Second, BM25 selected lexical candidates. Third, rank fusion merged the candidate lists. Fourth, a reranker sorted the merged candidates, and the top five contexts were passed to generation. The system retrieved more chunks than it used for generation so that reranking could correct early retrieval noise.

English query handling

English questions were rewritten or expanded for retrieval using a fixed bilingual regulatory glossary. The original English question was preserved for answer language and intent. Portuguese anchors were added only to improve retrieval against Portuguese source text. This was evaluated with and without rewrite during development to show whether bilingual retrieval improved English performance.

Generation and refusal policy

Answers were generated only from the top five retrieved contexts. The answer language followed the user question. The prompt required citation to the source document and article. If retrieved context was related but did not contain the specific requested answer, the system was instructed to say that the documents did not provide enough information. This rule was added after the first external stress test showed that the system sometimes answered unanswerable questions with nearby general rules.

Benchmark

The benchmark contained 200 bilingual, article-level questions: 70 Portuguese answerable questions, 70 English answerable questions, 20 multi-article or exception questions, and 40 unanswerable or adversarial questions. The benchmark was designed to test retrieval, citation, completeness, and refusal behavior in both languages.

Evaluation metrics

Retrieval was evaluated with source hit rate, source MRR, article Recall@5, article Precision@5, article MRR@5, article nDCG@5, and retrieved gold-term coverage. Generation was evaluated with answer term coverage, citation presence, article citation presence, retrieved-citation validity, and refusal accuracy. Automated answer-quality scoring used an LLM judge for faithfulness, citation correctness, completeness, and refusal correctness. Pair-clustered bootstrap intervals were used where applicable.

AI-judge evaluation

The generated answers and retrieval traces were frozen before judging. The judge evaluated each answer against saved retrieved evidence. The scores are automated labels and should be interpreted as technical evaluation signals. They are not inter-rater reliability, expert consensus, or external regulatory validation. Cohen's kappa was not applicable because there was no independent second human rater (Cohen, 1960).

Results

Internal held-out benchmark

On the post-repair internal held-out benchmark, both languages reached source hit rate 1.000 and article Recall@5 1.000. Generated-answer term coverage was 0.849 in English and 0.828 in Portuguese. Retrieved-citation validity and refusal accuracy were 1.000 in both languages.

AI-judge answer quality was also high. English faithfulness was 0.997, citation correctness was 1.000, completeness was 0.995, and refusal correctness was 1.000. Portuguese faithfulness, citation correctness, completeness, and refusal correctness were all 1.000.

These scores should not be reported as unbiased generalization performance. They were obtained after targeted repair of retrieval, completeness, and citation failures. The appropriate interpretation is that the final pipeline passed the curated internal benchmark.

External stress test

A 50-question prospective external stress test was then run once without tuning from it. It included 40 answerable and 10 unanswerable or adversarial questions. Answerable-question performance remained strong: source hit rate 1.000, normalized article Recall@5 0.967, normalized article MRR@5 0.913, retrieved-citation validity 0.975, faithfulness 1.000, citation correctness 0.975, and completeness 0.943.

The main weakness was refusal calibration. Refusal correctness on unanswerable and adversarial questions was 0.700. Error review showed that the system sometimes used related general rules when the exact requested fact was absent from the corpus.

Refusal-focused external test

After a separate refusal-development update, a new 30-question refusal-focused external test was run. It included 18 unanswerable or current-specific questions and 12 answerable controls. Refusal detection on unanswerable questions was 0.944, AI-judge refusal correctness was 0.944, and over-refusal on answerable controls was 0.000. Answerable-control faithfulness and citation correctness were 1.000, and completeness was 0.908.

The remaining boundary case concerned questions where the corpus provided a general enforcement consequence but not the exact requested penalty. This should remain visible in the limitations section.

Discussion

The strongest result is not the near-perfect internal benchmark. The stronger evidence is the sequence of evaluations: a repaired internal benchmark, a first untouched external stress test that exposed refusal weakness, and a second untouched refusal-focused test after calibration. This sequence gives a clearer account of what the system does well and where it remains fragile.

The technical choices are consistent with the needs of regulatory RAG. Article-aware chunks preserve citation units. BM25 improves exact-term matching. Dense retrieval improves semantic matching. Reranking improves selection after broad retrieval. Bilingual glossary expansion addresses English questions over Portuguese source documents. The refusal prompt reduces unsupported answers when retrieved evidence is related but incomplete.

The evaluation is still limited. The benchmark was constructed and judged without an expert panel. Automated judgment is useful for scale and consistency, but it can miss domain-specific legal nuance and can be biased by answer form. The external stress tests were AI-authored rather than independently authored by regulatory specialists. The corpus is closed and selected; it does not represent all ANVISA rules, current web pages, forms, fees, submission portals, or future regulatory changes.

For publication, the appropriate claim is therefore narrow: this is a technical validation of a bilingual article-aware RAG pipeline for selected ANVISA documents, evaluated with retrieval metrics, citation checks, refusal tests, and LLM-based judging. It should not be framed as deployment validation or as evidence that the system can replace professional regulatory interpretation.

Limitations

First, there was no independent human expert panel. Second, the AI judge was a single automated evaluator. Third, internal benchmark results may be inflated because pipeline repairs were made after error analysis. Fourth, external benchmarks were AI-authored. Fifth, the system can answer only from indexed documents and should not be used for current forms, fees, web pages, private submission status, or future regulatory changes. Sixth, refusal behavior improved but remains the main safety boundary to monitor.

Conclusion

The pipeline is suitable for a technical validation manuscript if the claims remain conservative. The main publishable contribution is the combination of article-aware indexing, hybrid retrieval, reranking, bilingual query expansion, citation-constrained generation, refusal calibration, and staged evaluation for a Portuguese-English regulatory corpus. The next publication step is not more prompt tuning. It is transparent reporting of the frozen pipeline, benchmark construction, automated judging protocol, and the remaining validation limits.

References

1. Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Kuttler, H., Lewis, M., Yih, W., Rocktaschel, T., Riedel, S., and Kiela, D. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS, 2020. https://papers.nips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html

2. Karpukhin, V., Oguz, B., Min, S., Lewis, P., Wu, L., Edunov, S., Chen, D., and Yih, W. Dense Passage Retrieval for Open-Domain Question Answering. EMNLP, 2020. https://aclanthology.org/2020.emnlp-main.550/

3. Robertson, S., and Zaragoza, H. The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval, 2009. https://doi.org/10.1561/1500000019

4. Nogueira, R., and Cho, K. Passage Re-ranking with BERT. arXiv:1901.04085, 2019. https://arxiv.org/abs/1901.04085

5. Gao, Y., Xiong, Y., Gao, X., Jia, K., Pan, J., Bi, Y., Dai, Y., Sun, J., Wang, M., and Wang, H. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv:2312.10997, 2023. https://arxiv.org/abs/2312.10997

6. Es, S., James, J., Espinosa-Anke, L., and Schockaert, S. RAGAS: Automated Evaluation of Retrieval Augmented Generation. arXiv:2309.15217, 2023. https://arxiv.org/abs/2309.15217

7. Zheng, L., Chiang, W., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., Zhang, H., Gonzalez, J., and Stoica, I. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. NeurIPS, 2023. https://arxiv.org/abs/2306.05685

8. Guha, N., Nyarko, J., Ho, D. E., Re, C., and collaborators. LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language Models. NeurIPS Datasets and Benchmarks, 2023. https://legalbench.ai/

9. Chalkidis, I., Fergadiotis, M., Malakasiotis, P., Aletras, N., and Androutsopoulos, I. LEGAL-BERT: The Muppets straight out of Law School. Findings of EMNLP, 2020. https://aclanthology.org/2020.findings-emnlp.261/

10. Cohen, J. A coefficient of agreement for nominal scales. Educational and Psychological Measurement, 1960. https://doi.org/10.1177/001316446002000104
