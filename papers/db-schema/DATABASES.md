# Databases

Every SQLite file in this vault, what kind it is, and how to add a new one. Two kinds exist,
and the distinction is the whole point of this page — picking the wrong one for a new table is
the mistake this doc exists to prevent.

## The two kinds

### Index DB — one per vault, fully disposable

**[papers/paper-index/papers.db](../paper-index/)** is the only one. Built by
`sophie-pipeline/paper-index/build_index.py`, which **deletes the whole file and recreates it
from scratch every run** — never edited in place, never trusted to persist anything on its
own. Its job is to aggregate every source (markdown notes, the candidates backlog, and any
Source DB, below) into one place for unified querying — `Papers.md` and this schema's own
[STATUS.md](STATUS.md) render off it via `sqlite-query` blocks.

**Because it's fully disposable, it must never be where anything authoritative lives.** If a
table in here held the only copy of some fact, deleting the file (which happens on every
rebuild) would destroy that fact. Every table in `papers.db` is a *derived copy* of something
that lives elsewhere — markdown frontmatter, a markdown table, or a Source DB.

Rebuild: `python build_index.py` in `sophie-pipeline/paper-index/`. Triggered automatically by
whatever workflow changes the underlying data (see "When does papers.db get rebuilt" below) —
not by the supervisor, and not on a timer. That was tried (2026-09-05/06) and reverted: tying a
rebuild to the tasks-supervisor's tick cadence meant rebuilding constantly for data that
changes rarely, for a table (`tasks`) that turned out not to even need it once `Desk.md`
reverted to live Dataview.

### Source DBs — one per structured, machine-generated data domain, persistent

**[gdocs/db/gdocs.db](../../gdocs/db/)** is the first one. A small, **never torn down**
SQLite file, written to directly by the script(s) that own that data
(`scripts/sync_gdocs_index.py`, `scripts/exact_match_gdocs.py`) instead of a markdown/JSON
file. `papers.db`'s rebuild reads FROM it (a straight table copy, see
`build_index.py`'s `read_gdocs_source_db()`) to populate its own derived `gdocs_index`/
`article_gdoc_matches` tables — the same role `gdocs/index.json` and
`gdocs/article-exact-matches.md` played before 2026-09-06.

