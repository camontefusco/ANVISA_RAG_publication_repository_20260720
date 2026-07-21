Bilingual Retrieval-Augmented Access to ANVISA Regulatory Documents: A Technical Evaluation Using Drug-Development and Health-Product Questions

Authors: Carlos Victor Montefusco-Pereira1*, Howard Lopes Ribeiro Junior2

1 Independent Researcher in Data Science and Artificial Intelligence in Industrial Pharmaceutics, Berlin, Germany

2 Center for Research and Drug Development (NPDM), Federal University of Ceara, Fortaleza 60430-275, Brazil; Post-Graduate Program in Pathology, Federal University of Ceara, Fortaleza, Brazil; Post-Graduate Program in Translational Medicine, Federal University of Ceara, Fortaleza, Brazil

ORCID: Carlos Victor Montefusco-Pereira, 0000-0003-4167-4653; Howard Lopes Ribeiro Junior, 0000-0003-2431-4779

Corresponding author: Carlos Victor Montefusco-Pereira. Friedrich-Wilhelm 28, 12103 Berlin, Germany. Email: cmontefusco@gmail.com. Phone: +49 15168108538.

Keywords: regulatory science; ANVISA; retrieval-augmented generation; clinical trials; pharmacovigilance; biological products and medical devices

Abbreviations: ANVISA, Agencia Nacional de Vigilancia Sanitaria; AREE, equivalent foreign regulatory authority; BM25, Best Matching 25; DDCM, Clinical Drug Development Dossier; DSUR, Development Safety Update Report; ICH, International Council for Harmonisation; MRR, mean reciprocal rank; RAG, retrieval-augmented generation; RRF, reciprocal rank fusion; SUSAR, suspected unexpected serious adverse reaction.

Abstract

Background. Regulatory teams often need to interpret long health-authority documents while working across languages. In Brazil, many regulatory sources are published in Portuguese, while companies and scientists may ask questions in English.

Objective. To evaluate whether a bilingual retrieval-augmented generation prototype could locate, cite, and summarize selected ANVISA regulatory requirements relevant to drug development and health-product regulation.

Methods. Six ANVISA regulatory documents were cleaned and indexed as an article-level closed corpus. The system was implemented in Python 3.10 using LlamaIndex, sentence-transformers, rank-bm25, Streamlit, and the Google Generative AI interface. Dense retrieval used sentence-transformers/all-MiniLM-L6-v2; keyword retrieval used BM25; candidates were merged by reciprocal rank fusion and reranked with cross-encoder/mmarco-mMiniLMv2-L12-H384-v1. The final answer model was models/gemini-flash-lite-latest. The benchmark included 200 bilingual questions: 70 Portuguese answerable, 70 English answerable, 20 multi-article or exception questions, and 40 unanswerable or adversarial questions. An automated AI judge scored faithfulness, citation correctness, completeness, and refusal correctness on a 0 to 1 scale.

Results. The final article-aware index contained 382 detected regulatory articles and 481 chunks. In the first AI-authored prospective stress test, answerable questions had source hit 1.000, source MRR 0.988, normalized article Recall@5 0.967, normalized article MRR@5 0.913, citation correctness 0.975, faithfulness 1.000, and completeness 0.943. Refusal correctness for unanswerable/adversarial questions was lower at 0.700. After refusal calibration using separate development data, a refusal-focused AI-authored test reached refusal correctness 0.944, with faithfulness 1.000, citation correctness 1.000, and completeness 0.908 on answerable controls.

Conclusion. A bilingual RAG system may support regulatory information access when answers are tied to verifiable articles and refusal is evaluated as a primary endpoint. The project did not validate regulatory advice. It tested a narrower use case: locating and summarizing evidence inside a defined ANVISA corpus.

Introduction

Drug-development decisions often begin with a narrow regulatory question. A sponsor may need to know how a Clinical Drug Development Dossier (DDCM) can be suspended, when a Development Safety Update Report (DSUR) must be submitted, what minimum information makes an adverse-event notification valid, whether a foreign-manufactured biological product can be registered without registration in its manufacturing country, or whether instructions for a medical device may be provided only in non-printed form. These questions affect trial operations, safety reporting, dossier planning, pharmacovigilance systems, and product labelling.

The difficulty is not only that the documents are long. The relevant answer may be in one article, while a nearby article discusses the same topic but does not answer the exact question. A user may also ask in English while the source document is in Portuguese. In that setting, a general search result is not enough. The user needs to know which document and article support the answer, and when the document collection does not contain the requested fact.

