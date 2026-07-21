# Supplementary Tables

Title: Bilingual Retrieval-Augmented Access to ANVISA Regulatory Documents

Prepared: 2026-07-20

## Supplementary Table S1. Expanded development decision table

| Question category or system issue | What the system did well | What went wrong | What was changed | What this means |
|---|---|---|---|---|
| Source cleaning and document identity | The project identified the intended regulatory corpus. | Local source files included formatting artifacts and one misleading local file name. | Source text was cleaned and document identity was checked against official regulation names. | Regulatory RAG needs a stable and auditable corpus before retrieval metrics are interpretable. |
| Direct article questions | Retrieved and cited the correct article for compact questions. | Some answers still omitted conditions. | Article-level indexing and completeness prompting were added. | Useful for navigation, but citations must be checked. |
| English questions over Portuguese sources | Improved after Portuguese retrieval anchors. | English completeness was initially weak. | Conservative bilingual term anchors were added. | Bilingual search is feasible but needs controlled terminology. |
| Rule-plus-exception questions | Often found the right document. | Sometimes gave the exception without the general rule. | Rule-plus-exception failures were tracked separately. | Regulatory answers must preserve legal structure. |
| Long-list questions | Often found the right article. | Omitted one element, condition, or deadline. | Answer-completeness checks were added. | Average metrics can hide operationally important omissions. |
| False-premise questions | Could correct the premise and cite evidence. | Automated labels could confuse false premise with refusal. | False-premise questions were kept as a separate category. | These questions should not be merged with ordinary unanswerable questions. |
| Current or operational facts outside corpus | Refused after calibration. | Earlier system answered from nearby general text. | A stricter refusal rule and separate refusal test were added. | Refusal calibration is central for regulatory safety. |
| AI-authored prospective-test questions | Confirmed strong answerable-question behavior. | Refusal correctness dropped to 0.700. | Refusal was repaired using separate development data. | AI-authored prospective testing changed the project story. |

## Supplementary Table S2. Expanded representative answer outcomes

| Question type | Example question | System behavior | Interpretation |
|---|---|---|---|
| Correct answer, pharmacovigilance | Which minimum information makes a notification valid and reportable? | Retrieved RDC 406/2020, Art. 32 and listed the minimum elements. | Correct source and correct main answer. |
| Correct false-premise handling | Is a notification valid without patient identification if the suspected medicine is named? | Answered no and cited RDC 406/2020, Art. 32. | Useful because it corrected the premise. |
| Correct clinical-trial safety answer | Does possible SUSAR reporting allow unblinding all participants? | Answered no; unblinding is limited to the affected participant and cited RDC 945/2024, Art. 67. | Correct and relevant to trial conduct. |
| Correct refusal | What is the current MedDRA version required today? | Refused because the indexed documents mention MedDRA but not the current required version. | Appropriate refusal for current operational information. |
| Correct refusal | What is the current phone number for Anvisa support for the adverse-event notification system? | Refused because the corpus does not contain current support contact information. | Appropriate evidence boundary. |
| Incomplete answer | What information must appear for non-printed instructions for use? | Retrieved RDC 751/2022, Art. 51 but omitted that instructions must remain available while the product is on the market. | Correct article, incomplete answer. |
| Incomplete answer | Can a foreign-manufactured biological product be registered without registration in the manufacturing country? | Gave the exception but did not clearly state the general rule. | Risk of treating an exception as the whole rule. |
| False refusal | Under RDC 945/2024, until when must DSURs be sent to Anvisa and what is the annual reference date? | Refused in one English prospective-test row although the corpus contained the answer. | Retrieval or answer threshold failure. |
| Refusal failure before calibration | What is the current electronic form model for notifying SUSARs to Anvisa? | Earlier AI-authored prospective testing sometimes answered with the general electronic-notification requirement. | Related context was mistaken for sufficient evidence. |

## Supplementary Table S3. Evaluation-stage summary

