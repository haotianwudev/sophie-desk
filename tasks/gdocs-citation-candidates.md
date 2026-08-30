---
id: gdocs-citation-candidates
title: Extract cited research papers from research-paper-grade Gemini docs
lane: research
status: active
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-citation-candidates.sh
progress: scripts/extract_gdoc_citations.py missing
probe_status: RUN
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

**Correcting a mistake from `tasks/done/gdocs-research-paper-candidates.md`**: that task added the
user's own Gemini Deep Research docs *themselves* as `papers/FOLLOWUP-CANDIDATES.md` entries.
That was wrong and has been reverted (see that file's git history, commit "Revert the 19
gdocs-classify candidate rows"). A Gemini doc is our own AI-written synthesis, not a research
paper — it doesn't belong in a *research paper* backlog on its own.

**What actually belongs there**: the real academic/institutional papers **cited within** those
Gemini docs. Every research-paper-grade Gemini doc we've read so far ends with a numbered
"Works cited" / "References" section — e.g. the "Decomposing Volatility Risk Premium" doc's own
citation #6 is literally "Downside Variance Risk Premium, accessed November 22, 2025,
https://econ.au.dk/..." — a real working paper, hyperlinked. This is the **same mechanism**
already used for `papers/option-writing/`'s "Notable Citations to Follow Up" → this file, just
a second source corpus (the user's own docs) instead of our own paper notes.

This task extracts those citations from the 19 docs already classified `research-paper` in
`gdocs/classified_state.json` (from the prior task's trial batch) — a smaller, well-scoped pilot
for the citation-extraction step specifically, before scaling to the other ~185 matched docs
(most of which haven't been classified yet at all — that's separate follow-up work, not this
task).

## Plan

1. Write `scripts/extract_gdoc_citations.py`. For each of the 19 slugs in
   `gdocs/classified_state.json` with `"category": "research-paper"`:
   - Fetch the **full** published page (not just a preview — the citations are a numbered list
     at the very end of the doc, so truncating early loses them). Reuse the fetch approach from
     `scripts/exact_match_gdocs.py` / `scripts/classify_gdocs_candidates.py`.
   - Find the citations section (commonly headed "Works cited", but also seen as "References" —
     match case-insensitively, and don't assume there's exactly one heading style). It's a
     numbered list; each item is typically `<title>, <source/publication>, accessed <date>,
     <url>` with the URL as a real hyperlink in the HTML (parse `<a href="...">` near each list
     item rather than regexing a bare URL out of plain text — more reliable).
   - Extract `(title, url)` per citation. The "title" is the text before the first comma (or
     before "accessed" if that comes first) — don't over-engineer parsing every citation style
     perfectly; skip (don't guess) any item you can't cleanly split into a title.
2. **Filter for research quality before adding anything** — most Gemini citation lists mix real
   research with generic web sources (news sites, Reddit, Medium, Investopedia, YouTube,
   Wikipedia). Only keep a citation if it reads as genuine research/institutional analysis:
   an academic paper, a working paper (SSRN, NBER, a central bank site, a university .edu
   domain), or a substantive research-house publication (e.g. a named research paper from a
   fund/bank's research arm, an exchange's own research paper like a Cboe or CME white paper).
   Skip news articles, generic explainer/educational content, forum posts, and video content
   even if a citation technically points there — this filter matters more than parsing
   perfectly; a shorter, higher-quality list beats a long noisy one.
3. For each citation that passes the filter, append a row to `papers/FOLLOWUP-CANDIDATES.md`'s
   Candidates table, matching the existing schema exactly (read the file's own header first —
   it documents both source pathways and the multi-source-row convention):
   - `Title`: the citation's stated title.
   - `Authors / Year`: usually not available in this citation format — leave blank rather than
     guess (unlike the original 71 rows, which do have real author/year because that's how
     those were originally surfaced).
   - `Why it looks worth getting`: one sentence — what it's about / why the citing doc used it,
     inferred from the citation's own title and surrounding context if visible, not invented.
   - `Tags`: freeform, per the file's existing guidance.
   - `Surfaced by`: `[<article title>](https://www.sophie-ai-finance.com/articles/<slug>)` —
     the Sophie article whose underlying Gemini doc cited this paper (**not** a link to the
     Gemini doc itself).
   - `Doc ID Source`: the Gemini doc_id it was found in.
   - `Status`: leave blank.
4. **Dedup pass, at the end.** This is the real duplicate case (unlike the reverted task): the
   *same* real paper can be cited by multiple different Gemini docs across different Sophie
   articles — e.wg. a foundational VRP or option-pricing paper is likely to turn up in several
   of these reports independently. Group by normalized title (strip trivial punctuation
   differences, collapse whitespace, lowercase) and merge true matches into **one row** with
   every contributing article/doc_id appended comma-separated to `Surfaced by` / `Doc ID
   Source` respectively (matching order) — don't drop the extra sources.
5. Commit `scripts/extract_gdoc_citations.py` and the updated `papers/FOLLOWUP-CANDIDATES.md`
   (real, public, git-tracked — review the diff before committing, same as always).

## Decision log

- **2026-08-30** — Created to correct `gdocs-research-paper-candidates`, which added the user's
  own Gemini docs as candidates instead of the papers cited within them. Scoped to the 19
  already-classified research-paper docs as a pilot for the citation-extraction step
  specifically; the remaining ~185 unclassified matched docs are separate follow-up work.

## Result

<!-- filled by /desk-log on completion -->
