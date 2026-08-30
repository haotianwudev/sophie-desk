# Harvesting the Volatility Risk Premium: A Learning-to-Rank Approach

- **Authors:** Maciej Wysocki
- **Year:** 2026
- **Link:** [https://arxiv.org/abs/2608.24786](https://arxiv.org/abs/2608.24786)
- **PDF:** `wysocki-2026-harvesting-vrp-ltr.pdf` (open-access copy)

## Testable Hypothesis

A learning-to-rank machine learning framework with uncertainty-based abstention gates outperforms passive put-writing benchmarks by dynamically selecting optimal strike deltas and sitting out unfavorable volatility regimes in 0DTE SPXW options.

## Summary

Implements a LightGBM LambdaRank model on 1-minute intraday data to rank candidate short-put strikes (0.05 to 0.45 delta) against a cash 'SKIP' option for 0DTE SPXW trading. Demonstrates robust out-of-sample Sharpe ratios and sharp drawdown suppression compared to mechanical CBOE PUT index benchmarks.

## Detailed Summary

### 1. Methodology & Learning-to-Rank Architecture

Wysocki formulates the problem of daily strike selection on the S&P 500 short-dated option surface as a supervised **Learning-to-Rank (LTR)** task using **LightGBM LambdaRank**, moving beyond static delta heuristics and standard regression/classification models.

1. **Candidate Universe & The "SKIP" Decision**:
   - Every trading day at 10:00 ET, the model ranks a discrete catalog of 9 choices: 8 delta-targeted short put candidates ($\Delta \in \{0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.45\}$) on 0DTE SPXW options, plus an explicit cash **"SKIP"** option.
   - The SKIP candidate carries zero return, zero margin requirement, and zero risk, allowing the model to explicitly choose abstention whenever expected downside risk or regime volatility exceeds compensation.

2. **Ranking Objective & Feature Pipeline**:
   - **Optimization Target**: Normalized Discounted Cumulative Gain (NDCG@1) evaluated on path-aware utility labels that penalize intra-day drawdowns, margin consumption, and tail losses.
   - **Feature Selection Pipeline**: Starts from ~190 engineered features spanning volatility surface dynamics (IV level, term slope, skew), per-strategy Greeks (delta, gamma, theta, vega, leverage), entry liquidity (bid-ask spread % at 10:00 ET), macro calendar events (FOMC, CPI, NFP, OPEX), and tail-risk markers (volatility surprise, prior drawdown, VIX z-score). Per-window feature selection isolates ~50–60 surviving features (27 always-surviving core features across all training splits, mean pairwise Jaccard similarity of 0.58).

3. **Risk Controls & Position Sizing Layer**:
   - **Confidence Gate (Abstention Gate)**: An uncertainty-aware gate that compares top-candidate score margins against a calibrated threshold $\tau^*$. If confidence is insufficient, the system overrides the trade and allocates to cash.
   - **Dynamic Position Sizing**: Evaluates 7 sizing architectures calibrated to a target 16% annualized volatility anchor: Edge Allocation (EA), Fixed Margin Utilization (FMU), Short-Richness Scaling (SRS), Volatility Targeting (VT), Gamma-Budgeted (GB), Half-Kelly (HK), and Quarter-Kelly (QK).

### 2. Data & Experimental Schedule

- **Sample Period**: 2017 – 2025 (9 calendar years).
  - *Warm-Up*: 2017 (feature initialization).
  - *Initial Training Window*: 2018 – 2020.
  - *Expanding Walk-Forward (WF)*: 2021 – 2024 (4 annual retraining windows).
  - *Out-of-Time Holdout (OOT)*: 2025 (strictly isolated holdout year).
- **Universe & Frictions**: CBOE SPXW 0DTE PM-settled weekly index options with 1-minute intraday quotes and full bid-ask spread execution modeling, CBOE VIX, and Effective Federal Funds Rate (EFFR).
- **Benchmarks**: S&P 500 Buy & Hold, CBOE PUT Index, CBOE WPUT (Weekly PutWrite) Index, and internal mechanical baselines (Always-25d, Always-45d, Random, Momentum, Rolling-Sharpe).

### 3. Key Quantitative Results

#### Headline Performance Across Sizing Architectures (Table 5)
- **Edge Allocation (EA) (Top Performer)**:
  - *Walk-Forward (2021–2024)*: Annualized **Sharpe 3.10**, Sortino **4.52**, Annual Return **10.91%**, Annualized Volatility **3.51%**, Maximum Drawdown **-2.28%**.
  - *Out-of-Time Holdout (2025)*: Annualized **Sharpe 5.76**, Sortino **7.03**, Annual Return **10.48%**, Volatility **1.82%**, Maximum Drawdown **-1.43%**.
- **Fixed Margin Utilization (FMU)**:
  - *Walk-Forward*: Sharpe 2.51, Sortino 2.99, Return 13.19%, Vol 5.25%, Max Drawdown -6.91%.
  - *Out-of-Time*: Sharpe 5.06, Sortino 6.04, Return 17.95%, Vol 3.54%, Max Drawdown -1.96%.
- **Short-Richness Scaling (SRS)**:
  - *Walk-Forward*: Sharpe 2.76, Return 12.70%, Vol 4.60%, Max Drawdown -6.14%.
  - *Out-of-Time*: Sharpe 5.26, Return 17.55%, Vol 3.34%, Max Drawdown -1.72%.
- **Volatility Targeting (VT)**:
  - *Walk-Forward*: Sharpe 2.21, Return 14.89%, Vol 6.74%, Max Drawdown -9.00%.
  - *Out-of-Time*: Sharpe 4.67, Return 23.88%, Vol 5.12%, Max Drawdown -3.43%.

#### Benchmark Separation & Baseline Failure (Table 5)
- **External Benchmarks**: CBOE PUT Index achieved a walk-forward Sharpe of **0.68** and OOT Sharpe of **0.18**; CBOE WPUT achieved WF Sharpe **0.72**.
- **Static Heuristics (Always-P25d, Always-P45d)**: Generated negative walk-forward Sharpe ratios (**-0.02 to -0.04**) and severe drawdowns exceeding **-40%**, demonstrating that unmanaged static 0DTE short put writing experiences fatal tail events without dynamic strike selection.

#### Statistical Significance & Multi-Test Deflation (Table 6)
- **Probabilistic Sharpe Ratio (PSR)**: Exceeds **0.98** for EA, FMU, and SRS across all benchmark comparisons.
- **Deflated Sharpe Ratio (DSR)**: After penalizing for $N_t = 75$ multiple-testing trials (encompassing all hyperparameter, sizing, gate, and ablation searches), Walk-Forward DSR remains exceptionally robust at **0.996** for Edge Allocation and **0.956** for Short-Richness Scaling.

#### Mechanism Decomposition (Table 10)
- On the walk-forward dataset:
  - Baseline model with neither control: Sharpe = **0.62**.
  - Confidence gate only: Sharpe = **0.76**.
  - Tail-risk features only: Sharpe = **0.16**.
  - Both controls combined (Headline): Sharpe surges to **3.11** (a massive **+2.81 interaction effect**).
- Proves that the primary source of alpha is the synergistic interaction between tail-risk feature identification and the confidence gate's power to withhold capital and execute SKIP during toxic regimes.

### 4. Relevance to Option Research

In `sophie-option-research`, Wysocki (2026) serves as the primary modern blueprint for integrating machine learning with systematic options trading:
1. **Machine Learning Architecture**: Directly guides the implementation of LightGBM LambdaRank models in `src/lab/ml.py` and `src/lab/experiments.py` for dynamic cross-sectional strike selection instead of rigid, hardcoded delta thresholds.
2. **Abstention as an Alpha Driver**: Confirms that integrating an explicit cash / SKIP action and confidence gate in `src/lab/strategy.py` is the single most potent defense against left-tail crashes in short volatility.
3. **Multi-Testing Deflation Protocols**: Establishes the requirement in `src/lab/metrics.py` and `src/lab/report.py` to evaluate backtests not merely on nominal Sharpe ratios, but with Probabilistic Sharpe Ratios (PSR) and Deflated Sharpe Ratios (DSR; $N_t$ trial adjustments) to eliminate false discoveries from parameter mining.

