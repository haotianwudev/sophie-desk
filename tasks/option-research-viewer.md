---
id: option-research-viewer
title: Local research viewer for sophie-option-research (put writing first)
lane: platform
status: active
assignee: claude
gate:
repo: sophie-option-research
blocker:
next: Phase 0 metric backfill, then the FastAPI read model
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

The 107 backtest runs in `sophie-option-research`'s local results store are only reachable by
opening a notebook and writing pandas. Build a local-only viewer that makes the research
browsable as strategy to study to parameter space to single run, starting with put writing
(`short_puts`, 104 of the 107 runs).

Done looks like two processes on the loopback interface — a FastAPI JSON service on 8010 over
`results/runs.parquet` plus `results/trades/`, and a standalone Next.js UI on 3010 — where you
can pick a study, see which parameter combinations were actually run and how each scored, click
one, and read its equity curve, trade log and the study memo with its auto-generated caveats
intact.

Read-only. Notebooks stay the only writer of the results store. Nothing here publishes to
Postgres, and nothing launches backtests from the browser — both would need their own gate.

## Plan

1. Phase 0 — `scripts/backfill_metrics.py`. 13 extended metrics, including
   `probabilistic_sharpe`, are NaN on the July 2026 runs and populated on the September ones.
   Recompute them from the stored trade logs (no chain data, no engine). Hard stop — the script
   must first reproduce a known-good September row's values exactly, or it does not write.
2. `src/lab/api/` — `readmodel.py` (parquet adapter, mtime-cached, parses `params_json` to flat
   dotted keys, classifies each study as grid or scatter from param cardinality), `schemas.py`,
   `app.py`, `memo.py`.
3. `scripts/serve_api.py` — uvicorn bound to 127.0.0.1, following
   `sophie-pipeline/sophie_agent/serve.py` as the local-only precedent.
4. `web/` — standalone Next.js app, mirroring the Sophie client's stack so components can
   graduate later. Routes for the strategy list, study list, param view, run detail, study memo.
5. Verify per the plan file — route contract checks, a cross-check of API numbers against
   `load_runs()` directly, the grid-vs-scatter classification, negative paths, and proof the
   store is untouched by a browsing session.

Full design, including the store quirks the API has to absorb, is in the plan file named in the
decision log below.

## Decision log

- 2026-09-20 — Designed after exploring the repo. Four decisions worth recording. (a) A study is
  a (tag, window) pair, not just a tag, because tags mix windows — `optuna04` holds 36 runs on
  2016-2023 and 4 on 2022-06-2023-12, and one grid spanning both would compare Sharpe across
  different market periods. (b) `optuna04`'s 40 trials are continuous in delta and take_profit,
  so they are a scatter, not a lattice; the API reports the shape and the UI renders accordingly
  rather than binning them onto a fake grid. (c) Local parquet only — the DB has just 6 of 107
  runs published, so reading it would hide most of the research. (d) Read-only server, ungated,
  consistent with how `spx-option-backfill` treats local-only work.
- 2026-09-20 — Plan file: `C:\Users\lswht\.claude\plans\design-a-option-research-replicated-chipmunk.md`

## Result
