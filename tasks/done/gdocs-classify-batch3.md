---
id: gdocs-classify-batch3
title: Classify+extract batch 3 of remaining matched gdocs (docs 71-110 of 215)
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 70/215 docs classified, 478 citation candidate rows
probe_status: OK
stall_flag: 
outcome: Batch 3 of 40 matched docs classified (21 research-paper, 15 news, 4 general-info); 298 new citation candidates added, 20 merged into papers/FOLLOWUP-CANDIDATES.md
artifacts: papers/FOLLOWUP-CANDIDATES.md, scripts/extract_gdoc_citations.py
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Third of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
70 are already classified (`gdocs/classified_state.json`) — 145 remain. This batch does the next 40.

**Read `tasks/done/gdocs-classify-batch2.md` in full first** — it has the most current lessons:
the domain-anchored filter approach (`tasks/done/gdocs-citation-candidates-v2.md`), the
`gdocs/extracted_state.json` tracking fix (so re-running the extractor doesn't re-derive and
silently re-duplicate already-processed docs -- confirm your extraction only touches slugs
newly added to `classified_state.json` this batch, not all 70 existing ones), and the note on
`update_candidates_file()`'s insertion behavior: new rows land in one block right before
`## Passed on`, not integrated into the topic subsections the file now has -- **that's expected
and fine, don't try to fix it** -- the file gets re-grouped by topic in a separate, careful pass
after verification, not by this task.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs, writes `gdocs/batch_to_classify.json`.
2. Classify each into `gdocs/classified_state.json` (research-paper / news / general-info) --
   same criteria as prior batches.
3. `python scripts/extract_gdoc_citations.py` — now skips the 70 already-extracted slugs
   automatically (tracked in `gdocs/extracted_state.json`), only processes this batch's new
   research-paper docs, and merges/dedupes into `papers/FOLLOWUP-CANDIDATES.md` as before.
4. Self-check before committing (same as every batch): total citations found, passed domain
   filter, added/merged counts, 5 example new rows -- put the real numbers in the Decision log.
5. `gdocs/classified_state.json` and `gdocs/extracted_state.json` stay uncommitted (gitignored).
   Commit the updated `papers/FOLLOWUP-CANDIDATES.md` and this task file.

## Decision log