Retrieval-augmented generation (RAG) systems may help by retrieving source passages before generating an answer [1,9]. Prior work in Therapeutic Innovation & Regulatory Science evaluated generative AI search over FDA guidance documents and reported both promise and limitations [2]. Source citation was useful, but incomplete or incorrect answers remained a concern. That finding is directly relevant to regulatory affairs. A fluent answer can be unsafe if it omits a condition, treats an exception as a rule, or answers a current operational question from a static regulatory document.

This study evaluated a bilingual RAG prototype using selected ANVISA documents. The aim was not to build a regulatory-advice tool. The aim was to test whether the system could support traceable information access: retrieve the relevant document and article, answer in Portuguese or English, cite the source, and refuse when the indexed documents did not provide the requested information.

The manuscript focuses on the regulatory behavior of the system rather than treating the application as a generic chatbot. The central questions were whether article-level retrieval improved traceability, whether bilingual queries over Portuguese source text could be handled, whether generated answers preserved complete regulatory conditions, and whether the system could abstain when the answer was outside the closed corpus.

Materials and Methods

Study design

This was a technical evaluation of a closed-corpus bilingual RAG prototype. The corpus was closed because the system was not allowed to search current web pages, submission portals, fee schedules, private company information, unpublished documents, or documents outside the local index. This design made the evidence boundary explicit. If the answer was not present in the indexed documents, the correct behavior was refusal.

The evaluation was developed in stages. Initial tests identified problems in corpus cleaning, retrieval, English questions over Portuguese documents, answer completeness, citation behavior, and refusal behavior. Repairs were made on development data. The final reporting separates development runs, internal held-out runs, the first AI-authored prospective stress test, and a later refusal-focused AI-authored test. This separation is important because internal scores can be inflated when the same project team writes questions, reviews errors, and repairs the system.

Regulatory corpus

The corpus included six selected ANVISA documents covering clinical trials, biological products, medical devices, pharmacovigilance, and reliance-based review [3-8]. The documents were chosen because they represent common questions in drug-development and health-product work. The final corpus included IN 338/2024, RDC 406/2020, RDC 55/2010, RDC 751/2022, RDC 945/2024, and RDC 9/2015. Corpus composition and use cases are summarized in Table 1.

Each source file was checked against its document identifier and topic before final indexing. Source verification identified one local-file metadata mismatch: the local file name suggested stability studies, while the document content was RDC 406/2020 on pharmacovigilance. The final corpus table therefore used official regulation numbers and topics rather than local file names.

Software and implementation

The prototype and evaluation scripts were implemented in Python 3.10. The environment file specified numpy 1.26, python-dotenv, PyTorch, sentence-transformers, ragas, Streamlit, LlamaIndex, llama-index-core, llama-index-embeddings-huggingface, llama-index-llms-google-genai, and rank-bm25 0.2.2 [10-15]. The user-facing application was a Streamlit app; a local launch and backend query smoke test are documented in Supplementary Figure S4. Indexing and evaluation were run from Python scripts in the project repository. The main implementation files were src/article_chunking.py, src/retrieval.py, src/prompts.py, src/engine.py, evaluation/publication_eval.py, evaluation/answer_quality.py, and evaluation/evaluation_statistics.py. Additional implementation and reproducibility details are provided in Supplementary Information and Supplementary Methods and Prompts.

The software implementation was derived from three course notebooks that progressed from a local LLM scaffold, to a chatbot, to a simple RAG application. The ANVISA project kept the teaching pattern of a Python environment, configuration module, model loader, engine, and app interface, but replaced the generic RAG design with regulatory source cleaning, article-aware indexing, hybrid retrieval, reranking, bilingual retrieval anchors, citation enforcement, refusal rules, and evaluation scripts. A recovered local ancestor of the ANVISA project was used to reconstruct the first working app and development decisions. A detailed decision trace is provided in Supplementary Table S5, with expanded development decisions and evaluation-stage disposition in Supplementary Tables S1, S3, and S4.

The answer-generation model and the AI-judge model were both models/gemini-flash-lite-latest. The embedding model was sentence-transformers/all-MiniLM-L6-v2. The reranker was cross-encoder/mmarco-mMiniLMv2-L12-H384-v1. The local reproducibility package records the cache snapshot paths used during development, but model names rather than cache paths are the primary reproducibility identifiers because local paths are machine-specific.

