# article_gdoc_matches

One row per Sophie article evaluated in `gdocs/article-exact-matches.md` — whether that
article's companion Gemini Deep Research doc could be found by matching Drive doc titles
against the article's own title. 220 articles evaluated as of 2026-09-05 (215 matched, 3
confirmed no-match, 2 fetch-failed).

Only populated when `gdocs/` exists on the machine running the build (same as
[gdocs_index](gdocs_index.md) — gitignored personal data, local-only).

## Columns

| Column | Type | Notes |
|---|---|---|
| `slug` | TEXT (primary key) | the Sophie article's slug |
| `article_title` | TEXT | the article's own title |
| `extracted_page_title` | TEXT | the title actually found in the fetched Drive doc — may read oddly for a no-match/fetch-failed row |
| `match_tier` | TEXT | `matched`, `no match (confirmed)`, or `fetch failed` |
| `matched_doc_id` | TEXT | references [gdocs_index](gdocs_index.md)`.doc_id`; empty when not matched |

## Example queries

```sql
-- join through to the real Drive doc title for every matched article
SELECT m.slug, m.article_title, g.title AS drive_title
FROM article_gdoc_matches m
JOIN gdocs_index g ON g.doc_id = m.matched_doc_id
WHERE m.match_tier = 'matched';

-- articles still needing a manual look
SELECT slug, article_title, match_tier FROM article_gdoc_matches WHERE match_tier != 'matched';
```
