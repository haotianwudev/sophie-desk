---
title: "The Puzzle of Index Option Returns"
authors: "George M. Constantinides, Jens C. Jackwerth, Alexi Savov"
year: 2013
link: "https://doi.org/10.1093/raps/rat004"
area: option-returns-anomaly
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The Puzzle of Index Option Returns

- **Authors:** George M. Constantinides, Jens C. Jackwerth, Alexi Savov
- **Year:** 2013 (Review of Asset Pricing Studies 3(2), 229–257; working paper 2009)
- **Link:** [https://doi.org/10.1093/raps/rat004](https://doi.org/10.1093/raps/rat004)
- **PDF:** `constantinides-jackwerth-savov-2013-puzzle-index-option-returns.pdf` (open-access copy, author site NYU Stern)

## Testable Hypothesis

Standard linear factor models and multi-factor equilibrium asset pricing models with factor risk premia estimated from the equity cross-section cannot explain the cross-sectional risk and return profile of S&P 500 index options across strikes and maturities; resolving the option returns puzzle requires crisis-related jump or volatility factors whose prices of risk are segmented and priced substantially higher in options markets than in equity markets.

## Summary

Resolves a severe methodological roadblock in empirical derivatives pricing and documents the fundamental segmentation between equity and option markets. Raw option returns exhibit extreme leverage, non-linearities, and violent skewness, causing linear pricing tests to fail or produce deceptively large $p$-values despite huge pricing errors (e.g. monthly RMS errors of 12%). Constantinides, Jackwerth, and Savov introduce an innovative panel of 54 leverage-adjusted option portfolios (27 call and 27 put portfolios spanning 30, 60, and 90 days and 9 moneyness levels), daily rebalanced to a target market beta of 1.0 by combining options with risk-free lending/borrowing. This construction normalizes return distributions, allowing rigorous linear factor tests. They show that standard equity models (CAPM, Fama-French 3-factor, Carhart 4-factor) fail completely: out-of-the-money puts display massive unexplained annualized alphas (exceeding 20% to 40% for option sellers). Introducing crisis-related factors (price jumps, volatility jumps, or liquidity) prices the option cross-section accurately, but only if factor premia are estimated from options rather than stocks, proving that options markets charge an independent, highly elevated premium for tail risk.

## Detailed Summary

### 1. Econometric Methodology & Leverage-Adjusted Portfolios

Testing multi-factor asset pricing models on raw option returns is plagued by econometric distortion:
1. **Extreme Non-Linearity & Skewness:** A 30-day out-of-the-money put has an effective leverage (elasticity $\Omega = \frac{\partial P}{\partial S}\frac{S}{P}$) between $-20$ and $-50$. In calm months, the option expires worthless ($-100\%$ return); in market crashes, it earns $+1,000\%$ to $+5,000\%$. The resulting monthly return distribution exhibits massive skewness ($\sim 15$) and kurtosis ($\sim 300$).
2. **Spurious Statistical Non-Rejection:** In raw option regressions, the colossal variance of the residuals inflates standard errors so drastically that a monthly root-mean-squared (RMS) pricing error of 12% cannot be rejected ($p$-values of 32%–34%).

**The Leverage-Adjustment Innovation:**
The authors construct a panel of 54 option portfolios rebalanced daily:
- 27 call portfolios and 27 put portfolios.
- 3 target maturities: $\tau \in \{30, 60, 90\}$ calendar days.
- 9 target moneyness bins: $K/S \in \{0.90, 0.925, 0.95, 0.975, 1.00, 1.025, 1.05, 1.075, 1.10\}$.

To neutralize leverage and eliminate mechanical option convexity, each portfolio invests in the target option and borrows or lends at the risk-free rate so that the portfolio's implied elasticity with respect to the index is identically equal to **1.0**:
$$w_{i, t} = \frac{1}{\Omega_{i, t}} = \frac{O_{i, t}}{\Delta_{i, t} S_t}$$
where $O_{i, t}$ is the option price, $\Delta_{i, t}$ is the Black-Scholes delta, and $w_{i, t}$ is the fraction of portfolio wealth allocated to the option, with $1 - w_{i, t}$ held in risk-free borrowing/lending.

Because each portfolio maintains unit market beta ($\beta = 1.0$), its monthly return distribution has variance, skewness, and kurtosis comparable to the underlying S&P 500 index itself (skewness $\in [-0.5, 0.2]$), satisfying classical Gauss-Markov and GMM regularity conditions.

### 2. Empirical Data & Sample Period

- **Sample Period:** April 1986 to January 2012 (26 full years, 309 monthly observation periods).
- **Data Sources:** 
  - 1986–1995: Berkeley Options Database (CBOE trade-by-trade and bid-ask quote records).
  - 1996–2012: OptionMetrics IvyDB (end-of-day quotes and Greeks).
  - High-frequency filtering: End-of-day quotes selected from the minute between 3:00 PM and 4:00 PM CST with the maximum simultaneous call and put quote liquidity to avoid non-synchronous closing noise.
  - Risk-free benchmark: Implied interest rate extracted from synthetic European forward conversions (put-call parity midpoints).
- **Factor Universes Tested:**
  1. Equity-derived factors: S&P 500 excess return, Fama-French 25 size/value portfolios, SMB, HML, and UMD (momentum).
  2. Option-derived crisis factors: Market excess return, VIX innovations ($\Delta \text{VIX}$ representing volatility jumps), squared index returns (capturing price jumps and non-linear quadratic variation), and Pastor-Stambaugh liquidity innovations.

### 3. Key Quantitative Results

#### Overwhelming Rejection of the Single-Factor CAPM
- Across the 54 beta-adjusted portfolios, testing the single-factor market model yields:
  - **Overwhelming Rejection:** Chi-square test statistic $p < 0.0001$.
  - **Large Pricing Errors:** Monthly Root Mean Squared (RMS) error of **1.34% per month for calls** and **1.08% per month for puts** (annualized pricing errors of 13%–16%).
  - **Monotonic Strike Alpha Pattern:** Unadjusted CAPM alphas for beta-adjusted options display a stark, monotonic trajectory across moneyness:
    - 30-day deep OTM calls ($K/S = 1.10$): Alphas are positive ($+1.85\%$/month, $t = 3.3$).
    - 30-day deep OTM puts ($K/S = 0.90$): Long alphas are **severely negative at $-1.89\%$ per month** ($t = -3.8$, annualized alpha of **$-22.7\%$**).
    - For raw un-levered OTM puts, this corresponds to an annualized short-put alpha exceeding **$+35\%$ to $+50\%$**.

#### Failure of Fama-French and Standard Equity Multi-Factor Models
- Adding SMB, HML, and momentum does not resolve the puzzle:
  - Factor risk premia estimated from equity portfolios (25 Fama-French portfolios) yield monthly RMS errors of **1.26% on options**.
  - Standard equities are not exposed to the severe discontinuous jump and volatility-of-volatility risks that dominate option pricing. Equity-derived factor risk premia underprice the true market price of variance risk by a factor of **3 to 5**.

#### Successful Resolution via Crisis-Related Factors (Table 4 & Table 5)
- When multi-factor models include a crisis-related factor and factor premia are estimated directly from the **option universe**:
  1. **Market + S&P 500 Return-Squared ($\Delta S^2$):** RMS pricing error collapses from $1.34\%$ down to **$0.24\%$ per month** for calls and **$0.29\%$** for puts.
  2. **Market + VIX Innovations ($\Delta \text{VIX}$):** RMS pricing error drops to **$0.28\%$ per month**.
  3. **Alpha Elimination:** The CAPM alphas of short-maturity out-of-the-money puts shrink to statistically and economically negligible levels (falling from $-1.89\%$/month to $-0.09\%$/month, $t = -0.4$).
- **The Segmentation Conclusion:** The pricing kernel required to price index options is significantly more volatile and sensitive to market distress than the pricing kernel that prices individual equities. Options markets constitute a partially segmented market where investors pay an exorbitant premium to insure against joint price and volatility shocks.

### 4. Relevance to Option Research

In `sophie-option-research`:
1. **Normalization of Backtest Returns:** Validates the leverage-adjusted portfolio methodology for analyzing option strategies. Raw percentage returns on short puts distort Sharpe ratios and drawdown metrics; normalizing by delta/elasticity (as in `lab/features.py`) provides a stationary return series suitable for factor attribution.
2. **Economic Justification for Put Selling Alpha:** Documents that the alpha earned by systematic put-selling strategies is the direct compensation for bearing market-wide jump and volatility shocks that are systematically unhedged in the broader equity market.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational empirical study proving that standard equity asset pricing models fail to price index options, and demonstrating that the outsized returns of short out-of-the-money put writing reflect a segmented market premium for bearing tail and volatility jumps. Introduces the leverage-adjustment framework for testing option strategy returns without econometric distortion.

## Notable Citations to Follow Up

1. **Coval, Joshua D., and Tyler Shumway (2001)** — *Expected Option Returns* (Journal of Finance, 56(3), 983–1009).
   - Establishes that option returns cannot be explained by standard market betas and documents that zero-beta straddles lose significant money.
2. **Black, Fischer, and Myron Scholes (1973)** — *The Pricing of Options and Corporate Liabilities* (Journal of Political Economy, 81(3), 637–654).
   - The foundational continuous-time option pricing framework and elasticity definition.
3. **Pastor, Lubos, and Robert F. Stambaugh (2003)** — *Liquidity Risk and Expected Stock Returns* (Journal of Political Economy, 111(3), 642–685).
   - Defines the market-wide liquidity innovation factor evaluated as a candidate driver of option returns.
