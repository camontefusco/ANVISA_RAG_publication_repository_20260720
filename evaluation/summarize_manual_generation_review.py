from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.evaluation_statistics import bootstrap_agreement_ci


DIMENSIONS = [
    "retrieval_correct",
    "answer_grounded",
    "answer_complete",
    "citation_correct",
    "refusal_correct",
    "overall_acceptable",
]


def parse_binary(value: str) -> int | None:
    value = str(value).strip()
    if value == "":
        return None
    if value not in {"0", "1"}:
        raise ValueError(f"Expected 0/1/blank, got {value!r}.")
    return int(value)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def completion(rows: list[dict[str, str]], pass_name: str) -> dict[str, int]:
    counts = {}
    for dimension in DIMENSIONS:
        column = f"{pass_name}_{dimension}_0_1"
        counts[dimension] = sum(parse_binary(row.get(column, "")) is not None for row in rows)
    return counts


def pass_summary(rows: list[dict[str, str]], pass_name: str) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for language in sorted({row["language"] for row in rows}):
        language_rows = [row for row in rows if row["language"] == language]
        for dimension in DIMENSIONS:
            column = f"{pass_name}_{dimension}_0_1"
            values = [
                parse_binary(row.get(column, ""))
                for row in language_rows
            ]
            labeled = [value for value in values if value is not None]
            output.append(
                {
                    "pass": pass_name,
                    "language": language,
                    "dimension": dimension,
                    "n_labeled": len(labeled),
                    "mean": mean(labeled) if labeled else None,
                }
            )
    return output


def agreement_summary(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    for dimension in DIMENSIONS:
        pass1_column = f"pass1_{dimension}_0_1"
        pass2_column = f"pass2_{dimension}_0_1"
        labels1: list[str] = []
        labels2: list[str] = []
        for row in rows:
            left = parse_binary(row.get(pass1_column, ""))
            right = parse_binary(row.get(pass2_column, ""))
            if left is None or right is None:
                continue
            labels1.append(str(left))
            labels2.append(str(right))
        agreement, agreement_low, agreement_high, count = bootstrap_agreement_ci(
            labels1, labels2, statistic="agreement"
        )
        kappa, kappa_low, kappa_high, _ = bootstrap_agreement_ci(
            labels1, labels2, statistic="kappa"
        )
        output.append(
            {
                "dimension": dimension,
                "n": count,
                "agreement": agreement,
                "agreement_ci_low": agreement_low,
                "agreement_ci_high": agreement_high,
                "cohen_kappa": kappa,
                "kappa_ci_low": kappa_low,
                "kappa_ci_high": kappa_high,
            }
        )
    return output


def fmt(value: object) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)


def write_markdown(
    path: Path,
    rows: list[dict[str, str]],
    pass_rows: list[dict[str, object]],
    agreements: list[dict[str, object]],
) -> None:
    root_causes = Counter(
        row.get("pass1_root_cause", "").strip()
        for row in rows
        if row.get("pass1_root_cause", "").strip()
    )
    lines = [
        "# Manual Generation Failure Review Summary",
        "",
        f"Rows in failure-review set: {len(rows)}",
        "",
        "## Pass Completion",
        "",
        "| Pass | Dimension | Labeled rows |",
        "|---|---|---:|",
    ]
    for pass_name in ("pass1", "pass2"):
        for dimension, count in completion(rows, pass_name).items():
            lines.append(f"| {pass_name} | {dimension} | {count} |")
    lines.extend(
        [
            "",
            "## Human-Labeled Failure-Set Quality",
            "",
            "| Pass | Language | Dimension | n | Mean acceptable |",
            "|---|---|---|---:|---:|",
        ]
    )
    for row in pass_rows:
        lines.append(
            f"| {row['pass']} | {row['language']} | {row['dimension']} | "
            f"{row['n_labeled']} | {fmt(row['mean'])} |"
        )
    lines.extend(
        [
            "",
            "## Intra-Rater Repeatability",
            "",
            "Only meaningful after delayed pass 2 is filled.",
            "",
            "| Dimension | n | Agreement (95% CI) | Cohen's kappa (95% CI) |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in agreements:
        lines.append(
            f"| {row['dimension']} | {row['n']} | "
            f"{fmt(row['agreement'])} ({fmt(row['agreement_ci_low'])}-"
            f"{fmt(row['agreement_ci_high'])}) | {fmt(row['cohen_kappa'])} "
            f"({fmt(row['kappa_ci_low'])}-{fmt(row['kappa_ci_high'])}) |"
        )
    lines.extend(["", "## Pass 1 Root Causes", ""])
    if root_causes:
        lines.extend(f"- {cause}: {count}" for cause, count in root_causes.most_common())
    else:
        lines.append("- No pass 1 root causes labeled yet.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize manual labels for generation failure review."
    )
    parser.add_argument("review_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    rows = load_rows(args.review_csv)
    output_dir = args.output_dir or args.review_csv.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    pass_rows = pass_summary(rows, "pass1") + pass_summary(rows, "pass2")
    agreements = agreement_summary(rows)
    (output_dir / "manual_generation_review_summary.json").write_text(
        json.dumps(
            {
                "pass_summary": pass_rows,
                "intra_rater_repeatability": agreements,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(
        output_dir / "manual_generation_review_summary.md",
        rows,
        pass_rows,
        agreements,
    )
    print(output_dir / "manual_generation_review_summary.md")


if __name__ == "__main__":
    main()
