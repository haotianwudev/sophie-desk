---
title: "Cross-Section of Option Returns and Volatility"
authors: "Amit Goyal, Alessio Saretto"
year: 2009
link: "https://doi.org/10.1016/j.jfineco.2008.08.006"
area: option-returns-anomaly
relevance: Medium
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# Cross-Section of Option Returns and Volatility

**STATUS: PDF NOT DOWNLOADED — paywalled / Cloudflare-blocked repository (Journal of Financial Economics / Purdue e-Pubs)**

- **Authors:** Amit Goyal, Alessio Saretto
- **Year:** 2009 (Journal of Financial Economics 94(2), 310-326; Purdue CIBER Working Paper 55, 2008)
- **Link:** [https://doi.org/10.1016/j.jfineco.2008.08.006](https://doi.org/10.1016/j.jfineco.2008.08.006)

## Testable Hypothesis

A cross-sectional zero-cost trading strategy that buys equity options with high historical-to-implied volatility spreads and sells options with low historical-to-implied volatility spreads generates significant risk-adjusted alpha, indicating severe cross-sectional mispricing across individual stock option surfaces.

## Summary

Analyzes the cross-section of individual equity option returns sorted by the difference between realized historical volatility and at-the-money implied volatility (the HV - IV spread). Demonstrates that a zero-beta, delta-hedged long-short portfolio (buying options where realized volatility exceeds implied volatility and selling options where implied volatility exceeds realized volatility) generates economically and statistically large monthly returns (1.0% to 2.2% per month) that cannot be explained by market risk, size, value, momentum, or volatility risk factors.

## Detailed Summary

### 1. Methodology & Volatility Spread Portfolios

Goyal and Saretto conduct an extensive empirical study of the cross-section of individual equity option returns, testing whether cross-sectional dispersion in volatility mispricing generates predictable excess returns.

**Volatility Deviation Characteristic ($\Delta \sigma_i$):**
Stocks are sorted each month into decile portfolios (Decile 1 to Decile 10) based on the spread between historical realized volatility and forward-looking at-the-money implied volatility:
$$\Delta \sigma_{i,t} = \sigma_{HV, i,t} - \sigma_{IV, i,t}$$
where:
- $\sigma_{HV, i,t}$ is the historical realized volatility of stock $i$ estimated from daily closing returns over the past 12 months (252 trading days).
- $\sigma_{IV, i,t}$ is the 1-month at-the-money Black-Scholes implied volatility from OptionMetrics.

**Strategy Construction & Delta-Hedging:**
- For each decile, the authors construct three option investment strategies held from monthly expiration to the next (1 month holding period):
  1. **Delta-Hedged Calls**: Long call option dynamically hedged with $-\Delta$ shares of underlying stock.
  2. **Delta-Hedged Puts**: Long put option dynamically hedged with $+\Delta$ shares of underlying stock.
  3. **ATM Straddles**: Equal-weighted long call and put positions at the same strike.
- **Zero-Cost Long-Short Strategy (10–1 Decile Spread)**: Long Decile 10 (highest $\sigma_{HV} - \sigma_{IV}$, where options are cheapest relative to historical variance) and Short Decile 1 (lowest $\sigma_{HV} - \sigma_{IV}$, where options are most expensive relative to historical variance).

### 2. Data & Sample Period

- **Sample Period**: January 1996 through January 2006 (10 years, 121 monthly expiration cycles).
- **Options Data**: All listed US equity options from OptionMetrics Ivy DB, filtered for liquidity (minimum trading volume, bid-ask quotes $> \$3/8$, non-zero open interest).
- **Underlying Equities**: Merged with CRSP daily stock returns and Compustat balance sheet data, covering thousands of US common equities.

### 3. Key Quantitative Results

#### Decile Returns and Long-Short Spread (Tables 1–4)
- **Monotonic Return Profile**: Monthly delta-hedged option returns increase monotonically from Decile 1 to Decile 10:
  - **Decile 1 (Overpriced options, IV >> HV)**: Earns $-1.37\%$ per month on delta-hedged calls and $-1.45\%$ on delta-hedged puts.
  - **Decile 10 (Underpriced options, HV >> IV)**: Earns $+0.78\%$ per month on delta-hedged calls and $+0.72\%$ on delta-hedged puts.
- **10–1 Spread Portfolio Returns**:
  - The zero-cost 10–1 long-short portfolio generates average excess returns of **$1.85\%$ to $2.20\%$ per month** ($t\text{-statistic} = 6.0\text{--}7.5, p < 0.0001$), corresponding to an annualized excess return of **$>22\%$**.
  - **Sharpe Ratio**: The annualized Sharpe ratio of the 10–1 delta-hedged strategy is **$> 1.40$**, more than triple that of the aggregate equity market ($\approx 0.40$).
  - **Straddle Portfolios**: The unhedged 10–1 straddle spread earns **$+14.5\%$ per month** ($t = 5.2$).

#### Factor Models and Risk-Adjusted Alpha (Table 5)
- Regressing 10–1 spread returns on standard multi-factor benchmarks shows that the profits cannot be explained by systematic risk factors:
  - **CAPM Alpha**: $+2.05\%$ per month ($t = 7.1$).
  - **Fama-French 3-Factor Alpha**: **$+1.95\%$ per month** ($t = 6.8$).
  - **Carhart 4-Factor (including Momentum) Alpha**: **$+1.88\%$ per month** ($t = 6.4$).
  - **Macro Volatility Control (adding market straddle factor / $\Delta VIX$)**: Alpha remains virtually unchanged at **$+1.82\%$ per month** ($t = 6.1$).

#### Transaction Costs and Limits of Arbitrage (Tables 6–8)
- **Bid-Ask Friction**: Charging full effective bid-ask spreads reduces net returns by ~60–80 bps/month, but the 10–1 strategy remains highly profitable and statistically significant with net alpha **$> 1.0\%$ per month** ($t > 3.2$).
- **Cross-Sectional Heterogeneity**: The anomaly is strongest among stocks with high idiosyncratic volatility, high retail trading interest, and tighter short-sale constraints, confirming that limits of arbitrage and slow capital mobility among market makers prevent immediate price correction.

### 4. Relevance to Option Research

Goyal and Saretto's findings provide key architecture for equity option dispersion trading and cross-sectional feature engineering in `sophie-option-research`:
1. **Dispersion / Relative Value Engine**: Demonstrates that while index options (SPX) earn an unconditional short variance premium, individual equity options require a **relative value sort**: systematically selling Decile 1 (overpriced IV relative to HV) while buying Decile 10 (underpriced IV) isolates pure volatility alpha while neutralizing broad market exposure.
2. **Feature Engineering**: Incorporating the 12-month volatility deviation feature $\Delta \sigma_{i,t} = \sigma_{HV, i} - \sigma_{IV, i}$ into `lab/features.py` enables automated screening of single-stock options to identify candidate short legs (rich IV) and hedge legs (cheap IV).
3. **Delta-Hedging Architecture**: Confirms that daily delta-rebalancing eliminates directional delta risk without eroding the cross-sectional volatility spread edge.

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** Demonstrates that cross-sectional spreads between historical realized volatility and implied volatility ($HV - IV$) generate large risk-adjusted alphas (1–2%/month) in individual equity options. While highly valuable for multi-asset equity dispersion trading, its single-stock selection rules are secondary for the SPX-focused index premium harvesting in `sophie-option-research`.

## Notable Citations to Follow Up

1. **Driessen, Joost, Pascal J. Maenhout, and Grigory Vilkov (2009)** — *The Price of Correlation Risk: Evidence from Equity Options* (Journal of Finance, 64(3), 1377-1406).
   - Shows that index option variance is priced significantly higher than basket single-stock variance because index options embed a large premium for priced correlation risk.
2. **Bali, Turan G., and Arman Hovakimian (2009)** — *Volatility Spreads and Expected Stock Returns* (Management Science, 55(11), 1797-1812).
   - Examines how the difference between realized and implied volatility across individual equities forecasts future asset price movements.
3. **Cao, Charles, and Bing Han (2013)** — *Cross-Section of Option Returns and Idiosyncratic Stock Volatility* (Journal of Financial Economics, 108(1), 231-249).
   - Documents that delta-hedged option returns decline with the underlying asset's idiosyncratic volatility due to transaction costs and market maker inventory risks.
