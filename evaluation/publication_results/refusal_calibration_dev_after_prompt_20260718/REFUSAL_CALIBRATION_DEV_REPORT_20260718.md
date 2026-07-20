# Refusal Calibration Development Report

## Purpose

This is a development-set check created after the prospective external stress test identified refusal calibration as the main residual weakness. It must not be reported as prospective external evidence.

## Change Tested

The answer prompt now distinguishes:

- sufficient evidence: answer with citations;
- partial-related evidence: refuse;
- insufficient evidence: refuse;
- false premise directly contradicted by retrieved context: answer with a cited negative.

The prompt also explicitly warns against substituting nearby general rules when the user asks for a current form, exact URL, fee, private status, future approval, or other specific fact absent from the retrieved context.

## Development Set

- File: `evaluation/refusal_calibration_dev_24.jsonl`
- Bilingual pairs: 12
- Questions: 24
- Unanswerable/current-specific questions: 16
- False-premise answerable questions: 8
- SHA-256: `641e35f84fae2f9f14f45d86c57b6a914cd1a668fe0437b64786dd6c8873a2ab`

## Dev Results

- Refusal detected on unanswerable questions: 1.000
- AI-judge refusal correctness on unanswerable questions: 0.938
- AI-judge faithfulness on answerable false-premise questions: 1.000
- AI-judge citation correctness on answerable false-premise questions: 1.000
- AI-judge completeness on answerable false-premise questions: 1.000

## Notes

The dev run suggests the refusal prompt improved the specific failure mode observed in the external stress test. However, this is a development result and should not replace the external result. To claim improved prospective refusal behavior, freeze this updated pipeline and run a second untouched external test.

One minor prompt-polish issue was found: the first false-premise rule said to answer `No`, which led two Portuguese false-premise answers to start in English. The rule was updated after this dev run to say use `Nao` for Portuguese and `No` for English.
