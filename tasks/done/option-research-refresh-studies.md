---
id: option-research-refresh-studies
title: Refresh the stored research studies to the newest chain date
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
outcome: sweep04, mgmt04, optuna04, vrp09 replayed on the extended window and wf_oos extended by two years, all as new studies
artifacts: sophie-option-research scripts/update_studies.py, tags sweep04 mgmt04 optuna04 vrp09 wf_oos, skill option-research-viewer
created: 2026-09-20
updated: 2026-09-20
---

## Goal

"Rerun as much as possible": bring every study in the results store up to the newest chain date. Follows
`option-research-data-monitor`, which did the two baseline sets.

## Plan

1. Find out how each stored study was actually made.
2. Replay the stored configs on the extended window, unified source, as new studies (nothing overwritten).
3. Extend the walk-forward study by full out-of-sample years only.
4. Cross-check, then look at the results critically.

## Decision log

- 2026-09-20 — The notebooks and the store disagree: the stored sweep04 has only delta 0.16 and 0.30, mgmt04 and
  vrp09 use shorter windows, and wf_oos starts in 2014. A notebook re-run would have been a different study, so
  the script replays each stored run's own name, params, entry filter and start, changing only the end date and the
  data source. sim is set to the default every stored run was proven to use, so the new runs' provenance derives.
- 2026-09-20 — optuna04 was the one I had wanted to skip, on the grounds that a fresh search finds a different
  optimum. Re-evaluating the same 40 trial parameter sets on the longer window is a real update, so it is included.
  It is explicitly not a new search.
- 2026-09-20 — wf_oos: `first_year=2020, last_year=2025` yields exactly two windows (tests 2024 and 2025), verified
  in the loop condition before running. 2026 is a partial year and is left out. The study keeps distinct windows,
  so the viewer still classifies it as walk-forward.
- 2026-09-20 — Ran 82 replayed configs plus the walk-forward years: none failed, no truncation warnings. Independent
  cross-check: the replayed sweep04 cell that equals the baseline short put reproduced the baseline run's trades
  exactly (353 of 353), two scripts arriving at the same result.
- 2026-09-20 — Reading the results critically. (a) The highest Sharpes are all no-stop-loss variants, which carry the
  tail: worst trade up to about 8.7 times the average credit, and a single loss of about a third of capital at 0.30
  delta. (b) optuna04: re-evaluating the same 36 trials, rank correlation of Sharpe between old and new windows is
  0.88, but that is confounded by the data-source change as much as the extra years; the old best trial is now rank 3
  and the new best was old rank 14. (c) Walk-forward: the 2025 test year had an out-of-sample Sharpe of 0.49 against an
  in-sample 1.28, with a 35 percent drawdown; the 2024 year was 0.95. The study now mixes legacy years (2014-2023)
  and unified years (2024-2025).
- 2026-09-20 — Time estimate was wrong: one run took 2.7 s on a short window but full-length runs are ~20 s of
  compute, so the first group took far longer than projected. It was alive (CPU and memory checked), just quiet,
  because results print per group.
- 2026-09-20 — Found while looking at a refreshed page: the study explorer refetched on mount and flashed a dimmed
  state under React StrictMode, because the skip-first-load guard was a one-shot flag. Fixed by comparing to the
  last-loaded key. The check that hard-coded `wf_oos` at exactly 10 runs failed, correctly, and was rewritten to
  assert distinct windows instead.

## Result

- Code: `scripts/update_studies.py` in `sophie-option-research` (idempotent; `--dry-run`, `--only`).
- The new runs are in the local results store (gitignored), under the same tags with new windows. Their numbers are
  on the viewer's study pages and go stale, so they are not copied here.
- Not refreshed, because they are not in the results store: the rolling and sizing studies (notebook 08) and ML
  meta-labeling (notebook 06).
- Operating notes and lessons are in the `option-research-viewer` skill.
