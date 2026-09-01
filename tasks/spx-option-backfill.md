---
id: spx-option-backfill
title: ThetaData backfill of the 2024-01 → 2026-08 SPX chain gap
lane: platform
status: blocked
assignee: none
gate: g3
repo: sophie-pipeline
blocker: Vendor/scope decision — accept a monthly-cycle corpus, or pay for a faster tier
next: Decide scope. 45-DTE studies never touch the near-daily tail that is stalling.
probe: bash probes/spx-option-backfill.sh
progress: <3>WSL (84090 - Relay) ERROR: CreateProcessCommon:640: execvpe(/bin/bash) failed: No such file or directory
probe_status: ERROR
outcome:
artifacts:
created: 2026-08-23
updated: 2026-08-31
---

## Goal

Fill the ~660 NYSE sessions between the OptionsDX corpus (ends 2023-12) and the live
`spx_option_snapshot` ETL seed (2026-08-21), as a local Parquet archive on F:. Local-only:
**`dry_run=True` is a standing instruction** and writing to the live Neon table is a separate
decision, not a continuation of this task. That is why this carries `gate: g3`.

Full incident history, root-cause analysis and the ThetaData gotchas remain in the
`spx-option-backfill` skill for now. Trim that file to the reusable parts once this task closes.

## Status — the honest read

Downloading since 2026-08-26 under the self-healing wrapper (`data/autorun_download.sh`).
SPX is complete. SPXW is the long tail.

**It is running, not stalled — and that is the worse answer.** Reading the log tail alone
suggests a dead job: nothing but `503`s and 1800s read-timeouts on 2025 near-daily expirations.
The probe says otherwise — the file count moved 441 → 442 during a single conversation and the
log was written 2h ago. So the wrapper is healthy and grinding. At roughly one file per hour
against 918 remaining jobs, that is **on the order of five to six weeks** to completion.

This is precisely why probes exist. "Stalled" would have prompted a restart that fixes nothing;
the real problem is a rate that no amount of patience improves.

**This is not a new bug.** It is the known recurring pattern, and the known fix (write a
header-only placeholder) must not be applied ahead of an actual per-job failure, and never to
monthly-cycle expirations — several of those hold real multi-MB 2024 data.

## The decision this is blocked on

The remaining SPXW tail is near-daily and 0DTE expirations. **The 45-DTE strategies this
research actually runs never select those contracts.** So:

- **Option A — declare the monthly/weekly corpus sufficient.** Stop the download, process what
  exists, and record the coverage limitation honestly in the archive. Unblocks immediately.
- **Option B — pay for a faster ThetaData tier.** More than one concurrent request removes the
  wedge dynamic that causes most of these stalls. Costs money, finishes the tail.
- **Option C — keep waiting.** Costs weeks and buys contracts no current study reads.

Option C is the current default by inaction, which is the actual problem.

## Not a blocker on research

Worth restating because it shaped the whole plan: the OptionsDX corpus (2010–2023, ~31M rows)
is complete, and all 102 existing backtest runs were built on it. This gap buys a 2024–2026
**out-of-sample window** — a validation input, not a prerequisite. Research proceeds regardless.

## Decision log

- **2026-08-23** — Confirmed free-tier wildcard behaviour: omitting `strike` and `right` returns
  a whole chain per `(symbol, expiration)`. Collapsed the request budget to ~1 per expiration.
- **2026-08-23** — Root cause of the instability found: a 60s client timeout on requests the
  server takes up to 1400s to serve, which wedges the single free-tier concurrent slot. Raised
  to 1800s.
- **2026-08-25** — HTTP 472 is ThetaData's documented `NO_DATA`, not an error. Was being counted
  as a failure and re-queried forever. Now cached as a header-only placeholder.
- **2026-08-27** — Same stuck-chunk pattern recurring across SPXW near-dailies. Reactive
  placeholder fix only; monthlies explicitly excluded.
- **2026-08-29** — Reviewed for the desk migration. Reclassified from "in progress" to
  **blocked on a scope decision**. Confirmed research does not depend on it.

## Result

<!-- filled by /desk-log on completion -->
