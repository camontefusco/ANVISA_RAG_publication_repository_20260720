from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.publication_eval import build_summary


BOOLEAN_COLUMNS = {
    "answerable",
    "rewrite_applied",
    "raw_vector_source_hit",
    "bm25_source_hit",
    "fused_source_hit",
    "source_hit",
    "refusal_detected",
    "citation_present",
    "article_citation_present",
}
NUMERIC_FRAGMENTS = (
    "_mrr",
    "_recall_at_k",
    "_precision_at_k",
    "_ndcg_at_k",
    "_coverage",
    "judge_",
    "citation_retrieved_validity",
)


def coerce_row(row: dict[str, str]) -> dict[str, object]:
    coerced: dict[str, object] = dict(row)
    for key, value in row.items():
        if not value:
            coerced[key] = None
        elif key in BOOLEAN_COLUMNS:
            coerced[key] = value.lower() == "true"
        elif any(fragment in key for fragment in NUMERIC_FRAGMENTS):
            coerced[key] = float(value)
    return coerced


def main() -> None:
    parser = argparse.ArgumentParser(description="Regenerate a publication summary.")
    parser.add_argument("detailed_csv", type=Path)
    parser.add_argument("summary_markdown", type=Path)
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()
    with args.detailed_csv.open(newline="", encoding="utf-8") as handle:
        rows = [coerce_row(row) for row in csv.DictReader(handle)]
    args.summary_markdown.write_text(
        build_summary(rows, generate=args.generate), encoding="utf-8"
    )
    print(args.summary_markdown)


if __name__ == "__main__":
    main()
