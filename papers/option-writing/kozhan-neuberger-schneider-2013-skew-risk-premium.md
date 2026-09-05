---
title: "The Skew Risk Premium in the Equity Index Market"
authors: "Roman Kozhan, Anthony Neuberger, Paul Schneider"
year: 2013
link: "https://doi.org/10.1093/rfs/hht039"
area: tail-risk
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The Skew Risk Premium in the Equity Index Market

- **Authors:** Roman Kozhan, Anthony Neuberger, Paul Schneider
- **Year:** 2013 (*Review of Financial Studies*, 26(9), 2174–2203)
- **Link:** [https://doi.org/10.1093/rfs/hht039](https://doi.org/10.1093/rfs/hht039)
- **PDF:** `kozhan-neuberger-schneider-2013-skew-risk-premium.pdf` (Open-access manuscript via City Research Online)

## Testable Hypothesis

The steep implied volatility smirk observed in S&P 500 index options is not merely an expectation of negative physical return skewness or the leverage effect (negative return-volatility covariance); rather, nearly half of the implied skew is driven by an economically large and priced skew risk premium (SRP). Furthermore, the skew risk premium and variance risk premium (VRP) are driven by the same single underlying state variable/risk factor, meaning that a delta-hedged and variance-hedged skew swap earns zero excess returns.

## Summary

This paper develops a rigorous, model-free methodology for defining and replicating a "skew swap" using standard vanilla options and underlying forwards, analogous to how standard variance swaps replicate the second moment. By constructing model-free implied skew from option prices and comparing it against dynamically replicated realized skew over non-overlapping monthly horizons (January 1996 to January 2012 for S&P 500 options), the authors quantify the skew risk premium.

Key empirical discoveries include:
1. **Magnitude of the Skew Risk Premium:** The average implied skew is -1.808 (scaled by $(v^L)^{3/2}$), while the average realized skew is -1.001. The difference represents a large negative skew risk premium: a buyer of a skew swap experiences an average excess return of -42.09% (median -68.20%). The skew risk premium accounts for approximately 45% (almost half) of the total implied volatility skew.
2. **Single Risk Factor Driving Skew and Variance Premia:** Skew swap excess returns and variance swap excess returns are exceptionally correlated ($ho = 0.897$). In joint regression systems (SUR and Three-Stage Least Squares), regressing skew swap returns on variance swap returns and market returns yields an intercept of zero ($lpha = -0.002$, $t = -0.06$). Symmetrically, regressing variance swap returns on skew swap returns and the market yields an intercept of zero ($lpha = -0.002$, $t = -0.11$). Once variance risk is hedged out, skew risk earns zero alpha, proving that VRP and SRP are different manifestations of the exact same priced risk factor (jump/tail risk).
3. **Crucial Role of Dynamic Rebalancing:** The clean economic equivalence between skew and variance premia holds strictly when the replicating portfolios are rebalanced dynamically (daily). Unhedged static buy-and-hold option strategies introduce substantial higher-order truncation and delta/gamma mismatch errors that artificially depress correlation to 0.311 and create spurious nonzero alphas.

## Key Takeaways for Option Writing

1. **Option Writing Captures Tail Risk, Not Distinct "Skew Risk":** Selling out-of-the-money puts harvests both the variance risk premium and the skew risk premium. However, quantitative desks should not treat VRP and SRP as independent sources of diversification. They are driven by the same underlying tail risk factor; strategies shorting skew and longing variance (or vice versa) generate zero net risk-adjusted excess returns after transaction costs.
2. **Implied Skew Greatly Overstates Physical Return Asymmetry:** Market-implied skewness (-1.81) is nearly double realized skewness (-1.00). Option sellers collecting steep OTM put premia are compensated not just for realized index drops, but for investors' willingness to pay an enormous structural premium to avoid downside jumps.
3. **Time-Varying Predictability via Market Uncertainty:** Both skew and variance risk premia vary countercyclically. They spike in absolute magnitude following severe market turmoil and are strongly predicted by the TED spread, implied kurtosis ($k_s$), and the implied third moment ($s_t$). Harvesting returns are systematically richer during regimes of elevated credit and funding spreads.
4. **Replication Discipline:** High-order payoff replication requires frequent (daily) delta-adjustments. Discretely managed option overlays that fail to adjust hedges suffer substantial tracking noise that degrades Sharpe ratios.

## Detailed Summary

### Core Theoretical Framework / Mechanics

Neuberger (2012) introduced realized skewness as a contract that measures the covariation between returns and changes in implied variance. Kozhan, Neuberger, and Schneider build on this to formalize tradeable quadratic, cubic, variance, and skew swap contracts.

Let $F_t$ denote the forward price of the underlying asset for maturity $T$, and $r_{t, t+	au} = \ln(F_{t+	au}/F_t)$. 
The price of a log contract that pays $2 \ln(F_T / F_t)$ is replicated statically by an option portfolio:
$$v_{t,T}^L = 2 \int_0^{F_t} rac{P_t(K)}{B_{t,T} K^2} dK + 2 \int_{F_t}^\infty rac{C_t(K)}{B_{t,T} K^2} dK$$

The entropy contract, which weights options inversely by strike times forward price, pays $2 [ (F_T - F_t)/F_t - \ln(F_T / F_t) ]$:
$$v_{t,T}^E = 2 \int_0^{F_t} rac{P_t(K)}{B_{t,T} K F_t} dK + 2 \int_{F_t}^\infty rac{C_t(K)}{B_{t,T} K F_t} dK$$

The **implied third moment** $s_{t,T}$ is model-free and defined simply as:
$$s_{t,T} = 3 (v_{t,T}^E - v_{t,T}^L)$$
And the **implied skew** is normalized as:
$$	ext{skew}_{t,T} = rac{s_{t,T}}{(v_{t,T}^L)^{3/2}}$$

The tradeable **realized third moment** is synthesized by holding an initial position in options and dynamically trading options and forwards over the month:
$$rs_{t,T} = \sum_{i=t}^{T-1} \left[ v_{i,T}^E (e^{r_{i,i+1}} - 1) + 6 (2 - 2 e^{r_{i,i+1}} + r_{i,i+1} + r_{i,i+1} e^{r_{i,i+1}}) ight]$$
The **realized skew** is then:
$$	ext{rskew}_{t,T} = rac{rs_{t,T}}{(v_{t,T}^L)^{3/2}}$$

The excess return on a long skew swap is:
$$x^s_t = rac{	ext{rskew}_t}{	ext{skew}_t} - 1$$
and for a variance swap:
$$x^v_t = rac{rv_t}{v_t^L} - 1$$

### Empirical Findings

Using OptionMetrics S&P 500 index options across 193 non-overlapping monthly periods from January 1996 to January 2012:

1. **Moments and Premia (Table 1):**
   - Implied Log Variance ($v^L 	imes 100$): Mean 0.475, Realized Variance ($rv 	imes 100$): Mean 0.382.
   - Variance swap excess return $x^v$: Mean -22.25% (Std Dev 66.06%, Median -36.83%).
   - Implied skew ($	ext{skew}$): Mean -1.808 (Std Dev 0.722, Range [-4.63, -0.74]).
   - Realized skew ($	ext{rskew}$): Mean -1.001 (Std Dev 2.241).
   - Skew swap excess return $x^s$: Mean -42.09% (Std Dev 117.55%, Median -68.20%).
   - Writing skew swaps generates massive positive excess returns (+42.09% per month), substantially higher in raw terms than shorting variance swaps (+22.25%).

2. **Predictive Regressions (Table 3):**
   - Implied skew forecasts realized skew: $	ext{rskew}_t = -0.282 + 0.398 \cdot 	ext{skew}_t$ ($R^2 = 1.11\%$, $t = 2.59$).
   - The slope of 0.398 is statistically different from 1 ($F = 6.46$, $p = 0.012$). If implied skew reflected physical expectations without risk premia, the slope would be 1.0. This formally proves that roughly 60% of the cross-time variation in implied skew reflects time-varying skew risk premia rather than realized asymmetry.

3. **Spanning and Equivalence of VRP and SRP (Table 5):**
   - Correlation between daily rebalanced $x^s$ and $x^v$ is **0.897**.
   - Seemingly Unrelated Regressions (SUR):
     - $x^s_t = -0.002 + 1.969 \cdot x^v_t + 5.584 \cdot x^m_t$ ($R^2 = 80.59\%$, $lpha$ $t$-stat = -0.06)
     - $x^v_t = -0.002 + 0.500 \cdot x^s_t - 2.927 \cdot x^m_t$ ($R^2 = 84.41\%$, $lpha$ $t$-stat = -0.11)
   - Three-Stage Least Squares (3SLS) using instruments (TED spread, implied kurtosis $k_s$, implied third moment $s_t$):
     - $x^s_t = -0.007 + 1.946 \cdot x^v_t + 5.386 \cdot x^m_t$ ($R^2 = 80.80\%$, $lpha$ $t$-stat = -0.16)
     - $x^v_t = 0.003 + 0.514 \cdot x^s_t - 2.768 \cdot x^m_t$ ($R^2 = 83.94\%$, $lpha$ $t$-stat = 0.17)
   - The alphas are identically zero. There is no orthogonal "skew premium" distinct from variance premium.

4. **Common Predictability Factor (Table 6):**
   - Testing a single-factor Cochrane-Piazzesi restricted specification reveals that both $x^s$ and $x^v$ load on the identical linear combination of macroeconomic and options variables:
     - TED spread ($t = 2.14$)
     - Implied kurtosis ($t = 1.79$)
     - Implied third moment ($t = 1.59$)
   - A Wald test fails to reject the restriction ($F = 0.03$ and $F = 0.10$), demonstrating that a single macro-tail factor drives the conditional dynamics of both premia.

5. **Pitfalls of Static Strategies (Table 7 & 8):**
   - For static (unrebalanced) monthly positions, the correlation between skew and variance returns drops to 0.311.
   - Regressions show large, spurious intercepts ($lpha = -33.1\%$ for skew, $lpha = +13.9\%$ for variance). However, 3SLS instrumental variable regressions reduce these intercepts to zero, proving that static strategy "abnormal returns" are an econometric artifact of unhedged delta/gamma leakage rather than distinct compensation for skewness.

### Implementation & Relevance to Sophie Desk / SPX Option Strategies

- **Single Underlying Premium:** For automated option strategies in `sophie-option-research`, whether selling ATM straddles (pure variance harvesting) or 10-20 delta OTM puts (skew + variance harvesting), the fundamental driver of alpha is the market's aversion to downside jump/tail risk.
- **Why OTM Puts Have Higher Sharpe Than ATM Straddles:** Because OTM puts load heavily on both $v^L$ and $s$, and because $x^s$ has an excess return of -42% vs -22% for $x^v$, selling OTM puts leverages the tail risk premium more efficiently per unit of capital than selling ATM straddles, provided margin/drawdown risk is managed.
- **Regime Indicator Integration:** The paper shows that TED spread and implied kurtosis are robust instrumental variables predicting future VRP and SRP harvesting profitability. Incorporating liquidity/funding spread metrics into the Sophie Desk sizing models provides a clean, theory-backed conditioning filter.

## Citations & Follow-ups

- **Feunou, Jahan-Parvar, and Okou (2018):** *Downside Variance Risk Premium* — extends this decomposition by separating total VRP into upside and downside variance risk premia.
- **Bakshi, Kapadia, and Madan (2003):** *Stock Return Characteristics, Skewness Laws, and the Differential Pricing of Individual and Index Options* — foundational theoretical model linking risk aversion, jump intensity, and higher-order risk-neutral moments.
- **Neuberger (2012):** *Realized Skewness* — establishes the mathematical theory of model-free realized skewness and replication via entropy contracts.
