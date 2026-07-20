#!/usr/bin/env python3
"""Build additional manuscript figures from archived corpus and benchmark audits."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
from pathlib import Path
from textwrap import fill

os.environ.setdefault("MPLCONFIGDIR", str(Path("/tmp") / "rag_mplconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "tirs_final_submission_package_20260720"
EVIDENCE = PACKAGE / "supplementary_materials" / "evidence_artifacts"
OUT = PACKAGE / "figures_from_development_20260720"

BENCHMARK_AUDIT = EVIDENCE / "benchmark" / "benchmark_200_audit.json"
CHUNK_AUDIT = EVIDENCE / "corpus" / "article_chunk_audit.json"


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def save_all(fig, stem: str) -> None:
    for ext in ("png", "pdf", "svg"):
        fig.savefig(OUT / f"{stem}.{ext}", bbox_inches="tight", dpi=300)
    plt.close(fig)


def source_row(figure, panel, item, value, source_path, calculation, notes="") -> dict[str, str]:
    return {
        "figure": figure,
        "panel": panel,
        "item": item,
        "value": str(value),
        "source_path": str(source_path.resolve()),
        "calculation": calculation,
        "notes": notes,
    }


def box(ax, xy, wh, title, body, fontsize=8):
    x, y = xy
    w, h = wh
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.025,rounding_size=0.02",
        linewidth=1.0,
        edgecolor="black",
        facecolor="0.96",
    )
    ax.add_patch(patch)
    wrapped = "\n".join(fill(part, 34) for part in body.split("\n"))
    ax.text(x + 0.03, y + h / 2, title, ha="left", va="center", fontsize=9.5, fontweight="bold")
    ax.text(x + w * 0.42, y + h / 2, wrapped, ha="left", va="center", fontsize=fontsize)


def arrow(ax, start, end):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            linewidth=1.0,
            color="black",
            shrinkA=4,
            shrinkB=4,
        )
    )


def plot_figure_1(chunk_audit: dict, benchmark_audit: dict, rows: list[dict[str, str]]) -> None:
    article_count = chunk_audit["article_count"]
    chunk_count = chunk_audit["chunk_count"]
    docs = len(chunk_audit["chunks_by_source"])
    benchmark_rows = benchmark_audit["rows"]
    external_note = "50-question stress test; 30-question refusal-focused test"

    for item, value, source, calc in [
        ("Indexed regulatory documents", docs, CHUNK_AUDIT, "count keys in chunks_by_source"),
        ("Detected articles", article_count, CHUNK_AUDIT, "article_count field"),
        ("Article-level chunks", chunk_count, CHUNK_AUDIT, "chunk_count field"),
        ("Internal benchmark questions", benchmark_rows, BENCHMARK_AUDIT, "rows field"),
    ]:
        rows.append(source_row("Figure 1", "Closed-corpus RAG workflow", item, value, source, calc))

    fig, ax = plt.subplots(figsize=(7.2, 7.0))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    boxes = [
        ((0.08, 0.82), (0.84, 0.105), "Corpus", f"{docs} ANVISA regulatory documents; closed collection"),
        ((0.08, 0.69), (0.84, 0.105), "Cleaning", "plain text; article labels and regulatory structure preserved"),
        ((0.08, 0.56), (0.84, 0.105), "Indexing", f"{article_count} detected articles; {chunk_count} article-level chunks"),
        ((0.08, 0.43), (0.84, 0.105), "Retrieval", "dense retrieval plus BM25; reciprocal-rank fusion; reranking"),
        ((0.08, 0.30), (0.84, 0.105), "Generation", "answer with source document and article citation, or refuse"),
        ((0.08, 0.17), (0.84, 0.105), "Evaluation", f"{benchmark_rows} bilingual questions; retrieval metrics; AI-judge audit"),
        ((0.08, 0.04), (0.84, 0.105), "External tests", external_note),
    ]
    for args in boxes:
        box(ax, *args)

    for y_top, y_bottom in [(0.82, 0.795), (0.69, 0.665), (0.56, 0.535), (0.43, 0.405), (0.30, 0.275), (0.17, 0.145)]:
        arrow(ax, (0.50, y_top), (0.50, y_bottom))
    save_all(fig, "Figure_1_closed_corpus_rag_workflow")


def pretty_source(label: str) -> str:
    mapping = {
        "IN_338_2024.txt": "IN 338/2024",
        "RDC_406_2020_Estudos_de_Estabilidade.txt": "RDC 406/2020",
        "RDC_55_2010_Registro_de_Produtos_Biológicos.txt": "RDC 55/2010",
        "RDC_751_2022_Regras_de_classificação_de_risco.txt": "RDC 751/2022",
        "RDC_945_2024.txt": "RDC 945/2024",
        "rdc09_2015.txt": "RDC 9/2015",
    }
    return mapping.get(label, Path(label).stem)


def plot_figure_2(benchmark_audit: dict, rows: list[dict[str, str]]) -> None:
    bucket_counts = benchmark_audit["bucket_counts"]
    source_counts = benchmark_audit["source_evidence_counts"]

    for item, value in bucket_counts.items():
        rows.append(source_row("Figure 2", "Benchmark question buckets", item, value, BENCHMARK_AUDIT, "bucket_counts field"))
    for item, value in source_counts.items():
        rows.append(source_row("Figure 2", "Gold source-evidence coverage", item, value, BENCHMARK_AUDIT, "source_evidence_counts field"))
    rows.append(
        source_row(
            "Figure 2",
            "Benchmark audit",
            "Unique gold citations",
            benchmark_audit["unique_gold_citations"],
            BENCHMARK_AUDIT,
            "unique_gold_citations field",
        )
    )

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(7.4, 6.2),
        gridspec_kw={"height_ratios": [1.0, 1.35], "hspace": 0.62},
    )

    bucket_order = ["pt_answerable", "en_answerable", "complex", "unanswerable"]
    bucket_labels = ["PT answerable", "EN answerable", "Complex/exception", "Unanswerable/adversarial"]
    bucket_values = [bucket_counts[k] for k in bucket_order]
    axes[0].barh(range(len(bucket_values)), bucket_values, color="0.35", height=0.62)
    axes[0].set_yticks(range(len(bucket_values)))
    axes[0].set_yticklabels(bucket_labels, fontsize=9)
    axes[0].invert_yaxis()
    axes[0].set_xlim(0, max(bucket_values) * 1.18)
    axes[0].set_xlabel("Questions")
    axes[0].set_title("Question buckets in the 200-question benchmark")
    axes[0].grid(axis="x", color="0.88", linewidth=0.6)
    for idx, value in enumerate(bucket_values):
        axes[0].text(value + max(bucket_values) * 0.02, idx, str(value), va="center", fontsize=8)

    source_items = sorted(source_counts.items(), key=lambda kv: kv[1], reverse=True)
    labels = [pretty_source(k) for k, _ in source_items]
    values = [v for _, v in source_items]
    axes[1].barh(range(len(values)), values, color="0.35", height=0.65)
    axes[1].set_yticks(range(len(values)))
    axes[1].set_yticklabels(labels, fontsize=9)
    axes[1].invert_yaxis()
    axes[1].set_xlabel("Questions with expected source evidence")
    axes[1].set_title("Gold source coverage among answerable and complex questions")
    axes[1].grid(axis="x", color="0.88", linewidth=0.6)
    axes[1].set_xlim(0, max(values) * 1.18)
    for idx, value in enumerate(values):
        axes[1].text(value + max(values) * 0.02, idx, str(value), va="center", fontsize=8)

    fig.suptitle("Bilingual benchmark design and source coverage", y=0.98, fontsize=13)
    fig.text(
        0.5,
        0.01,
        f"Benchmark audit status: {benchmark_audit['status']}; rows: {benchmark_audit['rows']}; bilingual pairs: {benchmark_audit['pairs']}; unique gold citations: {benchmark_audit['unique_gold_citations']}.",
        ha="center",
        fontsize=8,
    )
    save_all(fig, "Figure_2_benchmark_design_and_source_coverage")


def write_source_table(rows: list[dict[str, str]]) -> Path:
    path = OUT / "additional_figure_source_table.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def update_checksums() -> None:
    paths = sorted(p for p in OUT.iterdir() if p.is_file() and p.name != "figure_checksums.sha256")
    with (OUT / "figure_checksums.sha256").open("w", encoding="utf-8") as handle:
        for path in paths:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            handle.write(f"{digest}  {path.name}\n")


def update_readme() -> None:
    readme = OUT / "FIGURE_README_20260720.md"
    text = readme.read_text(encoding="utf-8")
    addition = (
        "\n## Additional Python-Generated Figures\n\n"
        "- `Figure_1_closed_corpus_rag_workflow.*`: workflow schematic generated from corpus and benchmark audit fields.\n"
        "- `Figure_2_benchmark_design_and_source_coverage.*`: benchmark bucket counts and source-evidence coverage from `benchmark_200_audit.json`.\n"
        "- `additional_figure_source_table.csv`: source table for Figure 1 and Figure 2 values.\n"
    )
    if "## Additional Python-Generated Figures" not in text:
        readme.write_text(text.rstrip() + addition + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    chunk_audit = load_json(CHUNK_AUDIT)
    benchmark_audit = load_json(BENCHMARK_AUDIT)
    rows: list[dict[str, str]] = []
    plot_figure_1(chunk_audit, benchmark_audit, rows)
    plot_figure_2(benchmark_audit, rows)
    write_source_table(rows)
    shutil.copy2(Path(__file__).resolve(), OUT / "build_additional_publication_figures.py")
    update_readme()
    update_checksums()


if __name__ == "__main__":
    main()
