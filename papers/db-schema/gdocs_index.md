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

See [article_gdoc_matches](article_gdoc_matches.md) for the subset of these that are tied to
a specific Sophie article.
