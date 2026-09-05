# Follow-up Paper Candidates

A todo list, not a library — papers surfaced as worth fetching later but not yet gathered. A
future librarian round should check this list first before searching from scratch, and remove
(or move to "Passed on") each entry once it's actually been fetched into a `papers/<area>/`
folder or deliberately rejected. No longer option-writing-only — see Tags below.

**Two ways entries get here:**

1. **Citation-following** (the original path) — the "Notable Citations to Follow Up" section in
   each paper's own `.md` note in `papers/option-writing/`. This file is the *consolidated* view
   across all of them, since 24+ scattered mentions across individual notes isn't actually
   scannable as a todo list. Whoever runs a review/citation-following pass should append new
   candidates here directly, not just leave them buried in a per-paper note. These rows link
   `Surfaced by` to an existing paper note, e.g. `[bondarenko-2014-why-are-puts-expensive]`.
2. **The user's own Gemini Deep Research docs** (added 2026-08-30) — a doc tied to a Sophie
   article via `gdocs/article-exact-matches.md` that turns out to be genuinely research-paper
   grade (structured, evergreen, original synthesis — not a news reaction piece or a 101-level
   explainer) is itself a candidate for a future `papers/<area>/` note. These rows link
   `Surfaced by` to the **Sophie article slug** that cited it, as a live link:
   `[Article Title](https://www.sophie-ai-finance.com/articles/<slug>)` — one click to the
   actual article a human is reading — **and** carry the raw Drive `doc_id` in `Doc ID Source`
   for machine lookup (fetch content, re-verify, etc. via `scripts/match_gdoc.py` /
   `gdocs/index.json`). Both are kept: the slug for a human tracing "which article cited this,"
   the doc_id for anything that needs to programmatically get back to the source doc directly.
   **One underlying research subject can surface from more than one article** (the user
   independently researched the same topic more than once, from different angles, across
   separate Sophie articles) — when that happens it's still one candidate row, not several:
   `Surfaced by` holds every contributing article as a comma-separated list of links, and
   `Doc ID Source` holds every contributing doc_id the same way, in matching order.

**Tags** classify the candidate's subject area — freeform, not a closed enum, extend as needed
(this file now spans everything the user researches, not just `option-writing`/`vrp`; expect
tags like `macro`, `crypto`, `portfolio-theory`, `ai-agents`, `market-microstructure`,
`credit`, `etf`, `behavioral-finance`, etc. alongside the original option-writing-era ones).
Existing pre-2026-08-30 rows have no Tags/Doc ID Source — safe to leave blank, not backfilled.

Whoever picks up a future gathering round should mark this file up as they resolve each entry.

## Candidates, by topic

Split into per-topic pages once the combined table passed ~1000 rows. Each page repeats the same schema (see above) in its own table.

- [Volatility Risk Premium & Option Writing](candidates/vrp-option-writing.md) — 229
- [Market Microstructure & Trading Mechanics](candidates/market-microstructure.md) — 142
- [AI Agents & Quant Infrastructure](candidates/ai-agents-infrastructure.md) — 59
- [Machine Learning & Deep Learning in Finance](candidates/ml-deep-learning.md) — 258
- [Portfolio Construction & Asset Allocation](candidates/portfolio-construction-allocation.md) — 192
- [Risk Management & Conformal Prediction](candidates/risk-management-conformal-prediction.md) — 61
- [Fixed Income & Macro](candidates/fixed-income-macro.md) — 29
- [Credit & Counterparty Risk](candidates/credit-counterparty-risk.md) — 32
- [Mathematical Finance & Stochastic Methods](candidates/mathematical-finance.md) — 48
- [Other / Uncategorized](candidates/other-uncategorized.md) — 134

## Querying across topics locally

Splitting into 10 per-topic pages (1184 rows total as of 2026-09-04) fixed the Dataview
scaling problem but made cross-topic queries ("all High-tags across every topic", full-text
search over `why`) awkward again. `sophie-pipeline/paper-index/build_index.py` rebuilds a local
SQLite copy of this backlog (plus `papers/option-writing/*.md` frontmatter) from these markdown
files into `papers/paper-index/papers.db` — a vault-relative path on purpose, so an Obsidian
SQLite plugin (SQLite Explorer, e.g.) can browse/query it directly, not just Python. Query
`candidates`/`candidates_fts` and `papers`/`papers_fts` with SQL; see
`sophie-pipeline/paper-index/README.md` for the schema and plugin setup. Markdown here stays
the source of truth; the DB is disposable and gitignored, rebuild it whenever these files change.

## Passed on

Candidates deliberately not pursued, with the reason — keeps them from being re-suggested by
a later pass that doesn't know they were already considered.

| Title | Why passed |
|---|---|