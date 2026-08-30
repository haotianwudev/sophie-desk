---
title: "The VIX, the Variance Premium and Stock Market Volatility"
authors: "Geert Bekaert, Marie Hoerova"
year: 2014
link: "https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1675.pdf"
area: vrp-measurement
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The VIX, the Variance Premium and Stock Market Volatility

- **Authors:** Geert Bekaert, Marie Hoerova
- **Year:** 2014 (Journal of Econometrics 183(2), 181-192; working paper 2013)
- **Link:** [https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1675.pdf](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1675.pdf) (ECB Working Paper Series No. 1675)
- **PDF:** `bekaert-hoerova-2014-vix-variance-premium.pdf` (open-access copy, European Central Bank repository)

## Testable Hypothesis

Decomposing the squared VIX into conditional physical variance and the equity variance risk premium isolates investor risk aversion from physical uncertainty, showing that the variance premium alone drives stock return predictability while conditional stock variance predicts real economic activity and financial instability.

## Summary

Develops a framework using high-frequency realized volatility and flexible forecasting models to decompose the squared VIX into two unobservable components: the conditional expectation of actual future stock market variance (physical volatility) and the variance risk premium (a proxy for risk aversion). Shows that while the variance risk premium reliably predicts future stock market excess returns at short-to-intermediate horizons, the conditional variance component is the primary driver forecasting macro-economic activity and banking sector stress. This separation resolves the ambiguity in index option-selling literature regarding whether high implied volatility reflects rising physical risk or surging risk compensation.

## Detailed Summary

### 1. Econometric Framework & VIX Decomposition

Bekaert and Hoerova develop a high-frequency econometric framework to deconstruct the squared CBOE VIX index into two distinct economic components:
$$VIX_t^2 = CV_t + VP_t$$
where:
1. **Conditional Physical Variance ($CV_t = E_t[RV_{t+1}^{(22)}]$)**: The expected physical stock market variance over the next 22 trading days (1 month), capturing physical economic uncertainty.
2. **Equity Variance Risk Premium ($VP_t = VIX_t^2 - E_t[RV_{t+1}^{(22)}]$)**: The payoff from selling a 1-month variance swap, isolating aggregate investor risk aversion from physical uncertainty.

**Realized Variance and Jump Isolation:**
- Daily realized variance ($RV_t$) is computed by summing 5-minute squared intraday returns plus the squared close-to-open return for the S&P 500 index.
- To prevent jump contamination, quadratic variation is separated into continuous variation ($C_t$) and jump variation ($J_t$) using Threshold Bipower Variation (TBPV; Corsi, Pirino, and Renò 2010):
  $$J_t = \max[RV_t - TBPV_t, 0], \quad C_t = RV_t - J_t$$
- Models incorporate Corsi (2009) Heterogeneous Autoregressive (HAR) cascades across daily ($h=1$), weekly ($h=5$), and monthly ($h=22$) horizons, along with asymmetric multi-frequency negative return shocks ($r_t^{(h)-}$) to capture leverage.

**Model Selection over 31 Competing Forecasting Specifications:**
The authors evaluate 14 level models, 14 log models, and 3 non-estimated benchmarks (including the Bollerslev, Tauchen, Zhou 2009 martingale $E_t[RV_{t+1}] = RV_t$). Models are judged on out-of-sample RMSE, MAE, MAPE, Mincer-Zarnowitz $R^2$, and Chow parameter stability.

### 2. Data & Sample Period

- **Primary Sample**: Daily S&P 500 5-minute intraday prices and CBOE VIX from January 2, 1990 to October 1, 2010 ($N = 5,208$ daily overlapping observations).
- **Out-of-Sample Forecasting Split**: 
  - *In-Sample Estimation*: January 1, 1990 to July 15, 2005 (75% of sample, $N = 3,912$).
  - *Out-of-Sample Evaluation*: July 16, 2005 to October 1, 2010 ($N = 1,296$, spanning the 2007–2009 Global Financial Crisis).

### 3. Key Quantitative Results

#### Volatility Model Horse Race & Winning Specifications (Table 3 & Equations 7–8)
- **Winning Model 8 (HAR-RV + $VIX^2$)**: Best overall stability and accuracy (lowest out-of-sample MAE $= 16.856$, out-of-sample $R^2 = 55.5\%$, average score 4.00):
  $$RV_t^{(22)} = 3.730 + 0.108 VIX_{t-22}^2 + 0.199 RV_{t-22}^{(22)} + 0.330 RV_{t-22}^{(5)} + 0.107 RV_{t-22}^{(1)}$$
- **Winning Model 11 (HAR-CJ with Continuous and Jump Decomposition)**: Stable, out-of-sample $R^2 = 54.4\%$, MAE $= 17.400$:
  $$RV_t^{(22)} = 3.855 - 0.212 C_{t-22}^{(22)} + 0.237 C_{t-22}^{(5)} + 0.223 C_{t-22}^{(1)} + 1.742 J_{t-22}^{(22)} + 0.327 J_{t-22}^{(5)} - 0.016 J_{t-22}^{(1)}$$
- **Rejection of BTZ Martingale**: The naive martingale model ($E_t[RV_{t+1}] = RV_t$, Model 30) performs an order of magnitude worse out-of-sample (MAPE $= 0.500$ vs. $0.347$ for Model 8; $R^2 = 40.5\%$), showing that unadjusted lagged realized variance significantly mismeasures conditional variance.

