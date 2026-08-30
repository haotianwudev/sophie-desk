---
id: summarize-covered-calls-uncovered
title: Deep-summarize "Covered Calls Uncovered" (Israelov & Nielsen, 2015)
lane: research
status: done
assignee: agy
gate:
repo: sophie-option-research
blocker:
next:
probe: bash probes/summarize-covered-calls-uncovered.sh
progress: Detailed Summary present, 982 words
probe_status: OK
outcome: Deep summary of Israelov & Nielsen (2015) added to papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md covering return decomposition, empirical results, and relevance to option-writing research.
artifacts: papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md
created: 2026-08-30
updated: 2026-08-29
---

## Goal

`papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md` already has a short
one-paragraph summary from the earlier paper-gathering pass — that was written from the
abstract, not a real read of the paper. This task asks for the real thing: **actually read
the PDF** (`papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.pdf`) and add
a genuinely deeper summary underneath the existing one.

Add a new `## Detailed Summary` section (leave the existing `## Summary` section untouched)
covering:

- **Methodology** — how they decompose covered call returns into equity risk / volatility
  risk premium / equity-reversal exposure. What's the actual construction (index, options
  used, delta-hedging mechanics)?
- **Data** — what sample period and universe did they use?
- **Key quantitative results** — actual numbers: Sharpe ratio improvement, how much of
  covered-call return the reversal bet explains, any specific figures/tables worth noting.
- **Relevance** — one paragraph on how this connects to the option-writing research already
  in `sophie-option-research` (short puts, VRP measurement) — does the reversal-hedging idea
  suggest anything testable there?

## Not in scope

Don't touch any other paper's note. Don't run any backtest or modify `sophie-option-research`
itself — this is a reading/writing task only.

## Decision log

- **2026-08-30** — Task claimed (`status: active`, `assignee: agy`). Read full text and exhibit data of `papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.pdf`.
- **2026-08-30** — Appended comprehensive `## Detailed Summary` section to `papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md` covering methodology (economic decomposition and daily futures delta-hedging), data universe (SPX, BXM, BXY from 1996 to 2014), key quantitative findings (Sharpe ratio 0.37 -> 0.52, risk contribution 26% uncompensated reversal, downside beta 0.85 -> 0.60), and research relevance to `sophie-option-research` (short put delta-hedging, VRP isolation, attribution tooling).
- **2026-08-30** — Verified probe passed (`OK Detailed Summary present, 982 words`), updated task to `status: done`, and archived to `tasks/done/`.

## Result

Added detailed methodology, empirical decomposition statistics, and research implications to:
- [`papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md`](file:///F:/workspace/sophie-desk/papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md)
