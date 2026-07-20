from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.evaluation_statistics import bootstrap_agreement_ci


HUMAN_COLUMNS = {
    "faithfulness": "human_answer_grounded_0_1",
    "citation_correctness": "human_citation_correct_0_1",
    "completeness": "human_answer_complete_0_1",
    "refusal_correctness": "human_safety_or_refusal_correct_0_1",
}
JUDGE_COLUMNS = {
    dimension: f"judge_{dimension}" for dimension in HUMAN_COLUMNS
}


@dataclass(frozen=True)
class RatingSource:
    name: str
    rows: dict[str, dict[str, str]]
    columns: dict[str, str]


def read_rows(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "id" not in reader.fieldnames:
            raise ValueError(f"{path} must contain an id column.")
        rows = {row["id"]: row for row in reader if row.get("id")}
    if not rows:
        raise ValueError(f"{path} contains no labeled rows.")
    return rows


def binary_label(value: str, threshold: float) -> str:
    value = str(value).strip()
    if not value:
        return ""
    try:
        return "1" if float(value) >= threshold else "0"
    except ValueError as exc:
        raise ValueError(f"Rating must be numeric, received {value!r}.") from exc


def compare_sources(
    left: RatingSource,
    right: RatingSource,
    threshold: float,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    metrics: list[dict[str, Any]] = []
    disagreements: list[dict[str, str]] = []
    shared_ids = sorted(set(left.rows) & set(right.rows))
    for dimension in HUMAN_COLUMNS:
        left_labels: list[str] = []
        right_labels: list[str] = []
        labeled_ids: list[str] = []
        for item_id in shared_ids:
            left_label = binary_label(
                left.rows[item_id].get(left.columns[dimension], ""), threshold
            )
            right_label = binary_label(
                right.rows[item_id].get(right.columns[dimension], ""), threshold
            )
            if not left_label or not right_label:
                continue
            labeled_ids.append(item_id)
            left_labels.append(left_label)
            right_labels.append(right_label)
            if left_label != right_label:
                disagreements.append(
                    {
                        "id": item_id,
                        "dimension": dimension,
                        "left_source": left.name,
                        "left_rating": left_label,
                        "right_source": right.name,
                        "right_rating": right_label,
                        "adjudicated_rating": "",
                        "disagreement_reason": "",
                        "notes": "",
                    }
                )
        kappa, kappa_low, kappa_high, count = bootstrap_agreement_ci(
            left_labels, right_labels, statistic="kappa"
        )
        agreement, agreement_low, agreement_high, _ = bootstrap_agreement_ci(
            left_labels, right_labels, statistic="agreement"
        )
        true_positive = sum(a == "1" and b == "1" for a, b in zip(left_labels, right_labels))
        false_negative = sum(a == "1" and b == "0" for a, b in zip(left_labels, right_labels))
        true_negative = sum(a == "0" and b == "0" for a, b in zip(left_labels, right_labels))
        false_positive = sum(a == "0" and b == "1" for a, b in zip(left_labels, right_labels))
        has_human_reference = left.name.startswith("human") and not right.name.startswith("human")
        sensitivity = (
            true_positive / (true_positive + false_negative)
            if has_human_reference and true_positive + false_negative
            else None
        )
        specificity = (
            true_negative / (true_negative + false_positive)
            if has_human_reference and true_negative + false_positive
            else None
        )
        metrics.append(
            {
                "comparison": f"{left.name} vs {right.name}",
                "dimension": dimension,
                "n": count,
                "agreement": agreement,
                "agreement_ci_low": agreement_low,
                "agreement_ci_high": agreement_high,
                "cohen_kappa": kappa,
                "kappa_ci_low": kappa_low,
                "kappa_ci_high": kappa_high,
                "sensitivity_vs_human": sensitivity,
                "specificity_vs_human": specificity,
            }
        )
    return metrics, disagreements


def parse_judge(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Use NAME=PATH for --judge.")
    name, path = value.split("=", 1)
    return name.strip(), Path(path)


def fmt(value: float | None) -> str:
    return "NA" if value is None else f"{value:.3f}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare blinded human reviews and calibrated LLM judges."
    )
    parser.add_argument("--human-pass-1", type=Path, required=True)
    parser.add_argument("--human-pass-2", type=Path)
    parser.add_argument("--judge", type=parse_judge, action="append", default=[])
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    human_1 = RatingSource(
        "human_pass_1", read_rows(args.human_pass_1), HUMAN_COLUMNS
    )
    sources = [human_1]
    if args.human_pass_2:
        sources.append(
            RatingSource(
                "human_pass_2", read_rows(args.human_pass_2), HUMAN_COLUMNS
            )
        )
    for name, path in args.judge:
        sources.append(RatingSource(name, read_rows(path), JUDGE_COLUMNS))

    metrics: list[dict[str, Any]] = []
    disagreements: list[dict[str, str]] = []
    for left_index, left in enumerate(sources):
        for right in sources[left_index + 1 :]:
            comparison_metrics, comparison_disagreements = compare_sources(
                left, right, args.threshold
            )
            metrics.extend(comparison_metrics)
            disagreements.extend(comparison_disagreements)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "judge_agreement.json"
    markdown_path = args.output_dir / "judge_agreement.md"
    disagreement_path = args.output_dir / "judge_disagreements.csv"
    json_path.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Human and AI Judge Agreement",
        "",
        "All confidence intervals use 2,000 percentile bootstrap resamples.",
        "Human pass 1 versus pass 2 is intra-rater repeatability, not inter-rater agreement.",
        "",
        "| Comparison | Dimension | n | Agreement (95% CI) | Cohen's kappa (95% CI) | Sensitivity | Specificity |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for metric in metrics:
        lines.append(
            f"| {metric['comparison']} | {metric['dimension']} | {metric['n']} | "
            f"{fmt(metric['agreement'])} ({fmt(metric['agreement_ci_low'])}-"
            f"{fmt(metric['agreement_ci_high'])}) | {fmt(metric['cohen_kappa'])} "
            f"({fmt(metric['kappa_ci_low'])}-{fmt(metric['kappa_ci_high'])}) | "
            f"{fmt(metric['sensitivity_vs_human'])} | "
            f"{fmt(metric['specificity_vs_human'])} |"
        )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fields = [
        "id",
        "dimension",
        "left_source",
        "left_rating",
        "right_source",
        "right_rating",
        "adjudicated_rating",
        "disagreement_reason",
        "notes",
    ]
    with disagreement_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(disagreements)
    print(markdown_path)
    print(disagreement_path)


if __name__ == "__main__":
    main()