| Stage | Main finding | Use in interpretation |
|---|---|---|
| Initial held-out evaluation | English completeness was the weak point; some answers omitted list items, conditions, or exceptions. | Development diagnosis. |
| Post-repair internal evaluation | High internal scores showed that the repaired system passed the curated benchmark. | Internal technical check, not independent validation. |
| AI-authored prospective stress test | Answerable questions were mostly supported, but refusal behavior was weak. | Diagnostic prospective evidence that changed the project focus. |
| Refusal-focused AI-authored test | Refusal improved after separate calibration, with no over-refusal on answerable controls. | Focused AI-authored check of refusal calibration. |

## Supplementary Table S4. Main-table disposition after revision

| Original table | Revision decision | Reason |
|---|---|---|
| Table 1. Regulatory domains represented in the corpus | Replaced with a shorter corpus-and-use-case table. | Reduces page splitting and overlaps less with Figure 2. |
| Table 2. Question categories and corrective actions | Condensed in the main text and expanded as Supplementary Table S1. | Full version was too dense for the main manuscript. |
| Table 3. Representative examples | Condensed in the main text and expanded as Supplementary Table S2. | Keeps the story visible while moving audit-level detail to the supplement. |
| Table 4. Summary of evaluation stages | Removed from the main text and moved to Supplementary Table S3. | Redundant with Figure 3A and Figure 3B. |

## Supplementary Table S5. Decision trace from course notebooks to final ANVISA RAG

| Stage | Local evidence | Main decision | Reason | Effect on final system |
|---|---|---|---|---|
| Course notebook 1: local LLM | Course notebook file and repository copy `notebooks/1_LLM.ipynb` | Start from a Python project pattern with environment.yml, .env, src/config.py, src/model_loader.py, src/engine.py, and main.py. | The course notebook provided a simple, reproducible local LLM scaffold. | The final project kept the separated configuration, model-loading, engine, and app structure. |
| Course notebook 2: chatbot | Course notebook file and repository copy `notebooks/2_chatbot.ipynb` | Add a chat interface and system prompt rather than a one-shot completion loop. | The target use case was question answering by regulatory users. | The final app kept an interactive Streamlit question-answer interface, although the final evaluation used scripted runs. |
| Course notebook 3: generic RAG | Course notebook file and repository copy `notebooks/3_rag.ipynb` | Replace the demonstration corpus with selected ANVISA text files. | The project idea was to adapt the teaching RAG workflow from a generic text example to regulatory documents. | The data folder became a closed ANVISA corpus rather than an open web or general-document system. |
| Borrowed Shenia source | src_RAG_Shenia/engine.py in the recovered project | Test a stronger RAG pattern using semantic splitting, HyDE, reranking, and chat memory. | The borrowed source worked in another project and showed useful retrieval options beyond the teacher notebook. | Some ideas were retained conceptually, especially reranking, but HyDE/semantic splitting/chat memory were not the final regulatory design. |
| First ANVISA implementation | Recovered ANVISA RAG project folder and Codex recovered copy | Build an ANVISA Streamlit app with LlamaIndex, local embeddings, Gemini, and indexed ANVISA text files. | The original DSAI2 project folder was later moved; the recovered project contains the app, ANVISA data, cleaned_data, evaluation notebooks, and vector stores. | This is the local ancestor of the publication repository. |
| Environment failure | Early app traceback: ModuleNotFoundError for llama_index | Treat dependency setup as part of reproducibility rather than an incidental app problem. | The app could not run without the correct conda/Python environment and LlamaIndex packages. | Methods now report Python version, packages, and implementation files. |
| Corpus cleaning | scripts/clean_regulatory_texts.py and reports/cleaned_data_audit.csv | Create raw-to-cleaned source processing before indexing. | Regulatory text exported from web/PDF-like sources contained markup and boilerplate. | The final corpus is indexed from cleaned text, with source links and checksums supplied for reproducibility. |
| Article-aware indexing | src/article_chunking.py and reports/article_chunk_audit.json | Use one article per chunk when possible, with document and article metadata. | Regulatory questions usually map to articles, not arbitrary token windows. | The final index contains 382 detected articles and 481 chunks. |
| Hybrid retrieval | src/retrieval.py | Combine dense retrieval and BM25, then merge candidates by reciprocal rank fusion. | Exact terms such as RDC 945/2024, DDCM, DEEC, Art. 33, and IN 338 matter in legal/regulatory text. | Dense and keyword retrieval are both reported and auditable. |
| Reranking | src/retrieval.py and src/config.py | Retrieve more candidates and rerank down to the final answer context. | Early retrieval could find broadly related but not exact passages. | The final answer context uses top reranked passages rather than only raw vector similarity. |
| English questions over Portuguese sources | src/model_loader.py and evaluation/compare_rewrite_runs.py | Add conservative Portuguese retrieval anchors while preserving regulatory terms. | English completeness was weak in the first held-out evaluation. | Bilingual access is supported, but language-specific metrics are reported separately. |
| Answer rules | src/prompts.py and evaluation/answer_quality.py | Require article citations and refusal when retrieved evidence is insufficient. | Correct source retrieval did not guarantee complete or safe answers. | Citation correctness, completeness, and refusal correctness became primary endpoints. |
| AI-judge evaluation | evaluation/publication_eval.py and Supplementary Methods | Use an automated judge because two independent experts were not available. | The project was performed by one researcher. | The claim is limited to technical evaluation; AI judging is not presented as expert validation. |
| Stress testing after high internal scores | prospective-test output files | Run an AI-authored prospective stress test after internal metrics became high. | Perfect-looking internal scores could reflect saturation, targeted repairs, or same-model-family judging. | The stress test exposed refusal weakness and changed the project interpretation. |
| Refusal calibration | refusal-development files and refusal-focused AI-authored test | Repair refusal on separate development data, then test a new refusal-focused set. | The first prospective test showed that nearby related text could trigger unsupported answers. | Refusal correctness improved, but answerable-control completeness showed a trade-off. |


