# Supplementary Methods and Prompts

Title: Bilingual Retrieval-Augmented Access to ANVISA Regulatory Documents

Prepared: 2026-07-20

## Purpose

This file provides reproducibility details that are too technical for the main manuscript. It documents corpus processing, article-aware chunking, retrieval, reranking, bilingual query support, generation prompts, refusal rules, evaluation metrics, and automated judging. Source files used to verify these details are included in `evidence_artifacts/code/`.

## Software Files Used for Reproducibility

| File | Role |
|---|---|
| `evidence_artifacts/code/config.py` | Models, paths, chunking constants, retrieval constants, reranker constants |
| `evidence_artifacts/code/prompts.py` | Final answer-generation prompt |
| `evidence_artifacts/code/retrieval.py` | Hybrid retrieval, BM25 tokenization, rank fusion, cross-encoder reranking, anchors |
| `evidence_artifacts/code/publication_eval.py` | Evaluation loop, generation loop, metrics exported to CSV, run manifests |
| `evidence_artifacts/code/answer_quality.py` | Citation extraction, citation validation, AI-judge prompt |
| `evidence_artifacts/code/evaluation_statistics.py` | Article retrieval metrics and bootstrap confidence intervals |

## Corpus Processing

The source corpus consisted of six selected ANVISA regulatory documents. The files were processed into cleaned plain-text files before indexing. Cleaning removed HTML/MHTML markup residue, page boilerplate, and formatting artifacts while preserving article labels and regulatory structure. The final cleaned corpus was the only source used for retrieval and answer generation.

The closed-corpus design was intentional. The system did not search live ANVISA pages, submission portals, current form repositories, fee tables, private company records, or documents outside the local index. A question asking for information outside the indexed documents was treated as unanswerable, even when it was regulatory in topic.

Source verification identified one metadata issue: the local file name `RDC_406_2020_Estudos_de_Estabilidade.txt` suggested stability studies, but the document content was RDC 406/2020 on pharmacovigilance. All manuscript and supplement tables therefore describe that document by official regulation number and topic.

## Article-Aware Chunking

The final index used article-aware chunking rather than arbitrary fixed-size chunks. The target unit was one regulatory article per chunk when possible. Nearby chapter, section, document, and citation metadata were retained with each chunk.

Chunking constants:

| Setting | Value |
|---|---:|
| Single-article chunk maximum | 500 tokens |
| Long-article chunk size | 400 tokens |
| Long-article overlap | 60 tokens |
| Embedding maximum length | 512 tokens |

Final index audit:

| Measure | Value |
|---|---:|
| Source documents | 6 |
| Detected articles | 382 |
| Total chunks | 481 |
| Single-chunk articles | 359 |
| Long articles split into multiple chunks | 23 |
| Split chunks from long articles | 150 |
| Median chunk length | 155 tokens |
| Maximum chunk length | 503 tokens |
| Chunks above 700 tokens | 0 |

## Embeddings and Vector Index

The embedding model was `sentence-transformers/all-MiniLM-L6-v2`. In the final package, the model path was recorded from the local cache:

`models--sentence-transformers--all-MiniLM-L6-v2/snapshots/c9745ed1d9f207416be6d2e6f8de32d1f16199bf`

The vector store was rebuilt after corpus cleaning and article-aware chunking. The pipeline manifest recorded 382 articles, 481 chunks, and six sources.

## Hybrid Retrieval

The final retriever combined dense vector retrieval and keyword retrieval.

Retrieval settings:

| Setting | Value |
|---|---:|
| Dense vector candidate depth | 100 |
| BM25 candidate depth | 100 |
| Rank-fusion candidate depth | 100 |
| Reciprocal-rank-fusion constant | 60 |
| Final reranked passages sent to answer model | 5 |
| Reranker batch size | 8 |

BM25 used normalized lexical tokens. Text was normalized by removing accents, lowercasing, and extracting alphanumeric tokens. BM25 was applied to searchable text that combined chunk text and metadata fields, including regulation identifier, document aliases, document title, citation label, chapter, section, and topics.

Dense and BM25 candidates were merged with reciprocal rank fusion:

`score = sum(1 / (60 + rank))`

Candidates were sorted by fused score and then reranked.

## Reranking

The reranker was `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`. In the final local cache, the model path was:

`models--cross-encoder--mmarco-mMiniLMv2-L12-H384-v1/snapshots/1427fd652930e4ba29e8149678df786c240d8825`

The reranker scored pairs of query text and searchable node text. The top five reranked passages were used to build the answer context.

Additional deterministic anchors were used for specific regulatory patterns:

- Source-identification questions could force an Article 1/source-scope anchor when the question asked which document covered a topic.
- Named regulation scope questions could anchor the corresponding regulation's Article 1.
- Certain exact legal patterns added a targeted anchor when previous development runs showed that the relevant article could be missed by generic reranking.
- Neighbor articles were added for selected scope, definition, exemption, responsibility, and medical-device questions when adjacent articles were likely to be needed for completeness.