Corpus cleaning and article-aware chunking

Raw regulatory text files were cleaned to remove markup residue, page boilerplate, and formatting artifacts while preserving article labels and regulatory structure. The final index used article-aware chunking rather than arbitrary fixed-size text windows. The target unit was one regulatory article per chunk when possible. Chapter, section, document, source-file, article-number, and citation-label metadata were retained with each chunk.

Article chunking used a single-article maximum of 500 tokens. Longer articles were split into 400-token chunks with 60-token overlap. Embedding maximum length was 512 tokens. The final index audit recorded six source documents, 382 detected articles, 481 total chunks, 359 articles represented by a single chunk, and 23 long articles split into multiple chunks. Median chunk length was 155 tokens, maximum chunk length was 503 tokens, and no chunk exceeded 700 tokens. The closed-corpus workflow and index audit are shown in Figure 1.

Retrieval, reranking, and answer generation

Retrieval combined dense vector search and keyword search. Dense retrieval used the sentence-transformers embedding model [11]. Keyword retrieval used BM25 over normalized text created from chunk content and metadata fields, including regulation identifier, document aliases, title, citation label, chapter, section, and topic tags [12]. Normalization removed accents, lowercased text, and extracted alphanumeric tokens.

The dense retriever returned 100 candidates. BM25 returned 100 candidates. Candidate lists were merged using reciprocal rank fusion with k = 60, retaining up to 100 fused candidates. Candidate passages were then reranked with the multilingual cross-encoder reranker in batches of 8; this choice was based on multilingual passage-ranking models trained on mMARCO-style data [13]. The final answer context contained the top 5 reranked passages.

English questions were answered in English, but retrieval was allowed to include conservative Portuguese anchors because the source documents were in Portuguese. Anchors included clinical trial/ensaio clinico, sponsor/patrocinador, biological product/produto biologico, medical device/dispositivo medico, stability study/estudo de estabilidade, and pharmacovigilance/farmacovigilancia. The original question remained visible to the answer model. These anchors were retrieval aids only; they did not add facts to the answer.

The answer prompt required the model to answer using only retrieved context, answer in the same language as the question, cite each material statement using the retrieved article-level citation label, and refuse if retrieved evidence did not contain enough information to answer the exact question. The refusal sentence was fixed by language: "The retrieved documents do not provide enough information to answer" for English questions and "Os documentos recuperados nao fornecem informacao suficiente para responder" for Portuguese questions. The final prompt is provided in Supplementary Methods and Prompts. Row-level generated answers, retrieval fields, and error flags are provided in Supplementary Data S1; AI-judge criteria, prompt, row-level scores, rationales, and stage-level conclusions are provided in Supplementary Data S2.

Benchmark

The main benchmark contained 200 bilingual questions: 70 Portuguese answerable questions, 70 English answerable questions, 20 multi-article or exception questions, and 40 unanswerable or adversarial questions. The benchmark had 100 Portuguese rows and 100 English rows organized as bilingual pairs. The audit recorded 78 unique gold article citations. Benchmark structure and gold source coverage are shown in Figure 2.

For answerable questions, the benchmark recorded expected source documents, gold article labels, gold citation labels, expected answer terms, and a short expected answer. For unanswerable questions, the expected behavior was refusal. The benchmark included direct article questions, long-list questions, rule-plus-exception questions, false-premise questions, current operational questions outside the corpus, and adversarial questions that were regulatory in topic but not answerable from the indexed documents.

Automated AI judge and scoring rules

Automated judging was used because an independent two-expert panel was not available. This limits the claim level. The automated judge was used as a structured technical scoring tool, not as an independent regulatory expert. The scoring dimensions followed common RAG-evaluation concepts such as faithfulness or groundedness, context-supported citation, answer completeness, and refusal for insufficient evidence [10,16,17]. The judge received the question, system answer, expected answer, answerability flag, and retrieved evidence. It returned JSON scores from 0 to 1 for four dimensions: faithfulness, citation correctness, completeness, and refusal correctness, plus a short rationale. The exact prompt, model settings, row-level outputs, and stage-level recommendations are provided in Supplementary Data S2.

Faithfulness measured whether factual claims were supported by retrieved evidence. Citation correctness measured whether citations existed when an answer was given, referred to retrieved evidence, and supported the associated claim. Article-level citations were accepted when the supporting sentence was within a retrieved cited article; paragraph or item suffixes were not required. Completeness measured whether the answer covered the expected answer's essential information, including material conditions and exceptions. Refusal correctness measured whether an unanswerable question was refused without unsupported content, or whether an answerable question was answered rather than refused.

