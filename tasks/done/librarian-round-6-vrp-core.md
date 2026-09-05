---
id: librarian-round-6-vrp-core
title: Librarian round 6 — 8 more core VRP/option-writing papers, download + full note + deep summary
lane: research
status: done
assignee: agy
gate:
repo: sophie-option-research
blocker:
next:
probe: bash probes/librarian-round-6-vrp-core.sh
progress: <3>WSL (14840 - Relay) ERROR: CreateProcessCommon:640: execvpe(/bin/bash) failed: No such file or directory
probe_status: ERROR
stall_flag:
outcome: 8 core VRP/option-writing papers filed (4 open-access PDFs + 4 recorded-unavailable), all with Detailed Summaries
artifacts: papers/option-writing/ait-sahalia-karaman-mancini-2015-term-structure-variance-swaps.md, papers/option-writing/bali-hovakimian-2009-volatility-spreads-expected-stock-returns.md, papers/option-writing/buraschi-trojani-vedolin-2014-when-uncertainty-blows-in-the-orchard.md, papers/option-writing/cao-han-2013-option-returns-idiosyncratic-volatility.md, papers/option-writing/driessen-maenhout-vilkov-2009-price-of-correlation-risk.md, papers/option-writing/gabaix-2012-variable-rare-disasters.md, papers/option-writing/israelov-nielsen-2014-covered-call-strategies-myths.md, papers/option-writing/kozhan-neuberger-schneider-2013-skew-risk-premium.md
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
- 2026-09-05 — Resumed execution from scratch (previous attempt timed out after downloading Gabaix (2012) PDF before any notes were written). Processing all 8 target papers systematically: downloading open-access PDFs, compiling deep summaries with empirical data and sophie-option-research links, and updating the candidates backlog.
- 2026-09-05 — All 8 target papers processed and verified:
  1. Aït-Sahalia, Karaman, Mancini (2015): PDF downloaded (1.26 MB), note created (`has_pdf: true`).
  2. Bali & Hovakimian (2009): Paywalled (Management Science / INFORMS), note created (`has_pdf: false`).
  3. Buraschi, Trojani, Vedolin (2014): Paywalled (Journal of Finance / Wiley), note created (`has_pdf: false`).
  4. Cao & Han (2013): PDF downloaded (813 KB), note created (`has_pdf: true`).
  5. Driessen, Maenhout, Vilkov (2009): Paywalled (Journal of Finance / Wiley), note created (`has_pdf: false`).
  6. Gabaix (2012): PDF downloaded (433 KB), note created (`has_pdf: true`).
  7. Kozhan, Neuberger, Schneider (2013): PDF downloaded (439 KB), note created (`has_pdf: true`).
  8. Israelov & Nielsen (2014): Paywalled (Financial Analysts Journal / CFA Institute), note created (`has_pdf: false`).
  All 8 rows in `papers/candidates/vrp-option-writing.md` updated to `Fetched -- <note-filename>`. Library in `papers/option-writing/` expanded from 32 to 40 notes (100% with Detailed Summaries, 32 local PDFs on disk). Moving task to `tasks/done/`.

## Result

- 8 new comprehensive markdown notes created in `papers/option-writing/` (all with full Detailed Summaries, hypotheses, and concrete linkages to `sophie-option-research`):
  - `ait-sahalia-karaman-mancini-2015-term-structure-variance-swaps.md` (+ local PDF)
  - `bali-hovakimian-2009-volatility-spreads-expected-stock-returns.md` (STATUS: PDF NOT DOWNLOADED — Management Science paywall)
  - `buraschi-trojani-vedolin-2014-when-uncertainty-blows-in-the-orchard.md` (STATUS: PDF NOT DOWNLOADED — Journal of Finance paywall)
  - `cao-han-2013-option-returns-idiosyncratic-volatility.md` (+ local PDF)
  - `driessen-maenhout-vilkov-2009-price-of-correlation-risk.md` (STATUS: PDF NOT DOWNLOADED — Journal of Finance paywall)
  - `gabaix-2012-variable-rare-disasters.md` (+ local PDF)
  - `kozhan-neuberger-schneider-2013-skew-risk-premium.md` (+ local PDF)
  - `israelov-nielsen-2014-covered-call-strategies-myths.md` (STATUS: PDF NOT DOWNLOADED — Financial Analysts Journal paywall)
- 4 local open-access PDFs downloaded and stored in `papers/option-writing/` (gitignored per repo rule):
  - `ait-sahalia-karaman-mancini-2015-term-structure-variance-swaps.pdf`
  - `cao-han-2013-option-returns-idiosyncratic-volatility.pdf`
  - `gabaix-2012-variable-rare-disasters.pdf`
  - `kozhan-neuberger-schneider-2013-skew-risk-premium.pdf`
- Candidate backlog in `papers/candidates/vrp-option-writing.md` updated with all 8 rows marked `Fetched -- <note-filename>`.
- Total library size in `papers/option-writing/`: 40 notes (excluding `REVIEW-INDEX.md`), 32 local PDFs on disk, 8 recorded-unavailable paywalled notes, and 40 notes with `## Detailed Summary`.
