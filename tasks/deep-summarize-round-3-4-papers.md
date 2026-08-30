---
id: deep-summarize-round-3-4-papers
title: Deep-summarize the 11 remaining papers (rounds 3-4), one at a time
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Work through the list below in order, one paper per commit.
probe: bash probes/deep-summarize-round-3-4-papers.sh
progress: 0/10 papers deep-summarized
probe_status: RUN
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Same treatment as `deep-summarize-remaining-papers` (already done for 13 papers) and
`israelov-nielsen-2015-covered-calls-uncovered` before that — apply it to the 11 papers still
only carrying an abstract-level note (all from rounds 3-4):

1. `andersen-benzoni-lund-2002-continuous-time-equity-return-models`
2. `bates-2008-market-for-crash-risk`
3. `bekaert-hoerova-2014-vix-variance-premium`
4. `bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp`
5. `bondarenko-2014-why-are-puts-expensive`
6. `dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk`
7. `feunou-jahan-parvar-okou-2018-downside-variance-risk-premium`
8. `garleanu-pedersen-poteshman-2009-demand-based-option-pricing`
9. `goyal-saretto-2009-cross-section-option-returns`
10. `zhong-2026-non-spanning-identification-scheduled-event-risk`
11. `zhou-2018-variance-risk-premia-macro-uncertainty`

**Note: `bondarenko-2014-why-are-puts-expensive` has no PDF** (`has_pdf: false` in its
frontmatter — recorded but not downloaded, round 4). Skip it for the deep-summary pass; there's
no PDF to read. Leave its note as-is.

**Work through the other 10 one at a time, not as one giant batch.** For each: read the actual
PDF (`papers/option-writing/<slug>.pdf`), add a `## Detailed Summary` section to its note
covering methodology, data/sample, key quantitative results (real numbers from the paper's own
tables), and one paragraph connecting it to something concrete in `sophie-option-research`.
Leave the existing `## Summary` and `## Relevance to Personal Trading & Research` sections
untouched. **Commit and push after every single paper.** Append one line to this task's own
Decision log after each (e.g. "4/10 done: bates-2008-market-for-crash-risk").

After finishing, update each paper's own frontmatter: set `has_detailed_summary: true` (it's
currently `false` on all of these).

## Not in scope

Don't touch any paper that already has a `## Detailed Summary`. Don't touch
`sophie-option-research` itself. Don't fetch anything from `papers/FOLLOWUP-CANDIDATES.md` —
that's a separate, future task.

## Decision log

- 2026-08-30: 1/10 done: andersen-benzoni-lund-2002-continuous-time-equity-return-models
- 2026-08-30: 2/10 done: bates-2008-market-for-crash-risk
- 2026-08-30: 3/10 done: bekaert-hoerova-2014-vix-variance-premium
- 2026-08-30: 4/10 done: bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp
- 2026-08-30: 5/10 done: dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk
- 2026-08-30: 6/10 done: feunou-jahan-parvar-okou-2018-downside-variance-risk-premium

## Result

<!-- pointer only: how many of the 10 got done, papers/Papers.md is the real answer -->
