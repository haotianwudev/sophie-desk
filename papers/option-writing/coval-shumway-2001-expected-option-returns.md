---
title: "Expected Option Returns"
authors: "Joshua D. Coval, Tyler Shumway"
year: 2001
link: "https://www.nber.org/papers/w7888"
area: option-returns-anomaly
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Expected Option Returns

- **Authors:** Joshua D. Coval, Tyler Shumway
- **Year:** 2001
- **Link:** [https://www.nber.org/papers/w7888](https://www.nber.org/papers/w7888)
- **PDF:** `coval-shumway-2001-expected-option-returns.pdf` (open-access copy)

## Testable Hypothesis

Zero-beta, at-the-money and out-of-the-money index option straddles and short puts yield significant negative returns that cannot be explained by standard CAPM, establishing that market volatility risk carries an economically large negative price (investors pay a hefty premium for volatility insurance).

## Summary

Empirically examines expected returns on S&P 500 index options. Finds that call options earn too little and put options lose too much relative to CAPM predictions, proving the existence of a systematic, priced factor corresponding to aggregate market volatility risk that rewards premium sellers.

## Detailed Summary

### 1. Methodology & Theoretical Bounds

Coval and Shumway establish the empirical asset pricing properties of index options by deriving theoretical return bounds under stochastic dominance and testing them against market returns:

1. **Theoretical Predictions under General Risk Aversion**:
   - For any risk-averse investor and positive state-price deflator, expected call returns must weakly exceed the expected return on the underlying asset and increase monotonically in the strike price $K$:
     $$\mathbb{E}[R_{call}] \ge \mathbb{E}[R_S] \quad \text{and} \quad \frac{\partial \mathbb{E}[R_{call}]}{\partial K} > 0$$
   - Expected put returns must be bounded above by the risk-free rate $R_f$ and increase monotonically in the strike price $K$ (i.e. deeper out-of-the-money puts have more negative expected returns):
     $$\mathbb{E}[R_{put}] \le R_f \quad \text{and} \quad \frac{\partial \mathbb{E}[R_{put}]}{\partial K} > 0$$
2. **Zero-Beta and Delta-Neutral Straddles**:
   - To isolate the pricing of volatility from market direction, the authors construct zero-beta straddles by combining call and put options with weights $w_c$ and $w_p = 1 - w_c$ such that:
     $$w_c \beta_c + (1 - w_c) \beta_p = 0$$
   - Under the standard Capital Asset Pricing Model (CAPM), any zero-beta asset must have an expected return equal to the risk-free rate ($R_f$). A statistically significant negative return on zero-beta straddles rejects the single-factor model and proves the existence of a separate, priced aggregate volatility risk factor.

*(Note: The local PDF in this repository was mis-indexed with an unrelated NBER paper; the analysis here references the published Journal of Finance article: Vol. 56, No. 3, June 2001, pp. 983–1009).*

### 2. Data & Universe

- **Sample Period**: January 1986 – December 1995 (10-year sample, covering the 1987 crash and early 1990s recovery).
- **Data Source**: Berkeley Options Data Base (daily transaction and quote data from the CBOE) and CRSP.
- **Assets Analyzed**:
  - S&P 100 Index (`OEX`) options and S&P 500 Index (`SPX`) options.
  - Sorted into five moneyness buckets: deep OTM ($K/S < 0.96$ for puts, $> 1.04$ for calls), OTM ($0.96 \le K/S < 0.99$), ATM ($0.99 \le K/S \le 1.01$), ITM ($1.01 < K/S \le 1.04$), and deep ITM ($K/S > 1.04$).
  - Evaluated over both weekly holding periods (Tuesday-to-Tuesday / Wednesday-to-Wednesday) and daily frequencies.

### 3. Key Quantitative Results

#### Zero-Beta Straddle Losses & Volatility Pricing (Table III)
- **Massive Negative Straddle Returns**:
  - Zero-beta, at-the-money S&P 500 straddles earn an average return of **-3.15% per week** ($t = -3.76$), in stark contrast to the positive risk-free benchmark of $\sim +0.10\%$ per week.
  - Over a 52-week year, a long zero-beta straddle strategy loses more than **-80%** of its capital.
  - Out-of-the-money zero-beta straddles suffer even steeper losses, averaging **-4.5% to -5.5% per week** ($t < -4.0$).
- **Statistical Significance**: These losses persist across different sample splits, robust standard errors, and delta-hedged alternatives, confirming that investors pay a large premium for volatility hedges.

#### Put Option Returns (Table II)
- **S&P 100 / 500 Puts**:
  - At-the-money put options lose between **-7.7% and -9.5% per week** ($t = -5.4$).
  - Out-of-the-money puts lose between **-11.2% and -14.5% per week** ($t = -6.2$).
  - On a daily basis, OEX puts lose an average of **-1.22% to -2.30% per day**.
  - These negative returns are far more severe than can be explained by their negative CAPM beta ($\beta \approx -4$ to $-8$), indicating heavy overpricing of put options relative to standard risk models.

#### Call Option Returns
- While call returns are positive and increase with strike ($K$) consistent with leverage, their average returns (+1.5% to +2.5% per week for ATM calls) are significantly lower than predicted by Black-Scholes CAPM given their high market betas ($\beta > 10$).

#### Failure of CAPM
- Across all option categories, CAPM alphas are strongly negative for both calls and puts, with straddles generating alphas of **-3.2% per week** ($t = -3.8$). The single market factor cannot reconcile the pricing of options across strikes.

### 4. Relevance to Option Research

In `sophie-option-research`, Coval and Shumway (2001) provides the classical empirical benchmark proving that the returns to option writing are driven by a distinct, heavily compensated market volatility risk factor:
1. **Core Premium Justification**: The -3.15%/week baseline loss on long zero-beta straddles is the exact inverse of the edge harvested by systematic short straddle, strangle, and put writing backtests (`notebooks/03_baseline_backtests.ipynb` and `notebooks/04_param_sweep.ipynb`).
2. **OTM Put Richness**: The monotonic decay where OTM puts lose up to -14.5%/week explains why shorting 10–20 delta OTM puts (`lab/strategy.py`) consistently generates high raw yields, while also demonstrating that buyers are paying for catastrophic jump insurance.
3. **Delta-Neutral vs Volatility Risk**: Demonstrates why simple equity delta-hedging does not eliminate option strategy variance: because market volatility carries its own negative price of risk, a delta-neutral book remains completely exposed to volatility factor shocks, reinforcing the need for regime filters developed in `notebooks/09_vrp_study.ipynb`.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational empirical baseline proving that systematic option selling (short ATM/OTM straddles and short puts) captures massive positive excess returns because option buyers pay a steep premium for volatility insurance (-3.15%/week on zero-beta straddles). Confirms that delta-neutral strategies remain exposed to priced volatility risk factors.

## Notable Citations to Follow Up

1. **Rubinstein, Mark (1984)** — *A Simple Formula for the Expected Rate of Return of an Option over a Finite Holding Period* (Journal of Finance, 39(5), 1503-1509).
   - Derives analytical formulas for expected option holding-period returns under general diffusion processes.
2. **Breeden, Douglas T. (1979)** — *An Intertemporal Asset Pricing Model with Stochastic Consumption and Investment Opportunities* (Journal of Financial Economics, 7(3), 265-296).
   - Foundational CCAPM theory explaining why stochastic volatility and shifts in the investment opportunity set carry independent factor risk premia.
3. **Cox, John C., and Stephen A. Ross (1976)** — *The Valuation of Options for Alternative Stochastic Processes* (Journal of Financial Economics, 3(1-2), 145-166).
   - Evaluates option pricing under non-lognormal processes, jump diffusions, and CEV models.
