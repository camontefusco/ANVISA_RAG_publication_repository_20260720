from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path


DEFAULT_RUNS = [
    (
        "en",
        Path(
            "evaluation/publication_results/generation_en_heldout_20260709/"
            "generation_evaluation_2026-07-10_01-03-11.csv"
        ),
        Path(
            "evaluation/publication_results/generation_en_heldout_20260709/"
            "generation_failure_audit_2026-07-10_01-03-11.csv"
        ),
    ),
    (
        "pt",
        Path(
            "evaluation/publication_results/generation_pt_heldout_20260709/"
            "generation_evaluation_2026-07-10_01-28-15.csv"
        ),
        Path(
            "evaluation/publication_results/generation_pt_heldout_20260709/"
            "generation_failure_audit_2026-07-10_01-28-15.csv"
        ),
    ),
]


REVIEW_COLUMNS = [
    "review_order",
    "id",
    "pair_id",
    "language",
    "category",
    "answerable",
    "automated_failure_types",
    "question",
    "expected_answer",
    "generated_answer",
    "gold_citations",
    "retrieved_citations",
    "retrieved_sources",
    "source_hit",
    "article_recall_at_k",
    "answer_term_coverage",
    "citation_retrieved_validity",
    "refusal_detected",
    "pass1_retrieval_correct_0_1",
    "pass1_answer_grounded_0_1",
    "pass1_answer_complete_0_1",
    "pass1_citation_correct_0_1",
    "pass1_refusal_correct_0_1",
    "pass1_overall_acceptable_0_1",
    "pass1_root_cause",
    "pass1_notes",
    "pass2_retrieval_correct_0_1",
    "pass2_answer_grounded_0_1",
    "pass2_answer_complete_0_1",
    "pass2_citation_correct_0_1",
    "pass2_refusal_correct_0_1",
    "pass2_overall_acceptable_0_1",
    "pass2_root_cause",
    "pass2_notes",
    "final_adjudication",
    "final_notes",
]


def read_by_id(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


def build_rows(root: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for language, evaluation_path, failure_path in DEFAULT_RUNS:
        evaluation_rows = read_by_id(root / evaluation_path)
        with (root / failure_path).open(newline="", encoding="utf-8") as handle:
            for failure in csv.DictReader(handle):
                full = evaluation_rows[failure["id"]]
                rows.append(
                    {
                        "id": failure["id"],
                        "pair_id": failure["pair_id"],
                        "language": language,
                        "category": failure["category"],
                        "answerable": failure["answerable"],
                        "automated_failure_types": failure["failure_types"],
                        "question": failure["question"],
                        "expected_answer": full.get("expected_answer", ""),
                        "generated_answer": full.get("answer", ""),
                        "gold_citations": failure["gold_citations"],
                        "retrieved_citations": failure["retrieved_citations"],
                        "retrieved_sources": full.get("retrieved_sources", ""),
                        "source_hit": full.get("source_hit", ""),
                        "article_recall_at_k": full.get("article_recall_at_k", ""),
                        "answer_term_coverage": full.get("answer_term_coverage", ""),
                        "citation_retrieved_validity": full.get(
                            "citation_retrieved_validity", ""
                        ),
                        "refusal_detected": full.get("refusal_detected", ""),
                    }
                )
    random.Random(20260714).shuffle(rows)
    for index, row in enumerate(rows, start=1):
        row["review_order"] = str(index)
        for column in REVIEW_COLUMNS:
            row.setdefault(column, "")
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a blinded manual review table for generation failures."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "evaluation/publication_results/"
            "generation_failure_manual_review_20260714.csv"
        ),
    )
    args = parser.parse_args()

    rows = build_rows(args.root)
    output_path = args.root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} review rows to {output_path}")


if __name__ == "__main__":
    main()
