---
id: librarian-round-3-vrp
title: Find NEW volatility-risk-premium papers without duplicating rounds 1-2
lane: research
status: done
assignee: agy
gate:
repo: sophie-option-research
blocker:
next:
probe: bash probes/librarian-round-3-vrp.sh
progress:
probe_status:
outcome: 5 new papers filed
artifacts: papers/option-writing/bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp.md, papers/option-writing/bekaert-hoerova-2014-vix-variance-premium.md, papers/option-writing/dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk.md, papers/option-writing/feunou-jahan-parvar-okou-2018-downside-variance-risk-premium.md, papers/option-writing/zhou-2018-variance-risk-premia-macro-uncertainty.md
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

- 2026-08-30: Read all 13 existing notes in `papers/option-writing/` first. Identified unaddressed angles in the existing library: macro return predictability of VRP, term structure of variance swaps across horizons (beyond 1M spot), separation of physical uncertainty vs. investor risk aversion in VIX, downside vs. upside semi-variance decomposition (DVRP), and multi-asset cross-market predictability puzzles.
- 2026-08-30: Searched specifically for seminal, high-impact VRP literature covering these distinct dimensions. Filtered for genuine open-access institutional repositories (Federal Reserve Board FEDS, European Central Bank, NBER, Bank of Canada). Tested each URL and verified PDF validity.
- 2026-08-30: Filed 5 new papers (within the 3-5 target):
  1. Bollerslev, Tauchen, Zhou 2009 (`bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp`): Canonical paper on VRP predicting aggregate quarterly equity excess returns.
  2. Bekaert & Hoerova 2014 (`bekaert-hoerova-2014-vix-variance-premium`): Decomposing VIX^2 into physical variance (economic activity predictor) and variance risk premium (risk aversion & stock return predictor).
  3. Dew-Becker, Giglio, Le, Rodriguez 2017 (`dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk`): Term structure of VRP showing only ultra-short variance (1-2 months) is priced, while forward variance beyond 2 months earns zero premium.
  4. Feunou, Jahan-Parvar, Okou 2018 (`feunou-jahan-parvar-okou-2018-downside-variance-risk-premium`): Semi-variance decomposition showing downside VRP drives equity predictability while upside VRP is negligible.
  5. Zhou 2018 (`zhou-2018-variance-risk-premia-macro-uncertainty`): Synthesis of VRP across equities, bonds, currencies, and credit default swaps explaining short-horizon asset predictability puzzles and macroeconomic uncertainty.
- 2026-08-30: Verified probe `probes/librarian-round-3-vrp.sh` passes cleanly (`OK 18 notes total, 5 new, 18 local PDFs`).

## Result

5 new open-access papers filed in `papers/option-writing/` (`.md` + `.pdf` each, PDFs gitignored):
- `bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp`
- `bekaert-hoerova-2014-vix-variance-premium`
- `dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk`
- `feunou-jahan-parvar-okou-2018-downside-variance-risk-premium`
- `zhou-2018-variance-risk-premia-macro-uncertainty`

Folder `papers/option-writing/` contains all 18 notes and 18 local PDFs. No existing paper notes were modified.
