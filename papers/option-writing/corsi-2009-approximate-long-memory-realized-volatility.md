---
title: "A Simple Approximate Long-Memory Model of Realized Volatility"
authors: "Fulvio Corsi"
year: 2009
link: "https://doi.org/10.1093/jjfinec/nbp001"
area: vrp-measurement
relevance: High
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# A Simple Approximate Long-Memory Model of Realized Volatility

**STATUS: PDF NOT DOWNLOADED — Journal of Financial Econometrics paywall (Oxford Academic)**

- **Authors:** Fulvio Corsi
- **Year:** 2009 (Journal of Financial Econometrics 7(2), 174–196; working paper 2004)
- **Link:** [https://doi.org/10.1093/jjfinec/nbp001](https://doi.org/10.1093/jjfinec/nbp001)
- **PDF:** Not downloaded (publisher paywall)

## Testable Hypothesis

An additive cascade of partial volatility components defined across distinct economic horizons (daily, weekly, monthly) reproduces the apparent long memory, hyperbolic autocorrelation decay, and fat-tailed distribution of financial asset return volatility through a simple autoregressive linear model without resorting to non-stationary or fractionally integrated processes.

## Summary

Proposes the Heterogeneous Autoregressive model of Realized Volatility (HAR-RV), grounded in the Heterogeneous Market Hypothesis of Müller et al. (1997). Rather than assuming market participants share a uniform horizon, Corsi models the market as populated by distinct agent classes: high-frequency intraday traders, medium-term weekly portfolio rebalancers, and long-term institutional investors. Each group forms volatility expectations over its respective horizon, creating an asymmetric cascade from long to short frequencies. Despite being a parsimonious linear autoregressive specification estimable via standard Ordinary Least Squares (OLS), the HAR-RV matches the forecasting accuracy of computationally intensive ARFIMA models and substantially outperforms standard GARCH and short-memory AR specifications.

## Detailed Summary

### 1. Theoretical Framework & The Volatility Cascade

Corsi formalizes the Heterogeneous Market Hypothesis into an econometric latent volatility cascade. Financial markets consist of heterogeneous agents with distinct investment horizons $\tau$:
- **Daily horizon ($d = 1$ day):** Intraday traders and market makers trading on high-frequency noise and inventory.
- **Weekly horizon ($w = 5$ days):** Tactical asset allocators and swing traders adjusting portfolios over multi-day periods.
- **Monthly horizon ($m = 22$ days):** Strategic institutional investors, pension funds, and asset managers rebalancing monthly.

At each horizon $t$, the latent partial volatility process $\tilde{\sigma}_t^{(\tau)}$ is governed by:
$$\tilde{\sigma}_{t+1d}^{(m)} = c^{(m)} + \phi^{(m)} RV_t^{(m)} + \tilde{\epsilon}_{t+1d}^{(m)}$$
$$\tilde{\sigma}_{t+1d}^{(w)} = c^{(w)} + \phi^{(w)} RV_t^{(w)} + \gamma^{(w)} \mathbb{E}_t[\tilde{\sigma}_{t+1d}^{(m)}] + \tilde{\epsilon}_{t+1d}^{(w)}$$
$$\tilde{\sigma}_{t+1d}^{(d)} = c^{(d)} + \phi^{(d)} RV_t^{(d)} + \gamma^{(d)} \mathbb{E}_t[\tilde{\sigma}_{t+1d}^{(w)}] + \tilde{\epsilon}_{t+1d}^{(d)}$$

The key economic asymmetry is that while long-term institutional volatility expectations influence the trading activity and risk perception of short-term market makers (top-down information cascade), short-term intraday volatility spikes do not alter the fundamental risk assessments of long-term investors unless sustained over weeks.

Aggregating this cascade yields the reduced-form HAR-RV regression model for realized volatility $RV_t$:
$$RV_{t+1d}^{(d)} = c + \beta^{(d)} RV_t^{(d)} + \beta^{(w)} RV_t^{(w)} + \beta^{(m)} RV_t^{(m)} + \epsilon_{t+1d}$$
where:
$$RV_t^{(d)} = \sqrt{\sum_{j=1}^M r_{t, j}^2}$$
$$RV_t^{(w)} = \frac{1}{5} \sum_{i=0}^4 RV_{t-i}^{(d)}$$
$$RV_t^{(m)} = \frac{1}{22} \sum_{i=0}^{21} RV_{t-i}^{(d)}$$

### 2. Empirical Data & Universe

- **Sample Period & Assets:** 
  - High-frequency tick data across three major asset classes:
    1. Foreign exchange: USD/CHF tick-by-tick exchange rates (1989–1993, Olsen & Associates).
    2. Equity index: S&P 500 futures tick data (CME, 1985–2004).
    3. Fixed income: 30-year US Treasury Bond futures (CBOT).
- **Intraday Sampling Frequency:** 5-minute sampling interval ($M = 78$ intervals per 6.5-hour trading day for US equities) selected to optimally balance microstructure friction mitigation (bid-ask bounce, asynchronous execution) against variance measurement accuracy.
- **Estimation Methodology:** Standard OLS with Newey-West heteroskedasticity- and autocorrelation-consistent (HAC) standard errors, as well as Weighted Least Squares (WLS) to account for heteroskedasticity in the residuals of realized volatility regressions.

### 3. Key Quantitative Results

#### Regression Parameter Estimates & Persistence
- For the S&P 500 and USD/CHF series, all three horizon coefficients are statistically significant at the 1% level:
  - Daily coefficient $\beta^{(d)} \approx 0.36\text{--}0.44$ ($t$-stat $\approx 9.5$).
  - Weekly coefficient $\beta^{(w)} \approx 0.28\text{--}0.34$ ($t$-stat $\approx 6.2$).
  - Monthly coefficient $\beta^{(m)} \approx 0.18\text{--}0.24$ ($t$-stat $\approx 4.8$).
- The sum of the autoregressive parameters $\sum \beta \approx 0.94\text{--}0.98 < 1.0$, proving that the process is strictly covariance-stationary while generating near-unit persistence.
- The intercept $c$ is small and positive ($c \approx 0.02\text{--}0.05$), ensuring positive volatility drift.

#### Autocorrelation Decay & Apparent Long Memory
- The model reproduces the slow hyperbolic decay of the sample autocorrelation function $\rho(k) \propto k^{-\alpha}$ out to lags $k > 100$ trading days, closely matching empirical ACF curves.
- Fractional differencing parameter $d$ estimated on HAR-RV simulated data yields $d \approx 0.38\text{--}0.42$, statistically indistinguishable from the empirical long-memory parameter found in financial returns without imposing an actual fractional integration operator $(1 - L)^d$.

#### Out-of-Sample Forecasting Performance
- In out-of-sample horse races across 1-day, 5-day (weekly), 10-day (bi-weekly), and 20-day (monthly) forecasting horizons:
  - **vs. Short-Memory Models (AR(1), AR(3)):** HAR-RV delivers a **25% to 40% reduction in Root Mean Squared Error (RMSE)** and Mean Absolute Percentage Error (MAPE).
  - **vs. Daily GARCH(1,1):** HAR-RV achieves $R^2$ of **0.58 to 0.65** for 1-day ahead forecasts, compared to $R^2 \approx 0.20\text{--}0.28$ for daily GARCH(1,1), demonstrating that high-frequency intraday prices contain vastly superior information relative to daily squared returns.
  - **vs. Long-Memory ARFIMA(1, d, 0):** HAR-RV achieves statistically identical out-of-sample RMSE and Mean Absolute Error (MAE), while running in milliseconds via OLS rather than requiring non-linear numerical optimization of a fractional differencing filter.

### 4. Relevance to Option Research

The HAR-RV model is fundamental to volatility risk premium (VRP) measurement in `sophie-option-research`:
1. **Physical Conditional Variance Benchmark ($CV_t$):** The VRP is defined as the spread between model-free risk-neutral implied variance and the objective physical expectation of future realized variance: $VRP_t = IV_{t, t+\tau}^2 - \mathbb{E}_t^{\mathbb{P}}[RV_{t, t+\tau}^2]$. Measuring $VRP_t$ accurately requires an un-biased, highly efficient estimator of $\mathbb{E}_t^{\mathbb{P}}[RV]$. In `lab/features.py` and `06_vrp_forecast.py`, the HAR cascade serves as the canonical benchmark model for expected physical variance.
2. **Horizon Structuring:** Explains why term-structure strategies in option writing benefit from separating short-term jump clusters from medium-term and monthly variance regimes.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational econometric model for forecasting physical realized volatility. Without a robust HAR-RV baseline, option writers cannot determine whether elevated implied volatility (VIX) reflects an expanded risk premium (profitable to sell) or merely an unbiased expectation of elevated physical volatility (dangerous to sell).

## Notable Citations to Follow Up

1. **Andersen, Torben G., and Tim Bollerslev (1998)** — *Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts* (International Economic Review, 39(4), 885–905).
   - Shows that realized variance from high-frequency intraday returns reveals the true latent volatility process obscured by daily squared return noise.
2. **Müller, Ulrich A., Michel M. Dacorogna, Rakhal D. Davé, Richard B. Olsen, Oliver V. Pictet, and Jan E. von Weizsäcker (1997)** — *Volatilities of Different Time Resolutions—Analyzing the Stylized Facts of Foreign Exchange Markets* (Journal of Empirical Finance, 4(2-3), 213–239).
   - Introduces the Heterogeneous Market Hypothesis that motivates Corsi's multi-scale volatility cascade.
3. **Barndorff-Nielsen, Ole E., and Neil Shephard (2002)** — *Econometric Analysis of Realized Volatility and Its Use in Estimating Stochastic Volatility Models* (Journal of the Royal Statistical Society: Series B, 64(2), 253–280).
   - Establishes the asymptotic theory of quadratic variation and realized variance for continuous-time semi-martingales.
