from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rebuild_index import rebuild_index
from scripts.clean_regulatory_texts import (
    DEFAULT_INPUT_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_REPORT_PATH,
    clean_directory,
)
from src.regulatory_documents import load_regulatory_documents


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean, index, verify, and evaluate the ANVISA RAG corpus."
    )
    parser.add_argument("--skip-cleaning", action="store_true")
    parser.add_argument("--skip-index", action="store_true")
    parser.add_argument("--skip-evaluation", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--split",
        choices=["calibration_20", "dev_remaining_5", "held_out_test_75", "all"],
        default="held_out_test_75",
    )
    parser.add_argument(
        "--results-dir",
        type=Path,
        default=ROOT / "evaluation" / "publication_results",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = datetime.now().isoformat(timespec="seconds")
    if not args.skip_cleaning:
        print("[1/4] Cleaning source documents...", flush=True)
        clean_directory(DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR, DEFAULT_REPORT_PATH)
    else:
        print("[1/4] Cleaning skipped.")

    print("[2/4] Validating article parser...", flush=True)
    documents = load_regulatory_documents(DEFAULT_OUTPUT_DIR)
    source_count = len({document.metadata["source_document"] for document in documents})
    if not documents or source_count != 6:
        raise RuntimeError(
            f"Corpus validation failed: {len(documents)} articles, {source_count} sources."
        )
    print(f"Validated {len(documents)} article records from {source_count} sources.")

    chunk_audit = None
    if not args.skip_index:
        print("[3/4] Rebuilding transactional article-aware index...", flush=True)
        chunk_audit = rebuild_index()
    else:
        print("[3/4] Index rebuild skipped.")

    if not args.skip_evaluation:
        print("[4/4] Running locked retrieval evaluation...", flush=True)
        command = [
            sys.executable,
            "-B",
            str(ROOT / "evaluation" / "publication_eval.py"),
            "--results-dir",
            str(args.results_dir),
        ]
        if args.split != "all":
            command.extend(["--split", args.split])
        if args.limit is not None:
            command.extend(["--limit", str(args.limit)])
        subprocess.run(command, cwd=ROOT, check=True)
    else:
        print("[4/4] Evaluation skipped.")

    pipeline_manifest = {
        "started": started,
        "completed": datetime.now().isoformat(timespec="seconds"),
        "cleaning_run": not args.skip_cleaning,
        "index_rebuilt": not args.skip_index,
        "evaluation_run": not args.skip_evaluation,
        "evaluation_split": args.split,
        "evaluation_limit": args.limit,
        "article_count": len(documents),
        "source_count": source_count,
        "chunk_count": chunk_audit.get("chunk_count") if chunk_audit else None,
    }
    manifest_path = ROOT / "reports" / "publication_pipeline_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(pipeline_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Pipeline manifest: {manifest_path}")


if __name__ == "__main__":
    main()
