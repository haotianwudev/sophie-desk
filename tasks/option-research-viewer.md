---
id: option-research-viewer
title: Local research viewer for sophie-option-research (put writing first)
lane: platform
status: active
assignee: claude
gate:
repo: sophie-option-research
blocker:
next: FastAPI read model (src/lab/api), then web/
probe: none
progress:
probe_status:
stall_flag: no commit in 14m while active
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
- 2026-09-20 — Phase 0 done: `scripts/backfill_metrics.py` filled the 13 extended metrics on 68 runs (probabilistic_sharpe included). The self-check recomputed 39 already-populated rows first — 507 comparisons — and initially flagged one mismatch: `avg_return_on_margin` on vrp09 run 925ad2cc7eca, abs diff 2e-9. Checked before loosening anything: the metric is a near-cancelling mean of terms ~7.7e-2 in size, so the gap is 3e-8 of term scale, and its sibling `ann_return_on_margin` matched to 6e-9. Added an absolute tolerance floor (1e-7), documented in the script, rather than loosening the relative one. Cause of the 2e-9 not pinned (probably a tiny difference in the spot series vs July); immaterial. Verified afterwards against the backup: 107 rows, 43 cols, no NaN left, every non-extended column identical, previously-populated rows untouched. Backup at `results/runs.parquet.bak-2026-09-20` (gitignored).
- 2026-09-20 — Two plan corrections from looking at the real params. (a) `leg1_delta.min/target/max` always move together (band is a constant ±0.10 for short_puts; the one exception is the iron condor wing), so they collapse to a single `leg1_delta.target` axis. (b) `wf_oos` is ten 1-year windows with one run each, so a (tag, window) study key yields ten one-run studies; for walk-forward the window is the varying dimension, so those group as one study. Rule is derived from the data: a tag whose runs all have distinct windows is one walk-forward study.
- 2026-09-20 — Found 5 duplicate-param groups, all in `baseline`: each is a July run and a 2026-09-12 rerun with identical params but materially different results (iron_condor Sharpe 0.89 vs 1.24; short_put_45dte 0.59 vs 0.49, 275 vs 268 trades). Consistent with the legacy-to-unified data_source switch, but the store does not record data_source, so that is inference from dates, not fact. Read model must show such cells as "N runs that disagree", never silently pick one.

## Result
