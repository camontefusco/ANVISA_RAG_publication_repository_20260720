from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
BENCHMARK = ROOT / "evaluation" / "publication_benchmark_200.jsonl"
SPLIT_MANIFEST = ROOT / "evaluation" / "benchmark_200_split_manifest.json"
PAIR_REVIEW = ROOT / "evaluation" / "benchmark_200_pair_review.csv"
CALIBRATION_REVIEW = ROOT / "evaluation" / "benchmark_200_calibration_20.csv"
SEED = 20260619

CALIBRATION_COUNTS = {"direct": 14, "complex": 2, "unanswerable": 4}
DEV_REMAINING_COUNTS = {"direct": 3, "complex": 1, "unanswerable": 1}


def load_rows() -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in BENCHMARK.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def stratum(row: dict[str, Any]) -> str:
    if not row["answerable"]:
        return "unanswerable"
    if row["category"] in {"multi_article", "exception"}:
        return "complex"
    return "direct"


def pair_record(pair_id: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_language = {row["language"]: row for row in rows}
    pt = by_language["pt"]
    en = by_language["en"]
    evidence = pt["gold_evidence"]
    return {
        "pair_id": pair_id,
        "stratum": stratum(pt),
        "category": pt["category"],
        "difficulty": pt["difficulty"],
        "answerable": pt["answerable"],
        "pt_id": pt["id"],
        "question_pt": pt["question"],
        "expected_answer_pt": pt["expected_answer"],
        "en_id": en["id"],
        "question_en": en["question"],
        "expected_answer_en": en["expected_answer"],
        "gold_citations": "; ".join(pt["gold_citations"]),
        "gold_evidence": "\n\n".join(evidence),
        "validation_status": pt["validation_status"],
    }


def select_split(records: list[dict[str, Any]]) -> dict[str, str]:
    rng = random.Random(SEED)
    by_stratum: dict[str, list[str]] = defaultdict(list)
    for record in records:
        by_stratum[record["stratum"]].append(record["pair_id"])
    assignments: dict[str, str] = {}
    for group, pair_ids in by_stratum.items():
        rng.shuffle(pair_ids)
        calibration_count = CALIBRATION_COUNTS[group]
        remaining_count = DEV_REMAINING_COUNTS[group]
        for pair_id in pair_ids[:calibration_count]:
            assignments[pair_id] = "calibration_20"
        for pair_id in pair_ids[calibration_count : calibration_count + remaining_count]:
            assignments[pair_id] = "dev_remaining_5"
        for pair_id in pair_ids[calibration_count + remaining_count :]:
            assignments[pair_id] = "held_out_test_75"
    return assignments


REVIEW_FIELDS = [
    "review_order",
    "split",
    "pair_id",
    "stratum",
    "category",
    "difficulty",
    "answerable",
    "pt_id",
    "question_pt",
    "expected_answer_pt",
    "en_id",
    "question_en",
    "expected_answer_en",
    "gold_citations",
    "gold_evidence",
    "pass1_question_clear_0_1",
    "pass1_answer_supported_0_1",
    "pass1_citations_exact_0_1",
    "pass1_bilingual_equivalent_0_1",
    "pass1_keep_revise_drop",
    "pass1_comments",
    "pass2_question_clear_0_1",
    "pass2_answer_supported_0_1",
    "pass2_citations_exact_0_1",
    "pass2_bilingual_equivalent_0_1",
    "pass2_keep_revise_drop",
    "pass2_comments",
    "final_decision",
    "adjudication_rationale",
]


def write_review(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_FIELDS)
        writer.writeheader()
        for order, record in enumerate(records, start=1):
            writer.writerow(
                {
                    "review_order": order,
                    "split": record["split"],
                    **{key: record.get(key, "") for key in REVIEW_FIELDS if key not in {"review_order", "split"}},
                }
            )


def main() -> None:
    rows = load_rows()
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["pair_id"]].append(row)
    records = [pair_record(pair_id, pair_rows) for pair_id, pair_rows in grouped.items()]
    assignments = select_split(records)
    for record in records:
        record["split"] = assignments[record["pair_id"]]

    rng = random.Random(SEED)
    rng.shuffle(records)
    calibration = [record for record in records if record["split"] == "calibration_20"]
    write_review(PAIR_REVIEW, records)
    write_review(CALIBRATION_REVIEW, calibration)

    benchmark_hash = hashlib.sha256(BENCHMARK.read_bytes()).hexdigest()
    split_counts = Counter(record["split"] for record in records)
    split_strata = Counter((record["split"], record["stratum"]) for record in records)
    manifest = {
        "seed": SEED,
        "benchmark_sha256": benchmark_hash,
        "pair_count": len(records),
        "row_count": len(rows),
        "split_counts": dict(split_counts),
        "split_stratum_counts": {
            f"{split}|{group}": count
            for (split, group), count in sorted(split_strata.items())
        },
        "assignments": assignments,
        "leakage_control": "Portuguese and English members of each pair share one split.",
    }
    SPLIT_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    if len(records) != 100 or split_counts != {"calibration_20": 20, "dev_remaining_5": 5, "held_out_test_75": 75}:
        raise ValueError(f"Unexpected split counts: {dict(split_counts)}")
    print(json.dumps({"split_counts": dict(split_counts), "split_strata": manifest["split_stratum_counts"]}, indent=2))
    print(f"Pair review: {PAIR_REVIEW}")
    print(f"Calibration review: {CALIBRATION_REVIEW}")
    print(f"Split manifest: {SPLIT_MANIFEST}")


if __name__ == "__main__":
    main()
