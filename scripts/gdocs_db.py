"""gdocs' own source db -- see scripts/sqlite_source_db.py for the shared
connection/full-refresh helpers this wraps, and papers/db-schema/DATABASES.md
for the registry entry.

Written directly by sync_gdocs_index.py and exact_match_gdocs.py. Lives in
its own dedicated folder (gdocs/db/), separate from gdocs/classified_state.json
and gdocs/extracted_state.json (those are script checkpoints, not part of
this database). The whole gdocs/ tree is gitignored -- personal data, never
committed -- same as papers/paper-index/papers.db, so keeping this data in a
db instead of a markdown/JSON file loses nothing git-tracking-wise.

Kept separate from papers/paper-index/papers.db on purpose: that file is
fully deleted and rebuilt from scratch on every build_index.py run
(disposable by design) -- which would destroy this data if it lived there
instead. build_index.py reads FROM this db to populate its own derived copy,
the same role gdocs/index.json and gdocs/article-exact-matches.md used to
play before 2026-09-06.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import sqlite_source_db

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = REPO_ROOT / "gdocs" / "db" / "gdocs.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS gdocs_index (
    doc_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    resource_key TEXT,
    relpath TEXT,
    mtime REAL
);

CREATE TABLE IF NOT EXISTS article_gdoc_matches (
    slug TEXT PRIMARY KEY,
    article_title TEXT,
    extracted_page_title TEXT,
    match_tier TEXT,
    matched_doc_id TEXT REFERENCES gdocs_index(doc_id)
);
"""


def connect(db_path: Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    return sqlite_source_db.connect(db_path, SCHEMA)


def full_refresh(conn: sqlite3.Connection, table: str, rows: list[dict]) -> None:
    sqlite_source_db.full_refresh(conn, table, rows)
