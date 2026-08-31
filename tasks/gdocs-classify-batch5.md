---
id: gdocs-classify-batch5
title: Classify+extract batch 5 of remaining matched gdocs (docs 151-190 of 215)
lane: research
status: active
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 150/215 docs classified, 849 citation candidate rows
probe_status: OK
stall_flag: 
outcome:
artifacts:
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

- **2026-08-31** — Batch 5 of the remaining 65 unclassified matched docs.

## Result

<!-- filled by /desk-log on completion -->