**When a Source DB is the right call, and when it isn't:** gdocs data qualified because all
three of these are true — check all three before creating a new one:
1. **Pure structured data, no prose.** A row of columns, not a document with sections a human
   or agent writes by hand (that's what papers/candidates/tasks markdown is for).
2. **Machine-generated, not hand-curated.** A script produces the complete current state each
   run; nobody opens the file to tweak one row.
3. **Gitignored (or otherwise not needing git history).** `gdocs/` is personal data, never
   committed, so a Source DB loses nothing git-diffability-wise over a text file. Papers,
   candidates, and tasks are all git-tracked *content* of this public repo — moving those to a
   database would mean either losing git history/diffability for them, or maintaining a
   text export anyway (recreating today's setup with the direction reversed). Don't.

If your new data fails any of those three, it stays markdown — that's not a limitation to work
around, it's the correct answer.

## When does papers.db get rebuilt

Nothing polls for changes. Instead:

- **A Source DB script triggers it directly**, as its own last step, right after it finishes
  writing (see `sqlite_source_db.trigger_index_rebuild()`, called from both
  `sync_gdocs_index.py` and `exact_match_gdocs.py` unless run with `--no-rebuild-index`) — the
  script finishing *is* the event that invalidates the index, so it's the right trigger.
- **A task that changes papers/candidates markdown should do the same** — call
  `python build_index.py` (in `sophie-pipeline/paper-index/`) as a closing step, the same way a
  Source DB script does. Not yet automated for librarian-round tasks; treat it as a manual
  step in "Closing a task" until/unless that's wired up.
- **Or just run it by hand** any time you want to be sure `Papers.md`/`STATUS.md` reflect the
  current state right now.

## How to register a new table

**Adding a table to papers.db (an Index DB table, derived from something else):**
1. Add the `CREATE TABLE` to `sophie-pipeline/paper-index/schema.sql`.
2. Add a loader in `build_index.py`'s `build()` that reads your source (markdown, JSON, or a
   Source DB) and `INSERT`s rows — follow an existing loader as a template depending on your
   source shape (`parse_paper_note` for frontmatter, `parse_candidates_file` for a markdown
   pipe-table, `read_gdocs_source_db` for another db).
3. Add a page under `papers/db-schema/` documenting it (columns, one example query) and link
   it from this file's Source/Index list and from [README.md](README.md)'s table list.
4. Rebuild and verify: row count matches what you expect, spot-check a few rows.

**Adding a new Source DB (only if your data passes the three-part test above):**
1. Give it its own dedicated folder, one db per folder (`<domain>/db/<domain>.db` — matches
   `gdocs/db/gdocs.db`), separate from any non-database files that domain also has (script
   checkpoints, etc.).
2. Write its schema as a `CREATE TABLE IF NOT EXISTS` string (idempotent — this file is never
   torn down) and use `scripts/sqlite_source_db.py`'s `connect()`/`full_refresh()` rather than
   reimplementing pragmas/transaction handling — see `scripts/gdocs_db.py` as the template (a
   thin wrapper supplying just the schema and default path).
3. Have the script(s) that write it call `sqlite_source_db.trigger_index_rebuild()` as their
   last step (with a `--no-rebuild-index` opt-out flag, matching `sync_gdocs_index.py` and
   `exact_match_gdocs.py`).
4. Add the Index DB loader + schema/doc steps above so `papers.db` picks it up.
5. Add it to this page's Source DB list.

## Standard SQLite practices applied here

Worth naming explicitly since they're easy to skip on a small local tool and then regret:

- **WAL journal mode** (`PRAGMA journal_mode = WAL`) on every Source DB connection — a
  concurrent reader (Obsidian's SQLite Explorer, a `build_index.py` rebuild) doesn't block on
  a writer mid-refresh, and never sees a half-written transaction.
- **`synchronous = NORMAL`** — the standard safe pairing with WAL.
- **`foreign_keys = ON`** — SQLite doesn't enforce these by default per-connection; if a
  column references another table's primary key (like `article_gdoc_matches.matched_doc_id` →
  `gdocs_index.doc_id`), turn this on or the reference is decorative. Store `NULL` for "no
  reference," never an empty string — `''` is not `NULL` and trips the constraint. Hit live:
  every unmatched row in the first `exact_match_gdocs.py` run against the new schema failed
  with `FOREIGN KEY constraint failed` until this was fixed.
- **DELETE-then-INSERT in one transaction** (`sqlite_source_db.full_refresh()`) for a source
  that re-derives its complete state every run, rather than an incremental diff. Atomic and
  simple; use parameterized `INSERT ... ON CONFLICT DO UPDATE` instead if a future source is
  naturally incremental (updates one row at a time rather than rescanning everything).
- **`PRAGMA defer_foreign_keys = ON` before a full-refresh transaction that touches a table
  another table holds an FK into.** SQLite checks FK constraints per statement by default, so
  refreshing `gdocs_index` (referenced by `article_gdoc_matches.matched_doc_id`) rejected the
  `DELETE` outright the moment any row referenced it — even though the very next statement
  would restore the same keys. Deferring to commit time means only a reference still dangling
  once everything's back in place actually fails, which is correct. Hit live: every
  `sync_gdocs_index.py` run failed with `FOREIGN KEY constraint failed` until this was added to
  `full_refresh()`.
- **Idempotent schema** (`CREATE TABLE IF NOT EXISTS`) on every Source DB — it's never torn
  down, so schema setup must be safe to run against a file that already has data.
- **Parameterized queries throughout** (`executemany` with `:name` placeholders) — never
  string-format a value into SQL.
