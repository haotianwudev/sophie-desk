---
id: librarian-test-option-writing
title: Find option-writing research papers and file them in papers/option-writing/
lane: research
status: done
assignee: agy
gate:
repo: sophie-option-research
blocker:
next:
probe: bash probes/librarian-test-option-writing.sh
progress: 9 notes, 9 local PDFs
probe_status: OK
outcome: 9 open-access papers filed into papers/option-writing/ with PDFs and testable hypotheses
artifacts: papers/option-writing/
created: 2026-08-30
updated: 2026-08-29
---

## Goal

A small, low-stakes first test of the claim-and-work loop end to end — not a real research
deliverable yet. Find research papers on **option writing / premium selling** (covered calls,
cash-secured puts, short puts, the volatility risk premium) and file them into
`papers/option-writing/`, one file pair per paper:

- `<short-slug>.pdf` — the paper itself, **only if it's genuinely open-access** (SSRN preprint,
  arXiv, a journal's own free version). Don't pull anything from behind a paywall or a pirate
  mirror. If a paper looks relevant but isn't legally downloadable, still write its note (below)
  with a link — a pointer is enough.
- `<short-slug>.md` — a short note: title, authors, year, link, and **one sentence on what
  testable hypothesis it suggests** (e.g. "selling 30-delta puts outperforms the underlying on a
  risk-adjusted basis when IV rank is elevated"). This one-hypothesis-per-paper habit is the
  actual point — a folder of unread PDFs isn't useful, a folder of one-line hypotheses is.

Aim for **5-10 papers** for this first pass. Quality and relevance over count — a paper that's
tangential to premium-selling strategies isn't worth including just to hit a number.

## Why this folder, why gitignored PDFs

`papers/` already exists in this repo for exactly this. PDFs under it are gitignored
(`papers/**/*.pdf`) since this repo is public — copyrighted papers don't belong in a public git
history even if the paper itself is freely readable elsewhere. The `.md` notes **are** committed;
they're what makes this folder useful to anyone (including a future Claude Code or agy session)
without needing the PDFs on hand.

## Not in scope for this pass

- Don't touch `sophie-option-research` itself or file anything into its notebooks — this is
  purely about building the paper library, not running any analysis yet.
- Don't decide these papers validate or invalidate anything. That's a Lane B / gate-2 judgement
  for later, once there's an actual backtest to check a hypothesis against.

## Decision log

- **2026-08-30** — Task created as a first real test of the desk's claim-and-work loop with
  agy. If this works cleanly, the next step is turning it into `/librarian`, a recurring
  weekly sweep (see `sophie/work-model.md`, Phase 3).
- **2026-08-30** — Claimed task (`status: active`). Downloaded 9 open-access PDFs and committed 9 markdown notes with testable hypotheses to `papers/option-writing/`. Verified probe passes with `OK 9 notes, 9 local PDFs`.

## Result

Filed 9 open-access research papers on option writing, covered calls, short puts, and volatility risk premium into `papers/option-writing/`:

1. `wysocki-2025-sizing-risk`: *Sizing the Risk: Kelly, VIX, and Hybrid Approaches in Put-Writing on Index Options* (2025)
2. `wysocki-2026-harvesting-vrp-ltr`: *Harvesting the Volatility Risk Premium: A Learning-to-Rank Approach* (2026)
3. `wysocki-slepaczuk-2024-construction-hedging`: *Construction and Hedging of Equity Index Options Portfolios* (2024)
4. `israelov-nielsen-2015-covered-calls-uncovered`: *Covered Calls Uncovered* (2015)
5. `santa-clara-saretto-2009-option-strategies-margin-calls`: *Option Strategies: Good Deals and Margin Calls* (2009)
6. `jurek-stafford-2015-cost-of-capital-alternative-investments`: *The Cost of Capital for Alternative Investments* (2015)
7. `frazzini-pedersen-2012-embedded-leverage`: *Embedded Leverage* (2012)
8. `coval-shumway-2001-expected-option-returns`: *Expected Option Returns* (2001)
9. `vazquez-2014-option-pricing-tail-risks`: *Option Pricing, Historical Volatility and Tail Risks* (2014)
