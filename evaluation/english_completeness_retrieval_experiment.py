from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Any

from llama_index.core.schema import NodeWithScore

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.publication_eval import (
    DEFAULT_BENCHMARK,
    DEFAULT_SPLIT_MANIFEST,
    citation_metrics,
    filter_benchmark_split,
    load_benchmark,
    metadata_value_from_node,
    reciprocal_rank,
    source_hit,
    source_name_from_node,
    write_csv,
)
from src.config import (
    BM25_TOP_K,
    HYBRID_FUSION_TOP_K,
    HYBRID_RRF_K,
    RERANKER_BATCH_SIZE,
    RERANKER_MODEL_NAME,
    RERANKER_TOP_N,
    SIMILARITY_TOP_K,
)
from src.engine import load_index
from src.model_loader import GlossaryQueryRewriter
from src.retrieval import HybridRetriever


DEFAULT_AI_JUDGE_CSV = (
    ROOT
    / "evaluation"
    / "publication_results"
    / "ai_judge_heldout_20260714"
    / "ai_judge_evaluation_2026-07-14_17-11-26.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT / "evaluation" / "publication_results" / "english_completeness_experiment_20260714"
)

EXTRA_QUERY_TERMS = {
    "primary sponsor": "patrocinador primário",
    "investigator-sponsor": "investigador-patrocinador",
    "structural units": "unidades estruturais",
    "keep": "manter",
    "retain": "manter",
    "clinical trial data": "dados do ensaio clínico",
    "development discontinuation": "descontinuação do desenvolvimento",
    "manual": "manual",
    "manually": "manual",
    "documentation submitted manually": "documentação protocolizada manualmente",
    "investigator's obligations": "obrigações do investigador",
    "suspended": "suspenso",
    "terminated": "encerrado",
    "master cell bank": "banco de célula mestre",
    "working cell bank": "banco de célula de trabalho",
    "cell banks": "bancos de células",
    "filing": "protocolização",
    "formats": "formatos",
    "foreign languages": "idiomas estrangeiros",
    "deadline": "prazo",
    "procedural adequacy": "adequação processual",
    "non-reportable": "não reportáveis",
    "revalidation": "revalidação",
    "marketing authorization holder": "detentor de registro de medicamento",
    "marketing authorization holders": "detentores de registro de medicamento",
    "pharmacovigilance": "farmacovigilância",
    "risk management plan": "plano de gerenciamento de risco",
    "risk minimization plan": "plano de minimização de risco",
    "risk minimization": "minimização de risco",
    "standard operating procedures": "procedimentos operacionais padrão",
    "sops": "POPs",
    "optimized analysis": "análise otimizada",
    "risk assessment": "avaliação de risco",
    "legal consequences": "sanções",
    "non-compliance": "descumprimento",
    "Anvisa's decisions": "decisões da Anvisa",
    "status": "situação",
    "excluded": "excluídos",
    "application": "aplicação",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def target_failure_ids(ai_judge_csv: Path, threshold: float) -> set[str]:
    rows = read_csv(ai_judge_csv)
    return {
        row["id"]
        for row in rows
        if row.get("language") == "en"
        and row.get("answerable") == "True"
        and float(row.get("judge_completeness") or 0) < threshold
    }


def append_extra_terms(question: str, query: str) -> str:
    lowered = question.lower()
    additions: list[str] = []
    for english, portuguese in sorted(EXTRA_QUERY_TERMS.items(), key=lambda item: len(item[0]), reverse=True):
        if re.search(rf"\b{re.escape(english)}\b", lowered):
            additions.append(f"{portuguese} ({english})")
    if not additions:
        return query
    unique = list(dict.fromkeys(additions))
    return f"{query} Termos adicionais: {'; '.join(unique)}."


def rrf_fuse_rankings(
    rankings: list[list[NodeWithScore]],
    *,
    limit: int,
    rrf_k: int,
) -> list[NodeWithScore]:
    nodes_by_id: dict[str, Any] = {}
    scores: Counter[str] = Counter()
    for ranking in rankings:
        for rank, node in enumerate(ranking, start=1):
            node_id = node.node.node_id
            nodes_by_id[node_id] = node.node
            scores[node_id] += 1.0 / (rrf_k + rank)
    ranked_ids = sorted(scores, key=lambda node_id: (-scores[node_id], node_id))[:limit]
    return [
        NodeWithScore(node=nodes_by_id[node_id], score=float(scores[node_id]))
        for node_id in ranked_ids
    ]


def multi_query_candidates(
    retriever: HybridRetriever,
    queries: list[str],
    *,
    dense_top_k: int,
    bm25_top_k: int,
    fusion_top_k: int,
    rrf_k: int,
) -> list[NodeWithScore]:
    rankings: list[list[NodeWithScore]] = []
    for query in queries:
        rankings.append(retriever.retrieve_dense(query, top_k=dense_top_k))
        rankings.append(retriever.retrieve_bm25(query, top_k=bm25_top_k))
    return rrf_fuse_rankings(rankings, limit=fusion_top_k, rrf_k=rrf_k)


def unique_nonempty(values: list[str]) -> list[str]:
    cleaned = [value.strip() for value in values if value and value.strip()]
    return list(dict.fromkeys(cleaned))


def build_summary(rows: list[dict[str, Any]]) -> str:
    by_strategy: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_strategy[str(row["strategy"])].append(row)

    lines = [
        "# English Completeness Retrieval Experiment",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Rows evaluated per strategy: {len(next(iter(by_strategy.values()), []))}",
        "",
        "## Metrics",
        "",
        "| Strategy | Rows | Source Hit | Article Recall@5 | Article Recall@8 | Article Recall@10 | Article MRR@5 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for strategy, strategy_rows in by_strategy.items():
        def avg(key: str) -> float:
            values = [float(row[key]) for row in strategy_rows if row.get(key) not in ("", None)]
            return mean(values) if values else 0.0

        lines.append(
            "| "
            + " | ".join(
                [
                    strategy,
                    str(len(strategy_rows)),
                    f"{avg('source_hit'):.3f}",
                    f"{avg('article_recall_at_5'):.3f}",
                    f"{avg('article_recall_at_8'):.3f}",
                    f"{avg('article_recall_at_10'):.3f}",
                    f"{avg('article_mrr_at_5'):.3f}",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `current_saved_query` replays the retrieval query saved in the generation CSV.",
            "- `expanded_glossary` adds failure-focused bilingual aliases to the deterministic glossary query.",
            "- `multi_query_expanded` fuses original English, saved query, and expanded glossary query.",
            "- `paired_pt_question` is a diagnostic upper bound using the paired Portuguese benchmark question.",
            "- `paired_pt_plus_gold_terms` is a leakage upper bound and must not be used as a production method.",
        ]
    )
    return "\n".join(lines) + "\n"


def run_experiment(
    benchmark_path: Path,
    split_manifest_path: Path,
    ai_judge_csv: Path,
    output_dir: Path,
    completeness_threshold: float,
    top_k_values: list[int],
    limit: int | None,
) -> tuple[Path, Path]:
    failure_ids = target_failure_ids(ai_judge_csv, completeness_threshold)
    items = filter_benchmark_split(
        load_benchmark(benchmark_path),
        split_manifest_path,
        "held_out_test_75",
    )
    items_by_id = {item.id: item for item in items}
    pt_question_by_pair = {
        item.pair_id: item.question
        for item in items
        if item.language == "pt"
    }
    en_items = [
        item
        for item in items
        if item.id in failure_ids and item.language == "en" and item.answerable
    ]
    if limit is not None:
        en_items = en_items[:limit]
    if not en_items:
        raise ValueError("No English low-completeness answerable rows found.")

    generation_rows = {
        row["id"]: row
        for row in read_csv(ai_judge_csv)
        if row.get("id") in failure_ids
    }

    index, _embed_model = load_index()
    retriever = HybridRetriever(
        index=index,
        dense_top_k=max(SIMILARITY_TOP_K, 100),
        bm25_top_k=max(BM25_TOP_K, 100),
        fusion_top_k=max(HYBRID_FUSION_TOP_K, 50),
        rrf_k=HYBRID_RRF_K,
        reranker_model_name=RERANKER_MODEL_NAME,
        reranker_top_n=max(RERANKER_TOP_N, max(top_k_values)),
        reranker_batch_size=RERANKER_BATCH_SIZE,
    )
    rewriter = GlossaryQueryRewriter()

    rows: list[dict[str, Any]] = []
    for index_number, item in enumerate(en_items, start=1):
        print(f"[{index_number}/{len(en_items)}] {item.id}", flush=True)
        saved_row = generation_rows[item.id]
        original_query = item.question
        saved_query = saved_row.get("retrieval_query") or rewriter.rewrite(item.question)
        expanded_query = append_extra_terms(item.question, rewriter.rewrite(item.question))
        paired_pt_query = pt_question_by_pair.get(item.pair_id, "")
        gold_terms_query = " ".join(item.gold_terms)
        strategies = {
            "current_saved_query": [saved_query],
            "expanded_glossary": [expanded_query],
            "multi_query_expanded": unique_nonempty(
                [original_query, saved_query, expanded_query]
            ),
            "paired_pt_question": unique_nonempty([paired_pt_query]),
            "paired_pt_plus_gold_terms": unique_nonempty(
                [paired_pt_query, f"{paired_pt_query} {gold_terms_query}"]
            ),
        }
        for strategy_name, queries in strategies.items():
            candidates = multi_query_candidates(
                retriever,
                queries,
                dense_top_k=100,
                bm25_top_k=100,
                fusion_top_k=50,
                rrf_k=HYBRID_RRF_K,
            )
            rerank_query = original_query if strategy_name != "paired_pt_question" else paired_pt_query
            reranked = retriever.rerank(rerank_query or original_query, candidates)
            retrieved_sources = [source_name_from_node(node) for node in reranked]
            retrieved_citations = [
                metadata_value_from_node(node, "citation_label") for node in reranked
            ]
            row: dict[str, Any] = {
                "id": item.id,
                "pair_id": item.pair_id,
                "question": item.question,
                "strategy": strategy_name,
                "query_count": len(queries),
                "queries": " || ".join(queries),
                "gold_citations": ";".join(item.gold_citations),
                "retrieved_citations": ";".join(retrieved_citations),
                "retrieved_sources": ";".join(retrieved_sources),
                "source_hit": source_hit(item.gold_sources, retrieved_sources),
                "source_mrr": reciprocal_rank(item.gold_sources, retrieved_sources),
                "original_judge_completeness": saved_row.get("judge_completeness", ""),
                "original_article_recall_at_k": saved_row.get("article_recall_at_k", ""),
                "original_answer": saved_row.get("answer", ""),
            }
            for top_k in top_k_values:
                metrics = citation_metrics(item.gold_citations, retrieved_citations, top_k)
                row[f"article_recall_at_{top_k}"] = metrics["article_recall_at_k"]
                row[f"article_precision_at_{top_k}"] = metrics["article_precision_at_k"]
                row[f"article_mrr_at_{top_k}"] = metrics["article_mrr_at_k"]
                row[f"article_ndcg_at_{top_k}"] = metrics["article_ndcg_at_k"]
            rows.append(row)

    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    detailed_path = output_dir / f"english_completeness_retrieval_experiment_{timestamp}.csv"
    summary_path = output_dir / f"english_completeness_retrieval_experiment_{timestamp}.md"
    write_csv(detailed_path, rows)
    summary_path.write_text(build_summary(rows), encoding="utf-8")
    print(f"Detailed results: {detailed_path}")
    print(f"Summary: {summary_path}")
    return detailed_path, summary_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diagnose English answer completeness failures with retrieval variants."
    )
    parser.add_argument("--benchmark", type=Path, default=DEFAULT_BENCHMARK)
    parser.add_argument("--split-manifest", type=Path, default=DEFAULT_SPLIT_MANIFEST)
    parser.add_argument("--ai-judge-csv", type=Path, default=DEFAULT_AI_JUDGE_CSV)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--completeness-threshold", type=float, default=0.8)
    parser.add_argument("--top-k-values", type=int, nargs="+", default=[5, 8, 10])
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_experiment(
        benchmark_path=args.benchmark,
        split_manifest_path=args.split_manifest,
        ai_judge_csv=args.ai_judge_csv,
        output_dir=args.output_dir,
        completeness_threshold=args.completeness_threshold,
        top_k_values=args.top_k_values,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
