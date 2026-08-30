---
id: gdocs-research-paper-candidates
title: Classify matched Drive docs as research-paper/news/general-info; candidate the papers
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-research-paper-candidates.sh
progress: scripts/classify_gdocs_candidates.py missing
probe_status: RUN
stall_flag: 
outcome: 30-doc trial batch classified (19 research-paper, 6 news, 5 general-info); 19 candidates added to backlog
artifacts: scripts/classify_gdocs_candidates.py, papers/FOLLOWUP-CANDIDATES.md
created: 2026-08-30
updated: 2026-08-30
---

## Goal

`gdocs/article-exact-matches.md` has 215 confirmed article ↔ Drive-doc pairs (Match Tier =
`matched`). Read each matched doc's actual content and classify it as one of:

- **research-paper** — a structured, evergreen, original analytical synthesis: multi-section
  (`## Section 1`, `## Part I`, etc.), states a thesis/methodology, not centered on one dated
  event. Examples already confirmed in this repo's own research: "Decomposing the Volatility
  Risk Premium," "A Comprehensive Institutional Study of the S&P 500 Index (SPX) as an
  Option-Writing Underlyer," "The Epistemology of Value" (sell-side research analysis).
- **news** — centered on one specific, dated market event: an earnings reaction, a single
  company's quarterly 13F filing, a specific day's market move. Examples: "The 2025 Financial
  Market Retrospective," "Appaloosa Management Q2 2026 13F Institutional Analysis," "NVIDIA
  Deep Dive: Why the Crush Despite the Beat."
- **general-info** — a basic educational explainer/101 overview with no original synthesis or
  real thesis. Examples: "Understanding the VIX Index," "Mutual Funds vs. ETFs: Which is
  Better?," "Bitcoin: How It Works and Investing."

**This is a judgment call, not a keyword match.** Read enough of each doc (opening section +
headers) to actually decide — comprehensive length alone does not make something a
research-paper; it needs a real synthesized thesis or methodology. When genuinely unsure
between research-paper and general-info, prefer general-info (don't inflate the candidate list
with borderline explainers).

For docs classified **research-paper only**, add a row to `papers/FOLLOWUP-CANDIDATES.md`'s
Candidates table — read that file first, the schema and both source pathways are documented at
its top (Tags / Surfaced-by-as-article-link / Doc ID Source were added today specifically for
this kind of entry). Do **not** touch `papers/option-writing/*.md` or create anything under
`papers/<area>/` — this task only populates the candidate backlog, not the actual paper library.

## Plan

1. Write `scripts/classify_gdocs_candidates.py`:
   - Parse `gdocs/article-exact-matches.md` for all `matched` rows: slug, doc_id.
   - Cross-reference each slug against `ai-stock-suggestion-client/src/data/articles/*.ts` to
     get the article's `title` and `googleDoc` published URL (reuse the parsing approach from
     `scripts/exact_match_gdocs.py`).
   - For each, fetch the published page's full body content the same way
     `scripts/exact_match_gdocs.py` fetches `<title>` (plain `urllib`, no new dependency) --
     but this time extract enough body text to (a) classify it and (b) pull the doc's real H1
     heading (the first `# ...` line) as a better candidate title than the article's own
     (often-rewritten) title.
   - **Process in a resumable, checkpointed way**: track which slugs have already been
     processed (e.g. a small local state file, or just re-derive "already handled" by checking
     which slugs already have a `Doc ID Source` in `papers/FOLLOWUP-CANDIDATES.md`) so a
     partial run doesn't redo work or lose progress if it's interrupted.
   - **Start with a batch of 30** (`--limit 30` or similar), not all 215 at once -- this is a
     trial run to validate the classification quality and output formatting before committing
     to the full set. Report back clearly how many of the 30 were research-paper / news /
     general-info, and how long it took, so a future run can decide whether to do the rest.
2. For each `research-paper` classification, append one row to `papers/FOLLOWUP-CANDIDATES.md`:
   - `Title`: the doc's own H1 heading (fall back to the `Extracted Page Title` already in
     `gdocs/article-exact-matches.md` if no clean H1 is found).
   - `Authors / Year`: `Gemini Deep Research (<year>)` using the article's own `date` field.
   - `Why it looks worth getting`: one sentence, the paper's actual core thesis/finding --
     specific, not generic ("comprehensive analysis of X" is not specific enough).
   - `Tags`: comma-separated, freeform (see the file's own Tags guidance at the top).
   - `Surfaced by`: `[<article title>](https://www.sophie-ai-finance.com/articles/<slug>)`.
   - `Doc ID Source`: the doc_id.
   - `Status`: leave blank.
3. **Dedup pass, at the end, on the newly-added rows only** (don't touch the 71 pre-existing
   citation-following rows). **The point of this pass**: the same underlying research subject
   can legitimately surface from more than one article -- the user researched the same topic
   independently, more than once, from different angles, in separate Gemini sessions tied to
   separate Sophie articles (already confirmed happening broadly across this corpus -- see
   `gdocs/duplicates.md` and the exact-title-match resolution work earlier today). That's still
   **one candidate**, not several. When two or more newly-added rows are about the same
   underlying research subject (start with normalized-title grouping like
   `scripts/find_gdoc_duplicates.py` -- strip a trailing `(N)`, collapse whitespace, lowercase --
   but also read the `Why it looks worth getting` summaries for cases where the titles differ
   but the subject is clearly the same, e.g. three separate "Monte Carlo Simulation" write-ups),
   **merge them into a single row** rather than dropping all but one:
   - `Surfaced by`: every contributing article, comma-separated, each still its own link.
   - `Doc ID Source`: every contributing doc_id, comma-separated, in the same order as the
     articles above (so position N in one list corresponds to position N in the other).
   - `Why it looks worth getting`: write one sentence that covers the shared subject, not just
     the first row's original text.
   Only leave two rows separate when they're genuinely different research subjects that happen
   to share a broad topic area (e.g. "Monte Carlo for derivative pricing" vs. "Monte Carlo for
   backtesting robustness" are different enough subjects to stay separate; three near-identical
   "Monte Carlo Simulation in Quant Finance" overviews are not).
4. Commit `scripts/classify_gdocs_candidates.py` and the updated
   `papers/FOLLOWUP-CANDIDATES.md` (this file is real and public, not gitignored -- unlike
   `gdocs/*.md`, review the diff before committing).

## Decision log

- **2026-08-30** — Scoped to a 30-doc trial batch first, not the full 215, per the user's "try
  some with agy, see if agy can finish this work" -- this task is heavier per-item than the
  prior title-matching pass (real reading + judgment per doc, not string comparison), so
  validate quality/throughput before committing to the rest in a follow-up task.
- **2026-08-30** — Evaluated first batch of 30 matched docs from gdocs/article-exact-matches.md. Extracted title tag, H1, heading outline, and body text preview. Classified 19 as research-paper, 6 as news, and 5 as general-info. Added 19 new candidate rows with concise core thesis, tags, live article links, and doc_id source to papers/FOLLOWUP-CANDIDATES.md. Dedup pass confirmed all 19 entries represent distinct research subjects.

## Result

Completed 30-doc trial classification via `scripts/classify_gdocs_candidates.py`. 19 research-paper candidates appended to `papers/FOLLOWUP-CANDIDATES.md` with full schema populated (Tags, Surfaced by link, Doc ID Source).

