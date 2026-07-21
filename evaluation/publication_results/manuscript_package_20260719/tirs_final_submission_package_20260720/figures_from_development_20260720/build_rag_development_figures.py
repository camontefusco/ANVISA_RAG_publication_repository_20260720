#!/usr/bin/env python3
"""Build traceable development figures from archived RAG evaluation artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT
EVIDENCE = PACKAGE / "supplementary_materials" / "evidence_artifacts"
OUT = PACKAGE / "figures_from_development_20260720"


CSV_SOURCES = {
    "internal_heldout": EVIDENCE / "evaluation" / "ai_judge_heldout_evaluation.csv",
    "english_repair": EVIDENCE / "evaluation" / "ai_judge_english_completeness_patch_evaluation.csv",
    "portuguese_repair": EVIDENCE / "evaluation" / "ai_judge_portuguese_residual_quality_evaluation.csv",
    "external_stress": EVIDENCE / "evaluation" / "external_stress_test_per_question.csv",
    "external_refusal": EVIDENCE / "evaluation" / "external_refusal_focus_per_question.csv",
}

AUDIT_SOURCES = {
    "benchmark_200_audit": EVIDENCE / "benchmark" / "benchmark_200_audit.json",
    "article_chunk_audit": EVIDENCE / "corpus" / "article_chunk_audit.json",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: str) -> bool | None:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y"}:
        return True
    if text in {"false", "0", "no", "n"}:
        return False
    return None


def numeric(value: str) -> float | None:
    parsed_bool = boolish(value)
    if parsed_bool is True:
        return 1.0
    if parsed_bool is False:
        return 0.0
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if math.isnan(number):
        return None
    return number


def mean_for(rows: list[dict[str, str]], metric: str, predicate) -> tuple[float | None, int, float]:
    values = []
    for row in rows:
        if predicate(row):
            value = numeric(row.get(metric, ""))
            if value is not None:
                values.append(value)
    if not values:
        return None, 0, 0.0
    return sum(values) / len(values), len(values), sum(values)


def row_answerable(row: dict[str, str]) -> bool | None:
    return boolish(row.get("answerable", ""))


def language_is(language: str):
    expected = language.lower()

    def _predicate(row: dict[str, str]) -> bool:
        return row_answerable(row) is True and row.get("language", "").strip().lower() == expected

    return _predicate


def answerable(row: dict[str, str]) -> bool:
    return row_answerable(row) is True


def unanswerable(row: dict[str, str]) -> bool:
    return row_answerable(row) is False


def source_row(
    figure: str,
    panel: str,
    stage_order: int,
    stage_label: str,
    metric: str,
    value: float | None,
    n: int,
    numerator: float,
    filter_text: str,
    source_path: Path,
    calculation: str,
    notes: str = "",
) -> dict[str, str]:
    return {
        "figure": figure,
        "panel": panel,
        "stage_order": str(stage_order),
        "stage_label": stage_label,
        "metric": metric,
        "value": "" if value is None else f"{value:.6f}",
        "n": str(n),
        "numerator_sum": f"{numerator:.6f}",
        "filter": filter_text,
        "source_path": str(source_path.resolve()),
        "calculation": calculation,
        "notes": notes,
    }


def add_mean(rows_out, figure, panel, stage_order, stage_label, metric, csv_rows, predicate, filter_text, source_path, source_column=None, notes=""):
    column = source_column or metric
    value, n, numerator = mean_for(csv_rows, column, predicate)
    rows_out.append(
        source_row(
            figure,
            panel,
            stage_order,
            stage_label,
            metric,
            value,
            n,
            numerator,
            filter_text,
            source_path,
            f"mean({column}) among rows matching filter; blanks/non-numeric values excluded",
            notes,
        )
    )


def build_source_table() -> list[dict[str, str]]:
    rows_out: list[dict[str, str]] = []
    loaded = {key: read_csv(path) for key, path in CSV_SOURCES.items()}

    stages = [
        (1, "Internal held-out", "internal_heldout"),
        (2, "English repair set", "english_repair"),
        (3, "Portuguese repair set", "portuguese_repair"),
        (4, "Prospective test", "external_stress"),
        (5, "Refusal test", "external_refusal"),
    ]

    metric_columns = [
        ("Faithfulness", "judge_faithfulness", answerable, "answerable == true"),
        ("Citation correctness", "judge_citation_correctness", answerable, "answerable == true"),
        ("Completeness", "judge_completeness", answerable, "answerable == true"),
        ("Refusal correctness", "judge_refusal_correctness", unanswerable, "answerable == false"),
    ]
    for stage_order, stage_label, source_key in stages:
        for label, column, predicate, filter_text in metric_columns:
            add_mean(
                rows_out,
                "Figure 3A",
                "Core answer-quality metrics by development stage",
                stage_order,
                stage_label,
                label,
                loaded[source_key],
                predicate,
                filter_text,
                CSV_SOURCES[source_key],
                column,
                "Stages use different evaluation sets; lines show development history, not paired repeated measurement.",
            )

    add_mean(
        rows_out,
        "Figure 3B",
        "Targeted weak-point repairs",
        1,
        "Initial English subset",
        "English completeness",
        loaded["internal_heldout"],
        language_is("en"),
        "answerable == true and language == en",
        CSV_SOURCES["internal_heldout"],
        "judge_completeness",
    )
    add_mean(
        rows_out,
        "Figure 3B",
        "Targeted weak-point repairs",
        2,
        "After English repair",
        "English completeness",
        loaded["english_repair"],
        answerable,
        "answerable == true",
        CSV_SOURCES["english_repair"],
        "judge_completeness",
        "English-only repair set.",
    )
    add_mean(
        rows_out,
        "Figure 3B",
        "Targeted weak-point repairs",
        3,
        "Prospective test",
        "Refusal correctness",
        loaded["external_stress"],
        unanswerable,
        "answerable == false",
        CSV_SOURCES["external_stress"],
        "judge_refusal_correctness",
    )
    add_mean(
        rows_out,
        "Figure 3B",
        "Targeted weak-point repairs",
        4,
        "After refusal prompt",
        "Refusal correctness",
        loaded["external_refusal"],
        unanswerable,
        "answerable == false",
        CSV_SOURCES["external_refusal"],
        "judge_refusal_correctness",
        "Refusal-focused AI-authored set.",
    )
    add_mean(
        rows_out,
        "Figure 3B",
        "Targeted weak-point repairs",
        5,
        "Prospective test",
        "Completeness trade-off",
        loaded["external_stress"],
        answerable,
        "answerable == true",
        CSV_SOURCES["external_stress"],
        "judge_completeness",
    )
    add_mean(
        rows_out,
        "Figure 3B",
        "Targeted weak-point repairs",
        6,
        "After refusal prompt",
        "Completeness trade-off",
        loaded["external_refusal"],
        answerable,
        "answerable == true",
        CSV_SOURCES["external_refusal"],
        "judge_completeness",
        "Shown to document that stricter refusal calibration reduced answerable-control completeness.",
    )

    add_mean(
        rows_out,
        "Figure S1",
        "Prospective-test retrieval validity",
        1,
        "Prospective test",
        "Source hit",
        loaded["external_stress"],
        answerable,
        "answerable == true",
        CSV_SOURCES["external_stress"],
        "source_hit",
    )
    add_mean(
        rows_out,
        "Figure S1",
        "Prospective-test retrieval validity",
        2,
        "Prospective test",
        "Source MRR",
        loaded["external_stress"],
        answerable,
        "answerable == true",
        CSV_SOURCES["external_stress"],
        "source_mrr",
    )
    add_mean(
        rows_out,
        "Figure S1",
        "Prospective-test retrieval validity",
        3,
        "Prospective test",
        "Normalized article recall@5",
        loaded["external_stress"],
        answerable,
        "answerable == true",
        CSV_SOURCES["external_stress"],
        "normalized_article_recall_at_5",
        "Uses normalized article audit columns, not raw article labels.",
    )
    add_mean(
        rows_out,
        "Figure S1",
        "Prospective-test retrieval validity",
        4,
        "Prospective test",
        "Normalized article MRR@5",
        loaded["external_stress"],
        answerable,
        "answerable == true",
        CSV_SOURCES["external_stress"],
        "normalized_article_mrr_at_5",
        "Uses normalized article audit columns, not raw article labels.",
    )

    with AUDIT_SOURCES["benchmark_200_audit"].open(encoding="utf-8") as handle:
        benchmark_audit = json.load(handle)
    category_counts = benchmark_audit.get("bucket_counts", benchmark_audit.get("category_counts", {}))
    for idx, (category, count) in enumerate(sorted(category_counts.items()), start=1):
        rows_out.append(
            source_row(
                "Figure S2",
                "Benchmark composition",
                idx,
                category,
                "Question count",
                float(count),
                int(count),
                float(count),
                "category_counts from benchmark_200_audit.json",
                AUDIT_SOURCES["benchmark_200_audit"],
                "reported category count",
            )
        )

    with AUDIT_SOURCES["article_chunk_audit"].open(encoding="utf-8") as handle:
        chunk_audit = json.load(handle)
    source_counts = chunk_audit.get("chunks_by_source", chunk_audit.get("source_file_counts", {}))
    for idx, (source, count) in enumerate(sorted(source_counts.items()), start=1):
        rows_out.append(
            source_row(
                "Figure S3",
                "Article-aware chunk distribution",
                idx,
                source,
                "Chunk count",
                float(count),
                int(count),
                float(count),
                "source_file_counts from article_chunk_audit.json",
                AUDIT_SOURCES["article_chunk_audit"],
                "reported source-file chunk count",
            )
        )

    return rows_out


def write_source_table(rows: list[dict[str, str]]) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "figure_metrics_source_table.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def rows_for(rows, figure):
    return [row for row in rows if row["figure"] == figure and row["value"]]


def value(row):
    return float(row["value"])


def save_all(fig, stem: str):
    for ext in ("png", "pdf", "svg"):
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", dpi=300)
    plt.close(fig)


def plot_figure_3a(rows: list[dict[str, str]]) -> None:
    data = rows_for(rows, "Figure 3A")
    metrics = ["Faithfulness", "Citation correctness", "Completeness", "Refusal correctness"]
    markers = ["o", "s", "^", "D"]
    styles = ["-", "--", "-.", ":"]
    fig, ax = plt.subplots(figsize=(8.2, 4.7))
    for metric, marker, style in zip(metrics, markers, styles):
        metric_rows = sorted([row for row in data if row["metric"] == metric], key=lambda r: int(r["stage_order"]))
        x = [int(row["stage_order"]) for row in metric_rows]
        y = [value(row) for row in metric_rows]
        ax.plot(x, y, color="black", linestyle=style, marker=marker, linewidth=1.2, markersize=5, label=metric)
    labels = [stage_label for _, stage_label in sorted({(row["stage_order"], row["stage_label"]) for row in data})]
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(0.55, 1.03)
    ax.set_ylabel("Mean AI-judge score")
    ax.set_title("Development-stage answer quality metrics")
    ax.grid(axis="y", color="0.85", linewidth=0.7)
    ax.legend(frameon=False, ncol=2, loc="lower left")
    ax.text(
        0.0,
        -0.33,
        "Different stages used different evaluation sets; this plot summarizes development history, not paired repeated measurement.",
        transform=ax.transAxes,
        fontsize=8,
        va="top",
    )
    save_all(fig, "Figure_3A_development_stage_answer_quality")


def plot_figure_3b(rows: list[dict[str, str]]) -> None:
    data = rows_for(rows, "Figure 3B")
    fig, axes = plt.subplots(1, 3, figsize=(9.0, 3.6), sharey=True)
    panels = [
        ("English completeness", "English completeness"),
        ("Refusal correctness", "Refusal correctness"),
        ("Completeness trade-off", "Completeness after refusal tuning"),
    ]
    for ax, (metric, title) in zip(axes, panels):
        metric_rows = sorted([row for row in data if row["metric"] == metric], key=lambda r: int(r["stage_order"]))
        x = range(len(metric_rows))
        y = [value(row) for row in metric_rows]
        ax.bar(x, y, color="0.35", width=0.6)
        ax.set_xticks(list(x))
        ax.set_xticklabels([row["stage_label"] for row in metric_rows], rotation=35, ha="right", fontsize=8)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", color="0.88", linewidth=0.6)
        for idx, yy in enumerate(y):
            ax.text(idx, min(yy + 0.015, 1.01), f"{yy:.3f}", ha="center", va="bottom", fontsize=8)
    axes[0].set_ylim(0.55, 1.05)
    axes[0].set_ylabel("Mean AI-judge score")
    fig.suptitle("Measured weak points and targeted repairs", y=1.02)
    save_all(fig, "Figure_3B_targeted_weak_point_repairs")


def plot_s1(rows: list[dict[str, str]]) -> None:
    data = sorted(rows_for(rows, "Figure S1"), key=lambda r: int(r["stage_order"]))
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    labels = [row["metric"] for row in data]
    y = [value(row) for row in data]
    ax.bar(range(len(data)), y, color="0.35", width=0.65)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylim(0.85, 1.03)
    ax.set_ylabel("Mean retrieval metric")
    ax.set_title("Prospective-test retrieval validity")
    ax.grid(axis="y", color="0.88", linewidth=0.6)
    for idx, yy in enumerate(y):
        ax.text(idx, min(yy + 0.006, 1.015), f"{yy:.3f}", ha="center", va="bottom", fontsize=8)
    save_all(fig, "Figure_S1_prospective_test_retrieval_validity")


def plot_s2(rows: list[dict[str, str]]) -> None:
    data = sorted(rows_for(rows, "Figure S2"), key=lambda r: value(r), reverse=True)
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    labels = [row["stage_label"].replace("_", " ") for row in data]
    y = [value(row) for row in data]
    ax.bar(range(len(data)), y, color="0.35", width=0.65)
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(labels, rotation=20, ha="right")
    ax.set_ylabel("Questions")
    ax.set_ylim(0, max(y) * 1.18)
    ax.set_title("Bilingual benchmark composition")
    ax.grid(axis="y", color="0.88", linewidth=0.6)
    for idx, yy in enumerate(y):
        ax.text(idx, yy + max(y) * 0.015, f"{int(yy)}", ha="center", va="bottom", fontsize=8)
    save_all(fig, "Figure_S2_benchmark_composition")


def plot_s3(rows: list[dict[str, str]]) -> None:
    data = sorted(rows_for(rows, "Figure S3"), key=lambda r: value(r), reverse=True)
    fig, ax = plt.subplots(figsize=(7.2, max(3.5, 0.34 * len(data))))
    label_map = {
        "IN_338_2024.txt": "IN 338/2024",
        "RDC_406_2020_Estudos_de_Estabilidade.txt": "RDC 406/2020 stability",
        "RDC_55_2010_Registro_de_Produtos_Biológicos.txt": "RDC 55/2010 biologics",
        "RDC_751_2022_Regras_de_classificação_de_risco.txt": "RDC 751/2022 risk classification",
        "RDC_945_2024.txt": "RDC 945/2024",
        "rdc09_2015.txt": "RDC 9/2015",
    }
    labels = [label_map.get(row["stage_label"], Path(row["stage_label"]).stem) for row in data]
    y = [value(row) for row in data]
    ax.barh(range(len(data)), y, color="0.35", height=0.65)
    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Article-level chunks")
    ax.set_title("Article-aware chunk distribution by source file")
    ax.grid(axis="x", color="0.88", linewidth=0.6)
    for idx, xx in enumerate(y):
        ax.text(xx + max(y) * 0.01, idx, f"{int(xx)}", va="center", fontsize=8)
    ax.set_xlim(0, max(y) * 1.12)
    save_all(fig, "Figure_S3_article_chunk_distribution")


def write_readme(rows: list[dict[str, str]]) -> Path:
    checksums = []
    for path in sorted(OUT.glob("*")):
        if path.name in {"FIGURE_README_20260720.md", "figure_checksums.sha256"}:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        checksums.append((digest, path.name))
    checksums_path = OUT / "figure_checksums.sha256"
    with checksums_path.open("w", encoding="utf-8") as handle:
        for digest, name in checksums:
            handle.write(f"{digest}  {name}\n")

    readme = OUT / "FIGURE_README_20260720.md"
    figure_files = "\n".join(f"- `{name}`" for _, name in checksums)
    source_files = "\n".join(f"- `{path.resolve()}`" for path in sorted(set(CSV_SOURCES.values()) | set(AUDIT_SOURCES.values())))
    readme.write_text(
        "# Development Figure Package\n\n"
        "These figures were generated only from archived evaluation CSV and audit JSON files in the submission package. "
        "The file `figure_metrics_source_table.csv` gives the source file, filter, calculation, numerator sum, and denominator for every plotted value.\n\n"
        "Important caveat: development-stage panels compare successive evaluation sets, not the same fixed question set rerun at every stage. "
        "They are suitable for describing the engineering history and observed weak points, but not for claiming paired statistical improvement.\n\n"
        "## Files\n\n"
        f"{figure_files}\n\n"
        "## Source Artifacts\n\n"
        f"{source_files}\n\n"
        "## Suggested Use\n\n"
        "- Main text: use Figure 3A or 3B only if the caption states that stages are different evaluation sets.\n"
        "- Supplement: include Figure S1, Figure S2, Figure S3, and the full source table.\n"
        "- Do not report a plotted value unless it is present in `figure_metrics_source_table.csv`.\n",
        encoding="utf-8",
    )
    return readme


def main() -> None:
    rows = build_source_table()
    write_source_table(rows)
    plot_figure_3a(rows)
    plot_figure_3b(rows)
    plot_s1(rows)
    plot_s2(rows)
    plot_s3(rows)
    if Path(__file__).resolve() != (OUT / "build_rag_development_figures.py").resolve():
        shutil.copy2(Path(__file__).resolve(), OUT / "build_rag_development_figures.py")
    write_readme(rows)


if __name__ == "__main__":
    main()
