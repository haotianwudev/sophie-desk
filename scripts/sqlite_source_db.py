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

import sqlite3
from pathlib import Path


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


def full_refresh(conn: sqlite3.Connection, table: str, rows: list[dict]) -> None:
    """Atomically replace every row in `table` with `rows` (dicts whose keys
    match the table's columns). The right pattern when the caller re-derives
    the complete current state each run (a full directory walk, a full
    re-match pass) rather than an incremental diff -- DELETE-then-INSERT in
    one transaction means a concurrent reader (under WAL) always sees either
    the complete old table or the complete new one, never a half-empty table
    mid-refresh. For a source that instead updates one row at a time, use
    plain parameterized INSERT ... ON CONFLICT DO UPDATE (SQLite upsert)
    directly instead of this helper."""
    with conn:  # sqlite3's context manager commits on success, rolls back on exception
        conn.execute(f"DELETE FROM {table}")
        if rows:
            columns = list(rows[0].keys())
            placeholders = ", ".join(f":{c}" for c in columns)
            conn.executemany(
                f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
                rows,
            )
