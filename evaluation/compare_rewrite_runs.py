from __future__ import annotations

import argparse
import csv
from pathlib import Path
from statistics import mean


METRICS = [
    ("Raw vector source hit", "raw_vector_source_hit"),
    ("Raw vector MRR", "raw_vector_source_mrr"),
    ("BM25 MRR", "bm25_source_mrr"),
    ("Fused MRR", "fused_source_mrr"),
    ("Operational top-5 MRR", "source_mrr"),
    ("Article Recall@5", "article_recall_at_k"),
    ("Article MRR@5", "article_mrr_at_k"),
    ("Article nDCG@5", "article_ndcg_at_k"),
    ("Top-5 gold-term coverage", "retrieved_term_coverage"),
]


def load_english_answerable(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return [
            row
            for row in csv.DictReader(handle)
            if row["language"] == "en" and row["answerable"].lower() == "true"
        ]


def metric_mean(rows: list[dict[str, str]], key: str) -> float:
    def numeric(value: str) -> float:
        if value.lower() in {"true", "false"}:
            return 1.0 if value.lower() == "true" else 0.0
        return float(value)

    return mean(numeric(row[key]) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare English retrieval with and without query rewrite.")
    parser.add_argument("baseline", type=Path)
    parser.add_argument("rewritten", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    baseline = load_english_answerable(args.baseline)
    rewritten = load_english_answerable(args.rewritten)
    if [row["id"] for row in baseline] != [row["id"] for row in rewritten]:
        raise ValueError("Runs do not contain the same ordered English benchmark questions.")
    if not all(row["rewrite_applied"].lower() == "true" for row in rewritten):
        raise ValueError("The rewritten run does not mark every English question as rewritten.")

    lines = [
        "# English Query Rewrite Comparison",
        "",
        f"Questions: {len(baseline)} answerable English questions",
        f"Baseline: `{args.baseline.name}`",
        f"Rewritten: `{args.rewritten.name}`",
        "",
        "| Metric | Without rewrite | With rewrite | Delta |",
        "|---|---:|---:|---:|",
    ]
    for label, key in METRICS:
        before = metric_mean(baseline, key)
        after = metric_mean(rewritten, key)
        lines.append(f"| {label} | {before:.3f} | {after:.3f} | {after - before:+.3f} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Positive deltas indicate that English query rewriting improved that metric.",
            "- Negative deltas indicate that the rewrite changed retrieval in an unfavorable direction for that metric.",
            "- This comparison uses only answerable English questions so it measures the intended bilingual retrieval effect.",
            "- Keep the paired run manifests with any manuscript supplement so the rewrite method is explicit.",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
