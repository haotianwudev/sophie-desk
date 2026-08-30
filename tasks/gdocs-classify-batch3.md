---
id: gdocs-classify-batch3
title: Classify+extract batch 3 of remaining matched gdocs (docs 71-110 of 215)
lane: research
status: queued
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress:
probe_status:
stall_flag:
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Third of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
70 are already classified (`gdocs/classified_state.json`) — 145 remain. This batch does the next 40.

**Read `tasks/done/gdocs-classify-batch2.md` in full first** — it has the most current lessons:
the domain-anchored filter approach (`tasks/done/gdocs-citation-candidates-v2.md`), the
`gdocs/extracted_state.json` tracking fix (so re-running the extractor doesn't re-derive and
silently re-duplicate already-processed docs -- confirm your extraction only touches slugs
newly added to `classified_state.json` this batch, not all 70 existing ones), and the note on
`update_candidates_file()`'s insertion behavior: new rows land in one block right before
`## Passed on`, not integrated into the topic subsections the file now has -- **that's expected
and fine, don't try to fix it** -- the file gets re-grouped by topic in a separate, careful pass
after verification, not by this task.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs, writes `gdocs/batch_to_classify.json`.
2. Classify each into `gdocs/classified_state.json` (research-paper / news / general-info) --
   same criteria as prior batches.
3. `python scripts/extract_gdoc_citations.py` — now skips the 70 already-extracted slugs
   automatically (tracked in `gdocs/extracted_state.json`), only processes this batch's new
   research-paper docs, and merges/dedupes into `papers/FOLLOWUP-CANDIDATES.md` as before.
4. Self-check before committing (same as every batch): total citations found, passed domain
   filter, added/merged counts, 5 example new rows -- put the real numbers in the Decision log.
5. `gdocs/classified_state.json` and `gdocs/extracted_state.json` stay uncommitted (gitignored).
   Commit the updated `papers/FOLLOWUP-CANDIDATES.md` and this task file.

## Decision log

- **2026-08-30** — Batch 3 of the remaining 145 unclassified matched docs.

## Result

<!-- filled by /desk-log on completion -->
