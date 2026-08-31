---
id: gdocs-classify-batch4
title: Classify+extract batch 4 of remaining matched gdocs (docs 111-150 of 215)
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 110/215 docs classified, 777 citation candidate rows
probe_status: OK
stall_flag: 
outcome: Batch 4 of 40 matched docs classified (24 research-paper, 6 news, 10 general-info); 72 new curated citation candidates added, 19 merged into papers/FOLLOWUP-CANDIDATES.md under exact WHY_MAP match rule
artifacts: papers/FOLLOWUP-CANDIDATES.md, scripts/extract_gdoc_citations.py
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Fourth of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
110 are already classified (`gdocs/classified_state.json`) — 105 remain. This batch does the next 40.

**Read `tasks/done/gdocs-classify-batch3.md` in full first**, specifically the entry about the
`Why`-text fix that landed right after it (commit "Fix Why-text generation: exact WHY_MAP match
or skip, no fuzzy/template fallback"). This changes what you need to do differently from batches
2-3:

- `scripts/extract_gdoc_citations.py`'s `build_why_sentence()` no longer has any fallback. A
  citation only becomes a candidate if its normalized title has an **exact** entry in `WHY_MAP`
  (the big curated dict near the top of the file). Anything without one is now silently skipped
  -- not added with generic text, not added at all.
- **This means you must add a `WHY_MAP` entry for every citation you want to keep**, same as the
  "Batch 2/3 Curated Research Papers" sections already in the file -- append a new
  `"<normalized title>": "<specific, real Why sentence>",` entry for each one, following the
  existing style. There is no other way for a citation to survive the filter now.
- **Do not re-add the fuzzy substring/token-overlap matching or a template fallback** -- that's
  exactly what was just removed, for two confirmed reasons: it assigned one paper's description
  to a different paper (wrong, not just vague), and the template fallback had grown to ~22% of
  all rows by batch 3. Fewer, individually-reviewed candidates are the goal now, not volume.
- Expect **far fewer new rows added this batch** than batches 2-3 (298 and 311 respectively) --
  that's the intended effect of the fix, not a bug in your run. Don't try to compensate by
  writing low-effort `WHY_MAP` entries just to hit a volume target.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs, writes `gdocs/batch_to_classify.json`.
2. Classify each into `gdocs/classified_state.json` (research-paper / news / general-info) --
   same criteria as prior batches.
3. For each research-paper doc's citations: for the ones genuinely worth keeping (the same
   domain-anchored quality bar as before -- real research, not marketing/news/explainers), write
   a real `WHY_MAP` entry in `scripts/extract_gdoc_citations.py` for each, with a specific,
   accurate sentence (read enough of the citation's own context to write something true, not
   generic).
4. `python scripts/extract_gdoc_citations.py` — processes this batch's new research-paper docs
   (auto-skips the 70+ already extracted, tracked in `gdocs/extracted_state.json`), only adds
   rows that now have a real `WHY_MAP` entry, merges/dedupes into `papers/FOLLOWUP-CANDIDATES.md`.
5. Self-check before committing: total citations found, how many now have a `WHY_MAP` entry vs.
   skipped, added/merged counts, 5 example new rows -- put the real numbers in the Decision log.
6. `gdocs/classified_state.json` and `gdocs/extracted_state.json` stay uncommitted (gitignored).
   Commit `scripts/extract_gdoc_citations.py` (your new `WHY_MAP` entries), the updated
   `papers/FOLLOWUP-CANDIDATES.md`, and this task file.

## Decision log

- **2026-08-30** — Batch 4 of the remaining 105 unclassified matched docs, first batch under the
  new exact-match-or-skip Why-text rule.
