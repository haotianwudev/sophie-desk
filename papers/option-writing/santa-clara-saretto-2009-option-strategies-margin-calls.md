---
title: "Option Strategies: Good Deals and Margin Calls"
authors: "Pedro Santa-Clara, Alessio Saretto"
year: 2009
link: "https://www.nber.org/papers/w11693"
area: sizing-risk
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Option Strategies: Good Deals and Margin Calls

- **Authors:** Pedro Santa-Clara, Alessio Saretto
- **Year:** 2009
- **Link:** [https://www.nber.org/papers/w11693](https://www.nber.org/papers/w11693)
- **PDF:** `santa-clara-saretto-2009-option-strategies-margin-calls.pdf` (open-access copy)

## Testable Hypothesis

High apparent Sharpe ratios from short out-of-the-money index options are economically constrained by margin requirements and severe liquidation risk during tail drawdowns, limiting the capital that can arbitrage the volatility risk premium.

## Summary

Investigates the performance of S&P 500 option selling strategies accounting for margin requirements, transaction costs, and potential margin calls. Shows that while unconstrained option writing yields extraordinarily high Sharpe ratios, margin constraints and margin call liquidations during market crashes significantly reduce feasible leverage.

## Detailed Summary

### 1. Methodology & Trading Friction Framework

Santa-Clara and Saretto investigate whether the extraordinarily high Sharpe ratios documented for S&P 500 option-selling strategies represent genuine arbitrageable "good deals" or if they are constrained by real-world institutional trading frictions: bid-ask spreads, exchange margin requirements, and path-dependent margin call liquidations.

1. **Option Strategy Menu**:
   - Analyzes zero-cost naked options (calls and puts), covered calls, protective puts, straddles, strangles, and calendar time-value spreads across different moneyness levels (At-The-Money ATM, 5% OTM, 10% OTM) and maturities (Near: 1-month / 22 trading days; Far: 2-month / 44 trading days).
   - Positions are rebalanced monthly. Benchmark pricing models tested include the CAPM, Fama-French 3-factor model, and Leland (1999) non-linear higher-moment asset pricing model.
   - Evaluates investor utility under CRRA power utility ($\gamma = 5$) and tests disaster/jump-risk crash probability sensitivity.

2. **Margin Requirements & Intraday Margin Calls**:
   - Models the official exchange margin formula imposed by the CBOE for writing index options:
     $$M_t = \max\left(P_t + \alpha S_t - \max(S_t - K, 0), P_t + \beta K\right) \quad \text{for puts}$$
     $$M_t = \max\left(C_t + \alpha S_t - \max(K - S_t, 0), C_t + \beta S_t\right) \quad \text{for calls}$$
     where $\alpha = 15\%$ and $\beta = 10\%$ for CBOE margin rules, and $\alpha = 40\%, \beta = 35\%$ for typical retail brokers (e.g., E*Trade).
   - **Margin Haircut**: Defined as the ratio of required margin capital to initial option premium: $(M_t - V_0) / V_0$.
   - **Path-Dependent Margin Call Liquidation**: Simulates dynamic intraday/daily margin tracking during the month. If an adverse market move widens losses and triggers a margin call, the investor meets the call by partially liquidating market/cash assets. If collateral is exhausted, the broker forcibly liquidates the option position at current market prices, locking in peak-loss drawdowns (the "Victor Niederhoffer liquidation effect").

### 2. Data & Universe

- **Sample Period**: January 1985 – December 2002 (18 years / 216 monthly cycles).
- **Primary Data**: Daily settlement quotes for CME S&P 500 futures and futures options provided by the Institute for Financial Markets (IFM), spanning major stress regimes including the 1987 crash, the 1997 Asian crisis, the 1998 LTCM collapse, and the 2000–2002 tech bust.
- **Microstructure / Spreads Data**: OptionMetrics Ivy DB closing bid and ask quotes for CBOE European S&P 500 index options (`SPX`) from January 1996 through December 2002.
- **Risk-Free Asset**: 1-month U.S. Treasury bills.

### 3. Key Quantitative Results

#### Unconstrained Option Selling Returns & Apparent "Good Deals" (Table 3, Table 6)
- **High Theoretical Sharpe Ratios**:
  - Selling Near ATM Straddles (`Straddle N ATM`): Mean monthly return **+14.0%**, monthly standard deviation 51.5%, monthly Sharpe ratio **0.273** (annualized **0.95**).
  - Selling Near 5% OTM Strangles (`Strangle N 5%`): Mean monthly return **+39.8%**, monthly Sharpe **0.468** (annualized **1.62**).
  - Selling Near 10% OTM Strangles (`Strangle N 10%`): Mean monthly return **+52.7%**, monthly Sharpe **0.548** (annualized **1.90**).
  - Selling Near 10% OTM Puts (`Put N 10%`): Mean monthly return **+59.1%**, monthly Sharpe **0.358** (annualized **1.24**), with kurtosis of 140.1 due to October 1987.
- **Economic Significance & Jump Risk Robustness (Table 6, Table 8)**:
  - A power-utility investor ($\gamma = 5$) optimally allocates 5.6% of wealth to shorting near 10% OTM strangles, generating a certainty equivalent gain of **+1.90% per month**.
  - Jump risk calibration reveals that to justify these premia without mispricing, market crash frequency would need to be **2 to 3 times higher** than historically observed (even including the once-in-a-century 1987 crash).

#### Impact of Transaction Costs / Bid-Ask Spreads (Table 10)
- Comparing mid-point execution vs. full bid-to-ask execution (OptionMetrics 1996–2002):
  - *Short Near 10% OTM Put*: Mid-price monthly Sharpe 0.555 $\rightarrow$ Bid-to-ask Sharpe **0.425** (mean return drops from 57.1% to 50.2%).
  - *Short Near 10% OTM Strangle*: Mid-price Sharpe 1.232 $\rightarrow$ Bid-to-ask Sharpe **0.970** (mean drops from 55.7% to 47.9%).
  - *Short Far ATM Put*: Mid-price Sharpe 0.166 $\rightarrow$ Bid-to-ask Sharpe **0.070**.
  - *Short Far ATM Straddle*: Mid-price Sharpe +0.126 $\rightarrow$ Bid-to-ask Sharpe **-0.137** (spread costs completely destroy strategy profitability, flipping Sharpe negative).

#### Magnitude of Margin Haircuts (Table 11)
- Under exchange rules, required margin dwarfs option premia, severely constraining leverage:
  - *CBOE Margin ($\alpha=15\%, \beta=10\%$)*: Short Near ATM Put haircut averages **7.0x** premium (max 22.4x); Near 10% OTM Put haircut averages **43.1x** premium (max **370.0x**!). Near 10% OTM Call haircut averages **108.0x** (max 1,015.8x).
  - *Retail Broker Margin ($\alpha=40\%, \beta=35\%$)*: Short Near 10% OTM Put haircut averages **150.0x** premium (max **1,295.0x**). Near 10% OTM Call haircut averages **363.4x** (max 3,555.3x).

#### Impact of Margin Calls and Forced Liquidation (Table 12)
- When intra-month margin calls force position liquidations during severe market drawdowns:
  - **Short Near ATM Put**: Unconstrained monthly Sharpe **+0.355** $\rightarrow$ With margin calls: Sharpe turns **negative (-0.027)**; mean return collapses from +2.2%/mo to +0.3%/mo; Certainty Equivalent drops from +1.44% to **-0.65%**.
  - **Short Near 5% OTM Put**: Unconstrained Sharpe **+0.366** $\rightarrow$ Margin call Sharpe **-0.098**; CE drops from +1.20% to **-0.06%**.
  - **Short Near 10% OTM Put**: Unconstrained Sharpe **+0.352** $\rightarrow$ Margin call Sharpe **-0.239**; mean return falls to -0.3%/mo; CE drops from +1.03% to **-0.71%**.
  - **Short Near 10% OTM Strangle**: Unconstrained Sharpe **+0.551** $\rightarrow$ Margin call Sharpe **-0.306**; mean return collapses from +2.7%/mo to **-0.9%/mo**; CE drops from +1.90% to **-0.31%**.

### 4. Relevance to Option Research

In `sophie-option-research`, Santa-Clara and Saretto (2009) is the foundational empirical study on **margin constraints, leverage limits, and path-dependent liquidation risks**:
1. **Realistic Margin Requirement Modeling**: Provides the exact regulatory CBOE and broker margin equations ($M_t$) required in `src/lab/backtest.py` and `src/lab/sizing.py`. Assuming unconstrained leverage or simple 100% cash-secured margin produces severely misleading capacity and return estimates; realistic margin haircuts (7x–43x premium) must dictate capital allocation.
2. **Path-Dependent Liquidation & Stop-Loss Defense**: Proves that unmanaged option selling strategies fail not because of terminal settlement losses, but because of forced intraday margin call liquidations at market bottoms. This provides direct empirical justification for the discrete stop-loss (e.g., 200%/300% stop) and strike management rules tested in `src/lab/rolling.py` and `notebooks/08_rolling.ipynb` to prevent catastrophic broker close-outs.
3. **Execution Spread Penalties**: Validates the requirement in `src/lab/market_data.py` to backtest with explicit bid-ask spreads rather than mid-prices, especially when evaluating multi-leg strategies (straddles, strangles, spreads) where transaction friction consumes substantial fractions of theoretical edge.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational study on real-world execution frictions for systematic option sellers; demonstrates that high theoretical Sharpe ratios (1.5–1.9) collapse or turn negative once CBOE/broker margin haircuts (7x to 43x premium) and path-dependent margin call liquidations are enforced. Critical for calibrating realistic margin formulas, position sizing constraints, and stop-loss/roll defenses in `sophie-option-research`.

## Notable Citations to Follow Up

1. **Liu, Jun, and Francis A. Longstaff (2004)** — *Losing Money on Arbitrage: Optimal Dynamic Portfolio Choice in Markets with Arbitrage Opportunities* (Review of Financial Studies, 17(3), 611-641).
   - Models optimal trading under margin constraints and shows how finite liquidity and margin calls force premature liquidation of fundamentally profitable arbitrage trades.
2. **George, Thomas J., and Francis A. Longstaff (1993)** — *Bid-Ask Spreads and Trading Activity in the S&P 100 Index Option Market* (Journal of Financial and Quantitative Analysis, 28(3), 381-397).
   - Provides extensive empirical cross-sectional analysis of option bid-ask spreads across strike moneyness and maturities, essential for realistic transaction cost modeling.
3. **Leland, Hayne E. (1999)** — *Beyond Mean-Variance: Performance Measurement in a Nonsymmetrical World* (Financial Analysts Journal, 55(1), 27-36).
   - Derives generalized performance measures and risk-adjusted alphas tailored for non-normal, skewed, and option-like payoff distributions.
