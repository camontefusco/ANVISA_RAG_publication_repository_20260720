from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import DATA_PATH
from src.regulatory_documents import load_regulatory_documents


DEFAULT_BENCHMARK = ROOT / "evaluation" / "publication_benchmark_200.jsonl"
DEFAULT_REPORT = ROOT / "evaluation" / "benchmark_200_audit.json"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def lexical_normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_text = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", ascii_text.lower()).strip()


def grounded_terms(requested: list[str], evidence: list[str]) -> list[str]:
    combined = " ".join(evidence)
    lexical_evidence = lexical_normalize(combined)
    terms: list[str] = []
    for term in requested:
        if lexical_normalize(term) in lexical_evidence and term not in terms:
            terms.append(term)
    if len(terms) >= 5:
        return terms[:7]
    stopwords = {
        "artigo", "anvisa", "devera", "disposto", "mediante", "podera",
        "quando", "resolucao", "segundo", "serao", "somente", "todos",
    }
    for token in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]{6,}", combined):
        if len(terms) >= 5:
            break
        if lexical_normalize(token) in stopwords or token in terms:
            continue
        terms.append(token)
    return terms[:7]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def audit(rows: list[dict[str, Any]], repair_terms: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    documents = load_regulatory_documents(DATA_PATH)
    corpus: dict[str, list[dict[str, str]]] = defaultdict(list)
    for document in documents:
        corpus[document.metadata["citation_label"]].append({
            "source": document.metadata["source_document"],
            "article": document.metadata["article"],
            "text": normalize(document.text),
        })

    expected_buckets = {
        "pt_answerable": 70,
        "en_answerable": 70,
        "complex": 20,
        "unanswerable": 40,
    }
    buckets = Counter()
    pairs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_counts: Counter[str] = Counter()
    term_repairs = 0

    for row in rows:
        pairs[row["pair_id"]].append(row)
        if not row["answerable"]:
            buckets["unanswerable"] += 1
        elif row["category"] in {"multi_article", "exception"}:
            buckets["complex"] += 1
        else:
            buckets[f"{row['language']}_answerable"] += 1

        if not row.get("question") or not row.get("expected_answer"):
            errors.append(f"{row.get('id')}: blank question or answer")
        if row["answerable"]:
            if not row.get("gold_citations") or not row.get("gold_evidence"):
                errors.append(f"{row['id']}: missing gold evidence")
                continue
            for citation, evidence, source, article in zip(
                row["gold_citations"],
                row["gold_evidence"],
                row["gold_sources"],
                row["gold_articles"],
            ):
                source_counts[source] += 1
                references = corpus.get(citation, [])
                if not references:
                    errors.append(f"{row['id']}: citation absent from corpus: {citation}")
                    continue
                if len(references) > 1:
                    errors.append(f"{row['id']}: ambiguous citation label: {citation}")
                matching = [
                    reference
                    for reference in references
                    if reference["source"] == source
                    and reference["article"] == article
                    and reference["text"] == normalize(evidence)
                ]
                if not any(
                    reference["source"] == source and reference["article"] == article
                    for reference in references
                ):
                    errors.append(f"{row['id']}: citation/source/article mismatch")
                if not matching:
                    errors.append(f"{row['id']}: gold evidence differs from parsed corpus")
            repaired = grounded_terms(row.get("gold_terms", []), row["gold_evidence"])
            if repaired != row.get("gold_terms", []):
                term_repairs += 1
                if repair_terms:
                    row["gold_terms"] = repaired
                else:
                    warnings.append(f"{row['id']}: gold terms need lexical repair")
            if len(repaired) < 3:
                warnings.append(f"{row['id']}: fewer than three grounded gold terms")
        else:
            if any(row.get(key) for key in ("gold_sources", "gold_articles", "gold_citations", "gold_evidence")):
                errors.append(f"{row['id']}: unanswerable item contains gold evidence")

    if len(rows) != 200:
        errors.append(f"Expected 200 rows, found {len(rows)}")
    if dict(buckets) != expected_buckets:
        errors.append(f"Bucket mismatch: {dict(buckets)}")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("Duplicate IDs")
    questions = [lexical_normalize(row["question"]) for row in rows]
    if len(questions) != len(set(questions)):
        errors.append("Duplicate normalized questions")

    for pair_id, pair in pairs.items():
        languages = {row["language"] for row in pair}
        if len(pair) != 2 or languages != {"pt", "en"}:
            errors.append(f"{pair_id}: expected one PT and one EN item")
            continue
        if pair[0]["gold_citations"] != pair[1]["gold_citations"]:
            errors.append(f"{pair_id}: bilingual citations differ")
        if pair[0]["answerable"] != pair[1]["answerable"]:
            errors.append(f"{pair_id}: bilingual answerability differs")

    return {
        "audited_at": datetime.now().isoformat(timespec="seconds"),
        "status": "pass" if not errors else "fail",
        "rows": len(rows),
        "pairs": len(pairs),
        "bucket_counts": dict(buckets),
        "language_counts": dict(Counter(row["language"] for row in rows)),
        "source_evidence_counts": dict(source_counts),
        "unique_gold_citations": len(
            {citation for row in rows for citation in row.get("gold_citations", [])}
        ),
        "ambiguous_corpus_citations": sorted(
            citation for citation, references in corpus.items() if len(references) > 1
        ),
        "term_rows_repaired_or_flagged": term_repairs,
        "errors": errors,
        "warnings": warnings,
        "human_review_status": "pending",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the 200-question benchmark.")
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--repair-terms", action="store_true")
    args = parser.parse_args()

    rows = load_jsonl(args.benchmark)
    report = audit(rows, repair_terms=args.repair_terms)
    if args.repair_terms:
        write_jsonl(args.benchmark, rows)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
