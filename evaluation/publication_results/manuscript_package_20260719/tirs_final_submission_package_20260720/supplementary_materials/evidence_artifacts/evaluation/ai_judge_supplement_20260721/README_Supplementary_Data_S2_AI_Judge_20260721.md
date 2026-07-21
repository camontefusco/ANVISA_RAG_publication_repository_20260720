# Supplementary Data S2. AI-Judge Results

This supplement documents the automated AI-judge evaluation layer used in the ANVISA RAG project.

## Files

- `Supplementary_Data_S2_AI_Judge_Per_Question_404_rows_20260721.csv`: row-level AI-judge results for the reported 404-row evaluation audit.
- `Supplementary_Data_S2_AI_Judge_Stage_Summary_20260721.csv`: stage-level AI-judge metrics and interpretations.
- `Supplementary_Data_S2_AI_Judge_Criteria_and_Prompt_20260721.md`: judge criteria, thresholds, model settings, and exact prompt template.
- `Supplementary_Data_S2_manifest_20260721.json`: file paths and SHA-256 checksums.

## What the AI judge analyzed

The judge analyzed the same reported evaluation rows used in Supplementary Data S1: internal held-out answers, English completeness repair rows, Portuguese residual-quality repair rows, the AI-authored prospective stress test, refusal-calibration development rows, and the second refusal-focused AI-authored test. The total reported AI-judge table contains 404 rows.

Stage summary:

- S1_internal_heldout: 150 judged rows; completeness 0.807; refusal correctness 1.000.
- S2_english_completeness_repair: 75 judged rows; completeness 0.995; refusal correctness 1.000.
- S3_portuguese_residual_quality_repair: 75 judged rows; completeness 0.995; refusal correctness 1.000.
- S4_ai_authored_prospective_stress_test: 50 judged rows; completeness 0.943; refusal correctness 0.700.
- S5_refusal_calibration_development: 24 judged rows; completeness 1.000; refusal correctness 0.938.
- S6_refusal_focused_ai_authored_test: 30 judged rows; completeness 0.908; refusal correctness 0.944.

## Main conclusions

- The initial held-out judge run found strong faithfulness and citation correctness but weak English completeness.
- Targeted English repair improved completeness, which justified reporting the repair as a development step rather than hiding the weakness.
- Saturated internal scores were not treated as proof of perfect reliability.
- The first external stress test identified refusal calibration as the main residual weakness.
- A second refusal-focused test showed improved refusal correctness after prompt calibration, with boundary cases still requiring monitoring.

## Recommendation for publication

Report the AI-judge layer as supplementary automated validation and diagnostic evidence. Do not describe it as expert validation. The strongest defensible claim is that AI judging helped identify and quantify answer completeness and refusal-calibration failures, guided targeted repair, and documented residual limitations.
