---
id: review-papers-relevance-and-citations
title: Rate each paper's relevance to personal trading/research, surface cited papers worth chasing
lane: research
status: queued
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Claim, then work through all 24 papers one at a time, committing after each.
probe: bash probes/review-papers-relevance-and-citations.sh
progress: 0/24 papers rated, REVIEW-INDEX.md 0 lines
probe_status: RUN
stall_flag: 
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

A second pass over every paper already in `papers/option-writing/` (24 currently) — not
gathering new papers, and not the deep-methodology summary that's already done for all of
them. This pass asks two different questions per paper:

**1. How relevant is this to actual personal trading and research, specifically?**
Ground this in what the research actually is, not a generic academic-quality judgment: the
user is researching and eventually trading option-writing / premium-selling strategies (short
puts, covered calls, iron condors), building and validating this in `sophie-option-research`
(a backtest platform already covering VIX rank, RSI, realized vol, VRP measurement,
walk-forward validation, ML meta-labeling, roll/management rules). Rate each paper **High /
Medium / Low**, with 1-2 sentences of *why*, tied to something concrete: does it suggest a
testable signal or rule this pipeline doesn't have yet? Does it validate or contradict an
assumption the pipeline already makes? Or is it tangential — right asset class but wrong
question, or a theory piece with no actionable strategy implication?

**2. What does this paper cite that's worth chasing down?**
Read the paper's own reference list. Name 2-3 specific cited works that look like genuinely
good candidates for a future paper-gathering round — not everything it cites, just the ones
that look substantively relevant and aren't already covered by the 24 papers already here
(check titles/authors against what's already in the folder before listing one). One line each
on why it looks worth getting. If a paper's references don't turn up anything new beyond
what's already covered, say so explicitly rather than forcing a citation.

## How to work through this

**One paper at a time, not as one batch.** For each paper:
1. Re-read its PDF (`papers/option-writing/<slug>.pdf`) and its own `.md` note.
2. Add a `## Relevance to Personal Trading & Research` section to that note (rating + reasoning).
3. Add a `## Notable Citations to Follow Up` section to that note (2-3 candidates + reasons,
   or an explicit "nothing new found" line).
4. Append one row to `papers/option-writing/REVIEW-INDEX.md` — create it if it doesn't exist,
   with columns: paper slug, relevance rating, one-line reason, # of new citation candidates
   found. This is what makes the whole pass scannable even if it stops partway.
5. Append one line to this task's own Decision log (e.g. "5/24 done: <slug>").
6. **Commit and push after every single paper**, not in batches. If this gets interrupted,
   everything done so far must already be safely on GitHub.

## Not in scope

- Don't actually go fetch or download any of the cited papers — that's a future round's job,
  this pass only surfaces candidates.
- Don't judge whether the current 24 papers collectively validate anything — that's separate,
  gated research work, not a relevance/citation review.
- Don't re-touch the existing `## Summary` or `## Detailed Summary` sections.

## Decision log

## Result

<!-- pointer only: how many of the 24 got reviewed, REVIEW-INDEX.md is the real answer -->