The primary reported metrics were continuous means, not binary expert adjudications. For per-question failure review, the code flagged answerable rows as problematic when the retrieved source was missing, article retrieval was incomplete, retrieved term coverage was below 0.50, generated answer-term coverage was below 0.50, citations were absent, cited labels were not among retrieved labels, or refusal occurred for an answerable question. AI-judge faithfulness below 0.80 was flagged as unfaithful. English completeness diagnosis used judge completeness below 0.80 to identify low-completeness rows for repair experiments. These thresholds were operational audit rules, not clinical or regulatory acceptance criteria. The resulting question-level flags are provided with generated answers in Supplementary Data S1 and with judge rationales in Supplementary Data S2.

Evaluation stages and leakage control

Development runs were used to identify and repair failures. Internal held-out runs were used to check the repaired system on the curated benchmark. When internal results became high, an AI-authored prospective stress test was run once to test whether the internal pattern generalized. That first AI-authored prospective stress test was treated as diagnostic prospective evidence and was not used directly for tuning. After it identified refusal calibration as the main weakness, refusal rules were adjusted using a separate development set. A second refusal-focused AI-authored test was then used to evaluate the repair.

The first AI-authored prospective stress test contained 50 questions organized as 25 bilingual pairs. It included 40 answerable questions and 10 unanswerable or adversarial questions. The first AI-authored prospective run required artifact recovery after output folders had been moved; a preserved 40-row checkpoint was merged with a regenerated 10-row unanswerable/adversarial block using the same frozen settings. No benchmark, retrieval, prompt, judge, threshold, or result-driven tuning edits were made before that recovery. The refusal-focused AI-authored test contained 30 questions organized as 15 bilingual pairs, with 18 unanswerable questions and 12 answerable controls.

Statistical handling and audit trail

Source-level retrieval was summarized by source hit and source MRR. Article-level retrieval was summarized by Recall@k, Precision@k, MRR@k, and nDCG@k after lowercasing, accent removal, and whitespace normalization of citation labels. For generated answers, the system recorded citation presence, article citation presence, retrieved-citation validity, answer-term coverage, refusal detection, and AI-judge scores. When confidence intervals were reported in supplementary files, pair-clustered percentile bootstrap resampling used bilingual pair ID as the cluster key, 2000 resamples, 95% confidence level, and seed 20260619.

For reproducibility, each evaluation row exported the question ID, pair ID, language, category, answerability flag, gold source documents, gold citations, raw vector candidates, BM25 candidates, fused candidates, final reranked contexts, generated answer, extracted citations, refusal detection, deterministic metrics, AI-judge scores, and judge rationale. The repository also contains manual-review templates. They were retained as audit scaffolds, but they were not completed as a two-expert validation dataset.

Results

Corpus and benchmark construction

The final index contained six ANVISA documents, 382 detected regulatory articles, and 481 article-level chunks (Figure 1). Most articles were short enough to be represented by one chunk. Long articles were split with overlap to preserve continuity. This mattered because regulatory questions often ask for all items in an article or for a condition that appears after the main rule.

The 200-question benchmark was balanced by language and included the intended mix of regulatory question types (Figure 2). Gold evidence covered 78 unique article citations. The source coverage was distributed across the six regulations, including clinical-trial, pharmacovigilance, biological-product, medical-device, and reliance questions. This structure was important because high performance on direct clinical-trial questions alone would not show whether the system handled rule-plus-exception or refusal boundaries.

Direct article questions

The system performed best when the question matched a compact article-level answer. For example, it correctly answered that a pharmacovigilance notification under RDC 406/2020 requires identification of the notifier, identification of the patient, description of the adverse event, and name of the suspected medicine, citing RDC 406/2020, Art. 32. It also correctly handled a false-premise version of the same issue by answering no when asked whether a notification is valid without patient identification if the suspected medicine is named.

The system also answered clinical-trial conduct questions. When asked whether possible SUSAR reporting allows unblinding all participants, it answered that unblinding should be limited to the affected participant and cited RDC 945/2024, Art. 67. These examples show why article-level citation was part of the evaluation rather than a display feature. The system's useful role was to narrow the search and provide a checkable summary; the regulatory user would still need to inspect the cited article before applying it.

Internal development metrics