#### Stock Return Predictability (Table 4)
- **Univariate Regressions (Panel A)**:
  - Raw $VIX^2$ has zero predictive power for stock excess returns across all horizons ($t = 0.14, \text{Adj. } R^2 = -0.4\%$).
  - $VP_8$ significantly predicts stock excess returns at 3-month ($\beta = 0.426, t = 2.43, R^2 = 4.2\%$) and 12-month horizons ($\beta = 0.241, t = 2.11, R^2 = 4.5\%$).
- **Bivariate Regressions ($VP + CV$, Panel B)**:
  - Disentangling risk aversion ($VP$) from physical uncertainty ($CV$) dramatically strengthens predictability:
  - For Model 8 at 3-month horizon: $VP_8$ coefficient increases to $\beta = 0.688$ ($t = 4.74$), while $CV_8$ is significantly negative ($\beta = -0.333, t = -5.46$), raising $\text{Adj. } R^2$ to **$9.5\%$**.
  - At 12-month horizon: $VP_8$ has $\beta = 0.287$ ($t = 3.12, R^2 = 4.6\%$).
- **Multivariate Macro Regressions (Panel C)**:
  - Controlling for 3-month T-bill rate, $\log(\text{dividend yield})$, credit spread, and term spread, $VP_8$ predictive power surges to $\beta = 0.796$ ($t = 5.45, \text{Adj. } R^2 = 17.1\%$) at 3 months and $\beta = 0.304$ ($t = 3.04, \text{Adj. } R^2 = 27.6\%$) at 12 months.

#### Economic Activity and Financial Instability (Tables 5 & 6)
- **Industrial Production Growth (Table 5)**: Predicted exclusively by physical conditional variance $CV$, not $VP$. $CV_8$ predicts quarterly output growth with $\beta = -0.113$ ($t = -12.5, R^2 = 27.6\%$), while $VP_8$ is statistically zero ($\beta = -0.028, t = -0.67$).
- **Financial Instability / ECB CISS Index (Table 6)**: $CV_8$ heavily predicts systemic stress across 1-month ($\beta = 0.301, t = 6.27, R^2 = 42.2\%$), 3-month ($\beta = 0.288, t = 9.29, R^2 = 34.9\%$), and 12-month horizons ($\beta = 0.200, t = 4.55$). $VP$ has only weak, short-lived effects.

### 4. Relevance to Option Research

In `sophie-option-research`, option selling strategies (e.g., short OTM puts and short straddles in `01_equity_curve.py`, `04_delta_selection.py`) are fundamentally exposed to time-varying VRP. The findings of Bekaert and Hoerova provide critical architecture for quantitative feature engineering:
1. **Superior VRP Metric Construction**: Using the naive BTZ proxy ($VIX^2 - RV_{t-22}$) creates substantial measurement error by treating variance as a martingale. Implementing Model 8 (HAR-RV augmented with $VIX^2$) yields an uncorrupted daily estimate of $VP_t = VIX_t^2 - CV_t$ in `lab/features.py`.
2. **Dual-Signal Regime Architecture**:
   - **Trade Entry Trigger ($VP > 0$)**: Elevated $VP$ reflects elevated investor risk aversion (rich option premiums), signaling optimal entry conditions for option sellers.
   - **Risk Management / Circuit Breaker ($CV \uparrow$)**: Elevated $CV$ signals impending macroeconomic contraction and systemic banking stress. When $CV$ spikes without a commensurate rise in $VP$, option writers face pure uncompensated physical tail risk, indicating that position sizes should be scaled down or paused in `08_rolling.py` / `lab/report.py`.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Crucial for systematic VRP feature engineering and trade filtering; demonstrates that decomposing $VIX^2$ into conditional physical variance ($CV$) and variance risk premium ($VP = VIX^2 - CV$) isolates risk compensation from physical uncertainty. Shows that $VP$ drives future equity returns and option-writing profitability, while $CV$ acts as an economic danger signal.

## Notable Citations to Follow Up

1. **Corsi, Fulvio (2009)** — *A Simple Approximate Long Memory Model of Realized Volatility* (Journal of Financial Econometrics, 7(2), 174-196).
   - Introduces the HAR-RV framework (daily, weekly, monthly realized variance cascades), which serves as the premier benchmark for estimating physical conditional volatility $CV$.
2. **Corsi, Fulvio, and Roberto Renò (2012)** — *Discrete-Time Volatility Forecasting with Persistent Leverage Effect and the Link with Continuous-Time Volatility Modeling* (Journal of Business & Economic Statistics, 30(4), 468-480).
   - Enhances HAR models with multi-frequency asymmetric returns (leverage effect) and jump components (LHAR-CJ), directly applicable to short-term option pricing features.
3. **Andersen, Torben G., Tim Bollerslev, and Francis X. Diebold (2007)** — *Roughing It Up: Including Jump Components in the Measurement, Modeling, and Forecasting of Return Volatility* (Review of Economics and Statistics, 89(4), 701-720).
   - Establishes bipower variation techniques to decompose realized quadratic variation into continuous diffusion versus discrete jump components.
