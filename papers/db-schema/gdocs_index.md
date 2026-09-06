# gdocs_index

One row per entry in `gdocs/index.json` — the raw scan of every `.gdoc` stub under the
user's Google Drive sync folder (`D:\GoogleDrive`), produced by
`scripts/sync_gdocs_index.py`. This is the *full* index of Gemini Deep Research sessions,
not just ones tied to a Sophie article — 335 entries as of 2026-09-05.

Only populated when `gdocs/` exists on the machine running the build — that folder is
gitignored personal data (real Drive doc titles), never committed, present only on the
user's own workstation.

## Columns

| Column | Type | Notes |
|---|---|---|
| `doc_id` | TEXT (primary key) | Google Drive document id |
| `title` | TEXT | the `.gdoc` stub's filename, minus extension — this *is* the Drive doc's title |
| `resource_key` | TEXT | often empty; only set for docs that need one to open |
| `relpath` | TEXT | path relative to the Drive sync root |
| `mtime` | REAL | epoch seconds |

## Example queries

```sql
-- most recently modified research sessions
SELECT title, datetime(mtime, 'unixepoch') AS modified FROM gdocs_index ORDER BY mtime DESC LIMIT 20;

-- does a given doc_id resolve to a real title?
SELECT title FROM gdocs_index WHERE doc_id = '<doc_id>';
```

**Finding duplicate research sessions** (recurring titles with a trailing `(1)`, `(2)`, etc.
— e.g. re-running the same Gemini Deep Research prompt) needs stripping that suffix before
grouping, which plain SQL can't do without a registered function. This replaced the old
static `gdocs/duplicates.md` report (removed 2026-09-05, along with `gdocs/index.md` and
every one-off batch-processing scratch file from the now-complete citation-extraction
pipeline — `gdocs/` keeps only the two source files that feed this DB
(`index.json`, `article-exact-matches.md`) plus `classified_state.json`/`extracted_state.json`,
the resumable checkpoints `scripts/extract_gdoc_citations.py` still reads by default):

```python
import sqlite3, re
conn = sqlite3.connect(r"F:\workspace\sophie-desk\papers\paper-index\papers.db")
conn.create_function("base_title", 1, lambda t: re.sub(r"\s*\(\d+\)$", "", t or "").strip().lower())
conn.execute("""
    SELECT base_title(title) AS base, count(*) AS n, group_concat(title, ' | ') AS titles
    FROM gdocs_index GROUP BY base HAVING n > 1 ORDER BY n DESC
""").fetchall()
```

See [article_gdoc_matches](article_gdoc_matches.md) for the subset of these that are tied to
a specific Sophie article.
