# papers

One row per paper note under `papers/<category>/*.md` (currently only the `option-writing/`
category exists), parsed from that note's own YAML frontmatter. `papers/option-writing/REVIEW-INDEX.md`
is skipped — it's an index file, not a paper note, and has no frontmatter.

## Columns

| Column | Type | Source | Notes |
|---|---|---|---|
| `slug` | TEXT (primary key) | filename stem | e.g. `bates-2008-market-for-crash-risk` |
| `title` | TEXT | frontmatter `title` | |
| `authors` | TEXT | frontmatter `authors` | comma-separated |
| `year` | INTEGER | frontmatter `year` | |
| `link` | TEXT | frontmatter `link` | |
| `area` | TEXT | frontmatter `area` | one of the tags documented in the `sophie-desk` skill (`vrp-measurement`, `tail-risk`, `covered-calls`, etc.) |
| `category` | TEXT | the folder the note lives in | currently always `option-writing` |
| `relevance` | TEXT | frontmatter `relevance` | `High` / `Medium` / `Low` |
| `has_pdf` | INTEGER | frontmatter `has_pdf` | 0/1 — false means recorded-but-not-downloaded (paywalled etc.), see the note's own `STATUS: PDF NOT DOWNLOADED` line |
| `has_detailed_summary` | INTEGER | frontmatter `has_detailed_summary` | 0/1 — true only if the note has a real `## Detailed Summary` section, not just an abstract-level stub |
| `citations_surfaced` | INTEGER | frontmatter `citations_surfaced` | count under the note's own "Notable Citations to Follow Up" |
| `file_path` | TEXT | computed | path relative to the workspace root, for opening the note from a query result |

## Paired full-text table: `papers_fts`

An FTS5 virtual table over `slug` / `title` / `authors` / `body` (`body` = the entire note
text after frontmatter, so this also searches Summary and Detailed Summary content). Query it
with `MATCH`, not `WHERE ... LIKE`:

```python
conn.execute("SELECT title, slug FROM papers_fts WHERE papers_fts MATCH 'variance risk premium'").fetchall()
# a hyphenated term needs to be quoted as a phrase, or FTS5 parses the "-" as NOT
conn.execute('SELECT slug FROM papers_fts WHERE papers_fts MATCH \'"HAR-RV"\'').fetchall()
```

## Example queries

```sql
-- everything still only abstract-level
SELECT slug, area, relevance FROM papers WHERE has_detailed_summary = 0;

-- recorded but not actually downloaded
SELECT slug, area FROM papers WHERE has_pdf = 0;

-- library composition by area
SELECT area, count(*) FROM papers GROUP BY area ORDER BY count(*) DESC;
```
