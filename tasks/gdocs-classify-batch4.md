---
id: gdocs-classify-batch4
title: Classify+extract batch 4 of remaining matched gdocs (docs 111-150 of 215)
lane: research
status: active
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 110/215 docs classified, 777 citation candidate rows
probe_status: OK
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Fourth of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
110 are already classified (`gdocs/classified_state.json`) — 105 remain. This batch does the next 40.

**Read `tasks/done/gdocs-classify-batch3.md` in full first**, specifically the entry about the
`Why`-text fix that landed right after it (commit "Fix Why-text generation: exact WHY_MAP match
or skip, no fuzzy/template fallback"). This changes what you need to do differently from batches
2-3:

- `scripts/extract_gdoc_citations.py`'s `build_why_sentence()` no longer has any fallback. A
  citation only becomes a candidate if its normalized title has an **exact** entry in `WHY_MAP`
  (the big curated dict near the top of the file). Anything without one is now silently skipped
  -- not added with generic text, not added at all.
- **This means you must add a `WHY_MAP` entry for every citation you want to keep**, same as the
  "Batch 2/3 Curated Research Papers" sections already in the file -- append a new
  `"<normalized title>": "<specific, real Why sentence>",` entry for each one, following the
  existing style. There is no other way for a citation to survive the filter now.
- **Do not re-add the fuzzy substring/token-overlap matching or a template fallback** -- that's
  exactly what was just removed, for two confirmed reasons: it assigned one paper's description
  to a different paper (wrong, not just vague), and the template fallback had grown to ~22% of
  all rows by batch 3. Fewer, individually-reviewed candidates are the goal now, not volume.
- Expect **far fewer new rows added this batch** than batches 2-3 (298 and 311 respectively) --
  that's the intended effect of the fix, not a bug in your run. Don't try to compensate by
  writing low-effort `WHY_MAP` entries just to hit a volume target.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs, writes `gdocs/batch_to_classify.json`.
2. Classify each into `gdocs/classified_state.json` (research-paper / news / general-info) --
   same criteria as prior batches.
3. For each research-paper doc's citations: for the ones genuinely worth keeping (the same
   domain-anchored quality bar as before -- real research, not marketing/news/explainers), write
   a real `WHY_MAP` entry in `scripts/extract_gdoc_citations.py` for each, with a specific,
   accurate sentence (read enough of the citation's own context to write something true, not
   generic).
4. `python scripts/extract_gdoc_citations.py` — processes this batch's new research-paper docs
   (auto-skips the 70+ already extracted, tracked in `gdocs/extracted_state.json`), only adds
   rows that now have a real `WHY_MAP` entry, merges/dedupes into `papers/FOLLOWUP-CANDIDATES.md`.
5. Self-check before committing: total citations found, how many now have a `WHY_MAP` entry vs.
   skipped, added/merged counts, 5 example new rows -- put the real numbers in the Decision log.
6. `gdocs/classified_state.json` and `gdocs/extracted_state.json` stay uncommitted (gitignored).
   Commit `scripts/extract_gdoc_citations.py` (your new `WHY_MAP` entries), the updated
   `papers/FOLLOWUP-CANDIDATES.md`, and this task file.

## Decision log

- **2026-08-30** — Batch 4 of the remaining 105 unclassified matched docs, first batch under the
  new exact-match-or-skip Why-text rule.

## Result

<!-- filled by /desk-log on completion -->
