---
id: option-research-data-monitor
title: Extend the baseline study to the present and add a raw SPX data availability monitor
lane: platform
status: done
assignee: claude
gate:
repo: sophie-option-research
blocker:
next:
probe: none
progress:
probe_status:
stall_flag:
outcome: baseline re-run to the newest chain date as a new study, and a data availability page added to the viewer
artifacts: sophie-option-research commit c41fdd3, study baseline 2016-01-01..2026-09-10, skill option-research-viewer
created: 2026-09-20
updated: 2026-09-20
---

## Goal

Two requests in one session. (1) Update the baseline runs "up to now" — they ended at 2023-12-31 while chain
data runs to 2026. (2) Somewhere to monitor whether the raw SPX option-chain data is available. Follows
`option-research-viewer`.

## Plan

1. Establish what data exists before extending any backtest into it.
2. Re-run notebook 03's five baseline configs to the newest chain date, unified source, as a new study.
3. Verify the extended runs against the earlier ones and against the data seams.
4. Add the monitor to the viewer, with its calendar validated against real trading days.

## Decision log

- 2026-09-20 — Read "some base run" as the `baseline` tag's five configs (unfiltered short put, three
  filtered variants, iron condor) on the 2016 start. The shorter 2022-start baseline set was not extended.
  `data_source` must be `unified` (the only source past 2023-12); the end date is the newest chain directory,
  2026-09-10. New window means a new study in the viewer, so nothing existing was overwritten.
- 2026-09-20 — Checked before running: chains near-daily and healthy through 2026 (50+ expirations a day), price
  features fresh through 2026-09-18 with no gaps, 10 GB free memory. The on-disk SPX/VIX caches are stale
  (last 2026-07-06); the loaders had used the Postgres prices table instead, which is why the run was fine.
- 2026-09-20 — Verification of the run: no failures; one warning (`vix_rank>0.8`, no entries in 2023) confirmed
  real, since 2023's maximum vix_rank was 0.79. The extended run reproduced the earlier unified run trade for
  trade over the overlap (256 of 256: dates, strike, P&L). One trade crosses the 2024-01-02 source seam; it has
  exactly one matching contract each side and its prices equal the chain mids. No baseline trade, old or new,
  entered or exited on a closed-day file.
- 2026-09-20 — Monitor findings worth knowing (the numbers are on the page and go stale, so not copied here):
  the archive is 6 sessions behind; there are historical gaps in the OptionsDX span; and chain files exist on
  some closed days. Tested my first guess that those closed-day files were carry-forward copies of the prior
  session — wrong (quotes differ like any consecutive pair; earliest expiration looks like a closed day). They
  look like vendor snapshots. Whether they are tradable is unknown.
- 2026-09-20 — Calendar: none installed, so NYSE holidays are computed and validated against the cached SPX
  price days (every session agrees over the whole cached span). `check_api.py` adds an oracle check that gaps
  equal (days SPX traded) minus (days with a chain file), independent of the calendar code.
- 2026-09-20 — Two defects found by looking at the rendered page: sessions after the newest file were counted
  both as gaps and as staleness (gap tile overstated by 6), and a linear percent-coverage colour scale would
  have hidden a month with one missing session. Fixed: gaps and freshness are separate; the matrix uses
  explicit states.

## Result

- Code: `sophie-option-research` commit `c41fdd3` — `src/lab/api/availability.py`, `web/app/data/page.tsx`,
  `scripts/update_baseline.py`, checks in `scripts/check_api.py`.
- The new runs are in the local results store (gitignored), tag `baseline`, window `2016-01-01..2026-09-10`.
  Re-running `scripts/update_baseline.py` skips them.
- Live view of the data state: the viewer's `/data` page. Live check: `scripts/check_api.py`.
- Lessons and how to operate it are in the `option-research-viewer` skill.
- Follow-up the same day: the 2022-start baseline set was extended too (`update_baseline.py --start 2022-01-01`,
  window `2022-01-01..2026-09-10`, five runs, none failed). It agrees with the 2016-start runs trade for trade
  from mid-January (mid-March for the iron condor); the only difference is at the start, where the longer run was
  still holding a position carried over from 2021. The 2022-start `vix_rank>0.8` warning (no 2023 entries) is the
  same real one, and `rsi<40 & vix_rank>0.5` has 25 trades, which the viewer flags as anecdotal.
- Not done: the other studies (sweep04, mgmt04, vrp09, wf_oos, optuna04) were not refreshed. They are searches,
  not fixed configs, so "refresh" needs a decision per study; optuna04 in particular would be a new search
  with a different result, not an update. The monitor does not query Postgres (a stale disk cache is shown, but
  the loaders may have used fresher DB prices). Nothing was pushed.
