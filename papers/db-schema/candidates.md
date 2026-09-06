# candidates

One row per entry in the pipe-table on any `papers/candidates/<topic>.md` page — the
follow-up backlog of papers surfaced as worth fetching but not yet gathered (or already
resolved into a real note). 1000+ rows total across all topic pages as of 2026-09, which is
exactly why this DB exists — Dataview can no longer handle this table's scale.

## Columns

| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER (primary key, autoincrement) | row identity, not meaningful beyond that |
| `topic` | TEXT | the topic page's filename stem, e.g. `vrp-option-writing`, `market-microstructure` |
| `title` | TEXT | best-guess paper title |
| `authors_year` | TEXT | free text, not split into separate fields |
| `why` | TEXT | why it looks worth getting |
| `tags` | TEXT | comma-separated, freeform |
| `surfaced_by` | TEXT | the paper slug or Sophie article link(s) that surfaced this candidate |
| `doc_id_source` | TEXT | Gemini Deep Research Drive `doc_id`(s), when sourced that way — comma-separated if more than one |
| `status` | TEXT | free text — empty (unresolved), `Selected -- <task-id>` (picked for an in-flight librarian round), or `Fetched -- <note-filename>` (resolved into a real `papers/option-writing/` note) |

## Paired full-text table: `candidates_fts`

FTS5 over `title` / `authors_year` / `why` / `tags`:

```python
conn.execute("SELECT title, authors_year FROM candidates_fts WHERE candidates_fts MATCH 'kelly'").fetchall()
```

## Example queries

```sql
-- backlog size by topic
SELECT topic, count(*) FROM candidates GROUP BY topic ORDER BY count(*) DESC;

-- unresolved candidates in one topic
SELECT title, authors_year FROM candidates WHERE topic = 'vrp-option-writing' AND status = '';

-- what's currently picked for an in-flight round but not yet fetched
SELECT title, status FROM candidates WHERE status LIKE 'Selected%';

-- sanity check after any bulk edit to a candidates source file -- every value
-- here should be a real status, never a title/link fragment (see the
-- escaped-pipe parsing gotcha noted in README.md)
SELECT DISTINCT status FROM candidates
WHERE status NOT LIKE '' AND status NOT LIKE 'Fetched%' AND status NOT LIKE 'Selected%';
```
