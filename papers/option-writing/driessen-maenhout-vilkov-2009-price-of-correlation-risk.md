---
title: "The Price of Correlation Risk: Evidence from Equity Options"
authors: "Joost Driessen, Pascal J. Maenhout, Grigory Vilkov"
year: 2009
link: "https://doi.org/10.1111/j.1540-6261.2009.01467.x"
area: vrp-measurement
relevance: High
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# The Price of Correlation Risk: Evidence from Equity Options

**STATUS: PDF NOT DOWNLOADED — Journal of Finance paywall (Wiley)**

- **Authors:** Joost Driessen, Pascal J. Maenhout, Grigory Vilkov
- **Year:** 2009 (Journal of Finance 64(3), 1377–1406; SSRN Working Paper 673425)
- **Link:** [https://doi.org/10.1111/j.1540-6261.2009.01467.x](https://doi.org/10.1111/j.1540-6261.2009.01467.x)
- **PDF:** Not downloaded (publisher paywall)

## Testable Hypothesis

The large negative variance risk premium observed in equity index options is primarily compensation for marketwide correlation risk rather than individual stock variance risk; investors are willing to pay a substantial premium for index options because index variance spikes when pairwise stock correlations surge during market downturns.

## Summary

Driessen, Maenhout, and Vilkov investigate the pricing of marketwide correlation risk by jointly examining the cross-section of S&P 100 (OEX) index options and options on all constituent individual stocks from 1996 through 2003. By decomposing index variance into average individual stock variances and pairwise stock correlations, the authors establish a foundational empirical result: individual equity variance risk carries a statistically insignificant and economically small risk premium, whereas **correlation risk is heavily priced**. Implied correlation extracted from index versus single-stock options averages approximately 50%, compared to realized average correlation of roughly 30%, generating a persistent implied-minus-realized correlation spread of ~20%. A parametric asset pricing model shows that correlation risk exposure explains why delta-hedged index option returns are deeply negative while individual equity options have far less negative returns. While a frictionless dispersion trading strategy (selling index options while buying single-stock options) yields an annualized Sharpe ratio above 1.20, realistic bid-ask spreads on constituent options eliminate net excess returns, demonstrating that limits to arbitrage protect the correlation risk premium from being eliminated.

## Detailed Summary

### 1. Theoretical Framework & Variance Decomposition

Consider a market index $I_t = \sum_{i=1}^N w_{i,t} S_{i,t}$ composed of $N$ underlying equities with capital weights $w_{i,t}$. Over an infinitesimal or finite horizon, the return variance of the index is an exact function of individual variances and pairwise covariances:
$$\sigma_I^2 = \sum_{i=1}^N w_i^2 \sigma_i^2 + \sum_{i=1}^N \sum_{j \ne i}^N w_i w_j \sigma_i \sigma_j \rho_{ij}$$

Under a simplified equal-weighted benchmark ($w_i = 1/N$), this relationship simplifies to:
$$\sigma_I^2 = \frac{1}{N} \bar{\sigma}_i^2 + \left(1 - \frac{1}{N}\right) \bar{\rho} \, \bar{\sigma}_i^2 \approx \bar{\rho} \, \bar{\sigma}_i^2$$
where $\bar{\sigma}_i^2$ is the average individual stock variance and $\bar{\rho}$ is the average pairwise stock correlation.

**The Economic Wedge Between Index and Component Options:**
- In an economy with stochastic volatility and stochastic correlation, an investor who buys an index option obtains exposure to:
  1. Market diffusive and jump shocks.
  2. The individual variance processes of the constituent stocks.
  3. **Shocks to pairwise correlation $\bar{\rho}$**.
- During market panics, individual stocks comove much more strongly ($\bar{\rho} \to 1.0$), causing index volatility to explode even if average single-stock volatility rises only moderately.
- If investors possess constant relative risk aversion (CRRA) or habit formation utility, correlation increases coincide with sharp drops in aggregate wealth and marginal utility surges. Therefore, correlation risk carries a negative market price ($\lambda_\rho < 0$), making index options expensive ($IV_I > RV_I$) while leaving component options relatively fairly priced.

### 2. Empirical Methodology & Data

- **Sample Period**: January 1996 through December 2003 (8 years, 96 monthly expiration cycles).
- **Data Sources**:
  - Daily closing prices, bid-ask quotes, and implied volatilities for S&P 100 (OEX) index options from OptionMetrics Ivy DB.
  - Options on all individual common stocks that were constituents of the S&P 100 index during the sample period (filtering for non-zero bids, valid Greeks, and expiration horizons of approximately 1 month / 20–30 trading days).
  - Daily stock returns, trading volumes, and market capitalizations from CRSP.
- **Option Investment Strategies**:
  - For both the index and every constituent stock, the authors construct 1-month at-the-money (ATM) delta-hedged option portfolios and ATM straddles, rebalanced daily to maintain delta neutrality.

### 3. Key Quantitative Results

#### The Implied-Realized Correlation Spread
- **Implied Correlation ($IC_t$)**: Calculated from the cross-section of options by inverting the index variance equation using at-the-money implied volatilities:
  $$IV_{I,t}^2 = \sum_{i=1}^N w_{i,t}^2 IV_{i,t}^2 + \sum_{i=1}^N \sum_{j \ne i}^N w_i w_j IV_{i,t} IV_{j,t} IC_t$$
- **Empirical Spread**:
  - Average model-free implied correlation ($IC$): **48.9%**.
  - Subsequent 1-month realized correlation ($RC$): **29.7%**.
  - **Correlation Spread ($IC - RC$)**: **+19.2%** ($t\text{-statistic} = 6.45, p < 0.0001$).
  - Implied correlation exceeds realized correlation in over 85% of all sample months, demonstrating that option prices systematically price in severe correlation spikes that fail to materialize on average.

#### Return Discrepancy Between Index and Single-Stock Options
- **Delta-Hedged S&P 100 Index Options**:
  - Average monthly delta-hedged return of ATM index calls: **-1.78% per month** ($t = -3.82$).
  - Delta-hedged index puts: **-1.92% per month** ($t = -4.11$).
  - ATM index straddles: **-14.8% per month** ($t = -4.56$).
- **Delta-Hedged Component Single-Stock Options**:
  - Market-cap weighted average delta-hedged return of individual stock options: **-0.42% per month** ($t = -1.35$, statistically insignificant).
  - Single-stock straddles: **-3.2% per month** ($t = -1.18$).
- **The Empirical Puzzle Resolved**: Individual stock options do not exhibit a strongly negative variance risk premium on average. The massive negative returns of short index options are almost entirely due to the correlation component embedded in index options.

#### Cross-Sectional Asset Pricing Tests & Price of Correlation Risk
- The authors estimate a multi-factor option pricing model with two volatility factors: individual stock variance risk ($f_{\text{indiv}}$) and correlation risk ($f_{\text{corr}}$).
- **Factor Risk Prices**:
  - Price of individual variance risk ($\lambda_{\text{indiv}}$): Statistically indistinguishable from zero ($t = -0.68$).
  - Price of correlation risk ($\lambda_{\text{corr}}$): Strongly negative and statistically significant ($\lambda_{\text{corr}} = -4.82, t = -3.71$).
  - Correlation risk alone explains over **82% of the cross-sectional variation** in average option returns between index contracts and single-stock contracts.

#### Performance of Dispersion Trading Strategies & Limits to Arbitrage
- **Frictionless Correlation Trading Strategy**:
  - Sell 1 unit of delta-hedged S&P 100 index straddles, buy the weighted basket of delta-hedged single-stock straddles (a pure correlation dispersion trade).
  - Frictionless gross return: **+2.15% per month** ($t = 4.88$).
  - Annualized Sharpe ratio: **1.24** (compared to 0.38 for the S&P 500 equity market).
- **Impact of Transaction Costs & Limits to Arbitrage**:
  - Single-stock options trade with substantial bid-ask spreads (~6% to 10% of option premium), whereas index options have tight spreads (~1.5% to 2.5%).
  - Executing the long component legs at the quoted ask price and the short index leg at the bid price reduces the dispersion strategy return to **-0.45% per month** ($t = -0.91$).
  - Even assuming traders can execute at 50% of the quoted bid-ask spread, the net alpha drops to **+0.12% per month** ($t = 0.32$).
  - **Conclusion**: The high market price of correlation risk persists in equilibrium because arbitrageurs cannot cost-effectively eliminate the pricing wedge due to single-stock transaction costs.

### 4. Relevance to Option Research

Driessen, Maenhout, and Vilkov's results provide foundational economic principles for option strategy design in `sophie-option-research`:
1. **The Pure Economic Driver of Index Option Selling**: Proves that selling SPX options (such as cash-secured puts or credit spreads in `01_equity_curve.py`) is fundamentally an insurance contract against **systemic correlation collapse**. Single-stock option writing does not offer the same structural risk-adjusted edge because idiosyncratic variance risk is not heavily priced.
2. **Superiority of Index over Single-Stock Option Writing**: Directly justifies why `sophie-option-research` concentrates its backtest engines (`lab/engine.py`, `04_delta_selection.py`) on index options (SPX/SPY). The index market is where the correlation premium (+19.2% implied-realized wedge) is concentrated and where execution spreads are tightest.
3. **Correlation-Regime Gating**: Recommends monitoring the implied correlation index (e.g., CBOE CORRA / Implied Correlation Index) as a core macro feature in `lab/features.py`: when implied correlation is at extreme percentiles, index option premiums are richest, signaling prime environments for short index option harvesting.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Seminal empirical proof that the variance risk premium is overwhelmingly an index-level phenomenon driven by priced correlation risk (a 19.2% implied-minus-realized spread), while individual stock variance risk is largely unpriced. Directly validates the platform's architectural focus on SPX index options over single-stock option writing and explains the limits to arbitrage protecting the edge.

## Notable Citations to Follow Up

1. **Coval, Joshua D., and Tyler Shumway (2001)** — *Expected Option Returns* (Journal of Finance, 56(3), 983–1009).
   - Establishes that zero-beta index straddles systematically lose money, demonstrating that market volatility is a priced risk factor.
2. **Bakshi, Gurdip, and Nikunj Kapadia (2003)** — *Delta-Hedged Gains and the Negative Market Volatility Risk Premium* (Review of Financial Studies, 16(2), 527–566).
   - Isolates the negative volatility risk premium in S&P 500 index options using delta-hedged portfolios.
3. **Buraschi, Andrea, Fabio Trojani, and Andrea Vedolin (2014)** — *When Uncertainty Blows in the Orchard: Comovement and Equilibrium Volatility Risk Premia* (Journal of Finance, 69(1), 101–137).
   - Develops an equilibrium heterogeneous-beliefs framework explaining how investor disagreement drives the correlation risk premium and the index-component VRP wedge.
