---
id: gdocs-classify-batch5
title: Classify+extract batch 5 of remaining matched gdocs (docs 151-190 of 215)
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 150/215 docs classified, 849 citation candidate rows
probe_status: OK
stall_flag: 
outcome: Classified docs 151-190 of 215 (24 research-paper, 5 news, 11 general-info). Extracted 1197 raw citations, added 187 new candidate rows and merged 21 rows into FOLLOWUP-CANDIDATES.md with exact WHY_MAP entries.
artifacts: papers/FOLLOWUP-CANDIDATES.md, scripts/extract_gdoc_citations.py
created: 2026-08-31
updated: 2026-08-30
---

## Goal

Fifth of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
150 are already classified (`gdocs/classified_state.json`) — 65 remain. This batch does the next 40
(leaving ~25 for a final batch 6).

**Read `tasks/done/gdocs-classify-batch4.md` in full first** — same exact-match-or-skip Why-text
rule as that batch (no fallback exists anymore in `build_why_sentence()`; every candidate needs
a real `WHY_MAP` entry you write, or it's silently skipped). That batch needed zero cleanup after
verification -- keep doing exactly what worked there, don't reintroduce fuzzy matching or
templated text.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs, writes `gdocs/batch_to_classify.json`.
2. Classify each into `gdocs/classified_state.json` (research-paper / news / general-info) --
   same criteria as prior batches.
3. For each research-paper doc's citations worth keeping (real research, not marketing/news/
   explainers), write a real, specific `WHY_MAP` entry in `scripts/extract_gdoc_citations.py`
   for each -- follow the "Batch 4 Curated Research Papers" section's style directly above where
   you add "Batch 5 Curated Research Papers".
4. `python scripts/extract_gdoc_citations.py` — processes this batch's new research-paper docs
   (auto-skips already-extracted slugs via `gdocs/extracted_state.json`), merges/dedupes into
   `papers/FOLLOWUP-CANDIDATES.md`.
5. Self-check before committing: total citations found, how many got a `WHY_MAP` entry vs.
   skipped, added/merged counts, 5 example new rows -- real numbers in the Decision log.
6. `gdocs/classified_state.json` and `gdocs/extracted_state.json` stay uncommitted (gitignored).
   Commit `scripts/extract_gdoc_citations.py`, the updated `papers/FOLLOWUP-CANDIDATES.md`, and
   this task file.

## Decision log

- **2026-08-31** — Batch 5 of remaining matched docs:
  - Fetched and classified docs 151–190 of 215 into `gdocs/classified_state.json`: 24 research papers, 5 news docs, 11 general-info docs.
  - Classified state progress: 190/215 docs total (25 remaining for Batch 6).
  - Extracted 1197 raw citations across the 24 newly classified research papers.
  - 314 citations passed domain pre-filter; 208 unique candidates passed full quality filter and deduplication with exact `WHY_MAP` entries.
  - Filtered out 968 non-research / news / generic marketing / legal statute / course notes entries.
  - Added 187 new candidate rows and merged 21 existing rows in `papers/FOLLOWUP-CANDIDATES.md` (probe: 1036 total candidate rows).
  - Added canonical title mappings in `clean_paper_title()`, source suffix strips (`- PMC`, `- PhilArchive`, `- UNSW`, `- DiVA`, etc.), and domain/path rejects.
- **2026-08-31** — Independently verified. Why-text fix continues to hold: reused-Why rows rose
  only 169 -> 171 out of 187 new (~1%), vs. the pre-fix ~22% rate. No junk titles. One valuable
  merge found: "A Machine Learning Approach to Regime Modeling" existed as a pre-fix row (old
  templated Why, from batch 2/3) and got independently re-discovered here with a genuinely
  specific description -- merged into one row using the good text and both source articles,
  fixing one of the old generic rows for free. Regrouped and diffed against the last commit
  before and after -- only the intentional merge changed anything.

## Result

- Candidate backlog: `papers/FOLLOWUP-CANDIDATES.md` — **1099 real candidate rows** (1035
  gdocs-sourced + 64 pure-citation-following), organized into topic sections.
- Extractor script: `scripts/extract_gdoc_citations.py`
- [FOLLOWUP-CANDIDATES.md](file:///F:/workspace/sophie-desk/papers/FOLLOWUP-CANDIDATES.md), [extract_gdoc_citations.py](file:///F:/workspace/sophie-desk/scripts/extract_gdoc_citations.py)

