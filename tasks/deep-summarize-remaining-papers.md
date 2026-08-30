---
id: deep-summarize-remaining-papers
title: Deep-summarize the remaining papers, one at a time
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Work through the list below in order, one paper per commit.
probe: bash probes/deep-summarize-remaining-papers.sh
progress: 1/13 papers have a Detailed Summary
probe_status: RUN
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Apply the same treatment `israelov-nielsen-2015-covered-calls-uncovered` already got (see its
`## Detailed Summary` section for the bar to hit) to the 12 papers in `papers/option-writing/`
that still only have an abstract-level note:

1. `augustin-cheng-vandenbergen-2021-volmageddon`
2. `carr-wu-2009-variance-risk-premia`
3. `cheng-2019-vix-premium`
4. `coval-shumway-2001-expected-option-returns`
5. `della-corte-ramadorai-sarno-2016-fx-volatility-risk-premia`
6. `frazzini-pedersen-2012-embedded-leverage`
7. `jurek-stafford-2015-cost-of-capital-alternative-investments`
8. `santa-clara-saretto-2009-option-strategies-margin-calls`
9. `vazquez-2014-option-pricing-tail-risks`
10. `wysocki-2025-sizing-risk`
11. `wysocki-2026-harvesting-vrp-ltr`
12. `wysocki-slepaczuk-2024-construction-hedging`

**Work through them one at a time, not as one giant batch.** For each paper: read the actual
PDF (`papers/option-writing/<slug>.pdf`), add a `## Detailed Summary` section to its `.md`
note covering methodology, data/sample, key quantitative results (real numbers from the
paper's own tables, not vague claims), and one paragraph connecting it to something concrete
in `sophie-option-research`. Leave the existing `## Summary` section untouched. **Commit and
push after each paper**, not once at the end — if this gets interrupted partway, the work
already done should be safely on GitHub, not lost.

Append one line to this task's own Decision log after each paper, so progress is visible
mid-run (e.g. "3/12 done: coval-shumway-2001-expected-option-returns").

## Not in scope

Don't touch `israelov-nielsen-2015-covered-calls-uncovered.md` (already done) or add any new
papers — that's a separate task. Don't touch `sophie-option-research` itself.

## Decision log

- 2026-08-30: 1/12 done: augustin-cheng-vandenbergen-2021-volmageddon
- 2026-08-30: 2/12 done: carr-wu-2009-variance-risk-premia
- 2026-08-30: 3/12 done: cheng-2019-vix-premium

## Result

<!-- pointer only: how many of the 12 got done, and the folder is the real answer -->