## Supplementary Table S6. Investigation of saturated internal metrics

| Observation | Why it was suspicious | Investigation performed | Interpretation for reliability |
|---|---|---|---|
| Internal refusal correctness reached 1.000 on curated unanswerable rows. | The rows were part of a benchmark built during the project and evaluated after targeted repair. | A separate AI-authored prospective stress test was run once after the pipeline was frozen. | The perfect internal value was not treated as proof of general refusal reliability. |
| Several post-repair means approached 1.000. | The repair sets were not paired repeats of the same baseline set and were created after error review. | Figure 3A labels these as development-stage results, not statistical before-after proof. | The values document that specific failure modes were repaired under controlled conditions. |
| Prospective answerable rows still showed faithfulness of 1.000. | Faithfulness can saturate when answers are short and tightly tied to retrieved articles. | Completeness, citation correctness, source MRR, article Recall@5, and examples were reported beside faithfulness. | Faithfulness alone is insufficient; incomplete answers remain possible even with supported claims. |
| The first prospective stress test had refusal correctness of 0.700. | This contradicted the internal refusal value of 1.000. | Failure review showed answers based on nearby general rules when the exact current or operational fact was absent. | This was the main evidence that internal 1.000 metrics were inflated or at least too narrow. |
| The refusal-focused AI-authored test improved refusal correctness to 0.944. | A high post-calibration score can also be overinterpreted. | Answerable controls were included and their completeness was reported at 0.908. | The final claim is bounded: refusal improved, but completeness trade-offs and closed-corpus limits remain. |
| The answer model and judge used the same model family. | Same-model-family grading can overestimate quality. | The manuscript reports this as a limitation and provides per-question outputs for audit. | The AI judge supports reproducibility, not independent expert validation. |
