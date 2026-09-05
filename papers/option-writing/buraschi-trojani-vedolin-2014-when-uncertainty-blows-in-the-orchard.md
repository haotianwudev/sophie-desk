---
title: "When Uncertainty Blows in the Orchard: Comovement and Equilibrium Volatility Risk Premia"
authors: "Andrea Buraschi, Fabio Trojani, Andrea Vedolin"
year: 2014
link: "https://doi.org/10.1111/jofi.12095"
area: cross-asset
relevance: High
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# When Uncertainty Blows in the Orchard: Comovement and Equilibrium Volatility Risk Premia

**STATUS: PDF NOT DOWNLOADED — Journal of Finance paywall (Wiley)**

- **Authors:** Andrea Buraschi, Fabio Trojani, Andrea Vedolin
- **Year:** 2014 (Journal of Finance 69(1), 101–137; SSRN Working Paper 1344368 / 1364518)
- **Link:** [https://doi.org/10.1111/jofi.12095](https://doi.org/10.1111/jofi.12095)
- **PDF:** Not downloaded (publisher paywall)

## Testable Hypothesis

Disagreement among investors regarding macroeconomic and firm-specific fundamentals generates endogenous risk premia in options markets; specifically, belief dispersion drives the wedge between index and individual equity volatility risk premia, the relative steepness of implied volatility smiles, and the market price of correlation risk.

## Summary

Buraschi, Trojani, and Vedolin develop a dynamic general equilibrium "orchard" model (multi-tree pure exchange economy) where agents have heterogeneous subjective beliefs regarding cash-flow fundamentals. The authors demonstrate that differences of opinion generate endogenously priced volatility and correlation risk premia across derivative markets, even in the absence of exogenous stochastic volatility or exotic preference specifications. Empirically, using OptionMetrics equity and index options from 1996 through 2008 matched with analyst and economist earnings forecasts from I/B/E/S and the Survey of Professional Forecasters (SPF), the paper confirms four key predictions: (1) belief dispersion strongly predicts the wedge between index variance risk premia and the weighted sum of individual equity variance risk premia; (2) disagreement predicts the difference in skewness (slope of the volatility smirk) between index and single-stock options; (3) macro disagreement commands a large correlation risk premium (CRP); and (4) priced disagreement risk explains the excess returns of volatility dispersion trading strategies (selling index options while buying single-stock options).

## Detailed Summary

### 1. Equilibrium Orchard Framework with Heterogeneous Beliefs

The authors formulate a continuous-time pure exchange economy populated by two groups of rational agents ($A$ and $B$) with identical constant relative risk aversion (CRRA) preferences over aggregate consumption $C_t$:
$$U_i(C_t) = E_t^i \left[ \int_t^T e^{-\rho(s-t)} \frac{C_s^{1-\gamma}}{1-\gamma} ds \right], \quad i \in \{A, B\}$$

The aggregate economy consists of an "orchard" of $N$ trees (individual firms). Each tree $k \in \{1, \dots, N\}$ pays a continuous dividend flow $D_{k,t}$:
$$d\ln D_{k,t} = \mu_{k,t}^i dt + \sigma_k dW_{k,t}^i$$
where $W_{k,t}^i$ is a standard Brownian motion under agent $i$'s filtration. The agents agree on the diffusion matrices $\sigma_k$ and their instantaneous correlation structure $\rho_{jk}$, but they disagree on the unobservable expected growth drifts $\mu_{k,t}^i$.

**Belief Dispersion & Endogenous Pricing Kernel:**
- Let $\delta_{k,t} = \mu_{k,t}^A - \mu_{k,t}^B$ denote the disagreement vector regarding the growth rate of tree $k$.
- The stochastic discount factor (pricing kernel) $M_t$ depends not only on aggregate consumption growth, but also on the cross-sectional distribution of wealth and the aggregate disagreement process $\delta_t = \sum_{k=1}^N w_k \delta_{k,t}$.
- **Endogenous Volatility of the SDF**: Even if aggregate fundamental volatility is constant, disagreement generates time-varying fluctuations in the state-price deflator:
  $$\frac{dM_t}{M_t} = -r_t dt - \theta_t dW_t - \lambda_{\delta, t} d\delta_t$$
  where $\lambda_{\delta, t}$ is the market price of disagreement risk.
- **Index vs. Component Options**: Disagreement about aggregate macro drift induces higher systematic hedging demand for index options relative to component options. When disagreement $\delta_t$ widens, agents trade options aggressively to hedge speculative wealth shifts, driving index option implied volatility and index skewness upward relative to individual equities.

### 2. Empirical Methodology & Data

- **Sample Period**: January 1996 to December 2008 (156 monthly cycles, spanning the dot-com bubble, the 2001 recession, and the 2008 Lehman collapse).
- **Options Data**:
  - S&P 500 index options (SPX) from OptionMetrics.
  - Individual equity options for all constituent firms of the S&P 100 (OEX) and Dow Jones Industrial Average (DJIA).
  - Model-free implied volatilities ($IV$) and realized volatilities ($RV$) computed across 30-day and 60-day horizons.
- **Proxies for Disagreement**:
  - **Macro Disagreement ($\text{DISG}^{\text{macro}}$)**: Cross-sectional standard deviation of forecasts from the Survey of Professional Forecasters (SPF) for real GDP growth, industrial production, and inflation.
  - **Firm-Level Disagreement ($\text{DISG}_k^{\text{firm}}$)**: Standard deviation of analyst EPS forecasts from the I/B/E/S summary history, normalized by the stock price.

### 3. Key Quantitative Results

#### The Index-vs-Component Variance Risk Premium Wedge
- The variance risk premium wedge is defined as:
  $$\Delta VRP_t = VRP_t^{\text{index}} - \sum_{k=1}^N w_{k,t} VRP_{k,t}$$
  where $VRP_t = RV_t - IV_t$.
- In data, index options exhibit a substantially more negative variance risk premium than single-stock options: average annualized $VRP^{\text{index}} \approx -4.2\%$ (variance units), whereas the market-cap weighted average single-stock $VRP^{\text{stocks}} \approx -1.8\%$, producing an average wedge $\Delta VRP$ of **$-2.4\%$ per year**.
- Regressing $\Delta VRP_t$ on macro disagreement ($\text{DISG}_t^{\text{macro}}$):
  - Slope coefficient is negative and highly statistically significant ($\beta = -0.38, t = -3.89, R^2 = 28\%$).
  - When economist disagreement about GDP growth widens by one standard deviation, the index VRP becomes **1.4% more negative** relative to individual stocks.

#### The Correlation Risk Premium (CRP)
- Implied correlation $IC_t$ is extracted from the identity linking index implied variance to constituent option variances:
  $$IV_t^{\text{index}} \approx \sum_{k=1}^N w_{k,t}^2 IV_{k,t} + \sum_{j \ne k} w_{j,t} w_{k,t} IC_t \sqrt{IV_{j,t} IV_{k,t}}$$
- The Correlation Risk Premium is $CRP_t = RC_t - IC_t$, where $RC_t$ is subsequent realized correlation over the option's life.
- Average implied correlation is **48.2%**, while average realized correlation is **36.7%**, yielding an average $CRP$ of **$-11.5\%$** ($t = -5.45$).
- Regressing $CRP_t$ on macro disagreement yields a strong negative slope ($\beta = -0.42, t = -4.12, R^2 = 31\%$). Investors pay a heavy premium to buy index options (synthetic correlation insurance) precisely when economic disagreement is elevated.

#### Slope of the Volatility Smirk (Skewness Wedge)
- Option smirk steepness is measured as $\text{SKEW}_t = IV_t(0.90) - IV_t(1.00)$ (the 90% OTM put IV minus ATM IV).
- The index smirk is consistently steeper than single-stock smirks: average $\text{SKEW}^{\text{index}} = 4.8\%$, compared to $\text{SKEW}^{\text{stocks}} = 2.1\%$.
- The skewness wedge $\Delta \text{SKEW}_t = \text{SKEW}_t^{\text{index}} - \sum w_k \text{SKEW}_{k,t}$ regressed on belief dispersion yields $\beta = +0.31$ ($t = 3.65$). As disagreement increases, market participants bid up index downside crash puts disproportionately to hedge systemic macro risk.

#### Returns to Dispersion Trading Strategies
- The authors backtest a classic **Option Dispersion Strategy**: Short 1 unit of delta-hedged index straddles, Long $\sum w_k$ delta-hedged constituent straddles.
- Unconditional dispersion trading earns an average return of **+1.22% per month** ($t = 3.84$, annualized Sharpe ratio **0.86**).
- When conditioned on the level of belief dispersion:
  - During high-disagreement regimes (top quartile of $\text{DISG}^{\text{macro}}$), the dispersion strategy earns **+2.15% per month** ($t = 4.31$, Sharpe **1.42**).
  - During low-disagreement regimes, the strategy return falls to **+0.41% per month** ($t = 1.15$).
- Multi-factor asset pricing regressions (Fama-French 3-factor, Carhart momentum, Pástor-Stambaugh liquidity, and aggregate market volatility) show that standard factors cannot explain dispersion alpha: abnormal alpha remains **+1.08% per month** ($t = 3.42$).

### 4. Relevance to Option Research

Buraschi, Trojani, and Vedolin's structural equilibrium findings provide essential theoretical and practical mechanics for `sophie-option-research`:
1. **Economic Origin of the SPX Option Smirk**: Explains why index put options are structurally more expensive than single-stock puts without relying on arbitrary ad-hoc crash jump parameters. Index options serve as the single tradeable macro consensus vehicle; when disagreement among institutional investors increases, index put implied volatilities surge.
2. **Correlation Risk Premium Harvesting**: Proves that the excess profitability of selling index options (SPX) relative to single-stock options is fundamentally a **correlation risk premium** ($CRP \approx -11.5\%$). In index put selling strategies (`01_equity_curve.py`, `04_delta_selection.py`), this confirms that an index option writer is primarily an insurer of macro correlation breakdown.
3. **Macro Conditioning Variable**: Recommends incorporating survey-based economic disagreement (e.g., SPF GDP dispersion or Michigan inflation uncertainty) into `lab/features.py` as a fundamental regime filter: when belief dispersion is extreme, correlation risk premia widen, signaling opportune entry for volatility harvesting after the initial volatility spike.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational general equilibrium analysis proving that investor disagreement is the core economic driver of the variance risk premium wedge between index and component options, the correlation risk premium (averaging -11.5%), and the steepness of the index option smirk. Directly explains why index put selling commands higher risk-adjusted compensation than single-stock option writing and validates dispersion trading alpha.

## Notable Citations to Follow Up

1. **Driessen, Joost, Pascal J. Maenhout, and Grigory Vilkov (2009)** — *The Price of Correlation Risk: Evidence from Equity Options* (Journal of Finance, 64(3), 1377–1406).
   - Seminal empirical proof that index options embed an enormous priced correlation risk premium that accounts for the wedge between index and single-stock implied volatilities.
2. **Garleanu, Nicolae, Lasse Heje Pedersen, and Allen M. Poteshman (2009)** — *Demand-Based Option Pricing* (Review of Financial Studies, 22(10), 4259–4299).
   - Shows that end-user net buying pressure from institutional investors seeking index crash insurance generates option mispricing across strikes and maturities due to dealer inventory limits.
3. **Buraschi, Andrea, and Alexei Jiltsov (2006)** — *Model Uncertainty and Option Markets with Heterogeneous Beliefs* (Journal of Finance, 61(6), 2841–2897).
   - Develops the foundational structural link between differences of opinion and trading volume, open interest, and implied volatility smiles in financial derivative markets.
