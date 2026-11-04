# Supplementary Data S16 Read first

## What this dataset contains

This is the dated-corpus comparison: 188 questions in 94 Portuguese/English pairs, two corpus conditions and 376 answer records from 366 distinct generation calls. References were author-approved before generation. Output component assessments remain provisional AI judgments; later author confirmation of outputs is documented separately and does not create new independent component ratings.

The archive supports Figure 6, Supplementary Section S12 and Tables S23-S25. It does not establish comprehensive current-law accuracy, fresh independent validation or human workflow benefit. The manuscript and response letter already incorporate these analyses.

## Start with the results

1. Open 03_Answers_and_results/README_RESULTS.md for findings and limitations.
2. Open 03_Answers_and_results/metric_counts_denominators.csv for metrics and denominators.
3. Open 03_Answers_and_results/paired_comparisons_descriptive_intervals.csv for paired differences and uncertainty.
4. Open 03_Answers_and_results/answer_level_provisional_AI_assessments_376.csv for individual answers, decisions and notes.
5. Open 04_Regulatory_dependency_audit/first_level_linked_instrument_registry_111.csv for the linked-instrument audit; unresolved endpoints remain explicitly unresolved.

## Folder guide

| Folder | Contents | Intended reader |
| --- | --- | --- |
| 01_Protocol | Frozen plan, subgroup definitions, common prompt, input hashes and exact-prompt reuse map | Readers checking design |
| 02_Questions_references_and_evidence | Questions, author-approved references, excluded questions, source registry and selected contexts | Readers checking source support |
| 03_Answers_and_results | Saved answers, provisional AI assessments, summary counts, paired results and intervals | Start here for results |
| 04_Regulatory_dependency_audit | Linked-instrument registry, revoked operative-reference flags, successor evidence and audit code | Readers checking regulatory validity |
| 05_Provenance_and_limitations | Recorded model/runtime details, source checks, hypotheses and negative results | Readers checking scope and provenance |
| 06_Reproduction_code | Original scripts plus a portable recalculation entry point | Readers reproducing counts |
| 07_Historical_validation | Original completion-stage QA and earlier README, explicitly historical | Audit trail, not current submission status |

FILE_INDEX.csv lists every supplied file, its purpose and SHA-256. ORIGINAL_PATH_MAP.csv connects the earlier flat layout to the organized layout, preserving filenames and scientific bytes. Only the active results-guide status sentence was corrected. The earlier release preserves the original archive.

## Reproduce the headline counts

With Python and NumPy installed, run:

    python 06_Reproduction_code/recalculate_counts.py

This reconstructs the original relative file layout in a temporary directory under /private/tmp and runs the unmodified count-recalculation script. It makes no model calls and changes no dataset files. It should report 144/188 versus 172/188 successful answers and 69/94 versus 83/94 bilingual pairs.

The original full-study analysis script requires the original private coordination layout and is retained as historical execution provenance, not a standalone reproduction command. It must not be mistaken for the portable count script. The plotting script additionally requires Matplotlib, Pillow and Arial. Archived QA statements about work not yet integrated describe their creation date; use this guide and the current manuscript for present status.
