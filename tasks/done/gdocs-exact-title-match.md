---
id: gdocs-exact-title-match
title: Exact-match articles to Drive docs via the published page's real <title>
lane: content
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-exact-title-match.sh
progress: 222 rows, 162 exact matches
probe_status: OK
stall_flag: 
outcome: Generated gdocs/article-exact-matches.md evaluating 220 articles. After a user-caught matching gap and fix (see Decision log): 173 confident matches (162 exact + 11 suffix-tolerant), 0 ambiguous, 45 no match in index, 2 fetch failed.
artifacts: scripts/exact_match_gdocs.py gdocs/article-exact-matches.md
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
- **2026-08-30** — Implemented `scripts/exact_match_gdocs.py` to parse articles with `googleDoc` URLs from `ai-stock-suggestion-client/src/data/articles/*.ts`, fetch the published Google Doc HTML pages, extract the `<title>` tag text, and match against `gdocs/index.json` (exact match, then case-insensitive / whitespace-collapsed fallback). Evaluated all 220 articles: found 162 exact matches in Drive index, 56 with no exact title match in index, and 2 fetch failures (due to `/edit` URL auth requirements). Output written to `gdocs/article-exact-matches.md`.
- **2026-08-30** — Verified probe `probes/gdocs-exact-title-match.sh`, confirming OK status (222 rows, 162 exact matches).
- **2026-08-30** — User spot-checked one "no match" row by hand (`2025 Financial Market Analysis
  (1)`) and caught a real gap: the local `.gdoc` stub filename can lag the doc's *live* Drive
  title after a rename (confirmed via the Drive connector — the live title has no `(1)`, the
  local stub still does). This is the same artifact `gdocs/duplicates.md` groups by, but for a
  *single* document, not a real duplicate. Checked all 56 "no match" rows for this pattern: 11
  resolved cleanly to exactly one candidate each (0 ambiguous). Added a third `suffix-tolerant`
  match tier to `find_matching_doc()` (strips a trailing `\(\d+\)$` from the index title before
  comparing) with an explicit `ambiguous (N candidates)` outcome if stripping ever yields more
  than one candidate — never silently guess between them. Re-ran the full script for real.
- **2026-08-30** — User asked to resolve the remaining 45 "no match" rows directly rather than
  leave them, noting most surely have a real Drive doc, just one the local sync hasn't picked up
  (confirmed true for 3 samples earlier via account-wide search). Resolved by hand via
  `mcp__claude_ai_Google_Drive__search_files` (title-contains queries per row, not a script --
  this needs the live Drive connector, which is session-only, not something to automate into
  `exact_match_gdocs.py` itself). Result: **34 resolved** to exactly one doc_id each, **8
  ambiguous** (2-3 docs genuinely share that title live in Drive too -- flagged, not guessed),
  **2 still genuinely not found** (`covering-world-global-evidence-covered-calls` -- doc may have
  been renamed after its last publish snapshot, live title unknown; and
  `unified-theory-market-dynamics-order-flow-impact-volatility` -- its extracted title
  `[2601.23172] A unified theory...` is an arXiv paper citation format, almost certainly not a
  Google Doc at all despite living in the `googleDoc` field), and **1 special case**
  (`supply-chain` -- extracted title `theta.md — Supply Chain Explorer | Theta Research` doesn't
  read as a Drive doc title either; a topically-plausible candidate exists ("Cross-Industry
  Supply Chain Signal Analysis") but wasn't confidently the same thing, left unmatched rather
  than guessed). Patched `gdocs/article-exact-matches.md` directly (gitignored, not committed;
  `scripts/exact_match_gdocs.py` itself is unchanged -- this was a manual, connector-dependent
  pass, not a re-runnable script step). New totals: **207 matched**, 8 ambiguous, 3 no match, 2
  fetch failed (of 220).
- **2026-08-30** — User asked to resolve the 8 ambiguous cases too, by checking actual content
  (not just dates). For each: fetched full content of every candidate doc via
  `get_file_metadata` and the published page's opening sentence via `WebFetch`, then compared.
  **All 8 turned out to be the same Gemini query re-run** (2 or 3 times), producing byte-
  identical or near-identical content each time -- genuine content duplicates, not a real
  "which one is correct" ambiguity, except one candidate in the 3-way
  `decoding-analyst-consensus-target-prices-conflicts-epistemology` case, which was a
  *different* document entirely (confirmed by opening-sentence mismatch) and correctly excluded.
  Where content was identical, picked the candidate closest to (and not after) the article's own
  `date` field -- one case (`strategic-portfolio-management-option-writing`) matched the same
  calendar day as publish. Patched all 8 rows from `ambiguous` to `matched`. Final totals:
  **215 matched**, 0 ambiguous, 3 no match, 2 fetch failed (of 220) -- 97.7% resolved.
- **2026-08-30** — User manually confirmed the remaining 3 "no match" articles
  (`covering-world-global-evidence-covered-calls`,
  `unified-theory-market-dynamics-order-flow-impact-volatility`, `supply-chain`) genuinely have
  no corresponding Drive doc. Closing this out at **215/220 matched, 3 confirmed-no-match, 2
  fetch failed** -- no further resolution work pending. The 2 fetch failures were never
  investigated (network/auth issue on those two `googleDoc` URLs specifically, not a "no match"
  question) -- worth a look only if this gets picked up again later.

## Result

- Script: `scripts/exact_match_gdocs.py` (3 match tiers -- exact, case-insensitive,
  suffix-tolerant -- collapsed to a single `matched` label in the report; explicit `ambiguous`
  outcome, never silently guessed)
- Generated Report (gitignored): `gdocs/article-exact-matches.md` — 220 articles evaluated,
  final state after two manual Drive-connector resolution passes: **215 matched**, 0 ambiguous,
  3 genuinely no match, 2 fetch failed (97.7%). Note: 42 of the 215 (34 by search, 8 by content
  comparison) were resolved by hand via the Drive connector (`search_files` /
  `get_file_metadata` / `WebFetch`), not by re-running the script -- `gdocs/index.json` (the
  script's local data source) was intentionally left unmodified, so re-running
  `exact_match_gdocs.py` will NOT reproduce this exact number; it'll fall back to the
  pre-resolution 173 unless the local sync catches up on its own.
- Probe verification: `bash probes/gdocs-exact-title-match.sh` -> `OK 222 rows, 215 matched`