The first held-out AI-judge evaluation showed high faithfulness but weaker completeness. Among 120 answerable internal held-out rows, mean AI-judge faithfulness was 0.997, citation correctness was 0.965, and completeness was 0.808. Among 30 unanswerable rows, refusal correctness was 1.000. English answer completeness was the main weak point in this stage: the English answerable subset had completeness 0.645. This result led to the English completeness repair work rather than to a claim that the system was already ready. The judged questions, scores, and rationales for this stage are reported in Supplementary Data S2.

After English repair, the English repair set had mean faithfulness 0.997, citation correctness 0.983, completeness 0.995, and refusal correctness 1.000. After Portuguese residual-quality repair, the Portuguese repair set had mean faithfulness 0.993, citation correctness 0.963, completeness 0.995, and refusal correctness 1.000. These results are shown as development history in Figure 3A. They should not be interpreted as paired repeated-measure improvements because the stages used different evaluation sets. The row-level judge outputs and stage recommendations are reported in Supplementary Data S2.

The saturated internal values, including refusal correctness of 1.000 on internal unanswerable rows, were investigated rather than accepted as evidence of a perfect system. They were considered potentially inflated because the benchmark and repair sets were created during development, targeted changes were made after error review, some metrics can saturate on small subsets, and the answer model and judge used the same model family. The first AI-authored prospective stress test was therefore run as a challenge to the internal pattern. Its refusal correctness of 0.700 showed that the internal 1.000 refusal result was too narrow for reliability claims. The AI-judge dossier documents this as a diagnostic recommendation rather than a tuning result, and the saturated-metric investigation is summarized in Supplementary Table S6.

Completeness errors

Completeness errors mattered more than raw retrieval. Several errors occurred even when the correct document or article was retrieved. In one pharmacovigilance question, the system listed the minimum elements of a valid notification but omitted the active-search obligation when required information is absent. In one DSUR question, the answer gave the annual submission timing but omitted the ICH E2F condition. In one medical-device question, it omitted the requirement that non-printed instructions remain available while the product remains on the market. In a biological-product question, it gave the exception for a foreign-manufactured biological product but did not first state the general rule. In a clinical-trial question, it omitted a 30-business-day response deadline.

These were not cosmetic errors. In regulatory work, an omitted condition can change how a sponsor plans a submission, designs a safety process, or prepares product information. A system that retrieves the right article but omits the condition is useful only if the user still checks the citation.

The development process therefore changed the evaluation focus. Early work asked whether the system could find the right source. Later work asked whether the answer included all material elements from the source and whether the system could abstain from unsupported operational claims. This sequence is summarized in Table 2, with expanded failure-to-repair categories in Supplementary Table S1. Representative answer outcomes are provided in Table 3 and expanded in Supplementary Table S2.

AI-authored prospective stress test

The first AI-authored prospective stress test was more informative than the internal post-repair scores. It contained 50 questions, including 40 answerable rows and 10 unanswerable or adversarial rows. For answerable questions, source hit was 1.000 and source MRR was 0.988. Normalized article Recall@5 was 0.967 and normalized article MRR@5 was 0.913. Citation presence and retrieved-citation validity were both 0.975. AI-judge faithfulness was 1.000, citation correctness was 0.975, and completeness was 0.943.

The same test exposed refusal behavior as the main remaining weakness. Literal refusal detection for unanswerable/adversarial questions was 0.600, and AI-judge refusal correctness was 0.700. The main failure pattern was answering from nearby general regulatory text when the question asked for a more specific current or operational fact not present in the corpus. For example, the system answered a question about a current electronic SUSAR notification form model using the general electronic notification requirement, instead of refusing because the specific current form model was not in the indexed documents.

Language-specific prospective-test results were similar but not identical. Among answerable prospective-test rows, normalized article Recall@5 was 0.950 for English and 0.983 for Portuguese. AI-judge completeness was 0.930 for English and 0.955 for Portuguese. AI-judge refusal correctness for unanswerable/adversarial rows was 0.800 for English and 0.600 for Portuguese. These results did not support a perfect-system claim. They supported a narrower claim: answerable regulatory questions were usually handled well, but refusal calibration remained a safety boundary.

Refusal calibration

After the first AI-authored prospective stress test, refusal rules were revised using a separate refusal-development set. The revision instructed the answer model to treat related-but-incomplete context as insufficient and to refuse current forms, exact URLs, current fees or values, private contract terms, company-specific submission status, personal contact information, market prices, reimbursement, taxes, patents, future approvals, and advice not explicitly stated in the retrieved regulatory text.

