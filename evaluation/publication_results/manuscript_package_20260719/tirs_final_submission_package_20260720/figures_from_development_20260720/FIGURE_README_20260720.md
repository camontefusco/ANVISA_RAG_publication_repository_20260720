# Development Figure Package

These figures were generated only from archived evaluation CSV and audit JSON files in the submission package. The file `figure_metrics_source_table.csv` gives the source file, filter, calculation, numerator sum, and denominator for every plotted value.

Important caveat: development-stage panels compare successive evaluation sets, not the same fixed question set rerun at every stage. They are suitable for describing the engineering history and observed weak points, but not for claiming paired statistical improvement.

## Files

- `Figure_1_closed_corpus_rag_workflow.pdf`
- `Figure_1_closed_corpus_rag_workflow.png`
- `Figure_1_closed_corpus_rag_workflow.svg`
- `Figure_2_benchmark_design_and_source_coverage.pdf`
- `Figure_2_benchmark_design_and_source_coverage.png`
- `Figure_2_benchmark_design_and_source_coverage.svg`
- `Figure_3A_development_stage_answer_quality.pdf`
- `Figure_3A_development_stage_answer_quality.png`
- `Figure_3A_development_stage_answer_quality.svg`
- `Figure_3B_targeted_weak_point_repairs.pdf`
- `Figure_3B_targeted_weak_point_repairs.png`
- `Figure_3B_targeted_weak_point_repairs.svg`
- `Figure_S1_prospective_test_retrieval_validity.pdf`
- `Figure_S1_prospective_test_retrieval_validity.png`
- `Figure_S1_prospective_test_retrieval_validity.svg`
- `Figure_S1_prospective_test_retrieval_validity.tif`
- `Figure_S2_benchmark_composition.pdf`
- `Figure_S2_benchmark_composition.png`
- `Figure_S2_benchmark_composition.svg`
- `Figure_S3_article_chunk_distribution.pdf`
- `Figure_S3_article_chunk_distribution.png`
- `Figure_S3_article_chunk_distribution.svg`
- `additional_figure_source_table.csv`
- `build_additional_publication_figures.py`
- `build_rag_development_figures.py`
- `figure_metrics_source_table.csv`

## Source Artifacts

- `supplementary_materials/evidence_artifacts/benchmark/benchmark_200_audit.json`
- `supplementary_materials/evidence_artifacts/corpus/article_chunk_audit.json`
- `supplementary_materials/evidence_artifacts/evaluation/ai_judge_english_completeness_patch_evaluation.csv`
- `supplementary_materials/evidence_artifacts/evaluation/ai_judge_heldout_evaluation.csv`
- `supplementary_materials/evidence_artifacts/evaluation/ai_judge_portuguese_residual_quality_evaluation.csv`
- `supplementary_materials/evidence_artifacts/evaluation/external_refusal_focus_per_question.csv`
- `supplementary_materials/evidence_artifacts/evaluation/external_stress_test_per_question.csv`

## Suggested Use

- Main text: use Figure 3A or 3B only if the caption states that stages are different evaluation sets.
- Supplement: include Figure S1, Figure S2, Figure S3, and the full source table.
- Do not report a plotted value unless it is present in `figure_metrics_source_table.csv`.
- Figure S4: Streamlit RAG-answer and source-table smoke-test screenshot. Use as supplementary application evidence, not as a benchmark metric.
