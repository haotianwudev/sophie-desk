# Papers

Live board over `option-writing/*.md` frontmatter — classification and progress, queryable
instead of scrolled through by eye. New here? **`FOLLOWUP-CANDIDATES.md`** is the todo list of
papers not yet gathered; this is the board for papers already in the library.

Every field below lives in each paper's own frontmatter, not here — this page is nothing but
queries, rendered via [paper-index/papers.db](paper-index/README.md) (needs the **SQLite
Explorer** Obsidian plugin — see [db-schema/README.md](db-schema/README.md)). **"Paper" below
is the title only, not a clickable link** — the query returns `slug`/`title` from the `papers`
table, not a file reference the plugin can render as a wiki-link; open the actual note from the
file tree (`option-writing/<slug>.md`) if you need to. **Rebuild before trusting this page** —
run `python build_index.py` in `sophie-pipeline/paper-index/` any time a paper note changes.
See the `sophie-desk` skill's "Tracking papers" section for the frontmatter schema.

---

## By relevance

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT title AS "Paper", area AS "Area", year AS "Year",
         has_detailed_summary AS "Deep summary?", has_pdf AS "PDF?"
  FROM papers
  WHERE COALESCE(relevance, '') <> ''
  ORDER BY CASE relevance WHEN 'High' THEN 3 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 1 ELSE 0 END DESC,
           area ASC
```

## By area

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT area AS "Area", count(*) AS "Papers", group_concat(relevance, ', ') AS "Relevance mix"
  FROM papers
  WHERE COALESCE(area, '') <> ''
  GROUP BY area
  ORDER BY count(*) DESC
```

## Still only abstract-level (no deep methodology read yet)

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT title AS "Paper", area AS "Area", relevance AS "Relevance"
  FROM papers
  WHERE has_detailed_summary = 0
  ORDER BY CASE relevance WHEN 'High' THEN 3 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 1 ELSE 0 END DESC
```

## Recorded but not actually downloaded

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT title AS "Paper", area AS "Area", relevance AS "Relevance"
  FROM papers
  WHERE has_pdf = 0
```

## Everything, sortable

```sqlite-query
source: /papers/paper-index/papers.db
sql: |
  SELECT title AS "Paper", authors AS "Authors", year AS "Year", area AS "Area",
         relevance AS "Relevance", citations_surfaced AS "Citations found"
  FROM papers
  ORDER BY area ASC,
           CASE relevance WHEN 'High' THEN 3 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 1 ELSE 0 END DESC
```
