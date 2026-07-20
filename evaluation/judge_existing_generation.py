from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.answer_quality import AnswerQualityJudge
from evaluation.publication_eval import (
    DEFAULT_BENCHMARK,
    DEFAULT_SPLIT_MANIFEST,
    BenchmarkItem,
    directory_checksums,
    expanded_context_pairs,
    filter_benchmark_split,
    load_benchmark,
    metadata_value_from_node,
    package_versions,
    sha256_file,
    write_csv,
)
from src.config import (
    BM25_TOP_K,
    DATA_PATH,
    EMBEDDING_MAX_LENGTH,
    GEMINI_ANSWER_MODEL,
    HUGGINGFACE_EMBEDDING_MODEL_ID,
    HYBRID_FUSION_TOP_K,
    HYBRID_RRF_K,
    RERANKER_BATCH_SIZE,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_N,
    SIMILARITY_TOP_K,
    VECTOR_STORE_PATH,
)
from src.engine import load_index
from src.retrieval import HybridRetriever


DEFAULT_OUTPUT_DIR = (
    ROOT / "evaluation" / "publication_results" / "ai_judge_heldout_20260714"
)
DEFAULT_GENERATION_CSVS = [
    ROOT
    / "evaluation"
    / "publication_results"
    / "generation_en_heldout_20260709"
    / "generation_evaluation_2026-07-10_01-03-11.csv",
    ROOT
    / "evaluation"
    / "publication_results"
    / "generation_pt_heldout_20260709"
    / "generation_evaluation_2026-07-10_01-28-15.csv",
]
JUDGE_FIELDS = [
    "judge_faithfulness",
    "judge_citation_correctness",
    "judge_completeness",
    "judge_refusal_correctness",
    "judge_rationale",
    "judge_error",
]


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def read_generation_csvs(paths: list[Path]) -> tuple[list[dict[str, str]], list[str]]:
    rows: list[dict[str, str]] = []
    fieldnames: list[str] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames:
                for field in reader.fieldnames:
                    if field not in fieldnames:
                        fieldnames.append(field)
            for row in reader:
                row["_generation_csv"] = str(path.resolve())
                rows.append(row)
    if not rows:
        raise ValueError("No generation rows found.")
    if "_generation_csv" not in fieldnames:
        fieldnames.append("_generation_csv")
    return rows, fieldnames


