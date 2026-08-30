---
id: summarize-bondarenko-2014
title: Deep-summarize "Why Are Put Options So Expensive?" (Bondarenko)
lane: research
status: done
assignee: agy
gate:
repo: sophie-option-research
blocker:
next:
probe: bash probes/summarize-bondarenko-2014.sh
progress: no Detailed Summary section yet
probe_status: RUN
stall_flag: 
outcome: Deep summary of Bondarenko (2014/2003) added to papers/option-writing/bondarenko-2014-why-are-puts-expensive.md covering model-free martingale restriction, empirical CME put returns, Peso problem calibration, and relevance to sophie-option-research.
artifacts: papers/option-writing/bondarenko-2014-why-are-puts-expensive.md
created: 2026-08-30
updated: 2026-08-30
---

## Goal

`papers/option-writing/bondarenko-2014-why-are-puts-expensive.md` just got its PDF for the
first time (the user found an open 2003 working-paper draft). It only has an abstract-level
`## Summary` — add a `## Detailed Summary` section, same bar as every other paper in this
library: methodology (the model-free statistical-arbitrage test this paper uses, applied to
1987-2000 S&P 500 put prices), data/sample specifics, key quantitative results (the real
numbers — this paper reports >40% annualized excess returns on ATM/OTM puts, a -23%/month
Jensen's alpha, an $18bn estimated wealth transfer; pull the actual supporting tables, don't
just restate the abstract), and one paragraph connecting it to `sophie-option-research`.

Leave the existing `## Summary`, `## Relevance to Personal Trading & Research`, and
`## Notable Citations to Follow Up` sections untouched. After writing the summary, set
`has_detailed_summary: true` in this paper's own frontmatter.

## Decision log

- 2026-08-30: Claimed task. Read full 40-page PDF draft of Bondarenko (2003/2014). Extracted key empirical tables (Tables 1-6) and theoretical mechanics of the model-free martingale restriction $E_t^v[Z_s / h_s(v)] = Z_t / h_t(v)$ and Average Weighted Return (AWR) metric.
- 2026-08-30: Added comprehensive `## Detailed Summary` section to `papers/option-writing/bondarenko-2014-why-are-puts-expensive.md` covering methodology (RND-deflated martingale restriction, ELM learning, AWR test), CME data sample (1987-2000, 161 monthly cycles), empirical returns (Table 1: -39% monthly ATM put returns; Table 2: Jensen's alpha -23%/mo; Table 4: 1.29 crashes/yr needed for AR=0; $17.8bn wealth transfer), model-free test rejection (Table 6: AWR = -0.35, p < 0.01), refutation of pricing kernel puzzle, and direct connections to `sophie-option-research` (short put edge, Peso problem refutation, regime-conditioned volatility defense). Set `has_detailed_summary: true`.
- 2026-08-30: Verified probe `bash probes/summarize-bondarenko-2014.sh` passes (`OK Detailed Summary present, 1732 words`). Committed paper note changes (commit `5603037`). Set `status: done` and moving task to `tasks/done/`.

## Result

- File: [`papers/option-writing/bondarenko-2014-why-are-puts-expensive.md`](file:///F:/workspace/sophie-desk/papers/option-writing/bondarenko-2014-why-are-puts-expensive.md)
- Commit: `5603037`
