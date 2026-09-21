---
id: spx-chain-local-sync
title: Keep the local SPX chain archive in sync with the live GCS capture
lane: platform
status: queued
assignee: none
gate:
repo: sophie-pipeline
blocker: Open decisions listed in docs/spx-chain-local-sync.md section 5
next: Answer the open decisions, then build spx-option-snapshot/sync_live_chain.py
probe: none
progress:
probe_status:
stall_flag:
outcome:
artifacts:
created: 2026-09-20
updated: 2026-09-20
---

## Goal

The unified SPX chain archive that backtests read is a local copy of the live GCS capture, and nothing keeps it
current. Build an idempotent sync that pulls new sessions, validates each day, publishes atomically, and reports
capture gaps. Design and dated evidence: `sophie-pipeline/docs/spx-chain-local-sync.md`. Local-only, so no gate;
it never writes to the bucket or to Postgres.

## Plan

1. Settle the open decisions in the design doc (back up the local-only history, refresh the price caches, where
   the script lives, whether the viewer gets a "Sync now" button, what to do when a past day changes upstream).
2. Build `spx-option-snapshot/sync_live_chain.py`: checksum manifest instead of `gsutil rsync`, download to temp and
   verify MD5, per-day validation, atomic publish, quarantine on failure, capture-gap report against the trading
   calendar, `_control/sync_status.json`, a distinct message when `gcloud` auth has expired.
3. Schedule it (Windows Task Scheduler, weekdays about 18:00 ET, run as soon as possible after a missed start).
4. Show sync status on the research viewer's `/data` page and home strip.
5. Test against a scratch copy and mutation-check the validation and publish steps (the viewer's removal tests are
   the pattern), before pointing it at the real archive.

## Decision log

- 2026-09-20 — Started from the research viewer's data monitor reporting the archive 6 sessions stale. Question was
  whether that was lost data or an unpulled copy. Read-only check of the bucket: all six sessions were in it, so it
  was a sync gap, recoverable. This distinction drives the design: sync gaps must self-heal, capture gaps (the ETL
  never recorded a session) are permanent and must be detected and reported.
- 2026-09-20 — `gsutil rsync` was rejected as the diff mechanism. A dry run proposed re-copying all 20 files
  including the 14 already pulled, which are byte-identical to the bucket (MD5), because the pulled files carry no
  preserved mtime. Use a manifest of MD5s so "new" and "changed" are exact.
- 2026-09-20 — The bucket has no lifecycle rule but versioning is suspended, so an upstream overwrite would leave no
  trace. That is why a changed past day is kept in `_superseded/` and reported, not just replaced.
- 2026-09-20 — The bucket holds only the live days (from 2026-08-21). The unified archive, the ThetaData backfill and
  its raw files, and the OptionsDX raw files exist only on this workstation, and the free ThetaData tier only
  reaches back about two years. A backup is proposed but not decided.
- 2026-09-20 — Correction to an older claim in the `spx-option-chain-unify` skill: the 12 chain files on closed days
  are not carry-forward copies of the prior day (measured: 1.5-9 percent identical quotes, like any consecutive
  pair). They look like vendor snapshots taken while the market was closed. Skill updated.
- 2026-09-20 — Documented only; nothing was built or changed. Docs and skills updated: the new design doc, pointers in
  `spx-option-snapshot-etl.md` and `cloud-etl-tracking.md`, a Step 6 in `sophie-etl-tracker`, the
  `spx-option-chain-unify` and `option-research-viewer` skills, and the research README.

## Result
