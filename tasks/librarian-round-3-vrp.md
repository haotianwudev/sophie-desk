---
id: librarian-round-3-vrp
title: Find NEW volatility-risk-premium papers without duplicating rounds 1-2
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Claim, check existing papers first, then search narrowly on VRP.
probe: bash probes/librarian-round-3-vrp.sh
progress: 13 notes total (baseline 13), 0 new yet
probe_status: RUN
outcome:
artifacts:
created: 2026-08-30
updated: 2026-08-30
---

## Goal

A third round, narrower than the first two: **specifically volatility risk premium (VRP)**,
not option-writing strategies in general. Find **3-5 new** open-access papers and file them
into `papers/option-writing/`, same folder, same convention.

**Before searching, read every existing `.md` note in `papers/option-writing/`** — there are
13 already, including two rounds' worth of VRP-adjacent work (`carr-wu-2009-variance-risk-premia`,
`cheng-2019-vix-premium`, `della-corte-ramadorai-sarno-2016-fx-volatility-risk-premia`,
`vazquez-2014-option-pricing-tail-risks`, among others). Don't re-add anything covering the
same ground. Good candidates for genuinely new angles: what actually *predicts* the VRP
(macro/liquidity/sentiment variables), its term structure across maturities, whether it's
priced consistently across single-stock vs. index options, realized-vs-implied variance
swap literature specifically (distinct from the options-based papers already here), or
VRP timing/conditioning strategies (when to harvest it vs. sit out).

Same file-pair convention: `<short-slug>.pdf` (only if genuinely open-access) +
`<short-slug>.md` (title, authors, year, link, one-sentence testable hypothesis).

## Why this folder, why gitignored PDFs

Same as rounds 1-2: PDFs are gitignored (`papers/**/*.pdf`, this repo is public); `.md` notes
are committed.

## Not in scope

- Don't touch or re-summarize any existing paper's note.
- Don't touch `sophie-option-research` itself.
- Don't judge whether these papers validate anything — that's a later, gated step.

## Decision log

## Result

<!-- pointer only: how many new papers, and the folder is the real answer -->
