---
id: librarian-round-5-vrp-core
title: Librarian round 5 — 8 core VRP/option-writing papers, download + full note + deep summary
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Dispatch to agy (auto-dispatch eligible — no gate).
probe: bash probes/librarian-round-5-vrp-core.sh
progress: 24 notes total (baseline 24), 0 new yet
probe_status: RUN
stall_flag: no commit in 23m while active
outcome:
artifacts:
created: 2026-09-04
updated: 2026-09-05
---

## Goal

Eight papers hand-picked as the most important *core* VRP/option-writing candidates out of the
229-row backlog in `papers/candidates/vrp-option-writing.md` (deliberately excluding that file's
correlation/dispersion-trading, CDO/copula credit-derivative, risk-parity, and pure
volatility-surface-mechanics tangents — those came from unrelated Sophie articles' citation
lists and are out of scope for this round). Each was picked for being foundational/highly-cited
in the VRP/option-writing literature and not already owned by any of the 24 notes in
`papers/option-writing/`.

For **each** of the 8 papers below: find it (arXiv/NBER/SSRN/journal open-access copy first),
download the PDF if genuinely open-access, and write a full `.md` note in
`papers/option-writing/` — **same convention as every prior librarian round**: frontmatter
(`title`, `authors`, `year`, `link`, `area`, `relevance`, `has_pdf`, `has_detailed_summary`,
`citations_surfaced`) plus body sections `# Title`, `## Testable Hypothesis`, `## Summary`,
`## Detailed Summary` (real methodology, data/sample period, actual quantitative results — not
a restatement of the abstract), `## Relevance to Option Research` (tie it to something concrete
in `sophie-option-research`), `## Relevance to Personal Trading & Research` (Rating + Rationale),
`## Notable Citations to Follow Up`. See `papers/option-writing/bates-2008-market-for-crash-risk.md`
for the exact target shape and depth — that's the bar, not just an abstract-level stub.

**If a paper turns out to be paywalled/blocked**: still write the note (title, authors, year,
link, hypothesis, summary from what's available), but put
`**STATUS: PDF NOT DOWNLOADED — <short reason>**` right after the title, and set
`has_pdf: false` in frontmatter. No matching `.pdf` file for that one. Don't spend more than
one real attempt per paper trying to get past a paywall.

**Slug convention**: `<first-author-lastname>-<year>-<short-topic-slug>.md`, matching existing
files (e.g. `moreira-muir-2017-volatility-managed-portfolios.md`).

## The 8 papers

1. **Corsi, Fulvio (2009)** — *A Simple Approximate Long Memory Model of Realized Volatility*
   (Journal of Financial Econometrics). The HAR-RV framework — the standard benchmark model for
   forecasting physical realized variance, foundational to VRP measurement (realized side of
   IV − RV).
2. **Britten-Jones, Mark, and Anthony Neuberger (2000)** — *Option Prices, Implied Price
   Processes, and Stochastic Volatility* (Journal of Finance). Establishes model-free implied
   volatility by integrating option prices across continuous strikes — the mathematical basis
   for VIX-style model-free IV, hence for measuring the VRP at all.
3. **Jackwerth, Jens Carsten (2000)** — *Recovering Risk Aversion from Option Prices and
   Realized Returns* (Review of Financial Studies). Documents the pricing-kernel anomaly and the
   exceptional risk-adjusted profitability of systematic put- and straddle-writing — cited
   directly by Bates (2008), already in the library, as the source of the "pricing kernel
   puzzle."
4. **Constantinides, George M., Jens C. Jackwerth, and Alexi Savov (2013)** — *The Puzzle of
   Index Option Returns* (Journal of Financial and Quantitative Analysis). Shows standard
   equilibrium models with jumps and stochastic volatility fail to explain the cross-section of
   S&P 500 option returns — a central "why does the VRP exist and persist" puzzle paper.
5. **Bollerslev, Tim, and Viktor Todorov (2011)** — *Tails, Fears, and Risk Premia* (Journal of
   Finance). Non-parametric extreme-value framework isolating the jump tail-risk premium from
   high-frequency options data — directly relevant to why short-dated OTM puts carry outsized
   premium.
6. **Moreira, Alan, and Tyler Muir (2017)** — *Volatility-Managed Portfolios* (Journal of
   Finance). Shows dynamically scaling exposure down in high-volatility regimes improves Sharpe
   ratios without sacrificing long-run return — one of the most cited papers in this literature,
   directly relevant to any volatility-conditioned sizing rule in `sophie-option-research`.
7. **Hill, Joanne M., Vasant Balasubramanian, Krag Gregory, and Ingrid Tierens (2006)** —
   *Finding Alpha via Covered Index Writing* (Financial Analysts Journal). The classic
   Goldman/CBOE-adjacent buy-write (BXM-style) performance study across bull and bear regimes —
   foundational for covered-call/buy-write evaluation.
8. **Figelman, Igor (2008)** — *Expected Return and Risk of Covered Call Strategies* (Journal of
   Portfolio Management). Analytical decomposition of covered-call returns into equity risk
   premium and net short-call risk premium — a cleaner analytical companion to the
   already-owned Israelov & Nielsen covered-call note.

## Not in scope

- Don't touch or re-summarize any existing paper's note.
- Don't touch sophie-option-research itself.
- Don't pull in anything from the correlation/dispersion, credit-derivative/copula,
  risk-parity, or vol-surface-mechanics sections of the candidates file — those are explicitly
  out of scope for this round.
- Don't judge whether these papers validate anything in the current backtest suite — that's a
  later, gated step.

## When done

Update `papers/candidates/vrp-option-writing.md`: for each of the 8 rows now labeled
`Selected -- librarian-round-5-vrp-core` in the Status column, either delete the row (it's now
a real note) or change the Status to `Fetched -- <new note filename>`, per that file's own
"mark this file up as they resolve each entry" convention.

## Decision log

- 2026-09-04 — Selected these 8 from the 229-row candidates backlog by hand: filtered to rows
  tagged/sourced as genuinely core VRP/option-writing (excluding the file's correlation,
  credit-copula, risk-parity, and vol-surface tangents), then picked for canonical/highly-cited
  status and no overlap with the 24 papers already in the library. Labeled the 8 source rows in
  the candidates file with `Selected -- librarian-round-5-vrp-core` before creating this task.
- 2026-09-05 — Claimed task (status: active). Starting round 5 execution: finding and downloading
  open-access PDFs, writing comprehensive markdown notes with Detailed Summaries for all 8 papers,
  and resolving the candidates backlog.

## Result

<!-- filled by /desk-log on completion -->