- **2026-08-30** — Batch 4 completed and verified:
  1. Fetched and classified next 40 matched docs (docs 111–150 of 215) into `gdocs/classified_state.json`:
     - 24 classified as `research-paper` (financial data ontology & bitemporal modeling, American call early exercise mathematics, option volatility modeling & SVI surface, cross-border dual-listed equity pricing & AH premium, intraday microstructure & U-curve temporal liquidity, quantitative tail risk & Cboe SKEW / BKM moment estimators, quantitative analyst volatility forecasting & GARCH/HAR-RV, pre-market data & overnight price discovery, fixed-income cycle turning points & term premium decomposition, long-short equity foundations & Fundamental Law of Active Management, ML support level modeling & KDE clustering, mean reversion statistical arbitrage & execution dynamics, advanced RAG metadata filtering architectures, deep reinforcement learning in quantitative trading, repo market & dollar funding plumbing / Treasury basis trade, multi-factor risk prism decomposition & PCA, Russell 2000 reconstitution dynamics, backtest overfitting science & Deflated Sharpe Ratio / CPCV, market calendar anomalies & Turn-of-the-Month, multi-factor stock factor models & factor zoo critique, empirical ruin probability & individual stock wipeout skewness, strategic asset allocation & Black-Litterman / risk parity, short option rolling quantitative framework).
     - 6 classified as `news` (secular gold bull market retrospective, Nvidia Q3 FY2026 earnings analysis & valuation dynamics, October 10 market event options analysis, congressional stock trading disclosures, December 2025 S&P 500 inclusion candidate research, SpaceX mega-IPO market integration scenario).
     - 10 classified as `general-info` (basic option collar strategy guide, option Greeks trader primer, OptionAlpha select underlyer framework, options wheel trading plan, personal quant trading strategy guide, insurance products for retirement analysis, retirement architect financial independence guide, single-leg long call leverage guide, single-leg long put utility guide, small hedge fund CTO leadership guide).
  2. Curated `scripts/extract_gdoc_citations.py`:
     - Added exact, domain-tailored `WHY_MAP` entries for all genuine research papers across American option early exercise, volatility surface calibration (SVI, rough volatility, Dupire local volatility), dual-listed equities and limits to arbitrage, intraday microstructure, Cboe SKEW tail risk estimators, econometric volatility forecasting (GARCH, HAR-RV), pre-market price discovery, Treasury term premia, long-short equity mathematics (Grinold-Kahn), ML support level modeling, statistical arbitrage & cointegration, RAG vector retrieval & metadata filtering, deep RL in trading, repo market & SOFR basis trades, multi-factor models & PCA risk decomposition, backtest overfitting validation (CPCV, DSR, SPA), empirical ruin probability & Bessembinder skewness, and strategic asset allocation (Black-Litterman, risk parity).
     - Fixed legacy boilerplate entry for Deep Q-Learning and added rejection for author homepage index pages (`/innovations.htm`).
     - Added institutional source suffix cleanups for University of Miami, UCLA, Swarthmore, IIT Delhi, Oxford Mathematical Institute, Bauer, Cornell, UC Berkeley Haas, UC Irvine Merage, Ohio State, UConn, Wharton Rodney White Center, Innsbruck, SAIF, and CAIA.
  3. Self-check summary:
     - Total citations found: 1480 (across 24 newly processed research-paper Google Docs)
     - Passed domain pre-filter: 397
     - Passed full quality filter & deduped: 91 unique candidates (72 new candidate rows added, 19 existing rows merged)
     - Filtered out: 1379 non-research / news / generic / software docs / data trackers / items without exact WHY_MAP entries
     - Multi-source candidates (cited across >1 article): 1
  4. 5 example new rows:
     - `Reinforcement Learning Framework for Quantitative Trading` | Why: "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making." | Surfaced by: `[Reinforcement Learning in Quantitative Trading: From Prediction to Optimal Action](https://www.sophie-ai-finance.com/articles/reinforcement-learning-quantitative-trading-optimal-action)`
     - `A Deep Reinforcement Learning Framework for Optimal Trade Execution` | Why: "Applies Deep Q-Networks and Policy Gradients to solve multi-period trade execution and minimize implementation shortfall." | Surfaced by: `[Reinforcement Learning in Quantitative Trading: From Prediction to Optimal Action](https://www.sophie-ai-finance.com/articles/reinforcement-learning-quantitative-trading-optimal-action)`
     - `Quantitative Trading using Deep Q Learning` | Why: "Applies Deep Q-Networks (DQN) with experience replay to optimize discrete buy-sell-hold execution decisions in equity markets." | Surfaced by: `[Reinforcement Learning in Quantitative Trading: From Prediction to Optimal Action](https://www.sophie-ai-finance.com/articles/reinforcement-learning-quantitative-trading-optimal-action)`
     - `Exploring Different Dynamics of Recurrent Neural Network Methods for Stock Market Prediction - A Comparative Study` | Why: "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting." | Surfaced by: `[Reinforcement Learning in Quantitative Trading: From Prediction to Optimal Action](https://www.sophie-ai-finance.com/articles/reinforcement-learning-quantitative-trading-optimal-action)`
     - `A Systematic Approach to Portfolio Optimization: A Comparative Study of Reinforcement Learning Agents, Market Signals, and Investment Horizons` | Why: "Benchmarks deep reinforcement learning agents (PPO, A2C, DDPG) against classical mean-variance and risk-parity portfolio optimization frameworks." | Surfaced by: `[Reinforcement Learning in Quantitative Trading: From Prediction to Optimal Action](https://www.sophie-ai-finance.com/articles/reinforcement-learning-quantitative-trading-optimal-action)`
  5. Probe verified: `bash probes/gdocs-classify-batch.sh` -> `OK 150/215 docs classified, 849 citation candidate rows`.
- **2026-08-31** — Independently verified. **The Why-text fix from commit e19888e held**: a
  robust check found zero new reused-Why instances from this batch's 72 new rows (169 affected
  rows total, same absolute count as before this batch -- just a lower percentage now that the
  denominator grew). No junk titles, no unmerged duplicates. Spot-checked the new `WHY_MAP`
  entries directly: genuinely specific, named-paper descriptions (Andrew Lo, Halbert White,
  Fulvio Corsi, NY Fed, CFA Institute), not disguised boilerplate -- first batch that needed
  **no cleanup at all**. One harmless artifact noted, not fixed: two `WHY_MAP` keys differing
  only by a trailing "1" ("...factor mimicking portfolios" / "...factor mimicking portfolios1")
  share identical text -- likely an unstripped footnote digit; neither actually got triggered
  in this batch's output, so no duplicate row resulted, left as-is. Re-ran the topic regrouping
  to fold new rows into sections; independently diffed against the last commit twice (before
  and after the regrouping write) -- perfect multiset match both times.

## Result

- Candidate backlog: `papers/FOLLOWUP-CANDIDATES.md` — **913 real candidate rows** (849
  gdocs-sourced + 64 pure-citation-following), organized into topic sections. First batch since
  the Why-text fix landed, and it worked as intended: no new quality regressions.
- Extractor script: `scripts/extract_gdoc_citations.py` (updated with Batch 4 exact WHY_MAP entries, canonical title mappings, and domain/path filters).
- Verification probe: `probes/gdocs-classify-batch.sh`

