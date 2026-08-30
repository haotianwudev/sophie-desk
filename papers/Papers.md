# Papers

Live board over `option-writing/*.md` frontmatter — classification and progress, queryable
instead of scrolled through by eye. New here? **`FOLLOWUP-CANDIDATES.md`** is the todo list of
papers not yet gathered; this is the board for papers already in the library.

Every field below lives in each paper's own frontmatter, not here — this page is nothing but
queries. See the `sophie-desk` skill's "Tracking papers" section for the schema and how to
keep it flat enough for Dataview to read.

---

## By relevance

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Paper",
  area AS "Area",
  year AS "Year",
  has_detailed_summary AS "Deep summary?",
  has_pdf AS "PDF?"
FROM "papers/option-writing"
WHERE relevance
SORT relevance DESC, area ASC
```

## By area

```dataview
TABLE WITHOUT ID
  area AS "Area",
  length(rows) AS "Papers",
  join(rows.relevance, ", ") AS "Relevance mix"
FROM "papers/option-writing"
WHERE area
GROUP BY area
SORT length(rows) DESC
```

## Still only abstract-level (no deep methodology read yet)

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Paper",
  area AS "Area",
  relevance AS "Relevance"
FROM "papers/option-writing"
WHERE has_detailed_summary = false
SORT relevance DESC
```

## Recorded but not actually downloaded

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Paper",
  area AS "Area",
  relevance AS "Relevance"
FROM "papers/option-writing"
WHERE has_pdf = false
```

## Everything, sortable

```dataview
TABLE WITHOUT ID
  link(file.link, title) AS "Paper",
  authors AS "Authors",
  year AS "Year",
  area AS "Area",
  relevance AS "Relevance",
  citations_surfaced AS "Citations found"
FROM "papers/option-writing"
SORT area ASC, relevance DESC
```
