---
id: gdocs-exact-title-match
title: Exact-match articles to Drive docs via the published page's real <title>
lane: content
status: queued
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-exact-title-match.sh
progress: scripts/exact_match_gdocs.py missing
probe_status: RUN
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

`gdocs-article-match-dedup` (done, see `tasks/done/`) matched articles to Drive docs by fuzzy
string similarity between the **article's own `title`** (often a rewritten/marketing headline)
and the **Drive filename**. The user correctly pointed out that's a raw signal. There's a much
better one available for the 220 articles that already carry a `googleDoc` published URL:

**A published Google Doc's page has a `<title>` HTML tag that holds the source document's real
Drive title verbatim** — confirmed live: fetching
`https://docs.google.com/document/d/e/2PACX-1vQmkYLuHPc5AzNNBbpux00HeeoGnszoxXmMcVu2dY9HCj5ddi6vosuCivIYzRZx8ufcgeegPnbR-HiY/pub`
(raw HTML, plain `curl`, no auth) gives `<title>Covered Calls vs. Short Puts` — an **exact**
string match against that doc's entry in `gdocs/index.json` (`"Covered Calls vs. Short Puts"`),
even though the article's own displayed title is "Covered Calls vs Cash-Secured Puts" (fuzzy
score only 0.81 in the old report). Published pages are **public** — no Drive API/auth needed,
so this is plain HTTP and doesn't need the Google Drive MCP connector agy doesn't have.

This task builds an exact-match report for every article that already has `googleDoc`, replacing
guesswork with a deterministic string comparison for that subset. It does **not** help articles
without `googleDoc` (nothing to fetch a real title from) — those stay on the fuzzy report from
the prior task.

## Plan

1. Parse every article's `slug`, `title`, and `googleDoc` (when present) from all
   `F:/workspace/ai-stock-suggestion-client/src/data/articles/{year}-q{n}.ts` files (skip
   `index.ts`, `types.ts`) — same extraction approach as the prior task's
   `scripts/match_articles_gdocs.py`, or reuse it directly.
2. Write `scripts/exact_match_gdocs.py`. For each article with a `googleDoc` URL (~220 of them):
   - Fetch the URL with `urllib.request` (stdlib — don't add a new dependency). Set a real
     `User-Agent` header; Google sometimes 4xx's a bare Python UA.
   - Extract the `<title>...` tag's text via regex (case-insensitive, handle no closing tag on
     the same line — Google's markup wraps oddly, confirmed live: `<title>Covered Calls vs.
     Short Puts` had no `</title>` on the same line in a naive same-line regex; search across
     the tag content up to the next `<` instead of requiring `</title>` on one line).
   - HTML-unescape the extracted text (`html.unescape`) and strip whitespace/trailing newline.
   - Look it up against `gdocs/index.json`'s `title` field: try an exact match first, then a
     case-insensitive/whitespace-collapsed fallback. Record which tier matched (or neither).
   - Be polite: small delay between requests (~0.3-0.5s), one retry on a network error/timeout,
     then record `fetch failed` and move on rather than aborting the whole run.
3. Write `gdocs/article-exact-matches.md`: a table — `Slug | Article Title | Extracted Page
   Title | Match Tier | Matched Doc ID` — where Match Tier is one of `exact`, `case-insensitive`,
   `no match in index`, `fetch failed`. Sort exact matches first, then case-insensitive, then the
   failures at the bottom (so the reviewer sees genuine matches before noise).
4. Run it for real against all ~220 articles, sanity-check a handful of rows against
   `gdocs/index.json` by eye.
5. Commit the script (not the gitignored `gdocs/*.md` report — same rule as every prior task in
   this series: check `.gitignore` covers `gdocs/`, don't force it in).

## Decision log

- **2026-08-30** — User flagged the fuzzy article-title-vs-filename score as "too raw" and
  pointed out the published page itself should carry the real title. Verified live (see Goal)
  that it does, exactly, for a doc already confirmed correct by full content comparison in the
  parent conversation. This task operationalizes that as a batch, deterministic check instead of
  one-off manual verification.

## Result

<!-- filled by /desk-log on completion -->