In the later refusal-focused AI-authored test, the system correctly refused 17 of 18 unanswerable questions by AI-judge scoring, giving refusal correctness 0.944. It did not over-refuse the answerable controls: answerable-control faithfulness was 1.000, citation correctness was 1.000, and completeness was 0.908. This improvement and the completeness trade-off are shown in Figure 3B. The result suggests that refusal calibration improved abstention behavior, but it also shows a cost: answerable-control completeness was lower than in the first AI-authored prospective stress test. The question-level judge rationales and remaining boundary failure are reported in Supplementary Data S2.

The remaining boundary problem involved questions where the corpus contained a related general rule but not the exact requested fact. This is a regulatory risk because related evidence can sound persuasive while still being insufficient. The safest interpretation is that refusal improved, not that refusal was solved.

Summary of quantitative evaluation

Across the development path, the main metrics changed in ways that affected the project interpretation. Initial internal held-out answer completeness was 0.808 overall for answerable rows, with English completeness 0.645. After targeted English repair, the English repair set reached completeness 0.995. After Portuguese residual-quality repair, the Portuguese repair set reached completeness 0.995. These internal repair results were not treated as independent proof because they followed error review and targeted changes.

The first AI-authored prospective stress test provided the main challenge to overfitting. It showed strong retrieval and answer grounding for answerable questions, with source hit 1.000, normalized article Recall@5 0.967, faithfulness 1.000, citation correctness 0.975, and completeness 0.943. It also showed weak refusal correctness at 0.700. The refusal-focused AI-authored test after separate calibration improved refusal correctness to 0.944 but had answerable-control completeness 0.908. Thus the main residual problem shifted from retrieval and language support to the boundary between partial related evidence and sufficient evidence.

Discussion

Interpretation of the development path

The main finding is not that the system achieved high average scores. The main finding is that a bilingual RAG prototype can support traceable access to selected ANVISA documents when it is treated as a closed-corpus evidence-location tool rather than as a regulatory-advice system. This interpretation is consistent with the broader RAG literature, which frames retrieval as a way to connect generation to external evidence, and with prior regulatory work showing that generative AI search can cite useful sources while still producing incomplete or incorrect answers [1,2,9].

The figures support that sequence rather than serving only as decoration. Figure 1 shows the engineering turn from a generic RAG scaffold to a closed, article-aware ANVISA pipeline. Figure 2 shows why the benchmark was not limited to easy article lookup: it mixed Portuguese and English questions, single-article questions, exception questions, and unanswerable or adversarial questions. Figure 3A then shows the development history after weak points were identified, while Figure 3B shows the later targeted repair of refusal behavior and the remaining completeness trade-off. Together, the figures make the main interpretation clearer: once article-aware indexing, hybrid retrieval, and reranking were in place, ordinary source retrieval was no longer the dominant weakness. The important question became whether the retrieved article was sufficient for the exact answer requested.

That shift is important for regulatory use. Metrics showed the overall pattern, but the examples explained the risk. The incomplete answers were not only stylistic omissions. They involved active-search obligations, ICH E2F conditions, market-availability requirements for instructions for use, the general rule before a biological-product exception, and a 30-business-day deadline. Similarly, refusal failures involved questions that sounded regulatory but asked for current operational facts such as a form model, phone number, petition code, or private case status. These examples show why completeness and refusal should be primary endpoints in regulatory RAG evaluation, not secondary notes.

Use in drug development and regulatory affairs

The most realistic use of this prototype is assisted navigation of a defined document set. A regulatory user could ask a question, receive a short answer, and inspect the cited article before using the information. This could reduce time spent searching across long Portuguese documents, especially for international teams working in English. It should not be used as a stand-alone regulatory decision tool because it does not access current portals, fee schedules, forms, company-specific status, authority correspondence, or the full current legal context.

The examples map to ordinary development and submission work. Before or during a clinical trial, a sponsor may need to check DDCM suspension procedures, DSUR timing, or the boundary between SUSAR reporting and trial unblinding. During safety-system design, the team may need to confirm the minimum information that makes a pharmacovigilance notification valid and what follow-up is expected when information is incomplete. During product-registration planning, a biological-product team may need to understand whether an exception applies or whether the general manufacturing-country registration rule still controls the case. For medical devices, labelling and supply teams may need to know whether non-printed instructions for use are acceptable for the intended use setting.

