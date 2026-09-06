# article_gdoc_matches

This is `papers.db`'s **derived copy** — a straight row-for-row copy of `gdocs/db/gdocs.db`'s
own `article_gdoc_matches` table (the source of truth, written directly by
`scripts/exact_match_gdocs.py`). See [DATABASES.md](DATABASES.md) for the Index-DB-vs-Source-DB
distinction. One row per Sophie article evaluated: whether that article's companion Gemini
Deep Research doc could be found by matching Drive doc titles against the article's own title.
220 articles evaluated as of 2026-09-06 (162 exact, 11 suffix-tolerant, 45 no match in index, 2
fetch-failed).

Only populated when `gdocs/db/gdocs.db` exists on the machine running the build (same as
[gdocs_index](gdocs_index.md) — gitignored personal data, local-only).

## Columns

| Column | Type | Notes |
|---|---|---|
| `slug` | TEXT (primary key) | the Sophie article's slug |
| `article_title` | TEXT | the article's own title |
| `extracted_page_title` | TEXT | the title actually found in the fetched Drive doc — may read oddly for a no-match/fetch-failed row |
| `match_tier` | TEXT | full-fidelity tier: `exact` / `case-insensitive` / `suffix-tolerant` / `ambiguous (N candidates)` / `no match in index` / `fetch failed`. Stored raw on purpose — collapsing the three matched tiers into one `matched` label was a markdown-report display convenience, not something baked into storage; collapse it at query time if you want that view (see below). |
| `matched_doc_id` | TEXT, nullable | references [gdocs_index](gdocs_index.md)`.doc_id`; **`NULL`** when not matched — not an empty string (that would trip the FK constraint in the source db; see [DATABASES.md](DATABASES.md)'s SQLite-practices section) |

## Example queries

```sql
-- join through to the real Drive doc title for every matched article
SELECT m.slug, m.article_title, g.title AS drive_title
FROM article_gdoc_matches m
JOIN gdocs_index g ON g.doc_id = m.matched_doc_id
WHERE m.match_tier IN ('exact', 'case-insensitive', 'suffix-tolerant');

-- collapse the fine-grained tiers into a single "matched" view
SELECT slug, article_title,
       CASE WHEN match_tier IN ('exact', 'case-insensitive', 'suffix-tolerant')
            THEN 'matched' ELSE match_tier END AS status
FROM article_gdoc_matches;

-- articles still needing a manual look
SELECT slug, article_title, match_tier
FROM article_gdoc_matches
WHERE match_tier NOT IN ('exact', 'case-insensitive', 'suffix-tolerant');
```
