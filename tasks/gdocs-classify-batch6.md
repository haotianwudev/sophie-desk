---
id: gdocs-classify-batch6
title: Classify+extract batch 6 (final) of remaining matched gdocs (docs 191-215 of 215)
lane: research
status: active
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 190/215 docs classified, 1035 citation candidate rows
probe_status: OK
stall_flag: 
outcome:
artifacts:
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

- **2026-08-31** — Final batch, the last 25 unclassified matched docs.

## Result

<!-- filled by /desk-log on completion -->
