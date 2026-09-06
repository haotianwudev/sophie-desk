#!/usr/bin/env python3
"""Match a query string against the indexed Google Drive documents.

Reads gdocs/db/gdocs.db's gdocs_index table and ranks doc titles by
similarity using difflib.SequenceMatcher. (Was gdocs/index.json before
2026-09-06 -- see gdocs_db.py and papers/db-schema/DATABASES.md.)

Usage:
    python scripts/match_gdoc.py "<query title>" [--top 5]
"""

from __future__ import annotations

import argparse
import difflib
import sqlite3
import sys
from pathlib import Path

import gdocs_db

REPO_ROOT = Path(__file__).resolve().parent.parent


def match_docs(
    query: str,
    db_path: Path = gdocs_db.DEFAULT_DB_PATH,
    top_n: int = 5,
) -> list[tuple[float, dict]]:
    """Ranks indexed documents against a query string by title similarity."""
    if not db_path.exists():
        sys.exit(
            f"Error: {db_path} does not exist.\n"
            "Please run 'python scripts/sync_gdocs_index.py' first to build the index."
        )

    conn = gdocs_db.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        docs = [dict(row) for row in conn.execute("SELECT * FROM gdocs_index")]
    finally:
        conn.close()

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
        "--db",
        type=Path,
        default=gdocs_db.DEFAULT_DB_PATH,
        help=f"Path to gdocs.db (default: {gdocs_db.DEFAULT_DB_PATH})",
    )

    args = parser.parse_args()

    matches = match_docs(args.query, db_path=args.db, top_n=args.top)
    for score, doc in matches:
        doc_id = doc.get("doc_id", "")
        title = doc.get("title", "")
        print(f"{score:.2f}  {doc_id}  {title}")


if __name__ == "__main__":
    main()
