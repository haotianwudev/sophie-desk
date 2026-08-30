---
id: librarian-round-2-option-writing
title: Find NEW option-writing papers without duplicating round 1
lane: research
status: queued
assignee: claude
gate:
repo: sophie-option-research
blocker:
next: Claim, check existing papers first, then search for genuinely new ones.
probe: bash probes/librarian-round-2-option-writing.sh
progress:
probe_status:
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

A second, small test of the claim-and-work loop — this time with **you (a fresh Claude Code
session with no memory of any prior conversation)** as the assignee, to check the same loop
that already worked for agy. Find **3-5 new** open-access papers on option writing / premium
selling and file them into `papers/option-writing/`, the same folder the first round used.

**Before searching, read every existing `.md` note in `papers/option-writing/`** to see
what's already there — titles, authors, and the specific hypothesis or empirical angle each
one covers. Don't just avoid re-adding the exact same paper; avoid papers that would be
substantively redundant with what's already covered (e.g., another generic "covered calls
outperform" survey covers no new ground if `israelov-nielsen-2015-covered-calls-uncovered`
already covers the reversal-decomposition angle in depth). Look for genuinely different
angles: tail risk, roll/management rules, cross-asset premium comparisons, machine-learning
approaches to timing the sell, whatever the existing set is missing.

Same file-pair convention as round 1:
- `<short-slug>.pdf` — only if genuinely open-access (SSRN preprint, arXiv, a journal's own
  free version). Never a paywalled or pirated copy.
- `<short-slug>.md` — title, authors, year, link, one-sentence testable hypothesis.

## Why this folder, why gitignored PDFs

Same as round 1: PDFs are gitignored (`papers/**/*.pdf`, this repo is public); `.md` notes are
committed and are what makes the folder useful without needing the PDFs on hand.

## Not in scope

- Don't touch or re-summarize any existing paper's note.
- Don't touch `sophie-option-research` itself.
- Don't judge whether these papers validate anything — that's a later, gated step.

## Decision log

## Result

<!-- pointer only: how many new papers, and the folder is the real answer -->
