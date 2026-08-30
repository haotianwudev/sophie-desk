---
id: summarize-covered-calls-uncovered
title: Deep-summarize "Covered Calls Uncovered" (Israelov & Nielsen, 2015)
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Read the actual PDF and write a real methodology/results summary.
probe: bash probes/summarize-covered-calls-uncovered.sh
progress: no Detailed Summary section yet
probe_status: RUN
outcome:
artifacts:
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

## Result
