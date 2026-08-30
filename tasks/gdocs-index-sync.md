---
id: gdocs-index-sync
title: Local index + title-matcher for D:\GoogleDrive research docs
lane: platform
status: active
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-index-sync.sh
progress: scripts/sync_gdocs_index.py or scripts/match_gdoc.py missing
probe_status: RUN
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

The user has ~335 Gemini Deep Research sessions saved as native Google Docs, synced locally
via Google Drive desktop into `D:\GoogleDrive` as `.gdoc` stub files (e.g. `AQR Research Paper
Summary and List.gdoc`). A `.gdoc` file is **not** the document content — it's a 172-byte JSON
pointer: `{"doc_id": "...", "resource_key": "...", "email": "..."}`. The filename (minus
extension) is the doc's title.

Goal of this task: build a local, greppable index of these titles + IDs, and a matcher that
can rank Drive docs against a query title (e.g. a paper's title from
`papers/option-writing/*.md` frontmatter). This task does **not** fetch actual document
content — that needs the Google Drive API/connector, which is a separate follow-up
(`tasks/gdocs-content-link.md`, assignee `claude`, queued behind this one). Do not touch
anything under `papers/` in this task — index-building only.

**Do not create `D:\GoogleDrive\.gitignore` or any files inside `D:\GoogleDrive`.** That
directory is Google Drive's live sync folder, entirely outside this repo — read-only for this
task. All output goes into this repo under `gdocs/` (already gitignored — see `.gitignore`,
these are personal doc titles and this repo is public).

## Plan

1. **`scripts/sync_gdocs_index.py`** — scan `D:\GoogleDrive` recursively for `*.gdoc` files.
   - Skip the `.tmp.drivedownload` directory and any directory whose name contains `personal`
     case-insensitively (e.g. `Important-Personal-DataStore`, `Important-Personal-Picture`) —
     those are not research material.
   - Parse each stub's JSON body for `doc_id` and `resource_key` (some may have an empty
     `resource_key` — that's normal, keep it as `""`).
   - Title = filename with the `.gdoc` extension stripped.
   - Also capture the file's mtime and its path relative to `D:\GoogleDrive`.
   - Write `gdocs/index.json`: a JSON array of objects
     `{"title": ..., "doc_id": ..., "resource_key": ..., "relpath": ..., "mtime": ...}`,
     sorted by title. Overwrite on every run (idempotent, not incremental).
   - When run directly (`python scripts/sync_gdocs_index.py`), print one summary line:
     `indexed N docs, skipped M (personal/tmp)`.
   - Only `.gdoc` files for now — leave `.gsheet`/`.gslides` out of scope, note it in a comment
     if you want to flag it for later, don't build it speculatively.

2. **`scripts/match_gdoc.py "<query title>"`** — load `gdocs/index.json`, score every entry's
   `title` against the query (Python's `difflib.SequenceMatcher(None, a, b).ratio()` is fine —
   deterministic, no network, no extra dependency), and print the top 5 matches, one per line,
   most similar first:
   ```
   0.62  1nOxFL4_KTDSGFKSrKAYuCL7E3-AE0srxt8NeKbffnNc  AQR Research Paper Summary and List
   ```
   Exit non-zero with a clear message if `gdocs/index.json` doesn't exist yet (tell the caller
   to run the sync script first) — this is the one place in this task where failing loudly is
   correct, since it's a CLI misuse, not a probe.

3. Run both once against the real `D:\GoogleDrive` to confirm they work end-to-end (the probe
   checks this too, but confirm yourself before calling it done — sanity-check a couple of the
   printed matches make sense, e.g. querying `"AQR"` should surface the AQR doc near the top).

4. Commit `scripts/sync_gdocs_index.py`, `scripts/match_gdoc.py`, and this task's frontmatter
   update. **Do not commit `gdocs/index.json`** — it's gitignored on purpose (personal content
   in a public repo); if `git status` shows it as untracked-but-not-ignored, stop and check
   `.gitignore` rather than committing it anyway.

## Decision log

- **2026-08-30** — Scoped tightly to index+match only; content-fetch needs the Google Drive
  MCP connector, which only a Claude Code session with that connector attached actually has —
  agy has no proven access to it, so that half is a separate `claude`-assigned task instead of
  being bundled in here.

## Result

<!-- filled by /desk-log on completion -->
