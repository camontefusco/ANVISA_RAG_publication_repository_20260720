# Supplementary technical information draft

This document is intended to absorb the technical material that should not dominate the main TIRS manuscript.

## Supplementary File 1. Corpus and preprocessing

Content to include:

- source document list
- official regulation names
- local file names
- cleaned character counts
- article counts
- chunk counts
- source verification notes
- statement that RDC 406/2020 was treated as pharmacovigilance, not stability
- cleaning pipeline description

Suggested table:

| Regulation | Local file | Topic | Cleaned characters | Chunks | Notes |
|---|---|---:|---:|---:|---|
| RDC 945/2024 | RDC_945_2024.txt | Clinical trials | 71,857 | 123 | Clinical-trial procedure and safety reporting |
| RDC 9/2015 | rdc09_2015.txt | Clinical trials | 53,346 | 107 | Earlier clinical-trial regulation |
| RDC 55/2010 | RDC_55_2010_Registro_de_Produtos_Biologicos.txt | Biological products | 43,062 | 69 | Biological-product registration |
| RDC 751/2022 | RDC_751_2022_Regras_de_classificacao_de_risco.txt | Medical devices | 80,024 | 102 | Classification, labelling, instructions |
| RDC 406/2020 | RDC_406_2020_Estudos_de_Estabilidade.txt | Pharmacovigilance | 39,879 | 61 | File name was misleading; content is pharmacovigilance |
| IN 338/2024 | IN_338_2024.txt | Optimized review/reliance | 14,450 | 19 | Equivalent foreign regulatory authorities |

The final article-aware index contained 382 detected articles and 481 chunks overall. The audit file reports 359 single-chunk articles and 23 long articles split into multiple chunks.

## Supplementary File 2. Retrieval and generation configuration

Move the following from the main paper:

- article-level chunking rules
- chunk size and overlap
- dense retrieval model
- BM25 retrieval
- reciprocal rank fusion
- reranking
- top-k settings
- query expansion
- answer-generation model and temperature
- refusal prompt
- citation formatting rules

This file can use technical language because it is for reproducibility.

## Supplementary File 3. Benchmark documentation

Include:

- 200-question bilingual benchmark design
- category counts
- language counts
- answerable and unanswerable counts
- article-level answer keys
- gold term fields
- split manifest
- benchmark checksum

Main-paper version should only describe the benchmark in plain terms and give examples.

## Supplementary File 4. Evaluation metrics and AI judge

Include definitions for:

- source hit rate
- source MRR
- article recall
- citation presence
- citation validity
- answer term coverage
- faithfulness
- citation correctness
- completeness
- refusal correctness
- pair-clustered bootstrap confidence intervals

Include the full AI-judge rubric and the limitation that the AI judge was not an independent expert panel.

## Supplementary File 5. Representative questions and full per-question results

This is now essential. It should contain the full table of:

- question ID
- language
- category
- question
- expected source/article
- answerability
- retrieved articles
- generated answer
- score
- error category if any

The main paper should include a short version of this table with 8 to 10 examples.

## Supplementary File 6. Development history and decision log

Use `TIRS_DECISION_RATIONALE_AND_VALIDATION_HISTORY_20260719.md` as the base. It should document:

- initial non-working application
- dependency repair
- corpus cleaning
- article-aware indexing
- hybrid retrieval
- English query support
- completeness repair
- refusal calibration
- external test
- final freeze

This belongs in supplementary material, not in the main narrative.
