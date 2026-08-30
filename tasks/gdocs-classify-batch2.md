---
id: gdocs-classify-batch2
title: Classify+extract batch 2 of remaining matched gdocs (docs 31-70 of 215)
lane: research
status: queued
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 30/215 docs classified, 171 citation candidate rows
probe_status: OK
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Second of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
30 are already classified (`gdocs/classified_state.json`) and had citations extracted
(`tasks/done/gdocs-citation-candidates-v2.md`) — 185 remain. This batch does the next 40.

**Read both prior tasks first** — `tasks/done/gdocs-research-paper-candidates.md` (reverted:
never add the Gemini doc itself as a candidate) and `tasks/done/gdocs-citation-candidates-v2.md`
(the corrected, verified approach: extract real papers *cited within* research-paper-classified
docs, domain-anchored filter before judgment, no templated `Why` text, dedup within a single
doc's own citation list too). Both scripts referenced below already encode these lessons —
follow their docstrings, don't re-derive the approach from scratch.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs (skips the 30 already done automatically) and writes
   `gdocs/batch_to_classify.json`.
2. Read each entry in that file and classify it **research-paper / news / general-info** —
   same criteria as the first batch (see that task's Goal section for the definitions and
   examples). Write each result into `gdocs/classified_state.json` under its slug, same shape
   as the 30 existing entries: `{"category", "reasoning", "clean_title", "thesis", "tags"}`.
   This script does **not** write classifications for you — you do, by editing the JSON.
3. `python scripts/extract_gdoc_citations.py` — reads **all** research-paper-classified slugs
   in state (old 30's research-paper subset + this batch's new ones), fetches their citations,
   filters (domain-anchored, see that script/task for the allowlist/reject-list), dedupes, and
   merges into `papers/FOLLOWUP-CANDIDATES.md`. It already merges against existing rows rather
   than duplicating (checked — safe to re-run across the growing state file each batch).
4. **Print a self-check before committing** (same as v2 required): total citations found, how
   many passed the domain filter, how many were added/merged, and 5 example new rows — the
   Decision log entry below must include this, with the actual numbers, not a vague claim.
5. `gdocs/classified_state.json` stays **uncommitted** (it's under `gdocs/`, gitignored — confirm
   `.gitignore` still covers it, don't force it in). Commit the updated
   `papers/FOLLOWUP-CANDIDATES.md` and this task file.

## Decision log

- **2026-08-30** — Batch 2 of the remaining 185 unclassified matched docs, following the
  verified v2 citation-extraction approach. Batches of ~40 chosen to keep each one reviewable.

## Result

<!-- filled by /desk-log on completion -->
