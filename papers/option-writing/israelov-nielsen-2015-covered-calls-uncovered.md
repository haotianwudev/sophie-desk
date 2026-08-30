---
title: "Covered Calls Uncovered"
authors: "Roni Israelov, Lars N. Nielsen"
year: 2015
link: "https://ssrn.com/abstract=2444999"
area: covered-calls
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Covered Calls Uncovered

- **Authors:** Roni Israelov, Lars N. Nielsen
- **Year:** 2015
- **Link:** [https://ssrn.com/abstract=2444999](https://ssrn.com/abstract=2444999)
- **PDF:** `israelov-nielsen-2015-covered-calls-uncovered.pdf` (open-access copy)

## Testable Hypothesis

Decomposing and delta-hedging the embedded short equity-reversal exposure in standard covered calls isolates pure volatility risk premium harvesting and substantially boosts the strategy's Sharpe ratio.

## Summary

Deconstructs covered call returns into equity risk, volatility risk premium, and an uncompensated short equity-reversal bet. Proposes a risk-managed covered call strategy that strips out the reversal component to achieve higher Sharpe ratios and lower downside equity beta.

## Detailed Summary

### 1. Methodology & Return Decomposition

The authors present a performance attribution framework that deconstructs the excess return of a standard covered call strategy into three economically distinct risk exposures:

$$\text{Covered Call} = \text{Equity} - \text{Call}$$
$$\text{Covered Call} = \underbrace{(1 - \bar{\Delta}_c) \times \text{Equity}}_{\text{Passive Strategic Equity}} - \underbrace{(\text{Call} - \Delta_{c,t} \times \text{Equity})}_{\text{Short Volatility (Delta-Hedged)}} + \underbrace{(\bar{\Delta}_c - \Delta_{c,t}) \times \text{Equity}}_{\text{Dynamic Active Equity (Market Timing / Reversal)}}$$

1. **Passive Strategic Equity**: Represents the long-term target equity exposure (e.g., $1 - \bar{\Delta}_c = 0.50$ for an at-the-money strategy, or $0.70$ for a 2% OTM strategy). It earns the standard Equity Risk Premium (ERP).
2. **Short Volatility (Delta-Hedged Call)**: The return of a hypothetical daily delta-hedged short option position, capturing the pure Volatility Risk Premium (VRP)—compensation for underwriting financial insurance.
3. **Dynamic Active Equity (Equity-Reversal Exposure)**: A time-varying tactical equity bet arising from option convexity (gamma). As the underlying index declines, the short call's delta ($\Delta_{c,t}$) falls towards 0, increasing the net portfolio delta towards 1.0 (mechanically buying into weakness). As the index rallies, $\Delta_{c,t}$ rises towards 1.0, reducing net portfolio delta towards 0.0 (capping upside and selling into strength).

This dynamic equity timing behaves like a naive equity-reversal strategy. Over an option expiration cycle, portfolio delta disperses from its initial ~0.50 level toward 0 or 1, with an average absolute active exposure of 0.21. On the day prior to expiration, equity-timing risk is roughly equal in magnitude to passive equity risk. Under efficient markets, this path-dependent timing bet has an expected return of zero and generates uncompensated risk and downside asymmetry.

**The Risk-Managed Covered Call (Dynamic Delta-Hedging):**
The authors propose daily delta-hedging using S&P 500 index futures or ETFs to neutralize the active equity timing component ($\Delta_{c,t} - \bar{\Delta}_c$). By keeping net equity delta constant at its target level (0.50 for ATM, 0.70 for 2% OTM), the strategy eliminates the uncompensated reversal risk while continuing to harvest both the equity risk premium and volatility risk premium.

### 2. Data & Universe

- **Sample Period**: March 25, 1996 – December 31, 2014 (~19 years).
- **Universe & Data Sources**: S&P 500 Index (`SPX`), S&P 500 front-month call options from OptionMetrics and CBOE, and US 3-month LIBOR as the risk-free rate.
- **Strategies Examined**:
  - *CBOE S&P 500 BuyWrite Index (BXM)*: Long SPX, sell 1-month at-the-money (ATM) front-month call options on monthly expiration Fridays.
  - *CBOE S&P 500 2% OTM BuyWrite Index (BXY)*: Long SPX, sell 1-month 2% out-of-the-money (OTM) call options on monthly expiration Fridays.
- **Subperiods for Robustness**: 1996–2001 (Dot-com boom/bust), 2002–2008 (Expansion & GFC), and 2009–2014 (Post-crisis recovery).

### 3. Key Quantitative Results

#### Performance Decomposition of Traditional BuyWrite Strategies (Table 1 & Table 3)
- **ATM Covered Call (BXM-style)**:
  - *Total Strategy*: 5.9% excess return, 11.4% annualized volatility, 0.52 simple Sharpe ratio (0.37 geometric), skew –1.7, kurtosis 8.7.
  - *Passive Equity*: 3.5% excess return, 8.5% volatility, 0.41 Sharpe ratio (67% total risk contribution).
  - *Short Volatility*: 1.9% excess return, 1.9% volatility, **0.98 Sharpe ratio** (only 7% total risk contribution, 1.7% alpha to SPX).
  - *Equity Timing (Reversal Bet)*: 0.5% excess return, 4.8% volatility, **0.10 Sharpe ratio** (t-stat 0.4, statistically insignificant; **26% total risk contribution**, –0.0% alpha).
- **2% OTM Covered Call (BXY-style)**:
  - *Total Strategy*: 7.1% excess return, 13.3% volatility, 0.53 Sharpe ratio.
  - *Passive Equity*: 4.7% return, 11.4% vol, 0.41 Sharpe ratio (83% risk contribution).
  - *Short Volatility*: 1.8% return, 1.9% vol, 0.98 Sharpe ratio (5% risk contribution).
  - *Equity Timing*: 0.5% return, 4.0% vol, 0.13 Sharpe ratio (12% risk contribution).

#### Risk-Managed (Delta-Hedged) vs. Traditional BuyWrite (Table 6)
- **Sharpe Ratio Improvement**: For the ATM strategy (BXM), daily futures hedging of active delta improves the geometric Sharpe ratio from **0.37 to 0.52** by reducing annualized volatility from **11.4% to 9.2%** while slightly increasing geometric excess return from **4.2% to 4.8%** (5.1% simple). For BXY, hedging reduces volatility from 13.3% to 12.4% and raises the geometric Sharpe ratio from 0.41 to 0.46.
- **Downside Asymmetry Correction**: Traditional BXM exhibits heavy downside beta asymmetry (downside beta of 0.85 vs. upside beta of 0.46). Risk-managed hedging brings downside beta down from **0.85 to 0.60** (upside beta 0.49), significantly curbing drawdowns.
- **Tail Risk Reduction**: In hedged BXM, kurtosis drops from **7.6 to 4.2**, and negative skewness improves from **–1.6 to –1.1**.

#### Subperiod Robustness (Table 5)
Across all three market regimes (1996–2001, 2002–2008, 2009–2014), the short volatility component consistently delivered superior risk-adjusted returns (Sharpe ratios of 1.49, 0.40, and 1.39) while accounting for less than 10% of portfolio risk (9%, 6%, and 7%). Conversely, dynamic equity timing consistently introduced 23%–28% of the risk while yielding negligible Sharpe ratios (0.08, 0.18, and 0.04).

### 4. Relevance to Option Research

In option selling research (such as short puts, iron condors, and VRP harvesting in `sophie-option-research`), short put writing possesses the exact same structural exposure as a covered call via put-call parity ($\text{Cash-Secured Short Put} \equiv \text{Covered Call} - \text{Long Cash}$). Unhedged short puts inherently suffer from the same uncompensated negative gamma and dynamic equity-reversal exposure: downside market moves cause short put deltas to expand toward –1.0 (leveraging equity exposure at market bottoms), while market rallies diminish delta toward 0.0 (shedding equity exposure during runs), resulting in severe downside beta asymmetry and left-tail kurtosis.

This paper suggests several concrete, testable avenues for `sophie-option-research`:
1. **Delta-Hedged VRP Extraction**: Evaluating systematic futures delta-hedging (e.g., daily or delta-threshold rebalancing using SPY/MES/SPX futures) against the naked short put book to measure pure VRP Sharpe without directional equity reversal drag.
2. **Attribution Modeling**: Implementing a performance attribution module in `lab/report.py` / `lab/features.py` that separates strategy returns into passive equity beta, delta-hedged VRP/gamma P&L, and dynamic delta drift.
3. **Discrete Roll Rules vs. Continuous Hedging**: Benchmarking discrete mechanical adjustments (such as tastylive delta roll rules in `08_rolling.py` / `mgmt04`) against continuous/daily delta hedging to determine how much of the uncompensated reversal variance is mitigated by practical discrete strike management.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Crucial performance attribution framework for covered calls and short put strategies; proves that unhedged short options introduce uncompensated dynamic equity-reversal risk (~25% of strategy variance) due to negative gamma. Demonstrates that active delta management / roll rules isolate pure VRP (Sharpe ~1.0) while reducing downside beta from 0.85 to 0.60.

## Notable Citations to Follow Up

1. **Israelov, Roni, and Lars N. Nielsen (2014)** — *Covered Call Strategies: One Fact and Eight Myths* (Financial Analysts Journal, 70(6), 23-31).
   - Clarifies the economic mechanics of covered calls, debunking prevalent retail myths about downside protection and yield generation.
2. **Figelman, Igor (2008)** — *Expected Return and Risk of Covered Call Strategies* (Journal of Portfolio Management, 34(4), 81-97).
   - Provides an analytical model decomposing covered call returns into equity risk premia and net short call risk premia.
3. **Hill, Joanne M., Vasant Balasubramanian, Krag Gregory, and Ingrid Tierens (2006)** — *Finding Alpha via Covered Index Writing* (Financial Analysts Journal, 62(5), 29-46).
   - Evaluates the long-term risk-adjusted performance and alpha generation of systematic buy-write strategies across bull and bear regimes.
