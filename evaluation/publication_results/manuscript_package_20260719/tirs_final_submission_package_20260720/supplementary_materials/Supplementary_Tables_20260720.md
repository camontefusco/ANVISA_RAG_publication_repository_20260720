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
| External stress-test questions | Confirmed strong answerable-question behavior. | Refusal correctness dropped to 0.700. | Refusal was repaired using separate development data. | External testing changed the project story. |

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
| False refusal | Under RDC 945/2024, until when must DSURs be sent to Anvisa and what is the annual reference date? | Refused in one English external-test row although the corpus contained the answer. | Retrieval or answer threshold failure. |
| Refusal failure before calibration | What is the current electronic form model for notifying SUSARs to Anvisa? | Earlier external testing sometimes answered with the general electronic-notification requirement. | Related context was mistaken for sufficient evidence. |

## Supplementary Table S3. Evaluation-stage summary

| Stage | Main finding | Use in interpretation |
|---|---|---|
| Initial held-out evaluation | English completeness was the weak point; some answers omitted list items, conditions, or exceptions. | Development diagnosis. |
| Post-repair internal evaluation | High internal scores showed that the repaired system passed the curated benchmark. | Internal technical check, not independent validation. |
| External stress test | Answerable questions were mostly supported, but refusal behavior was weak. | Diagnostic external evidence that changed the project focus. |
| Refusal-focused external test | Refusal improved after separate calibration, with no over-refusal on answerable controls. | Focused external check of refusal calibration. |

## Supplementary Table S4. Main-table disposition after revision

| Original table | Revision decision | Reason |
|---|---|---|
| Table 1. Regulatory domains represented in the corpus | Replaced with a shorter corpus-and-use-case table. | Reduces page splitting and overlaps less with Figure 2. |
| Table 2. Question categories and corrective actions | Condensed in the main text and expanded as Supplementary Table S1. | Full version was too dense for the main manuscript. |
| Table 3. Representative examples | Condensed in the main text and expanded as Supplementary Table S2. | Keeps the story visible while moving audit-level detail to the supplement. |
| Table 4. Summary of evaluation stages | Removed from the main text and moved to Supplementary Table S3. | Redundant with Figure 3A and Figure 3B. |
