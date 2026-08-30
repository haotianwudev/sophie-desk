---
id: librarian-round-4-option-writing
title: Find NEW option-writing papers (round 4) — record anything you can't download
lane: research
status: done
assignee: agy
gate:
repo: sophie-option-research
blocker:
next:
probe: bash probes/librarian-round-4-option-writing.sh
progress:
probe_status:
outcome: 6 new papers filed (4 open-access PDFs + 2 recorded-unavailable)
artifacts: papers/option-writing/garleanu-pedersen-poteshman-2009-demand-based-option-pricing.md, papers/option-writing/andersen-benzoni-lund-2002-continuous-time-equity-return-models.md, papers/option-writing/bates-2008-market-for-crash-risk.md, papers/option-writing/zhong-2026-non-spanning-identification-scheduled-event-risk.md, papers/option-writing/bondarenko-2014-why-are-puts-expensive.md, papers/option-writing/goyal-saretto-2009-cross-section-option-returns.md
created: 2026-08-30
updated: 2026-08-30
---

## Goal

A fourth round, back to the general scope (option writing / premium selling broadly, not
narrowed to VRP like round 3). Find **3-5 new** open-access papers and file them into
papers/option-writing/, same convention as every prior round.

**Before searching, read every existing .md note in papers/option-writing/** — there are
18 already, across four angles: general covered-call/put-writing decomposition, tail risk,
cross-asset/FX premium, VIX-futures roll premium, and now VRP predictors/term-structure from
round 3. Don't re-cover ground any of these already own.

## New this round: if you find a paper worth including but can't get the PDF

Some relevant papers will be paywalled, behind a dead link, or otherwise not actually
downloadable even though they're clearly real and relevant. **Don't just skip these silently.**
Instead, still write the .md note (title, authors, year, link, one-sentence hypothesis) but
put this line right after the title, before anything else:

`
**STATUS: PDF NOT DOWNLOADED — <short reason, e.g. "paywalled, SSRN preview only">**
`

No matching .pdf file for that one — that absence plus the STATUS line is what marks it
as "found but not fetched," so the user can go look at it themselves later and decide whether
it's worth getting some other way. Every other note keeps the existing convention (no STATUS
line, has a matching PDF).

Same file-pair convention otherwise: <short-slug>.pdf (only when genuinely open-access) +
<short-slug>.md.

## Why this folder, why gitignored PDFs

Same as every prior round: PDFs are gitignored (papers/**/*.pdf, this repo is public);
.md notes are committed.

## Not in scope

- Don't touch or re-summarize any existing paper's note.
- Don't touch sophie-option-research itself.
- Don't judge whether these papers validate anything — that's a later, gated step.

## Decision log

- 2026-08-30: Read all 18 existing notes in papers/option-writing/ across prior rounds (covered calls, margin constraints, embedded leverage, VIX roll premium, FX VRP, variance term structure, downside semi-variance, etc.). Identified remaining uncovered structural angles in option writing / premium harvesting: dealer inventory risk & end-user demand pressure (explaining index put premia and skew), continuous-time jump-diffusion models with stochastic volatility and asymmetric leverage, equilibrium crash risk and heterogeneous crash aversion, scheduled macro event risk (FOMC/CPI/NFP) in short-dated SPX options, model-free statistical arbitrage bounds on overpriced puts, and cross-sectional historical vs. implied volatility spread trading.
- 2026-08-30: Searched across academic repositories (NBER, arXiv, Federal Reserve, journals). Downloaded and verified 4 open-access PDFs using pdftotext.exe to guarantee PDF integrity:
  1. Gârleanu, Pedersen, Poteshman 2009 (garleanu-pedersen-poteshman-2009-demand-based-option-pricing): Foundational theoretical and empirical paper linking end-user net demand pressure (net long index OTM puts) and dealer unhedgeable inventory risk to the index volatility smirk and elevated put prices.
  2. Andersen, Benzoni, Lund 2002 (ndersen-benzoni-lund-2002-continuous-time-equity-return-models): Seminal EMM estimation demonstrating that accurate option pricing requires both state-dependent Poisson jumps and stochastic volatility with asymmetric return-volatility leverage.
  3. Bates 2008 (ates-2008-market-for-crash-risk): Equilibrium crash-risk model showing how less crash-averse option writers insure more crash-averse investors, systematically inflating OTM put prices above physical crash probabilities and explaining the empirical pricing kernel puzzle.
  4. Zhong 2026 (zhong-2026-non-spanning-identification-scheduled-event-risk): Recent arXiv study formulating a non-spanning expiry identification protocol to isolate scheduled macroeconomic announcement jump markups (FOMC, CPI, NFP) from baseline continuous volatility in short-dated SPX options (2022–2025).
- 2026-08-30: Recorded 2 highly relevant but paywalled/blocked papers using the new STATUS: PDF NOT DOWNLOADED — <reason> convention:
  5. Bondarenko 2014 (ondarenko-2014-why-are-puts-expensive): Model-free statistical arbitrage proof showing the S&P 500 put anomaly cannot be explained by standard asset-pricing kernels or Peso problems (STATUS: PDF NOT DOWNLOADED — paywalled (World Scientific / Quarterly Journal of Finance)).
  6. Goyal & Saretto 2009 (goyal-saretto-2009-cross-section-option-returns): Seminal paper on trading the cross-section of equity options sorted by realized vs. implied volatility spreads (HV - IV), generating 1-2%/month alpha (STATUS: PDF NOT DOWNLOADED — paywalled / Cloudflare-blocked repository (Journal of Financial Economics / Purdue e-Pubs)).
- 2026-08-30: Verified probe probes/librarian-round-4-option-writing.sh passes cleanly (OK 24 notes total, 6 new (2 recorded-unavailable), 22 local PDFs).

## Result

6 new papers filed in papers/option-writing/ (4 with open-access PDFs, 2 recorded-unavailable with STATUS header):
- garleanu-pedersen-poteshman-2009-demand-based-option-pricing.md (+ .pdf)
- ndersen-benzoni-lund-2002-continuous-time-equity-return-models.md (+ .pdf)
- ates-2008-market-for-crash-risk.md (+ .pdf)
- zhong-2026-non-spanning-identification-scheduled-event-risk.md (+ .pdf)
- ondarenko-2014-why-are-puts-expensive.md (STATUS: PDF NOT DOWNLOADED)
- goyal-saretto-2009-cross-section-option-returns.md (STATUS: PDF NOT DOWNLOADED)

Folder papers/option-writing/ now contains 24 notes total and 22 local PDFs (all PDFs gitignored).
