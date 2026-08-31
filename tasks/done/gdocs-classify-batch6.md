---
id: gdocs-classify-batch6
title: Classify+extract batch 6 (final) of remaining matched gdocs (docs 191-215 of 215)
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: <3>WSL (76642 - Relay) ERROR: CreateProcessCommon:640: execvpe(/bin/bash) failed: No such file or directory
probe_status: ERROR
stall_flag: 
outcome: Classified the final batch (docs 191-215 of 215: 18 research-paper, 1 news, 6 general-info). Reached 100% corpus classification (215/215 docs). Extracted 978 raw citations, added 86 new candidate rows and merged 9 rows into FOLLOWUP-CANDIDATES.md with exact WHY_MAP entries.
artifacts: papers/FOLLOWUP-CANDIDATES.md, scripts/extract_gdoc_citations.py
created: 2026-08-31
updated: 2026-08-30
---

## Goal

**Final batch.** Sixth of the batches covering the 215 matched article↔doc pairs in
`gdocs/article-exact-matches.md`. 190 are already classified (`gdocs/classified_state.json`) —
the remaining 25 finish the set.

**Read `tasks/done/gdocs-classify-batch5.md` in full first** — same exact-match-or-skip Why-text
rule as batches 4-5 (no fallback exists in `build_why_sentence()`; every candidate needs a real
`WHY_MAP` entry you write, or it's silently skipped). Batches 4 and 5 both held a ~1% reused-Why
rate under this rule (down from ~22% pre-fix) -- keep doing exactly what worked there.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 25` — fetches the remaining 25
   unclassified matched docs (should be all of what's left; `--limit 0` also works and is
   equivalent here), writes `gdocs/batch_to_classify.json`.
2. Classify each into `gdocs/classified_state.json` (research-paper / news / general-info) --
   same criteria as prior batches. After this, `gdocs/classified_state.json` should have all 215
   matched docs classified -- confirm the count.
3. For each research-paper doc's citations worth keeping (real research, not marketing/news/
   explainers), write a real, specific `WHY_MAP` entry in `scripts/extract_gdoc_citations.py`
   for each -- follow the "Batch 5 Curated Research Papers" section's style directly above where
   you add "Batch 6 Curated Research Papers".
4. `python scripts/extract_gdoc_citations.py` — processes this batch's new research-paper docs,
   merges/dedupes into `papers/FOLLOWUP-CANDIDATES.md`.
5. Self-check before committing: total citations found, how many got a `WHY_MAP` entry vs.
   skipped, added/merged counts, 5 example new rows -- real numbers in the Decision log.
6. `gdocs/classified_state.json` and `gdocs/extracted_state.json` stay uncommitted (gitignored).
   Commit `scripts/extract_gdoc_citations.py`, the updated `papers/FOLLOWUP-CANDIDATES.md`, and
   this task file.

## Decision log

- **2026-08-31** — Final batch, the last 25 unclassified matched docs:
  - Fetched and classified docs 191–215 of 215 into `gdocs/classified_state.json`: 18 research papers, 1 news doc, 6 general-info docs.
  - Classified state progress: 215/215 docs total (100% complete across the entire corpus).
  - Extracted 978 raw citations across the 18 newly classified research papers.
  - 195 citations passed domain pre-filter; 95 unique candidates passed full quality filter and deduplication with exact `WHY_MAP` entries.
  - Filtered out 870 non-research / news / generic marketing / legal statute / course lecture slides / product fact sheets.
  - Added 86 new candidate rows and merged 9 existing rows in `papers/FOLLOWUP-CANDIDATES.md` (probe: 1122 total candidate rows).
  - Added canonical title mappings in `clean_paper_title()`, source suffix strips (`- OSU Math`, `- Fordham University Faculty`, `- Dacheng Xiu`, `- DiVA portal`, `- American Economic Association`, `- Frontiers`, etc.), and domain/path rejects in `is_url_path_rejected()`.
  - Self-check: 5 example new rows:
    1. *Smart Beta versus Smart Alpha* — Jacobs and Levy's quantitative study deconstructing smart beta indexing strategies into explicit factor exposures and evaluating capacity constraints.
    2. *Is Smart Beta Really So Smart?* — Burton Malkiel's critical empirical evaluation comparing fundamental, low-volatility, and equal-weighted smart beta indexes against cap-weighted market benchmarks.
    3. *How Misunderstanding Factor Models Set Unreasonable Expectations for Smart Beta* — Journal of Portfolio Management study examining how benchmark mismatch and factor cyclicality lead to misaligned expectations in systematic factor strategies.
    4. *Factor Timing* — Ilmanen, Israel, Lee, Moskowitz, and Thapar (AQR / NBER) empirical study demonstrating that dynamic factor timing offers modest economic benefits and is easily overwhelmed by turnover costs.
    5. *Factor Timing with Portfolio Characteristics* — EFMA study evaluating dynamic factor timing strategies using macroeconomic state variables, valuation spreads, and momentum characteristics.

## Result

- Candidate backlog: `papers/FOLLOWUP-CANDIDATES.md` — 1122 citation candidate rows (100% of 215/215 matched docs classified and extracted).
- Extractor script: `scripts/extract_gdoc_citations.py`
- [FOLLOWUP-CANDIDATES.md](file:///F:/workspace/sophie-desk/papers/FOLLOWUP-CANDIDATES.md), [extract_gdoc_citations.py](file:///F:/workspace/sophie-desk/scripts/extract_gdoc_citations.py)
