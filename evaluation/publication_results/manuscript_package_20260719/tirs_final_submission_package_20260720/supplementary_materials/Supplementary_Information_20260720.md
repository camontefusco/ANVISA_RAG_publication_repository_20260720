# Supplementary Information

Title: Bilingual Retrieval-Augmented Access to ANVISA Regulatory Documents

Prepared: 2026-07-20

## Supplementary File 1. Corpus and preprocessing

The indexed corpus was a closed collection of six ANVISA regulatory documents. The system did not search current web pages, portals, fee schedules, private submission systems, or documents outside the index.

| Regulation | Local file | Topic | Cleaned characters | Chunks | Notes |
|---|---|---|---:|---:|---|
| RDC 945/2024 | RDC_945_2024.txt | Clinical trials | 71,857 | 123 | Clinical-trial procedure and safety reporting |
| RDC 9/2015 | rdc09_2015.txt | Clinical trials | 53,346 | 107 | Earlier clinical-trial regulation |
| RDC 55/2010 | RDC_55_2010_Registro_de_Produtos_Biologicos.txt | Biological products | 43,062 | 69 | Biological-product registration |
| RDC 751/2022 | RDC_751_2022_Regras_de_classificacao_de_risco.txt | Medical devices | 80,024 | 102 | Classification, labelling, instructions |
| RDC 406/2020 | RDC_406_2020_Estudos_de_Estabilidade.txt | Pharmacovigilance | 39,879 | 61 | Local file name was misleading; document content is pharmacovigilance |
| IN 338/2024 | IN_338_2024.txt | Optimized review/reliance | 14,450 | 19 | Equivalent foreign regulatory authorities |

The final article-aware index contained 382 detected articles and 481 chunks. The chunk audit recorded 359 single-chunk articles and 23 long articles split into multiple chunks. The median chunk length was 155 tokens, the largest chunk was 503 tokens, and no chunk exceeded 700 tokens.

Cleaning converted source files to plain text, removed page and markup residue, preserved article labels, and rebuilt the index with metadata for document name, article number, citation label, source file, and chunk identifier. Source verification found one local-file metadata mismatch: the file name suggested stability studies, while the content was RDC 406/2020 on pharmacovigilance. The manuscript and supplement therefore describe the corpus using official regulation names and topics rather than local file names.

## Supplementary File 2. Retrieval and generation configuration

The final retrieval pipeline used article-aware chunks. One regulatory article was kept as one chunk when possible. Long articles were split into approximately 400-token chunks with 60-token overlap. The dense embedding model recorded in the chunk audit was sentence-transformers/all-MiniLM-L6-v2, loaded from the local model cache. Retrieval used semantic retrieval plus keyword/BM25 retrieval for exact regulatory terms, including DDCM, RDC numbers, article numbers, IN 338/2024, and Portuguese legal terms. Candidate passages were merged and reranked before answer generation.

English questions were supported with conservative Portuguese retrieval anchors. The original question language was preserved for response generation, but retrieval included term anchors such as clinical trial/ensaio clinico, sponsor/patrocinador, biological product/produto biologico, medical device/dispositivo medico, stability study/estudo de estabilidade, and pharmacovigilance/farmacovigilancia.

The final answer prompt required a direct answer, article-level citation, and refusal when the retrieved context did not contain the requested fact. The refusal rule was tightened after the first AI-authored prospective stress test because the system sometimes answered current operational questions from related but insufficient regulatory text.

Full reproducibility details, including exact retrieval constants, model identifiers, final answer prompt, refusal wording, AI-judge prompt, and metric definitions, are provided in `Supplementary_Methods_and_Prompts_20260720.md`. The relevant source files are archived in `evidence_artifacts/code/`.

## Supplementary File 3. Benchmark dataset documentation

The main benchmark contained 200 bilingual questions:

- 70 Portuguese answerable questions
- 70 English answerable questions
- 20 multi-article or exception questions
- 40 unanswerable or adversarial questions