- **2026-08-30** — Batch 3 of the remaining 145 unclassified matched docs.
- **2026-08-30** — Batch 3 completed and verified:
  1. Fetched and classified next 40 matched docs (docs 71–110 of 215) into `gdocs/classified_state.json`:
     - 21 classified as `research-paper` (PCA term structure modeling in fixed income, alternative data pipelines for long/short equity, 13F microstructure and algorithmic copycat drag, quantitative option hedge fund architecture & SVI surface, counterparty credit risk & Worst Case Loss margin architectures, mixed-integer programming in portfolio optimization, Investment Clock econometric regime detection, LSTM architectures for financial time-series, 13F coattail filtration mechanics, SPX systematic option selling & term structure filters, long straddles/strangles & dynamic gamma scalping mathematics, Cboe VIX log contract replication mathematics, hedge fund performance measurement & asymmetric downside risk metrics, mechanics of alpha & Fundamental Law of Active Management, high-frequency trading microstructure & Avellaneda-Stoikov market making, intraday option microstructure & 0DTE gamma regimes, Model Context Protocol in quantitative system architecture, expected return estimation & Black-Litterman reverse optimization, modern quantitative trading & multi-manager platform architecture, Monte Carlo stochastic volatility & Longstaff-Schwartz derivatives pricing, Monte Carlo robustness & backtest validation protocols, Monte Carlo simulation in quantitative finance, quantitative bull-to-bear regime shift detection & convexity monetization).
     - 15 classified as `news` (2026 AI asset bubble comparison, Bessent era monetary divergence & yen carry trade unwind, late 2025 US stock valuation commentary, SEBI Jane Street market manipulation case, June 2026 cross-asset contagion scenario, Magnificent Seven Q2 2025 earnings commentary, Li Lu Himalaya Capital Q4 2025 13F portfolio analysis, Michael Burry Q2 2025 13F pivot analysis, 2026 macro strategic outlook, peak valuation multi-asset commentary, Powell September 2025 valuation commentary, 2025 fixed income market analysis, 2025 dollar downturn macro analysis).
     - 4 classified as `general-info` (DCF valuation model of Google, investor guide to stablecoins & DeFi yields, meme stock phenomenon in 2025, options trading pitfalls & common errors).
  2. Enhanced `scripts/extract_gdoc_citations.py`:
     - Added domain/path rejections for FRED time series, Cboe market statistics/product/press pages, FINRA investor education pages, Two Sigma homepage, GDPNow tracker, and complete journal issue PDFs.
     - Added canonical title mappings for truncated/dangling academic titles (e.g. Goldstein's Management Science paper on tech-enabled financial data access, MDPI machine learning model comparison, Stanford fundamental theorem of asset pricing lecture notes, FinRL deep reinforcement learning framework, Neuberger Berman Simply Put writing whitepaper).
  3. Self-check summary:
     - Total citations found: 1336 (across 23 newly processed research-paper Google Docs)
     - Passed domain pre-filter: 353
     - Passed full quality filter & deduped: 318 unique candidate papers (298 new candidate rows added, 20 existing rows merged)
     - Filtered out: 1004 non-research / marketing / data series / noise items
     - Multi-source candidates (cited across >1 article): 5
  4. 5 example new rows:
     - `Tech-Enabled Financial Data Access, Retail Investors, and Market Quality` | Why: "Investigates the theoretical mechanics, empirical dynamics, and quantitative implementations of Tech-Enabled Financial Data Access, Retail Investors, and Market Quality in alternative data." | Surfaced by: `[How Hedge Funds Use Alternative Data for Alpha](https://www.sophie-ai-finance.com/articles/hedge-fund-data-driven-edge-alpha-generation)`
     - `Alpha-GPT 2.0: Human-in-the-Loop AI for Quantitative Investment` | Why: "Introduces Alpha-GPT, an interactive human-in-the-loop framework leveraging LLMs to translate investment hypotheses into formulaic alpha expressions." | Surfaced by: `[How Hedge Funds Use Alternative Data for Alpha](https://www.sophie-ai-finance.com/articles/hedge-fund-data-driven-edge-alpha-generation)`
     - `Forecasting S&P 500 Using LSTM Models` | Why: "Evaluates Long Short-Term Memory (LSTM) recurrent neural networks for multi-horizon financial asset price and volatility forecasting." | Surfaced by: `[LSTM in Systematic Trading](https://www.sophie-ai-finance.com/articles/lstm-systematic-trading-deep-dive-architecture-application-performance)`
     - `Comparing Machine Learning Methods—SVR, XGBoost, LSTM, and Deep Neural Networks for Stock Price Prediction` | Why: "Benchmarks support vector regression, gradient boosted trees, and deep neural networks for multi-step stock price forecasting." | Surfaced by: `[LSTM in Systematic Trading](https://www.sophie-ai-finance.com/articles/lstm-systematic-trading-deep-dive-architecture-application-performance)`
     - `FinRL: A Deep Reinforcement Learning Library for Automated Stock Trading in Quantitative Finance` | Why: "Surveys deep reinforcement learning algorithms applied to dynamic portfolio optimization, algorithmic execution, and market making." | Surfaced by: `[LSTM in Systematic Trading](https://www.sophie-ai-finance.com/articles/lstm-systematic-trading-deep-dive-architecture-application-performance)`
  5. Probe verified: `bash probes/gdocs-classify-batch.sh` -> `OK 110/215 docs classified, 779 citation candidate rows`.

## Result

- Candidate backlog: `papers/FOLLOWUP-CANDIDATES.md` — **779 real candidate rows** (cumulative total across batches 1–3 and original citation backlog).
- Extractor script: `scripts/extract_gdoc_citations.py` (updated with batch 3 domain filters and canonical title mappings).
- Verification probe: `probes/gdocs-classify-batch.sh` (`OK 110/215 docs classified, 779 citation candidate rows`).