These anchors were rule-based retrieval aids. They did not add facts to the answer. The answer model still had to use retrieved context and article citations.

## English Query Support

English questions were answered in English, but retrieval was allowed to include Portuguese anchors because the source documents were in Portuguese. The original question remained visible to the answering model. Conservative terminology anchors were used for regulatory terms:

| English term | Portuguese retrieval anchor |
|---|---|
| clinical trial | ensaio clinico |
| sponsor | patrocinador |
| biological product | produto biologico |
| medical device | dispositivo medico |
| stability study | estudo de estabilidade |
| pharmacovigilance | farmacovigilancia |

The purpose was retrieval support, not translation of the benchmark answer.

## Answer Model

The answer model was `models/gemini-flash-lite-latest`. Generation used the retrieved context and the original question. The answer had to be in the same language as the question. Answers were post-processed only to normalize article citation brackets when the answer added paragraph or item suffixes to a retrieved article-level citation.

## Final Answer Prompt

The final answer prompt was:

```text
You are an ANVISA regulatory evidence assistant. Answer the question using only the
retrieved context below.

Rules:
1. Do not use outside knowledge or infer facts not stated in the context.
2. Answer in the same language as the question.
   The retrieved context may be Portuguese; still answer in English when the
   question is English.
   If the question is written in Portuguese, answer in Portuguese. Do not
   translate Portuguese questions into English.
3. Cite every material statement inline using the context's citation_label exactly,
   formatted in square brackets, for example [RDC 945/2024, Art. 23].
   Put each citation in its own pair of brackets.
   Do not add paragraph, item, section, page, or line suffixes unless they are part
   of the retrieved citation_label itself.
   Every non-refusal answer must include at least one citation containing "Art.";
   do not rely only on a preamble or document-level citation when article evidence
   is available.
4. Never invent a document number, article, section, deadline, or requirement.
5. If the context does not contain enough evidence to answer the exact question,
   respond only with the appropriate sentence below and do not add a citation:
   Portuguese: Os documentos recuperados nao fornecem informacao suficiente para responder.
   English: The retrieved documents do not provide enough information to answer.
   Treat related-but-incomplete context as insufficient. Do not substitute a nearby
   general rule, procedure, system name, deadline, definition, or article when the
   question asks for a more specific fact that is absent.
   This includes questions asking for current forms, form models, exact URLs,
   current fees or values, private contract terms, company-specific submission
   status, personal contact information, market prices, reimbursement, taxes,
   patents, future approvals, or advice that is not explicitly stated in the
   retrieved regulatory text.
6. Before answering, silently classify the retrieved evidence as one of:
   sufficient: it directly answers every material part of the question;
   partial_related: it discusses the topic but omits the requested specific fact;
   insufficient: it does not contain relevant evidence.
   Answer only when evidence is sufficient. For partial_related or insufficient,
   return only the refusal sentence from rule 5.
7. For yes/no or false-premise questions, answer with a cited negative only when
   the retrieved context directly contradicts the premise. Use "Nao" for
   Portuguese questions and "No" for English questions. If the context merely
   lacks the premise or does not address it, use the refusal sentence instead.
8. Prefer a concise direct answer, but answer every material part of the question.
   Include deadlines, formats, lists of required documents, conditions,
   exceptions, and consequences when the question asks for them and the context
   provides them.
   When the relevant article contains numbered items, lettered subitems, or
   paragraphs such as I, II, III, a), b), §1, §2, read the whole retrieved
   article before answering. For "what documents", "what information", "which
   are excluded", "which are exempt", or similar list questions, include every
   relevant category from the retrieved article. You may group related items to
   stay concise, but do not omit early or later items from the same article.
9. When the question asks which regulatory document covers a topic, matching article
   text plus its regulation_id or citation_label is sufficient evidence to name that
   document. Cite the most directly relevant retrieved article.
10. For purpose or scope questions, supplement preamble evidence with relevant
   objective, scope, or definitions articles when they are retrieved.

Final validation: unless the response is the refusal sentence or answers a publication
date found only in the preamble, it is invalid if it does not contain the literal text
", Art." inside at least one square-bracket citation. Revise it using retrieved article
evidence before returning it. Never invent an article citation for preamble-only facts.

Retrieved context:
---------------------
{context_str}
---------------------

Question: {query_str}
Answer:
```

## Refusal Rule

The refusal sentence was language-specific:

| Question language | Refusal sentence |
|---|---|
| Portuguese | Os documentos recuperados nao fornecem informacao suficiente para responder. |
| English | The retrieved documents do not provide enough information to answer. |

Refusal was required when context was absent, irrelevant, or only partially related. The final prompt explicitly classified related-but-incomplete evidence as insufficient. This was added because the first AI-authored prospective stress test showed that the system sometimes answered current operational questions from nearby general regulatory text.

