#!/usr/bin/env python3
"""Match a query string against the indexed Google Drive documents.

Loads gdocs/index.json and ranks doc titles by similarity using
difflib.SequenceMatcher.

Usage:
    python scripts/match_gdoc.py "<query title>" [--top 5]
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INDEX_PATH = REPO_ROOT / "gdocs" / "index.json"


def match_docs(
    query: str,
    index_path: Path = DEFAULT_INDEX_PATH,
    top_n: int = 5,
) -> list[tuple[float, dict]]:
    """Ranks indexed documents against a query string by title similarity."""
    if not index_path.exists():
        sys.exit(
            f"Error: {index_path} does not exist.\n"
            "Please run 'python scripts/sync_gdocs_index.py' first to build the index."
        )

    try:
        with open(index_path, "r", encoding="utf-8") as f:
            docs = json.load(f)
    except Exception as exc:
        sys.exit(f"Error reading {index_path}: {exc}")

    query_norm = query.strip().lower()
    scored: list[tuple[float, dict]] = []

    for doc in docs:
        title = doc.get("title", "")
        ratio = difflib.SequenceMatcher(None, query_norm, title.strip().lower()).ratio()
        scored.append((ratio, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Query string (e.g. paper title)")
    parser.add_argument(
        "--top",
        "-n",
        type=int,
        default=5,
        help="Number of top matches to display (default: 5)",
    )
    parser.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX_PATH,
        help=f"Path to index.json (default: {DEFAULT_INDEX_PATH})",
    )

    args = parser.parse_args()

    matches = match_docs(args.query, index_path=args.index, top_n=args.top)
    for score, doc in matches:
        doc_id = doc.get("doc_id", "")
        title = doc.get("title", "")
        print(f"{score:.2f}  {doc_id}  {title}")


if __name__ == "__main__":
    main()
