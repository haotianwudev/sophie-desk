---
title: "Expected Stock Returns and Variance Risk Premia"
authors: "Tim Bollerslev, George Tauchen, Hao Zhou"
year: 2009
link: "https://www.federalreserve.gov/pubs/feds/2007/200711/200711pap.pdf"
area: vrp-measurement
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Expected Stock Returns and Variance Risk Premia

- **Authors:** Tim Bollerslev, George Tauchen, Hao Zhou
- **Year:** 2009 (Review of Financial Studies 22(11), 4463-4492; working paper 2007)
- **Link:** [https://www.federalreserve.gov/pubs/feds/2007/200711/200711pap.pdf](https://www.federalreserve.gov/pubs/feds/2007/200711/200711pap.pdf) (Federal Reserve Board FEDS 2007-11)
- **PDF:** `bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp.pdf` (open-access copy, Federal Reserve Board repository)

## Testable Hypothesis

The variance risk premium—defined as the difference between model-free implied variance and realized variance—predicts aggregate quarterly equity returns with a statistically and economically significant positive coefficient, accounting for more return variation at 3-to-6 month horizons than traditional valuation ratios.

## Summary

Establishes that the difference between model-free implied variance (from option prices) and realized variance (from high-frequency returns) contains powerful predictive information for aggregate stock market returns, explaining up to 15% of return variation at a quarterly horizon. Demonstrates that this predictability peaks at intermediate horizons (1 to 4 months) and dominates classical predictors such as the price-earnings ratio, dividend yield, and consumption-wealth ratio (CAY). Motivates these empirical results within a consumption-based equilibrium model with recursive preferences where time-varying economic uncertainty and volatility risk generate predictable variation in the equity risk premium.

## Detailed Summary

### 1. Methodology & Model-Free Variance Concepts

Bollerslev, Tauchen, and Zhou formalize the model-free measurement of the equity Variance Risk Premium ($VRP_t$) and evaluate its power to forecast aggregate stock market returns.

**Model-Free Implied Variance ($IV_t$):**
Following Carr and Madan (1998), Demeterfi et al. (1999), and Britten-Jones and Neuberger (2000), the risk-neutral expected return variation over $[t, t+1]$ is extracted directly from a continuous portfolio of European out-of-the-money options across strikes without imposing any parametric option pricing model:
$$IV_t \equiv 2 \int_0^\infty \frac{C_t(t+1, K) - C_t(t, K)}{K^2} dK = E_t^\mathbb{Q}[\text{Return Variation}(t, t+1)]$$
Empirically, this corresponds to the squared CBOE VIX index ($VIX_t^2 / 12$).

**Model-Free Realized Variance ($RV_t$):**
Ex-post return variation over $[t-1, t]$ is computed from high-frequency intraday prices to eliminate noise and discretization error:
$$RV_t \equiv \sum_{j=1}^n \left[ p_{t-1 + \frac{j}{n}} - p_{t-1 + \frac{j-1}{n}} \right]^2 \longrightarrow \text{Return Variation}(t-1, t)$$
Using 5-minute sampling intervals across 22 trading days per month ($n = 22 \times 78 = 1,716$ intraday observations) plus squared overnight returns.

**Variance Risk Premium ($VRP_t$):**
$$VRP_t \equiv IV_t - RV_t$$
$VRP_t$ measures the wedge between ex-ante risk-neutral expectations and backward-looking realized variance. The authors show that $VRP_t$ serves as a direct proxy for time-varying aggregate risk aversion within a representative agent framework with Epstein-Zin recursive preferences.

### 2. Data & Sample Period

- **Primary Sample**: Monthly and quarterly observations from 1990Q1 through 2005Q1 ($N = 61$ quarters / 181 months).
- **Asset Data**: S&P 500 composite index high-frequency 5-minute returns (Institute of Financial Markets) and CBOE VIX index.
- **Macro-Finance Benchmarks**: Log price-earnings ratio $\log(P_t/E_t)$, log price-dividend ratio $\log(P_t/D_t)$, Moody's BAA–AAA default spread ($DFSP_t$), 10-year minus 3-month Treasury term spread ($TMSP_t$), stochastically de-trended risk-free rate ($RREL_t$), and consumption-wealth ratio ($CAY_t$, Lettau and Ludvigson 2001).

### 3. Key Quantitative Results

#### Summary Statistics & Time-Series Properties (Table 1)
- **Mean Variance Levels**: S&P 500 annualized excess return mean $= 5.97\%$ (Std Dev $31.44\%$).
- **Implied vs. Realized Variance**: Mean $IV_t = 36.30$, mean $RV_t = 14.90$ (in percentage points squared).
- **Average VRP**: $\overline{VRP} = 21.40$ (Std Dev $14.86$). The variance risk premium is positive in virtually all quarters, reflecting persistent compensation demanded for bearing variance risk.
- **Low Autocorrelation**: First-order autocorrelation of $VRP_t$ is only **$AR(1) = 0.31$** (compared to $0.91$ for $P/E$, $0.96$ for $P/D$, and $0.90$ for $CAY$). This near-absence of persistence proves that $VRP$ is a fast-moving cyclical signal, completely avoiding the spurious regression bias that plagues persistent valuation ratios.

#### Quarterly Return Predictability (Table 2)
- **Univariate Regressions**:
  - $VRP_t$ alone yields $\beta = 0.86$ ($t = 3.94$, Newey-West 4 lags) and explains **$15.14\%$ of quarterly excess return variance** ($\text{Adj. } R^2 = 15.14\%$).
  - $IV_t$ alone: $R^2 = 6.32\%$ ($\beta = 0.34, t = 2.38$).
  - $RV_t$ alone: $R^2 = -1.05\%$ ($\beta = 0.17, t = 0.56$).
  - Traditional predictors: $\log(P/E)$ ($R^2 = 6.22\%$), $\log(P/D)$ ($R^2 = 2.76\%$), $CAY$ ($R^2 = 4.83\%$), $DFSP$ ($R^2 = 0.27\%$), $TMSP$ ($R^2 = -1.63\%$), $RREL$ ($R^2 = -0.66\%$).
- **Bivariate & Multivariate Regressions**:
  - Combining $VRP_t$ with $\log(P/E)$ surges explanatory power to **$\text{Adj. } R^2 = 26.37\%$** ($\beta_{VRP} = 0.98, t = 4.87; \beta_{P/E} = -3.57, t = -2.09$).
  - Full multivariate model ($VRP + P/E + TMSP + RREL$): achieves **$\text{Adj. } R^2 = 27.67\%$** ($\beta_{VRP} = 1.11, t = 5.27; \beta_{RREL} = 7.59, t = 2.29$).

#### Model-Free vs. Black-Scholes / Daily Measures (Table 3)
- Replacing model-free measures with standard Black-Scholes implied variance and daily realized variance ($IV^* - RV^*$) causes the quarterly predictive $R^2$ to collapse from **$15.14\%$ down to $3.62\%$** ($t = 1.90$).
- Model-free $IV$ with daily $RV^*$: $R^2 = 8.08\%$.
- Black-Scholes $IV^*$ with 5-minute $RV$: $R^2 = 7.30\%$.
- Demonstrates that high-frequency intraday sampling and model-free option integration are critical to isolate pure risk aversion from measurement noise.

#### Additional Horizon and Risk Specifications (Tables 4–6)
- **Monthly Horizon (Table 4)**: $VRP_t$ univariate $R^2 = 1.24\%$ ($t = 2.87$); combined with $P/E$, $R^2 = 3.98\%$. Predictability is strongest at the 3-to-4 month intermediate horizon.
- **Volatility Risk Premium (Table 5)**: The standard deviation spread ($\sqrt{IV_t} - \sqrt{RV_t}$) in isolation generates an even higher quarterly predictive $R^2 = \mathbf{18.50\%}$ ($\beta = 4.42, t = 4.90$).
- **Realized Quarticity ($RQ_t$, Table 6)**: Adding realized quarticity $\sum \Delta p_j^4$ (volatility-of-volatility) boosts the multivariate $R^2$ to **$30.18\%$** ($t = 2.33$).

### 4. Relevance to Option Research

Bollerslev, Tauchen, and Zhou provides the benchmark framework for variance risk premium calculation and strategy timing across `sophie-option-research`:
1. **Core VRP Pipeline**: Defines the standard method for constructing daily/monthly $VRP_t = VIX_t^2 - RV_t$ features in `lab/features.py` using 5-minute SPX intraday returns.
2. **Economic Rationale for Option Selling**: Proves that the average spread of $21.40$ variance points is positive and statistically robust, providing the structural premium harvested by systematic short put and short straddle strategies (`01_equity_curve.py`, `04_delta_selection.py`).
3. **Macro Return-Timing Signal**: High VRP signals elevated market risk aversion and higher expected future equity returns, serving as a dynamic exposure-scaling filter in multi-strategy allocation engines.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** The cornerstone academic work establishing model-free Variance Risk Premium ($VRP = IV - RV$) using high-frequency intraday data and option portfolios. Empirically validates that high VRP predicts positive excess market returns (explaining >15% quarterly variance), directly validating the core thesis of systematic equity option selling and VRP timing engines.

## Notable Citations to Follow Up

1. **Britten-Jones, Mark, and Anthony Neuberger (2000)** — *Option Prices, Implied Price Processes, and Stochastic Volatility* (Journal of Finance, 55(2), 839-866).
   - Establishes the mathematical foundation of model-free implied volatility by integrating European option prices across continuous strikes.
2. **Demeterfi, Kresimir, Emanuel Derman, Michael Kamal, and Joseph Zou (1999)** — *A Guide to Volatility and Variance Swaps* (Journal of Derivatives, 6(4), 9-32).
   - Classic quantitative reference detailing log-contract replication, discrete variance swap payoff mechanics, and practical trading implementations.
3. **Jiang, George, and Yisong Tian (2005)** — *Model-Free Implied Volatility and Its Information Content* (Review of Financial Studies, 18(4), 1305-1342).
   - Demonstrates how model-free implied volatility subsumes Black-Scholes IV and addresses discrete strike truncation and option pricing frictions.