## Benchmark Design

The 200-question benchmark contained 100 bilingual pairs and 200 rows:

| Bucket | Count |
|---|---:|
| Portuguese answerable | 70 |
| English answerable | 70 |
| Multi-article or exception | 20 |
| Unanswerable or adversarial | 40 |

Language counts were balanced: 100 Portuguese rows and 100 English rows. The benchmark audit recorded 78 unique gold article citations. Portuguese and English members of each pair shared the same data split to avoid leakage across languages.

Split counts:

| Split | Rows |
|---|---:|
| Held-out test | 75 |
| Calibration | 20 |
| Development remainder | 5 |

The AI-authored prospective stress test contained 50 questions, organized as 25 bilingual pairs. The refusal-focused AI-authored test contained 30 questions, organized as 15 bilingual pairs.

## Evaluation Outputs

For each row, the evaluation script saved:

- question id
- pair id
- language
- category
- answerability
- gold source documents
- gold articles
- gold citations
- raw vector sources and citations
- BM25 sources and citations
- fused sources and citations
- final retrieved sources and citations
- retrieval query and rerank query
- rewrite status
- answer text
- answer citations
- refusal detection
- citation validity
- answer term coverage
- AI-judge scores when judging was enabled

Manual-review templates were also exported with fields for human source correctness, groundedness, completeness, citation correctness, safety/refusal correctness, error type, and comments. These were retained as audit scaffolds even though the final evaluation used AI judging only.

## Retrieval Metrics

Source-level metrics:

- source hit: whether any gold source document was retrieved in the evaluated top-k
- source MRR: reciprocal rank of the first gold source document

Article-level metrics:

- article Recall@k: fraction of gold article citations retrieved in top-k
- article Precision@k: fraction of top-k retrieved citations that were gold citations
- article MRR@k: reciprocal rank of first gold citation
- article nDCG@k: ranking quality for gold citation placement

Gold and retrieved labels were normalized by lowercasing, removing accents, and collapsing whitespace before comparison.

## Answer Metrics

Answer-level metrics:

- citation presence: whether the answer contained a recognized bracketed citation
- citation retrieved validity: fraction of citation-like brackets matching retrieved citation labels
- article citation presence: whether at least one answer citation contained an article label
- answer term coverage: fraction of expected answer terms found in the generated answer
- refusal detected: whether the answer matched the defined refusal patterns

## Operational Failure Thresholds

The primary reported metrics were continuous means. They were not converted into a single binary success claim for the manuscript. The evaluation code nevertheless used operational flags to identify rows requiring review:

| Audit condition | Flag used |
|---|---|
| Answerable row with no retrieved gold source | `wrong_or_missing_source` |
| Answerable row with article Recall@k below 1.0 | `incomplete_article_retrieval` |
| Retrieved expected-term coverage below 0.50 | `low_evidence_term_coverage` |
| Answerable row that returned the refusal sentence | `incorrect_refusal` |
| Answerable row without a recognized citation | `missing_citation` |
| Citation-like label not present among retrieved citation labels | `unsupported_or_unretrieved_citation` |
| Generated answer-term coverage below 0.50 | `incomplete_answer` |
| AI-judge faithfulness below 0.80 | `judge_flagged_unfaithful` |
| Unanswerable row without literal refusal detection | `failed_to_refuse` |

The English completeness diagnostic experiment used AI-judge completeness below 0.80 to identify low-completeness answerable English rows. These thresholds were used for technical error analysis and targeted repair. They were not regulatory acceptance criteria.

## Automated AI Judge

The automated judge used `models/gemini-flash-lite-latest` with temperature 0.0. It received the question, system answer, expected answer, answerability flag, and retrieved evidence, then returned four numeric scores from 0 to 1: faithfulness, citation correctness, completeness, and refusal correctness. The judge was used as a structured technical scoring tool, not as an independent regulatory expert panel. The answer model and automated judge used the same Gemini model family, so same-model-family grading may overestimate answer quality.

The exact judge prompt, scoring definitions, model settings, row-level scores, rationales, and stage-level summaries are provided only in Supplementary Data 2 to avoid duplication across supplementary files.

## Confidence Intervals

When confidence intervals were reported, the method was pair-clustered percentile bootstrap:

| Setting | Value |
|---|---:|
| Confidence level | 95% |
| Resamples | 2000 |
| Seed | 20260619 |
| Cluster key | bilingual pair id |

Pair clustering was used because Portuguese and English questions were written as paired items.

## Reproducibility Boundary

The package supports reproduction of the reported technical evaluation if the same code, corpus files, model identifiers, benchmark files, API model behavior, and package versions are available. A conda environment export and pip freeze file are included as environment.lock.yml and requirements-freeze.txt. Exact generated answers may still vary because hosted LLM behavior can change over time even when the model name and prompt are fixed. The archived per-question CSVs are therefore part of the evidence record and should be used to audit the reported results.
