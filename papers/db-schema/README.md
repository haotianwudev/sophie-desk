# papers.db schema

Reference for the local SQLite index built from this vault's own markdown — `papers/`,
`papers/candidates/`, and `gdocs/`. The database itself lives at
[papers/paper-index/papers.db](../paper-index/) (gitignored, disposable, rebuilt from
markdown any time it changes) — these notes document its *shape*, they aren't the database.

**Source of truth stays the markdown.** Nothing here is hand-maintained data; it's a map of
what querying the DB gets you. The actual build script and full column-level schema live in
the `sophie-pipeline` repo, not this vault:

- `sophie-pipeline/paper-index/build_index.py` — the builder
- `sophie-pipeline/paper-index/schema.sql` — the authoritative `CREATE TABLE` statements
- `sophie-pipeline/paper-index/README.md` — rebuild command, querying examples, Obsidian
  SQLite-plugin setup

Rebuild any time `papers/` or `gdocs/` markdown changes:

```bash
cd /f/workspace/sophie-pipeline/paper-index
python build_index.py
```

## Tables

| Table | Rows from | Note |
|---|---|---|
| [papers](papers.md) | `papers/<category>/*.md` frontmatter | one row per paper note |
| [candidates](candidates.md) | `papers/candidates/*.md` tables | one row per backlog candidate |
| [gdocs_index](gdocs_index.md) | `gdocs/index.json` | raw Google Drive `.gdoc` stub scan |
| [article_gdoc_matches](article_gdoc_matches.md) | `gdocs/article-exact-matches.md` | article slug → matched Drive doc |

`gdocs_index` and `article_gdoc_matches` are only populated when `gdocs/` exists on the
machine running the build — that folder is gitignored personal data (the user's own Drive
research-session titles), present only on their workstation, never in this public repo.

## A parsing gotcha worth knowing before trusting a query

Every table above is parsed out of markdown pipe-tables. A literal `|` inside a cell is
written `\|` per standard markdown escaping, and the shared row-splitter respects that
(splits on *unescaped* `|` only, then un-escapes `\|` back to `|`) — but this was a real bug
until 2026-09-05: naive `str.split("|")` silently shifted every later column by one for any
row whose title/why text contained an escaped pipe. It corrupted `status` in 3 `candidates`
rows and `match_tier`/`matched_doc_id` in 1 `article_gdoc_matches` row before the fix. If a
future markdown edit reintroduces raw (unescaped) pipes in a cell instead of `\|`, that same
corruption pattern will return — worth a spot-check (`SELECT DISTINCT status FROM candidates`
should only ever show real status strings, never a title/link fragment) after any bulk edit
to a candidates or gdocs source file.