def read_checkpoint(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    judged: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            judged[str(row["id"])] = row
    return judged


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_benchmark_by_id(
    benchmark_path: Path,
    split_manifest_path: Path,
    split: str | None,
) -> dict[str, BenchmarkItem]:
    items = filter_benchmark_split(load_benchmark(benchmark_path), split_manifest_path, split)
    return {item.id: item for item in items}


def retrieve_contexts(
    retriever: HybridRetriever,
    retrieval_query: str,
    rerank_query: str,
    question: str,
    top_k: int,
) -> list[tuple[str, str]]:
    fused_nodes = retriever.retrieve_fused(retrieval_query)
    candidate_nodes = retriever.rerank(rerank_query, fused_nodes)
    retrieved_nodes = candidate_nodes[:top_k]
    return expanded_context_pairs(retriever, retrieved_nodes, question)


def numeric_values(rows: list[dict[str, Any]], key: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        value = row.get(key, "")
        if value in ("", None):
            continue
        try:
            values.append(float(value))
        except (TypeError, ValueError):
            continue
    return values


def metric_mean(rows: list[dict[str, Any]], key: str) -> str:
    values = numeric_values(rows, key)
    return f"{mean(values):.3f}" if values else "not available"


def build_summary(rows: list[dict[str, Any]], generation_csvs: list[Path]) -> str:
    judged_rows = [row for row in rows if not row.get("judge_error")]
    error_rows = [row for row in rows if row.get("judge_error")]
    answerable_rows = [row for row in judged_rows if parse_bool(row.get("answerable"))]
    unanswerable_rows = [
        row for row in judged_rows if not parse_bool(row.get("answerable"))
    ]
    languages = sorted({row.get("language", "") for row in judged_rows})

    lines = [
        "# AI-Judge Evaluation of Frozen Held-Out RAG Answers",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Input rows: {len(rows)}",
        f"Successfully judged rows: {len(judged_rows)}",
        f"Rows with judge errors: {len(error_rows)}",
        f"Answerable judged rows: {len(answerable_rows)}",
        f"Unanswerable judged rows: {len(unanswerable_rows)}",
        "",
        "## Inputs",
        "",
    ]
    for path in generation_csvs:
        lines.append(f"- {path}")

    lines.extend(
        [
            "",
            "## Overall AI-Judge Metrics",
            "",
            f"- Faithfulness, answerable rows: {metric_mean(answerable_rows, 'judge_faithfulness')}",
            f"- Citation correctness, answerable rows: {metric_mean(answerable_rows, 'judge_citation_correctness')}",
            f"- Completeness, answerable rows: {metric_mean(answerable_rows, 'judge_completeness')}",
            f"- Refusal correctness, unanswerable rows: {metric_mean(unanswerable_rows, 'judge_refusal_correctness')}",
            "",
            "## By Language",
            "",
        ]
    )
    for language in languages:
        language_rows = [row for row in judged_rows if row.get("language") == language]
        language_answerable = [
            row for row in language_rows if parse_bool(row.get("answerable"))
        ]
        language_unanswerable = [
            row for row in language_rows if not parse_bool(row.get("answerable"))
        ]
        lines.extend(
            [
                f"### {language}",
                "",
                f"- Judged rows: {len(language_rows)}",
                f"- Faithfulness: {metric_mean(language_answerable, 'judge_faithfulness')}",
                f"- Citation correctness: {metric_mean(language_answerable, 'judge_citation_correctness')}",
                f"- Completeness: {metric_mean(language_answerable, 'judge_completeness')}",
                f"- Refusal correctness: {metric_mean(language_unanswerable, 'judge_refusal_correctness')}",
                "",
            ]
        )

    lines.extend(
        [
            "## Publication Use",
            "",
            "- These scores are automated LLM-judge labels over frozen generated answers.",
            "- They should be reported as AI-judge validation, not as human expert validation.",
            "- The retrieved evidence was reconstructed with the saved retrieval and rerank queries from the original generation CSVs.",
            "- The generation outputs were not regenerated during this judge-only run.",
        ]
    )
    return "\n".join(lines) + "\n"


def run_judge(
    generation_csvs: list[Path],
    benchmark_path: Path,
    split_manifest_path: Path,
    split: str | None,
    output_dir: Path,
    top_k: int,
    limit: int | None,
    continue_on_error: bool,
) -> tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, original_fields = read_generation_csvs(generation_csvs)
    benchmark_by_id = load_benchmark_by_id(benchmark_path, split_manifest_path, split)
    rows = [row for row in rows if row.get("id") in benchmark_by_id]
    if limit is not None:
        rows = rows[:limit]
    if not rows:
        raise ValueError("No rows remain after matching generation CSV rows to benchmark.")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    checkpoint_path = output_dir / f"ai_judge_checkpoint_{timestamp}.jsonl"

    index, _embed_model = load_index()
    retriever = HybridRetriever(
        index=index,
        dense_top_k=max(SIMILARITY_TOP_K, top_k),
        bm25_top_k=max(BM25_TOP_K, top_k),
        fusion_top_k=max(HYBRID_FUSION_TOP_K, top_k),
        rrf_k=HYBRID_RRF_K,
        reranker_model_name=RERANKER_MODEL_NAME,
        reranker_top_n=RERANKER_TOP_N,
        reranker_batch_size=RERANKER_BATCH_SIZE,
    )
    judge = AnswerQualityJudge(GEMINI_ANSWER_MODEL)

    judged_rows: list[dict[str, Any]] = []
    resumed = read_checkpoint(checkpoint_path)
    for row_number, row in enumerate(rows, start=1):
        item = benchmark_by_id[str(row["id"])]
        if row["id"] in resumed:
            judged_rows.append(resumed[row["id"]])
            continue

        print(f"[{row_number}/{len(rows)}] judging {row['id']}", flush=True)
        output_row: dict[str, Any] = dict(row)
        try:
            retrieval_query = row.get("retrieval_query") or row.get("question") or item.question
            rerank_query = row.get("rerank_query") or retrieval_query
            row_top_k = int(row.get("top_k") or top_k)
            contexts = retrieve_contexts(
                retriever=retriever,
                retrieval_query=retrieval_query,
                rerank_query=rerank_query,
                question=row.get("question") or item.question,
                top_k=row_top_k,
            )
            judged = judge.evaluate(
                question=row.get("question") or item.question,
                answer=row.get("answer", ""),
                expected_answer=item.expected_answer,
                answerable=item.answerable,
                contexts=contexts,
            )
            output_row.update(
                {
                    "judge_faithfulness": judged.faithfulness,
                    "judge_citation_correctness": judged.citation_correctness,
                    "judge_completeness": judged.completeness,
                    "judge_refusal_correctness": judged.refusal_correctness,
                    "judge_rationale": judged.rationale,
                    "judge_error": "",
                }
            )
        except Exception as exc:
            if not continue_on_error:
                raise
            output_row.update(
                {
                    "judge_faithfulness": "",
                    "judge_citation_correctness": "",
                    "judge_completeness": "",
                    "judge_refusal_correctness": "",
                    "judge_rationale": "",
                    "judge_error": f"{type(exc).__name__}: {exc}",
                }
            )

        judged_rows.append(output_row)
        append_jsonl(checkpoint_path, output_row)

    output_fields = list(original_fields)
    for field in JUDGE_FIELDS:
        if field not in output_fields:
            output_fields.append(field)
    detailed_path = output_dir / f"ai_judge_evaluation_{timestamp}.csv"
    summary_path = output_dir / f"ai_judge_summary_{timestamp}.md"
    manifest_path = output_dir / f"ai_judge_manifest_{timestamp}.json"

    write_csv(
        detailed_path,
        [{field: row.get(field, "") for field in output_fields} for row in judged_rows],
    )
    summary_path.write_text(build_summary(judged_rows, generation_csvs), encoding="utf-8")
    manifest = {
        "timestamp": timestamp,
        "purpose": "AI-judge evaluation of frozen held-out generation CSVs",
        "generation_csvs": [str(path.resolve()) for path in generation_csvs],
        "generation_csv_sha256": {
            str(path.resolve()): sha256_file(path) for path in generation_csvs
        },
        "benchmark": str(benchmark_path.resolve()),
        "benchmark_sha256": sha256_file(benchmark_path),
        "split": split or "all",
        "split_manifest": str(split_manifest_path.resolve()) if split else None,
        "split_manifest_sha256": sha256_file(split_manifest_path) if split else None,
        "question_count": len(judged_rows),
        "top_k": top_k,
        "judge_model": GEMINI_ANSWER_MODEL,
        "retrieval": {
            "embedding_model": HUGGINGFACE_EMBEDDING_MODEL_ID,
            "embedding_max_length": EMBEDDING_MAX_LENGTH,
            "dense_top_k": max(SIMILARITY_TOP_K, top_k),
            "bm25_top_k": max(BM25_TOP_K, top_k),
            "fusion_top_k": max(HYBRID_FUSION_TOP_K, top_k),
            "rrf_k": HYBRID_RRF_K,
            "reranker": RERANKER_MODEL_NAME,
            "reranker_top_n": RERANKER_TOP_N,
        },
        "corpus_checksums": directory_checksums(DATA_PATH, "*.txt"),
        "vector_store_checksums": directory_checksums(VECTOR_STORE_PATH, "*.json"),
        "package_versions": package_versions(),
        "note": "Generation answers are frozen; this run reconstructs retrieval evidence and judges answer quality only.",
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"AI-judge results: {detailed_path}")
    print(f"AI-judge summary: {summary_path}")
    print(f"AI-judge manifest: {manifest_path}")
    return detailed_path, summary_path, manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Use an AI judge to score already-generated RAG answers."
    )
    parser.add_argument(
        "--generation-csv",
        action="append",
        type=Path,
        dest="generation_csvs",
        help="Generation evaluation CSV to judge. Can be passed more than once.",
    )
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT_MANIFEST)
    parser.add_argument(
        "--split",
        choices=["calibration_20", "dev_remaining_5", "held_out_test_75"],
        default="held_out_test_75",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_judge(
        generation_csvs=args.generation_csvs or DEFAULT_GENERATION_CSVS,
        benchmark_path=args.benchmark,
        split_manifest_path=args.split_manifest,
        split=args.split,
        output_dir=args.output_dir,
        top_k=args.top_k,
        limit=args.limit,
        continue_on_error=args.continue_on_error,
    )


if __name__ == "__main__":
    main()
