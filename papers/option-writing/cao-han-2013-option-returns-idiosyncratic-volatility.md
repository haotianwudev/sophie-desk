---
title: "Cross Section of Option Returns and Idiosyncratic Stock Volatility"
authors: "Jie Cao, Bing Han"
year: 2013
link: "https://doi.org/10.1016/j.jfineco.2012.11.010"
area: option-returns-anomaly
relevance: Medium
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Cross Section of Option Returns and Idiosyncratic Stock Volatility

- **Authors:** Jie Cao, Bing Han
- **Year:** 2013 (Journal of Financial Economics 108(1), 231–249; SSRN Working Paper 1786607)
- **Link:** [https://doi.org/10.1016/j.jfineco.2012.11.010](https://doi.org/10.1016/j.jfineco.2012.11.010)
- **PDF:** `cao-han-2013-option-returns-idiosyncratic-volatility.pdf` (Open-access post-print from University of Toronto TSpace repository)

## Testable Hypothesis

Due to market imperfections, transaction costs, and inventory holding risks faced by capital-constrained option market makers, delta-hedged equity option returns decrease monotonically with the idiosyncratic volatility of the underlying stock; options written on high-idiosyncratic-volatility stocks are priced at a substantial premium, generating excess returns for option sellers that cannot be explained by standard systematic risk factors.

## Summary

Cao and Han provide an extensive empirical investigation into how firm-level idiosyncratic volatility affects the cross-section of equity option returns. Analyzing over 210,000 monthly delta-hedged option returns across approximately 6,000 underlying US equities between 1996 and 2008, the authors uncover a strong and robust negative relationship: delta-hedged option returns decline monotonically as the underlying stock's idiosyncratic volatility ($IVOL$) increases. Because delta-hedged option positions have negative returns on average (option buyers lose money to the volatility risk premium), selling delta-hedged options on high-IVOL stocks generates vastly higher returns than on low-IVOL stocks. A long-short zero-beta option strategy that sells delta-hedged calls on the highest IVOL quintile and buys delta-hedged calls on the lowest IVOL quintile earns **+1.40% per month** ($t = 6.64$), with a multi-factor risk-adjusted alpha of **+1.32% per month** ($t = 5.76$) after controlling for Fama-French factors, momentum, and systematic market volatility risk. The anomaly is shown to be driven by limits to arbitrage and intermediary constraints: dealers charge a steep premium to supply options on high-IVOL stocks because hedging their residual inventory is costly and risky.

## Detailed Summary

### 1. Theoretical Motivation & Limits of Arbitrage in Option Markets

Classical option pricing theory posits that in frictionless, complete markets with continuous trading, options are redundant securities dynamically replicated by the underlying stock and a riskless bond (Black & Scholes 1973; Merton 1973). Under no-arbitrage, idiosyncratic volatility should not command any premium because market makers can fully delta-hedge away directional price movements.

However, real-world option markets operate under severe market imperfections (Figlewski 1989; Garleanu, Pedersen, and Poteshman 2009):
1. **Discrete Rebalancing & Basis Risk**: Market makers cannot hedge continuously and face execution frictions, gamma risk, and jump risk.
2. **Holding Costs & Capital Constraints**: As formalized by Pontiff (1996, 2006) and Shleifer and Vishny (1997), idiosyncratic volatility serves as the single largest cost of arbitrage because arbitrageurs cannot diversify away unhedgeable tracking error in concentrated dealer inventories.
3. **End-User Buying Pressure & Intermediary Markup**: Retail and institutional investors actively buy options on volatile, speculative single stocks (for embedded leverage and lottery payoffs). Because market makers are risk-averse and capital-constrained, they require compensation for taking the other side of these trades. Consequently, dealers set option implied volatilities well above expected volatility for high-IVOL stocks, making those options expensive and depressing subsequent delta-hedged buyer returns.

### 2. Empirical Methodology & Data

- **Sample Period**: January 1996 through December 2008 (156 months).
- **Options Data**:
  - All listed US equity options from OptionMetrics Ivy DB.
  - Options selected closest to at-the-money ($0.95 \le S/K \le 1.05$) with approximately 45 days (1.5 months) to expiration.
  - Final sample comprises **211,812 individual delta-hedged call option returns** and **207,635 delta-hedged put option returns** covering 6,000 distinct underlying stocks.
- **Delta-Hedged Return Calculation**:
  - At inception $t$, buy one option contract ($C_t$) and short $\Delta_t$ shares of the underlying stock ($S_t$). The daily-rebalanced delta-hedged gain accumulated to maturity $t+\tau$ is:
    $$\Pi_{t, t+\tau} = C_{t+\tau} - C_t - \sum_{k=0}^{\tau-1} \Delta_{t+k} (S_{t+k+1} - S_{t+k}) - \sum_{k=0}^{\tau-1} r_{t+k} (C_{t+k} - \Delta_{t+k} S_{t+k})$$
  - The percentage delta-hedged return is scaled by the net initial investment: $R_{t, t+\tau}^{\Delta} = \Pi_{t, t+\tau} / (\Delta_t S_t - C_t)$.
- **Idiosyncratic Volatility ($IVOL$) Definition**:
  - Estimated each month by regressing daily stock returns over the prior month on the Fama-French three-factor model:
    $$R_{i,d} - r_{f,d} = \alpha_i + \beta_{i,MKT} MKT_d + \beta_{i,SMB} SMB_d + \beta_{i,HML} HML_d + \epsilon_{i,d}$$
  - $IVOL_i = \sqrt{\frac{1}{D-3} \sum_{d=1}^D \epsilon_{i,d}^2}$, annualized. Systematic volatility ($SVOL_i$) is the standard deviation of the fitted regression return.

### 3. Key Quantitative Results

#### Delta-Hedged Option Returns Across IVOL Quintiles (Table 8)
- Delta-hedged option returns are unconditionally negative across all quintiles, but losses deepen dramatically as IVOL increases:
  - **Quintile 1 (Lowest IVOL)**: Average monthly return of delta-hedged calls is **-0.45%**.
  - **Quintile 2**: Average return is **-0.62%**.
  - **Quintile 3**: Average return is **-0.89%**.
  - **Quintile 4**: Average return is **-1.28%**.
  - **Quintile 5 (Highest IVOL)**: Average return is **-1.85%**.
- **Selling Delta-Hedged Calls (Short Quintile Strategy)**:
  - Shorting delta-hedged calls on Quintile 5 earns **+1.85% per month**.
  - Shorting delta-hedged calls on Quintile 1 earns **+0.45% per month**.
  - **Quintile 5 - Quintile 1 Spread Portfolio Return**: **+1.40% per month** ($t = 6.64, p < 0.0001$).
  - For put options (Table 7 Panel B), the 5-1 spread return is equally strong at **+1.28% per month** ($t = 5.92$).

#### Decoupling Idiosyncratic from Systematic Volatility (Table 8 Panels D & E)
- In two-way independent and conditional sorts:
  - Controlling for systematic volatility ($SVOL$), the negative relation between delta-hedged return and $IVOL$ remains highly significant across all SVOL tiers, with the 5-1 spread ranging from **+0.82% per month** (low SVOL) to **+2.07% per month** (high SVOL).
  - Conversely, after controlling for $IVOL$, the relation between delta-hedged returns and systematic volatility is mildly *positive* ($\beta > 0$), confirming that the pricing anomaly is uniquely driven by firm-specific, unhedgeable risk.

#### Asset Pricing Alphas and Factor Regressions (Table 9)
- Regressing monthly spread returns (Short Q5 / Long Q1 delta-hedged calls) on multi-factor benchmarks:
  - **CAPM Alpha**: **+1.42% per month** ($t = 6.78$).
  - **Fama-French 3-Factor Alpha**: **+1.35% per month** ($t = 6.12$).
  - **Carhart 4-Factor Alpha**: **+1.28% per month** ($t = 5.65$).
  - **Controlling for Systematic Volatility Factors**:
    - Adding the S&P 500 zero-beta straddle factor, CBOE $\Delta VIX$, and the Driessen-Maenhout-Vilkov common individual stock variance risk factor leaves an unexplained abnormal alpha of **+1.32% per month** ($t = 5.76$).
  - This establishes that the excess profitability of selling options on high-IVOL stocks is orthogonal to aggregate volatility risk premia and macroeconomic factors.

#### Limits to Arbitrage & Intermediary Constraints (Table 10)
- **Impact of Bid-Ask Spreads**:
  - At mid-quote execution (zero effective spread), monthly strategy return is +1.40%.
  - Charging 10% of quoted bid-ask spread: return is **+1.16%** ($t = 5.21$).
  - Charging 25% of quoted bid-ask spread: return is **+0.79%** ($t = 3.35$).
  - At 50% of quoted spread (half-spread), return declines to **+0.17%** ($t = 0.68$, statistically insignificant).
  - This proves that high execution friction and bid-ask spreads act as an effective barrier to arbitrage, preventing outside hedge funds and retail traders from exploiting the dealer markup.
- **Cross-Sectional Arbitrage Proxies**:
  - The negative relation between option returns and IVOL is concentrated among illiquid stocks (Amihud illiquidity), low-priced stocks ($< \$10$), stocks with low institutional ownership, and firms with high analyst forecast dispersion. Controlling for these limits-to-arbitrage variables reduces the coefficient magnitude of IVOL by **approximately 40%**.

### 4. Relevance to Option Research

Cao and Han's findings deliver critical architectural and risk-management principles for `sophie-option-research`:
1. **Understanding the Limits of Delta Hedging in Single Stocks**: Explains why short-volatility strategies applied to individual stocks cannot be hedged using simple linear delta-neutral models without incurring massive unhedgeable holding costs and bid-ask friction.
2. **Dealer Inventory Premium as Source of Edge**: Confirms that market-maker compensation for holding unhedgeable risk ($\Delta S - C$) is a structural source of option-selling alpha. In index options (SPX), where market-makers hold aggregate inventory risk, an analogous mechanism drives the index VRP.
3. **Screening & Selection Filters in `lab/features.py`**: If single-stock overwriting or dispersion trading is evaluated, idiosyncratic volatility must be a core selection feature: selling rich options on high-IVOL equities provides significantly wider volatility cushions, provided transaction costs are tightly controlled.

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** High-quality empirical documentation proving that delta-hedged option returns decline with the underlying stock's idiosyncratic volatility (generating a 1.4%/month short-volatility spread) due to dealer inventory costs and limits to arbitrage. Highly relevant for equity dispersion and single-stock option overwriting, though secondary to the index-level SPX put-writing architecture in `sophie-option-research`.

## Notable Citations to Follow Up

1. **Garleanu, Nicolae, Lasse Heje Pedersen, and Allen M. Poteshman (2009)** — *Demand-Based Option Pricing* (Review of Financial Studies, 22(10), 4259–4299).
   - Foundational model showing how end-user net demand pressure combined with dealer inventory risk and costly replication dictates option implied volatility surfaces.
2. **Pontiff, Jeffrey (2006)** — *Costly Arbitrage and Idiosyncratic Risk* (Journal of Finance, 61(1), 35–55).
   - Establishes that idiosyncratic risk is the single largest cost faced by arbitrageurs, explaining the persistence of asset pricing anomalies across financial markets.
3. **Goyal, Amit, and Alessio Saretto (2009)** — *Cross-Section of Option Returns and Volatility* (Journal of Financial Economics, 94(2), 310–326).
   - Documents large excess returns from sorting single-stock options on historical-versus-implied volatility spreads.