Confidence should therefore depend on the question type. Confidence is highest for direct article questions, definition-like questions, and false-premise questions where the cited article clearly supports the answer. Confidence is moderate for rule-plus-exception questions, multi-article questions, and complete-list questions, because these are the settings where the evaluation found omissions. Confidence is low for current operational details, exact portal codes, current MedDRA versions, phone numbers, URLs, fee information, product-specific strategy, private case status, legal advice, or future approval likelihood. For those questions, the safest behavior is refusal or a statement that the indexed documents do not provide enough information.

Limitations and future work

This study used a selected closed corpus and does not cover all ANVISA rules or current operational resources. Benchmark construction did not include an independent panel of regulatory experts. Automated judging was used and should be interpreted as technical scoring, not expert validation. This choice is consistent with current work on scalable LLM evaluation, but the literature also warns that automated judges may show bias and incomplete agreement with human judgment [10,16,17]. In this study, that limitation is especially relevant because the answer model and automated judge used the same Gemini model family.

The 1.000 values are therefore reported as part of the quality story, not as a claim of perfection. Internal refusal correctness reached 1.000, and some post-repair judge scores approached or reached 1.000, but those values came after benchmark construction, error review, and targeted repair. The first AI-authored prospective stress test was important because it challenged those saturated values without tuning from that set. It contradicted the internal refusal result: refusal correctness fell to 0.700 even while answerable-question retrieval and grounding remained strong. Figure 3A should therefore be read as development history, and Figure 3B as evidence that refusal calibration improved the main safety weakness but introduced a visible trade-off, with answerable-control completeness below the first prospective answerable set. The most defensible claim is limited but useful. The system can help locate and summarize evidence in selected ANVISA documents, provided users verify the cited article and treat refusal boundaries seriously.

Future studies should test the system with regulatory-affairs users and measure whether it reduces time to locate evidence without increasing overconfidence. A stronger validation study should include independent expert review of selected answers, blinded error classification, prospective question authoring by users not involved in system development, and comparison with standard document search. The corpus should also be expanded and versioned so users can see when a question requires current information outside the indexed corpus.

Conclusion

A bilingual RAG prototype can help retrieve and summarize selected ANVISA regulatory documents when the answer is present in the indexed corpus and the cited article is checked. The evaluation showed useful performance for clinical-trial, pharmacovigilance, biological-product, medical-device, and reliance questions. It also showed why regulatory RAG evaluation should report concrete successes and failures. The central safety boundary is not only retrieval accuracy; it is the ability to avoid incomplete answers and to refuse when the documents do not contain the requested fact.

Funding

The authors received no specific funding for this work.

Conflict of Interest

The authors declare no competing financial interests.

Author Contributions

C.V.M.-P. conceived and designed the study, developed the software pipeline, prepared the corpus, constructed the benchmark, performed the analyses, interpreted the results, and drafted the manuscript. H.L.R.J. contributed to the regulatory and pharmaceutical framing, interpretation of results, and critical revision of the manuscript. Both authors approved the final manuscript and agree to be accountable for the work.

Data Availability

The code, benchmark manifests, generated outputs, prompts, and non-restricted derived artifacts are archived in a private project repository during manuscript preparation and will be made publicly available after manuscript acceptance. Files needed for peer review are included as supplementary materials. Official ANVISA source URLs, source-file checksums, and the cleaning script are provided in the source reproducibility folder. Full cleaned copies of ANVISA regulatory text are derived from public agency documents; if redistribution of full cleaned text is restricted or unnecessary, the public repository will provide official source links, checksums, and cleaning scripts rather than republishing the full source text.

Ethics Approval

Ethics approval was not required because the study used public regulatory documents and generated benchmark questions. No human participants, patient data, animal data, or clinical trial data were used.

Clinical Trial Registration

Not applicable.

References

1. Lewis P, Perez E, Piktus A, et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Advances in Neural Information Processing Systems. 2020;33:9459-9474.

2. Proestel S, Jeng LJB, Smith C, et al. Semantic Search of FDA Guidance Documents Using Generative AI. Ther Innov Regul Sci. 2025;59(5):1148-1159. doi:10.1007/s43441-025-00798-8.

3. Agencia Nacional de Vigilancia Sanitaria. Instrucao Normativa - IN No. 338, de 29 de novembro de 2024. Establishes the list of equivalent foreign regulatory authorities and criteria for optimized review under RDC 945/2024. AnvisaLegis. Accessed 19 July 2026.

