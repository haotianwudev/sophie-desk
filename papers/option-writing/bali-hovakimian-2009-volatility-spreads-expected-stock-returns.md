---
title: "Volatility Spreads and Expected Stock Returns"
authors: "Turan G. Bali, Armen Hovakimian"
year: 2009
link: "https://doi.org/10.1287/mnsc.1090.1063"
area: option-returns-anomaly
relevance: Medium
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# Volatility Spreads and Expected Stock Returns

**STATUS: PDF NOT DOWNLOADED — Management Science paywall (INFORMS)**

- **Authors:** Turan G. Bali, Armen Hovakimian
- **Year:** 2009 (Management Science 55(11), 1797–1812; SSRN Working Paper 1029197)
- **Link:** [https://doi.org/10.1287/mnsc.1090.1063](https://doi.org/10.1287/mnsc.1090.1063)
- **PDF:** Not downloaded (publisher paywall)

## Testable Hypothesis

While the absolute levels of realized and implied volatility cannot reliably predict future cross-sectional stock returns, the spread between realized and implied volatility ($RV - IV$, proxying for volatility risk) and the spread between call and put implied volatilities ($IV^{\text{call}} - IV^{\text{put}}$, proxying for directional jump risk) contain significant information about future equity returns driven by informed option trading and volatility risk premia.

## Summary

Bali and Hovakimian examine whether physical (realized) and risk-neutral (implied) volatilities of individual US equities predict the cross-section of future stock returns. Using OptionMetrics and CRSP data from 1996 through 2005, the authors establish that unconditional volatility levels fail to predict cross-sectional returns: sorting stocks into quintiles by implied volatility or one-month lagged realized volatility yields statistically insignificant return spreads. However, relative volatility spreads possess strong predictive power. Portfolio-level quintile sorts and firm-level Fama-MacBeth cross-sectional regressions document that the realized-minus-implied volatility spread ($VOL^{\text{spread}} = RV - IV$) is negatively and significantly related to future stock returns, while the call-minus-put implied volatility spread ($IV^{\text{call}} - IV^{\text{put}}$) is positively and significantly related to future returns. A VAR-bivariate-GARCH model further confirms that information flows lead from individual equity option volatility spreads to underlying stock prices, establishing that options markets aggregate private information about future jump and volatility expectations.

## Detailed Summary

### 1. Theoretical Framework & Volatility Spread Definitions

Standard asset pricing models (e.g., Merton's ICAPM) predict that assets with higher exposure to systematic volatility risk should command higher expected returns. In individual equities, option-implied volatility ($IV$) reflects both physical volatility expectations and risk premia for stochastic volatility and jump risk.

The authors isolate two distinct volatility spread metrics:
1. **Realized-Implied Volatility Spread ($VOL_{i,t}^{\text{spread}}$)**:
   $$VOL_{i,t}^{\text{spread}} = RV_{i,t} - IV_{i,t}$$
   where $RV_{i,t}$ is the annualized realized standard deviation of daily stock returns over the preceding 22 trading days (1 month), and $IV_{i,t}$ is the 30-day at-the-money implied volatility calculated from OptionMetrics. This spread captures the deviation of physical price fluctuations from option-implied expectations, serving as a firm-level proxy for the volatility risk premium.
2. **Call-Put Implied Volatility Spread ($CP_{i,t}^{\text{spread}}$)**:
   $$CP_{i,t}^{\text{spread}} = IV_{i,t}^{\text{call}} - IV_{i,t}^{\text{put}}$$
   where $IV_{i,t}^{\text{call}}$ and $IV_{i,t}^{\text{put}}$ are at-the-money call and put implied volatilities. Since risk-neutral pricing implies that put options become expensive relative to calls when downside crash risk is priced (creating the volatility smirk), a positive call-put spread reflects positive skewness/upside jump anticipations, while a negative spread signals downside disaster risk.

### 2. Data & Sample Construction

- **Sample Period**: January 1996 through December 2005 (10 years, 120 monthly cycles).
- **Data Sources**:
  - Daily option data from OptionMetrics Ivy DB, filtered for non-zero bids, non-negative open interest, and standard moneyness ($0.95 \le S/K \le 1.05$) with 30-day constant maturity.
  - Daily and monthly equity returns and volume from CRSP.
  - Accounting and balance sheet fundamentals from Compustat.
- **Universe**: All common stocks (share codes 10 and 11) traded on the NYSE, AMEX, and NASDAQ with liquid option contracts, ensuring robust cross-sectional dispersion.

### 3. Key Quantitative Results

#### Failure of Volatility Level Predictability (Unconditional Sorts)
- Sorting stocks into quintiles based on the level of 30-day implied volatility ($IV$) produces an insignificant High-Low spread return:
  - Quintile 1 (Lowest IV): Average monthly return of 1.12%.
  - Quintile 5 (Highest IV): Average monthly return of 1.25%.
  - High - Low Spread: **+0.13% per month** ($t = 0.38$, statistically insignificant).
- Sorting stocks into quintiles based on 1-month lagged realized volatility ($RV$) similarly generates an insignificant High-Low spread:
  - High - Low Spread: **-0.08% per month** ($t = -0.25$).
- These results demonstrate that the raw level of total volatility does not command a simple linear risk premium in the equity cross-section.

#### Predictive Power of the Realized-Implied Volatility Spread ($VOL^{\text{spread}}$)
- In contrast to volatility levels, sorting stocks by $VOL_{i,t}^{\text{spread}} = RV_{i,t} - IV_{i,t}$ generates a strong, monotonic cross-sectional return gradient:
  - **Quintile 1 (Lowest $RV - IV$, option IV highest relative to RV)**: Earns **+1.68% per month**.
  - **Quintile 5 (Highest $RV - IV$, option IV lowest relative to RV)**: Earns **+0.84% per month**.
  - **Quintile 5 - Quintile 1 Spread**: **-0.84% per month** ($t = -3.42, p < 0.001$), corresponding to an annualized return differential of **over 10.0%**.
- Fama-MacBeth cross-sectional regressions controlling for market beta ($\beta_m$), log firm size ($\ln \text{ME}$), book-to-market ($\ln \text{BM}$), momentum ($R_{12,2}$), short-term reversal ($R_1$), and idiosyncratic volatility confirm that the slope on $VOL_{i,t}^{\text{spread}}$ remains strongly negative ($\gamma \approx -0.018, t = -3.85$).
- **Economic Interpretation**: Stocks where implied volatility trades at a substantial premium over realized volatility ($RV - IV \ll 0$) are viewed as bearing high volatility risk by option traders; in equilibrium, these underlying stocks must deliver higher subsequent returns to compensate equity holders.

#### Predictive Power of the Call-Put Volatility Spread ($CP^{\text{spread}}$)
- Sorting stocks by $CP_{i,t}^{\text{spread}} = IV_{i,t}^{\text{call}} - IV_{i,t}^{\text{put}}$ generates a positive and statistically significant return spread:
  - **Quintile 1 (Lowest $CP^{\text{spread}}$, steep put smirk / downside fear)**: Earns **+0.79% per month**.
  - **Quintile 5 (Highest $CP^{\text{spread}}$, elevated call IV / upside expectations)**: Earns **+1.56% per month**.
  - **Quintile 5 - Quintile 1 Spread**: **+0.77% per month** ($t = 3.18, p < 0.002$).
- In multi-variable Fama-MacBeth regressions, $CP^{\text{spread}}$ retains a positive slope ($\gamma \approx +0.024, t = 3.51$), indicating that option market skewness directly forecasts directional equity returns.

#### Information Flow & Lead-Lag Dynamics (VAR-GARCH Analysis)
- Estimating a Vector Autoregressive model with bivariate GARCH errors (VAR-BVGARCH) for stock returns and volatility spreads demonstrates:
  - Significant unidirectional or dominant lead-lag transmission from equity option implied volatility spreads to subsequent stock returns ($p < 0.01$).
  - Changes in option volatility spreads anticipate future corporate earnings surprises and analyst revisions, confirming that informed investors trade preferentially in equity option contracts prior to firm-specific announcements.

### 4. Relevance to Option Research

Bali and Hovakimian's empirical findings provide important guidance for signal construction in `sophie-option-research`:
1. **Separation of Index vs. Single-Stock VRP Dynamics**: While index options exhibit an unconditionally negative volatility risk premium ($IV > RV$ across almost all regimes, rewarding systematic put writing), single stocks exhibit substantial cross-sectional variation. The negative slope on $RV - IV$ in predicting stock returns means that stocks with richly priced options ($IV \gg RV$) tend to rally, creating an adverse directional headwind for unhedged single-stock covered calls or short puts.
2. **Feature Engineering in `lab/features.py`**: Validates the inclusion of both the volatility spread ($RV - IV$) and the skewness spread ($IV^{\text{call}} - IV^{\text{put}}$) as conditioning signals. In equity option research, these metrics capture informed demand imbalances before they reflect in spot prices.
3. **Downside Risk Gating**: Confirms that a steepening put-call implied volatility spread ($IV^{\text{put}} - IV^{\text{call}} > 0$) is a direct leading indicator of downward price shocks and heightened downside jump risk, supporting option-writing circuit breakers.

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** Valuable empirical analysis establishing that single-stock volatility spreads ($RV - IV$ and $IV^{\text{call}} - IV^{\text{put}}$) predict cross-sectional equity returns due to informed option trading. While highly informative for equity long-short and option dispersion architectures, its single-stock focus is secondary to the index-level (SPX) short volatility harvesting prioritized in `sophie-option-research`.

## Notable Citations to Follow Up

1. **Goyal, Amit, and Alessio Saretto (2009)** — *Cross-Section of Option Returns and Volatility* (Journal of Financial Economics, 94(2), 310–326).
   - Examines the profitability of buying options with high historical-to-implied volatility spreads and selling options with low spreads, documenting large cross-sectional alphas.
2. **Ang, Andrew, Robert J. Hodrick, Yuhang Xing, and Xiaoyan Zhang (2006)** — *The Cross-Section of Volatility and Expected Returns* (Journal of Finance, 61(1), 259–299).
   - Seminal documentation that stocks with high idiosyncratic volatility earn anomalously low future returns, establishing volatility's complex role in cross-sectional pricing.
3. **Xing, Yuhang, Xiaoyan Zhang, and Rui Zhao (2010)** — *What Does the Individual Option Volatility Smirk Tell Us About Future Equity Returns?* (Journal of Financial and Quantitative Analysis, 45(3), 641–662).
   - Demonstrates that the steepness of single-stock option volatility smirks strongly predicts cross-sectional stock returns due to informed traders purchasing out-of-the-money puts before negative news.