Questions covered clinical trials, SUSAR handling, DSUR timing, pharmacovigilance notification validity, biological-product registration exceptions, medical-device instructions for use, reliance pathways, false premises, and current operational facts outside the corpus. Answerable questions included expected document and article labels. Unanswerable/adversarial questions were expected to trigger refusal.

Benchmark source files, split manifests, and checksums are included in the evidence-artifact folder.

## Supplementary File 4. Evaluation metrics and AI judge

Retrieval metrics included source hit rate, source mean reciprocal rank, and normalized article Recall@5. Answer metrics included citation presence, citation validity, answer term coverage, faithfulness, citation correctness, completeness, and refusal correctness. For unanswerable questions, the desired behavior was refusal rather than answer generation.

Automated judging was used because an independent expert panel was not available. The judge assessed whether the answer was supported by retrieved evidence, whether the cited document and article matched the support, whether material answer elements were present, and whether refusal was appropriate. AI-judge results are technical scoring with audit trails, not expert regulatory validation.

Supplementary Data S2 reports the automated AI-judge layer as a separate audit file. It identifies which questions were judged, the four scoring criteria, model settings, the exact prompt template, row-level scores and rationales, stage-level metrics, and the conclusions and recommendations drawn from each stage. It also documents the interpretive boundary: AI-judge scores are reproducible technical screening outputs, not expert regulatory validation.

## Supplementary File 5. Representative questions and per-question results

Supplementary Data S1 provides a consolidated per-question audit table for the reported evaluation rows. It contains 404 evaluated rows across six stages: 150 internal held-out rows, 75 English completeness-repair rows, 75 Portuguese residual-quality rows, 50 AI-authored prospective stress-test rows, 24 refusal-calibration development rows, and 30 refusal-focused AI-authored test rows. The table includes the question, generated answer, expected answer fields when available, retrieval and citation outputs, deterministic metrics, AI-judge scores, detected error flags, and the fix or action linked to each row. The 404 evaluated rows should not be described as a 500-question evaluation. The authored question files contain 304 rows because some development and test stages evaluate overlapping question types rather than one single independent question bank.

The evidence-artifact folder contains per-question CSV outputs for the held-out internal benchmark, English completeness repair, Portuguese residual-quality repair, first AI-authored prospective stress test, refusal-development run, and refusal-focused AI-authored prospective test. These files include question identifiers, language, category, expected source or article fields when present, generated answers, retrieved evidence fields, and scoring fields.

The main manuscript reports representative correct answers, incomplete answers, false refusals, and refusal failures. Expanded decision-history, example, and stage-summary tables are provided in `Supplementary_Tables_20260720.md`. The CSV files should be retained with the supplement so readers can audit which questions produced each result category.

## Supplementary File 6. Development history and decision log

The development-results story table and TIRS decision-rationale file document the repair sequence: initial application/dependency diagnosis, corpus cleaning, article-aware indexing, hybrid retrieval, reranking, English retrieval anchors, answer-completeness repair, Portuguese residual-quality review, AI-authored prospective stress testing, refusal calibration, and final pipeline freeze.

Internal post-repair scores should not be interpreted as independent proof of generalization. They show that the repaired system passed its curated benchmark. The first AI-authored prospective stress test changed the interpretation by showing that refusal calibration was the main remaining weakness. The second refusal-focused AI-authored prospective test evaluated that repair using a separate AI-authored prospective question set.

## Supplementary File 7. Methods and prompts for reproducibility

`Supplementary_Methods_and_Prompts_20260720.md` contains the expanded methods and prompt documentation requested for journal reproducibility review. It includes article-aware chunking settings, dense and BM25 retrieval settings, reciprocal rank fusion, cross-encoder reranking, English query anchors, final answer prompt, refusal prompt, AI-judge prompt, metric definitions, bootstrap confidence-interval settings, and the reproducibility boundary for hosted LLM outputs.
