---
id: librarian-round-6-vrp-core
title: Librarian round 6 — 8 more core VRP/option-writing papers, download + full note + deep summary
lane: research
status: active
assignee: agy
gate:
repo: sophie-option-research
blocker:
next: Active — retrieving papers, downloading open-access copies, drafting deep summaries.
probe: bash probes/librarian-round-6-vrp-core.sh
progress: <3>WSL (14840 - Relay) ERROR: CreateProcessCommon:640: execvpe(/bin/bash) failed: No such file or directory
probe_status: ERROR
stall_flag:
outcome:
artifacts:
created: 2026-09-04
updated: 2026-09-05
---

## Goal

A second batch of 8 core VRP/option-writing papers, picked the same way as round 5: hand-filtered
from the 229-row `papers/candidates/vrp-option-writing.md` backlog for canonical/highly-cited
status, excluding the file's correlation/dispersion-trading, CDO/copula credit-derivative,
risk-parity, and pure volatility-surface-mechanics tangents, and with no overlap against the 24
notes already in `papers/option-writing/` **or** the 8 papers from round 5
(`librarian-round-5-vrp-core`, dispatched 2026-09-04).

Same convention as every prior librarian round for each of the 8 papers below: find it
(arXiv/NBER/SSRN/journal open-access copy first), download the PDF if genuinely open-access,
and write a full `.md` note in `papers/option-writing/` — frontmatter (`title`, `authors`,
`year`, `link`, `area`, `relevance`, `has_pdf`, `has_detailed_summary`, `citations_surfaced`)
plus body sections `# Title`, `## Testable Hypothesis`, `## Summary`, `## Detailed Summary`
(real methodology, data/sample period, actual quantitative results — not a restatement of the
abstract), `## Relevance to Option Research` (tie it to something concrete in
`sophie-option-research`), `## Relevance to Personal Trading & Research` (Rating + Rationale),
`## Notable Citations to Follow Up`. See
`papers/option-writing/bates-2008-market-for-crash-risk.md` for the exact target shape and
depth — that's the bar, not just an abstract-level stub.

**If a paper turns out to be paywalled/blocked**: still write the note (title, authors, year,
link, hypothesis, summary from what's available), but put
`**STATUS: PDF NOT DOWNLOADED — <short reason>**` right after the title, and set
`has_pdf: false` in frontmatter. No matching `.pdf` file for that one. Don't spend more than
one real attempt per paper trying to get past a paywall.

**Slug convention**: `<first-author-lastname>-<year>-<short-topic-slug>.md`, matching existing
files.

## The 8 papers

1. **Aït-Sahalia, Yacine, Mustafa Karaman, and Loriano Mancini (2015)** — *The Term Structure of
   Variance Swaps, Risk Premia and the Expectations Hypothesis* (Journal of Financial
   Econometrics / working paper). Continuous-time no-arbitrage term-structure model separating
   jump risk from diffusive volatility risk across the variance swap curve.
2. **Bali, Turan G., and Arman Hovakimian (2009)** — *Volatility Spreads and Expected Stock
   Returns* (Management Science). Examines how the realized-minus-implied volatility spread
   across individual equities forecasts future returns.
3. **Buraschi, Andrea, Fabio Trojani, and Andrea Vedolin (2014)** — *When Uncertainty Blows in
   the Orchard: Comovement and Equilibrium Volatility Risk Premia* (Journal of Finance). Models
   how belief dispersion and economic uncertainty drive comovement and cross-sectional pricing of
   volatility risk premia.
4. **Cao, Charles, and Bing Han (2013)** — *Cross-Section of Option Returns and Idiosyncratic
   Stock Volatility* (Journal of Financial Economics). Documents that delta-hedged option
   returns decline with the underlying's idiosyncratic volatility due to transaction costs and
   market-maker inventory risk.
5. **Driessen, Joost, Pascal J. Maenhout, and Grigory Vilkov (2009)** — *The Price of Correlation
   Risk: Evidence from Equity Options* (Journal of Finance). Shows index option variance is
   priced significantly higher than basket single-stock variance because index options embed a
   large correlation-risk premium — central to why the VRP is larger on indices than single
   names.
6. **Gabaix, Xavier (2012)** — *Variable Rare Disasters: An Exactly Solved Framework for Ten
   Puzzles in Macro-Finance* (Quarterly Journal of Economics). Time-varying disaster-recovery
   model explaining why short-dated volatility carries extreme premia while long-dated forward
   volatility remains comparatively unpriced.
7. **Kozhan, Roman, Anthony Neuberger, and Paul Schneider (2013)** — *The Skew Risk Premium in
   the Equity Index Market* (Review of Financial Studies). Characterizes the pricing and
   tradeable replication of the skewness risk premium using model-free option portfolios.
8. **Israelov, Roni, and Lars N. Nielsen (2014)** — *Covered Call Strategies: One Fact and Eight
   Myths* (Journal of Portfolio Management / AQR). Clarifies the economic mechanics of covered
   calls, debunking prevalent retail myths about downside protection and yield generation —
   distinct companion piece to the already-owned "Covered Calls Uncovered" note by the same
   authors.

## Not in scope

- Don't touch or re-summarize any existing paper's note, including the 8 from round 5.
- Don't touch sophie-option-research itself.
- Don't pull in anything from the correlation/dispersion, credit-derivative/copula,
  risk-parity, or vol-surface-mechanics sections of the candidates file.
- Don't judge whether these papers validate anything in the current backtest suite — that's a
  later, gated step.

## When done

Update `papers/candidates/vrp-option-writing.md`: for each of the 8 rows labeled
`Selected -- librarian-round-6-vrp-core` in the Status column, either delete the row (it's now
a real note) or change the Status to `Fetched -- <new note filename>`.

## Decision log

- 2026-09-04 — Selected these 8 alongside round 5, same session: hand-filtered for genuinely
  core VRP/option-writing, canonical/highly-cited, no overlap with the 24 existing papers or
  round 5's 8. Labeled the 8 source rows in the candidates file with
  `Selected -- librarian-round-6-vrp-core`. **Deliberately held out of `tasks/` and not queued
  yet** — the research lane's WIP limit is 1 and round 5 was still active at the time this was
  drafted; queuing a second `assignee: agy, gate: (empty)` task while one is still active risks
  the supervisor's `tick()` dispatching both in the same pass (a real gotcha hit before on this
  repo). Move this file into `tasks/librarian-round-6-vrp-core.md` and commit/push only after
  `librarian-round-5-vrp-core` reaches `status: done` in `tasks/done/`.
- 2026-09-05 — `librarian-round-5-vrp-core` finished (all 8 papers, 4 downloaded + 4
  recorded-unavailable, all with Detailed Summaries, library now at 32 notes). Moved this file
  into `tasks/` and queued it.
- 2026-09-05 — Claimed task (status: active). Starting round 6 execution: finding and downloading
  open-access PDFs, writing comprehensive markdown notes with Detailed Summaries for all 8 papers,
  and resolving the candidates backlog.

## Result

<!-- filled by /desk-log on completion -->
