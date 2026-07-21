# External Refusal-Focused Test After Prompt Calibration

## Status

This is a second, refusal-focused external test created after the first AI-authored prospective stress test identified refusal calibration as the main residual weakness and after a refusal-specific development prompt update.

It should be reported separately from:

- the original repaired internal benchmark;
- the first AI-authored prospective stress test;
- the refusal-calibration development set.

## Benchmark

- File: `evaluation/external_refusal_focus_candidate_30.jsonl`
- SHA-256: `86b59e6fe1b997e25f32aff68e111e48232145a83fe8b4299b60d2f380b1bfdf`
- Questions: 30
- Bilingual pairs: 15
- Answerable controls: 12
- Unanswerable/current-specific questions: 18

## Main Result

The updated refusal prompt substantially improved the main weakness observed in the first AI-authored prospective stress test.

- Refusal detected on unanswerable questions: 0.944
- AI-judge refusal correctness on unanswerable questions: 0.944
- AI-judge faithfulness on answerable questions: 1.000
- AI-judge citation correctness on answerable questions: 1.000
- AI-judge completeness on answerable questions: 0.908
- Refusal detected on answerable questions: 0.000

## Interpretation

The stricter refusal rule improved abstention behavior without making the system generally over-refuse answerable regulatory questions. False-premise answerable controls were answered with cited negative answers rather than refused.

The remaining error was `EXTREF_008_PT`, where the question asked for the exact penalty for inconsistent instructions of use. The model answered with the general penalties and sanitary measures described in RDC 751/2022 instead of refusing the request for an exact case-specific penalty. This is a boundary-label issue as well as a refusal issue: the retrieved article gives general penalty authority, but not a specific case penalty.

## Remaining Weakness

The main residual weakness moved from broad refusal failure to finer-grained boundary judgment:

- When the corpus gives a general enforcement consequence but not the exact requested penalty, the system may still answer with the general rule.
- Completeness on answerable controls remains lower than faithfulness/citation correctness, mainly because concise answers omit secondary clauses from the cited article.

## Publication Wording

Defensible wording:

> After refusal-prompt calibration, a second 30-question refusal-focused external test showed improved AI-judge refusal correctness (0.944) and no over-refusal on answerable controls. Residual errors involved boundary cases where the corpus contained related general enforcement provisions but not the exact requested case-specific fact.

Avoid wording:

> Refusal behavior is solved.

## Recommendation

Report refusal calibration as substantially improved but still requiring boundary-case monitoring. For publication, present the first AI-authored prospective stress test as the honest diagnostic result and this second refusal-focused AI-authored test as post-calibration evidence.
