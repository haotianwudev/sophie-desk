"""Generic helper for a "source" SQLite db: a small, persistent, authoritative
file owned by whatever script writes it directly, as opposed to
papers/paper-index/papers.db (the "index" db -- fully disposable, torn down
and rebuilt from scratch every run, aggregates every source for unified
querying). See papers/db-schema/DATABASES.md for the full registry and the
index-vs-source distinction.

A source db is never torn down -- schema application must be idempotent
(CREATE TABLE IF NOT EXISTS), and writes should assume the file already has
data in it from a previous run.

Usage: a domain-specific module (e.g. gdocs_db.py) supplies its own schema
and default path, and calls connect()/full_refresh() from here rather than
reimplementing pragmas/transaction handling per source.
"""

from __future__ import annotations

import subprocess
import sys
import sqlite3
from pathlib import Path

PAPER_INDEX_BUILD = Path(__file__).resolve().parent.parent.parent / "sophie-pipeline" / "paper-index" / "build_index.py"


def connect(db_path: Path, schema_sql: str) -> sqlite3.Connection:
    """Open a source db with standard pragmas for a small local, single-
    writer, occasional-reader SQLite file, and ensure its schema exists.

    - WAL journal mode: a concurrent reader (Obsidian's SQLite Explorer,
      build_index.py) doesn't block on a writer mid-refresh, and doesn't see
      a half-written transaction -- it sees either the last-committed state
      or the new one, never a torn read.
    - synchronous=NORMAL: the standard safe pairing with WAL (full durability
      on the WAL file itself; the small window that's not fsync'd is the
      most recent commit only, acceptable for a locally-regenerable index).
    - foreign_keys=ON: SQLite doesn't enforce these by default per-connection.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(schema_sql)
    return conn


def trigger_index_rebuild() -> bool:
    """Run sophie-pipeline/paper-index/build_index.py so papers.db picks up
    whatever this source db just wrote. Call this as the last step of any
    script that writes to a source db and wants papers.db to reflect it
    promptly, instead of waiting for someone to remember a manual rebuild --
    the event that invalidates the index (this script finishing) is the
    right trigger, not a poll on a timer (that was tried for tasks via the
    supervisor and reverted, see papers/db-schema/DATABASES.md). Best-effort:
    prints a warning and returns False on failure rather than raising, so a
    sync failure here never masks the caller's own real work having
    succeeded."""
    if not PAPER_INDEX_BUILD.exists():
        print(f"WARN: paper index not rebuilt -- {PAPER_INDEX_BUILD} not found")
        return False
    res = subprocess.run(
        [sys.executable, str(PAPER_INDEX_BUILD)],
        cwd=PAPER_INDEX_BUILD.parent, capture_output=True, text=True,
    )
    if res.returncode != 0:
        print(f"WARN: paper index rebuild failed: {res.stderr.strip()[-300:]}")
        return False
    return True


def full_refresh(conn: sqlite3.Connection, table: str, rows: list[dict]) -> None:
    """Atomically replace every row in `table` with `rows` (dicts whose keys
    match the table's columns). The right pattern when the caller re-derives
    the complete current state each run (a full directory walk, a full
    re-match pass) rather than an incremental diff -- DELETE-then-INSERT in
    one transaction means a concurrent reader (under WAL) always sees either
    the complete old table or the complete new one, never a half-empty table
    mid-refresh. For a source that instead updates one row at a time, use
    plain parameterized INSERT ... ON CONFLICT DO UPDATE (SQLite upsert)
    directly instead of this helper.

    Sets `defer_foreign_keys` for this transaction: refreshing one table that
    another table holds a foreign key into (e.g. gdocs_index, referenced by
    article_gdoc_matches.matched_doc_id) means the DELETE momentarily removes
    rows a *different* table still points at, even though the following
    INSERT restores the same keys -- SQLite checks FK constraints per
    statement by default and rejects that DELETE outright. Deferring to
    commit time means only a FK reference still dangling once everything is
    back in place actually fails, which is the correct behavior. Hit live:
    every gdocs_index refresh failed with FOREIGN KEY constraint failed
    before this fix, as soon as article_gdoc_matches had any rows in it."""
    conn.execute("PRAGMA defer_foreign_keys = ON")
    with conn:  # sqlite3's context manager commits on success, rolls back on exception
        conn.execute(f"DELETE FROM {table}")
        if rows:
            columns = list(rows[0].keys())
            placeholders = ", ".join(f":{c}" for c in columns)
            conn.executemany(
                f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
                rows,
            )
