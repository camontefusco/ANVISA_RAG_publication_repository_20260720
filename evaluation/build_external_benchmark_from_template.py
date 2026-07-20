from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path


REQUIRED_COLUMNS = {
    "pair_id",
    "category",
    "difficulty",
    "answerable",
    "pt_question",
    "en_question",
    "gold_sources",
    "gold_articles",
    "gold_citations",
    "gold_evidence",
    "expected_answer_pt",
    "expected_answer_en",
    "gold_terms",
    "notes",
    "validation_status",
}


def split_semicolon(value: str) -> list[str]:
    return [part.strip() for part in value.split(";") if part.strip()]


def parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_row(row: dict[str, str], line_number: int) -> list[str]:
    errors: list[str] = []
    pair_id = row.get("pair_id", "").strip()
    if not pair_id:
        errors.append("missing pair_id")
    answerable = parse_bool(row.get("answerable", ""))
    pt_question = row.get("pt_question", "").strip()
    en_question = row.get("en_question", "").strip()
    if not pt_question:
        errors.append("missing pt_question")
    if not en_question:
        errors.append("missing en_question")
    if answerable:
        for field in (
            "gold_sources",
            "gold_articles",
            "gold_citations",
            "gold_evidence",
            "expected_answer_pt",
            "expected_answer_en",
            "gold_terms",
        ):
            if not row.get(field, "").strip():
                errors.append(f"answerable row missing {field}")
    else:
        if not row.get("expected_answer_pt", "").strip():
            errors.append("unanswerable row missing expected_answer_pt refusal rationale")
        if not row.get("expected_answer_en", "").strip():
            errors.append("unanswerable row missing expected_answer_en refusal rationale")
    return [f"line {line_number}: {error}" for error in errors]


def benchmark_items(row: dict[str, str]) -> list[dict[str, object]]:
    pair_id = row["pair_id"].strip()
    answerable = parse_bool(row["answerable"])
    common = {
        "pair_id": pair_id,
        "category": row["category"].strip(),
        "difficulty": row["difficulty"].strip(),
        "answerable": answerable,
        "gold_sources": split_semicolon(row["gold_sources"]),
        "gold_articles": split_semicolon(row["gold_articles"]),
        "gold_citations": split_semicolon(row["gold_citations"]),
        "gold_evidence": split_semicolon(row["gold_evidence"]),
        "gold_terms": split_semicolon(row["gold_terms"]),
        "provenance": "prospective_external_test",
        "validation_status": row["validation_status"].strip() or "pending_review",
        "notes": row["notes"].strip(),
    }
    return [
        {
            **common,
            "id": f"{pair_id}_PT",
            "question": row["pt_question"].strip(),
            "language": "pt",
            "expected_answer": row["expected_answer_pt"].strip(),
        },
        {
            **common,
            "id": f"{pair_id}_EN",
            "question": row["en_question"].strip(),
            "language": "en",
            "expected_answer": row["expected_answer_en"].strip(),
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a prospective external-test authoring CSV to benchmark JSONL."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    with args.input.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise SystemExit(f"Template is missing columns: {sorted(missing)}")
        for line_number, row in enumerate(reader, start=2):
            if not any((value or "").strip() for value in row.values()):
                continue
            rows.append({key: value or "" for key, value in row.items()})

    errors: list[str] = []
    for index, row in enumerate(rows, start=2):
        try:
            errors.extend(validate_row(row, index))
        except ValueError as exc:
            errors.append(f"line {index}: {exc}")
    if errors:
        raise SystemExit("Template validation failed:\n" + "\n".join(errors))

    items: list[dict[str, object]] = []
    seen_ids: set[str] = set()
    for row in rows:
        for item in benchmark_items(row):
            item_id = str(item["id"])
            if item_id in seen_ids:
                raise SystemExit(f"Duplicate benchmark id: {item_id}")
            seen_ids.add(item_id)
            items.append(item)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for item in items:
            handle.write(json.dumps(item, ensure_ascii=False) + "\n")

    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "Prospective external benchmark created after final pipeline freeze",
        "input_csv": str(args.input),
        "output_jsonl": str(args.output),
        "pair_count": len(rows),
        "question_count": len(items),
        "languages": {"pt": len(rows), "en": len(rows)},
        "answerable_pairs": sum(parse_bool(row["answerable"]) for row in rows),
        "unanswerable_pairs": sum(not parse_bool(row["answerable"]) for row in rows),
        "output_sha256": sha256_file(args.output),
        "rule": "Do not tune the pipeline on this file before reporting external-test metrics.",
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {args.output}")
    print(f"Wrote {args.manifest}")
    print(f"SHA-256: {manifest['output_sha256']}")


if __name__ == "__main__":
    main()

