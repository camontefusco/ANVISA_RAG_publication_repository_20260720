# External Prospective Stress Test Interpretation

## Status

This result should be reported as an **AI-authored prospective stress test with artifact recovery**.

The first external run completed in the terminal, but after working output folders were reorganized, only a 40-row checkpoint remained in the recovered project evidence folder. The missing 10 rows were the unanswerable and adversarial block (`EXTERNAL_021` through `EXTERNAL_025`, PT and EN). Those 10 rows were regenerated once with the same frozen settings and merged with the preserved 40-row checkpoint.

No benchmark edits, retrieval edits, prompt edits, judge edits, threshold edits, or result-driven tuning were performed.

## Main Finding

The AI-authored prospective stress test does **not** support the strongest version of the internal perfect-score claim. It supports a more nuanced and publishable claim:

> The final RAG system showed strong prospective source retrieval, citation grounding, and answer faithfulness on an AI-authored AI-authored prospective stress test, but refusal behavior on unanswerable/adversarial regulatory questions remained a residual weakness.

## Key Metrics

- Questions: 50
- Bilingual pairs: 25
- Answerable questions: 40
- Unanswerable/adversarial questions: 10
- Source hit, answerable only: 1.000
- Source MRR, answerable: 0.988
- Normalized article recall@5, answerable: 0.967
- Normalized article MRR@5, answerable: 0.913
- Citation presence, answerable: 0.975
- Citation retrieved-validity, answerable: 0.975
- AI-judge faithfulness, answerable: 1.000
- AI-judge citation correctness, answerable: 0.975
- AI-judge completeness, answerable: 0.943
- Literal refusal detected, unanswerable/adversarial: 0.600
- AI-judge refusal correctness, unanswerable/adversarial: 0.700

## Language Split

English:

- Normalized article recall@5, answerable: 0.950
- Answer term coverage, answerable: 0.744
- AI-judge faithfulness, answerable: 1.000
- AI-judge completeness, answerable: 0.930
- AI-judge refusal correctness, unanswerable/adversarial: 0.800

Portuguese:

- Normalized article recall@5, answerable: 0.983
- Answer term coverage, answerable: 0.778
- AI-judge faithfulness, answerable: 1.000
- AI-judge completeness, answerable: 0.955
- AI-judge refusal correctness, unanswerable/adversarial: 0.600

## Failure Pattern

The main failure class was **refusal calibration**, not source retrieval.

Unanswerable/adversarial failures:

- `EXTERNAL_022_PT`: asked for the current electronic form model for SUSAR notification. The system answered with the general electronic notification requirement instead of saying that the specific current form model is not in the documents.
- `EXTERNAL_022_EN`: same failure pattern as the Portuguese pair.
- `EXTERNAL_025_PT`: false-premise question about notification validity without patient identification. The answer was legally correct, but the judge marked refusal behavior incorrect because the item was labeled adversarial/refusal.
- `EXTERNAL_025_EN`: technically handled the false premise correctly, but did not trigger the literal refusal detector.

Answerable completeness weaknesses:

- `EXTERNAL_003_PT`: omitted the active-search obligation when required minimum notification fields are missing.
- `EXTERNAL_011_PT`: omitted ICH E2F format for DSUR.
- `EXTERNAL_011_EN`: false refusal; the system did not answer an answerable DSUR question.
- `EXTERNAL_012_PT`: omitted the requirement to ensure instructions remain available while the product is on the market.
- `EXTERNAL_016_PT` and `EXTERNAL_016_EN`: gave the exception for foreign-made biological products but omitted the general rule.
- `EXTERNAL_019_EN`: omitted the 30-business-day deadline for sponsor response to a technical requirement.

## Metric Caveat

The raw runner article-recall fields are zero for this external set because the external gold article labels were formatted differently from the internal benchmark. The recovered report therefore includes normalized article audit columns. Use the normalized article metrics for this external test.

## Publication Interpretation

This external test is good news, but not perfect-system evidence.

The defensible publication wording is:

> In a 50-question AI-authored prospective stress test, the frozen system retrieved the correct source for all answerable questions and achieved high normalized article recall@5, citation validity, faithfulness, and completeness. However, refusal correctness dropped to 0.70 on unanswerable/adversarial questions, indicating that abstention behavior remains the principal residual limitation.

Avoid saying:

> The external test confirms perfect generalization.

## Recommendation

Do not tune from this external set if it is reported as prospective evidence. For the manuscript, report it as a stress test and list refusal calibration as the main residual limitation. If you want to improve refusal behavior next, create a second untouched external set before claiming improved prospective performance.