4. Agencia Nacional de Vigilancia Sanitaria. Resolucao de Diretoria Colegiada - RDC No. 406, de 22 de julho de 2020. Good pharmacovigilance practices for holders of human medicine registrations. AnvisaLegis. Accessed 19 July 2026.

5. Agencia Nacional de Vigilancia Sanitaria. Resolucao - RDC No. 55, de 16 de dezembro de 2010. Registration of new biological products and biological products. AnvisaLegis. Accessed 19 July 2026.

6. Agencia Nacional de Vigilancia Sanitaria. Resolucao - RDC No. 751, de 15 de setembro de 2022. Medical-device risk classification, notification and registration regimes, labelling, and instructions for use. AnvisaLegis. Accessed 19 July 2026.

7. Agencia Nacional de Vigilancia Sanitaria. Resolucao da Diretoria Colegiada Anvisa No. 945, de 29 de novembro de 2024. Guidelines and procedures for clinical trials for later medicine registration. AnvisaLegis. Accessed 19 July 2026.

8. Agencia Nacional de Vigilancia Sanitaria. Resolucao RDC No. 9, de 20 de fevereiro de 2015. Regulation for clinical trials with medicines in Brazil. AnvisaLegis. Accessed 19 July 2026.

9. Gao Y, Xiong Y, Gao X, et al. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv. 2023. doi:10.48550/arXiv.2312.10997.

10. Es S, James J, Espinosa-Anke L, Schockaert S. RAGAS: Automated Evaluation of Retrieval Augmented Generation. arXiv. 2023. doi:10.48550/arXiv.2309.15217.

11. Reimers N, Gurevych I. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In: Proceedings of EMNLP-IJCNLP. Association for Computational Linguistics; 2019:3982-3992. doi:10.18653/v1/D19-1410.

12. Robertson S, Zaragoza H. The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval. 2009;3(4):333-389. doi:10.1561/1500000019.

13. Bonifacio L, Jeronymo V, Abonizio HQ, Campiotti I, Fadaee M, Lotufo R, Nogueira R. mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset. arXiv. 2021. doi:10.48550/arXiv.2108.13897.

14. LlamaIndex. LlamaIndex: a data framework for LLM applications. GitHub repository. https://github.com/run-llama/llama_index. Accessed 21 July 2026.

15. Google AI for Developers. Gemini 2.5 Flash-Lite model documentation. https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-lite. Accessed 21 July 2026.

16. Chang Y, Wang X, Wang J, et al. A Survey on Evaluation of Large Language Models. ACM Transactions on Intelligent Systems and Technology. 2024;15(3). doi:10.1145/3641289.

17. Zheng L, Chiang WL, Sheng Y, et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. Advances in Neural Information Processing Systems. 2023;36.

Official AnvisaLegis URLs and SHA-256 checksums for references 3-8 are provided in the supplementary source reproducibility file.

Figure Legends

Figure 1. Closed-corpus RAG workflow. The workflow shows the path from selected ANVISA source documents to cleaned text, article-aware chunks with metadata, hybrid retrieval, reranking, answer generation, and evaluation. Source artifacts recorded six indexed regulatory documents, 382 detected articles, 481 article-level chunks, and a 200-question internal benchmark.

Figure 2. Benchmark design and source coverage. The benchmark contained 70 Portuguese answerable questions, 70 English answerable questions, 20 multi-article or exception questions, and 40 unanswerable or adversarial questions. Gold source evidence covered all six indexed ANVISA documents and 78 unique article citations.

Figure 3A. Development-stage answer-quality metrics. Mean AI-judge scores are shown for faithfulness, citation correctness, completeness, and refusal correctness across the main evaluation stages. The stages used different evaluation sets; the plot summarizes development history and should not be interpreted as a paired repeated-measure comparison. Underlying AI-judge rows, rationales, and stage-level recommendations are provided in Supplementary Data S2.

Figure 3B. Targeted weak-point repairs. The left panel shows English answer completeness before and after the English-completeness repair set. The middle panel shows refusal correctness in the first AI-authored prospective stress test and in the later refusal-focused AI-authored test after refusal-prompt calibration. The right panel shows answerable-question completeness in the AI-authored prospective stress test and in the answerable controls of the refusal-focused test. Because the panels compare different evaluation sets, the figure documents observed development decisions rather than paired statistical improvement. Underlying AI-judge rows, rationales, and stage-level recommendations are provided in Supplementary Data S2.
