---
title: "An Empirical Investigation of Continuous-Time Equity Return Models"
authors: "Torben G. Andersen, Luca Benzoni, Jesper Lund"
year: 2002
link: "https://www.nber.org/papers/w8510"
area: return-dynamics-modeling
relevance: Medium
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# An Empirical Investigation of Continuous-Time Equity Return Models

- **Authors:** Torben G. Andersen, Luca Benzoni, Jesper Lund
- **Year:** 2002 (Journal of Finance 57(3), 1239-1284; NBER Working Paper 8510, 2001)
- **Link:** [https://www.nber.org/papers/w8510](https://www.nber.org/papers/w8510)
- **PDF:** ndersen-benzoni-lund-2002-continuous-time-equity-return-models.pdf (open-access copy, NBER Working Paper 8510)

## Testable Hypothesis

Capturing the empirical dynamics of equity index returns and option prices requires both time-varying Poisson jump intensity and stochastic volatility with a pronounced asymmetric leverage effect, demonstrating that option sellers are compensated for bearing both jump and diffusive volatility risks.

## Summary

Conducts an extensive empirical estimation of continuous-time parametric models for S&P 500 returns and options using efficient method of moments (EMM). Concludes that standard stochastic volatility diffusion models fail to fit the empirical return distribution unless augmented by discrete jumps with state-dependent arrival rates (volatility-dependent jump intensity) and a strong negative correlation between return and volatility innovations (leverage effect). Shows that the structural features extracted from physical return time-series directly align with the risk premia implicit in cross-sectional option prices.

## Detailed Summary

### 1. Methodology & Model Specifications

The paper provides an econometric evaluation of continuous-time jump-diffusion representations for daily S&P 500 equity-index returns under the physical probability measure $\mathbb{P}$, and assesses their implications for option pricing under the risk-neutral measure $\mathbb{Q}$.

The general continuous-time framework models the index price $S_t$ and variance process $V_t$ as:
$$\frac{dS_t}{S_t} = (\mu + c V_t - \lambda(t) \bar{\kappa}) dt + \sqrt{V_t} dW_{1,t} + \kappa(t) dq_t$$

Two alternative variance diffusion processes are tested:
1. **Log-Variance Model ($SV_1$)**:
   $$d \ln V_t = (\alpha - \beta \ln V_t) dt + \eta dW_{2,t}$$
2. **Square-Root / Affine CIR Model ($SV_2$, Heston 1993)**:
   $$d V_t = (\alpha - \beta V_t) dt + \eta \sqrt{V_t} dW_{2,t}$$

Here $W_1$ and $W_2$ are Brownian motions with asymmetric leverage correlation $\text{corr}(dW_{1,t}, dW_{2,t}) = \rho$. The jump process $q_t$ has Poisson intensity $\lambda(t) = \lambda_0 + \lambda_1 V_t$, and jump size is log-normally distributed: $\ln(1 + \kappa(t)) \sim N(\ln(1 + \bar{\kappa}) - 0.5 \delta^2, \delta^2)$ with $\bar{\kappa} = 0$.

**Efficient Method of Moments (EMM):**
Parameter estimation is conducted via the EMM procedure of Gallant and Tauchen (1996), matching moments generated from the score generator of an auxiliary Semi-Nonparametric (SNP) model: an $\text{ARMA}(0,0)\text{-EGARCH}(1,1)\text{-}K_z(8)\text{-}K_x(0)$ density expansion using orthogonal Hermite polynomials. The EMM criterion function provides a formal $\chi^2$ goodness-of-fit specification test for over-identifying restrictions across nested and non-nested models.

### 2. Data & Sample Period

- **Primary Sample**: Daily S&P 500 index returns from January 2, 1953 to December 31, 1996 ($N = 11,076$ trading days).
- **Subsample for Stability Check**: January 3, 1980 to December 31, 1996 ($N = 4,298$ trading days).
- **Data Filtering**: Daily returns are prefiltered with a single $\text{MA}(1)$ filter to purge spurious microstructural autocorrelation (non-synchronous trading) while preserving full variance dynamics and leptokurtosis.

### 3. Key Quantitative Results

#### Model Rejections and Goodness-of-Fit Tests (Table III & Table IV)
- **Pure Diffusions Fail Overwhelmingly**:
  - Constant-volatility Black-Scholes (BS): $\chi^2 = 127.35$ ($p < 10^{-5}$).
  - Merton (1976) jump-diffusion without stochastic volatility (BSJ): $\chi^2 = 89.60$ ($p < 10^{-5}$).
  - Symmetric stochastic volatility without jumps ($SV_1, \rho = 0$): $\chi^2 = 121.11$ ($p < 10^{-5}$).
  - Asymmetric stochastic volatility without jumps ($SV_1, \rho \neq 0$): $\chi^2 = 30.92$ ($p = 0.00031$); $SV_2$ affine: $\chi^2 = 31.94$ ($p = 0.00020$). Even with strong leverage $\rho$, pure SV diffusions cannot generate enough kurtosis to match daily returns.
- **Stochastic Volatility Jump-Diffusions (SVJD) Succeed**:
  - Log-variance with constant jump intensity ($SV_1J, \lambda_1 = 0$): $\chi^2 = 13.34$ ($p = 0.06429$; with volatility-in-mean, $\chi^2 = 13.13, p = 0.06905$).
  - Square-root affine with constant jump intensity ($SV_2J$ / Bates 1996a): $\chi^2 = 14.90$ ($p = 0.03736$; with volatility-in-mean, $\chi^2 = 14.09, p = 0.04957$).
  - Both SVJD models pass specification tests at conventional significance levels, proving that both stochastic volatility and discrete jumps are mandatory ingredients.

#### Estimated Parameter Values (Full Sample, Table III & IV)
- **Mean & Volatility Persistence**: Drift $\mu = 0.0304\%$ daily (~7.91% annualized). Log-volatility persistence $\beta = 0.0145$, implying daily persistence $\exp(-\beta) = 0.9856$ (half-life $\approx 48$ days).
- **Asymmetric Leverage**: $\rho = -0.6127$ ($t\text{-stat} = -9.8$), tightly estimated across all asymmetric specifications (range $-0.58$ to $-0.62$).
- **Jump Frequency & Size**: Jump intensity $\lambda_0 = 0.0137$ jumps/day, corresponding to **3.45 jumps per year** (~3 to 4 jumps/year). Jump standard deviation $\delta = 0.0151$ (1.51%), indicating most jumps lie within $\pm 3.0\%$.
- **State-Dependent Jump Intensity**: The affine parameter $\lambda_1$ is statistically insignificant ($\lambda_1 = 0.00010$, $t = 0.01$), indicating daily equity return time-series does not require jump intensity to vary with instantaneous variance under $\mathbb{P}$.
- **1980–1996 Subsample (Table VI)**: Jumps are slightly more frequent ($\lambda_0 = 0.0192 \approx 4.8\text{ jumps/year}$) and larger ($\delta = 2.17\%$, range $\pm 4.3\%$), while leverage remains strongly negative ($\rho = -0.3856$).

#### Option Pricing Implications (Section III, Figures 2–5)
- **Source of Implied Volatility Smirk**: The steep smirk in short-maturity options (1–3 weeks) is generated almost entirely by the jump component, while the long-maturity smirk (6 months) is governed by continuous asymmetric leverage $\rho$.
- **Physical vs. Risk-Neutral Discrepancy**: The diffusive volatility-of-volatility parameter $\eta$ under physical measure $\mathbb{P}$ is $\eta = 0.1845$, which is approximately half the value extracted from option prices under $\mathbb{Q}$ ($\eta \approx 0.38$ in Bakshi, Cao, Chen 1997). This gap reflects the substantial variance risk premium priced into options.

### 4. Relevance to Option Research

In `sophie-option-research`, option selling strategies (e.g., short OTM puts and iron condors across 0–45 DTE) systematically harvest the spread between implied variance and realized variance. The findings of Andersen, Benzoni, and Lund directly illuminate the two distinct risk drivers of this premium:
1. **Jump Risk vs. Diffusive Variance**: At short maturities (<30 DTE), options are priced primarily against discrete jump risk ($\lambda_0 \approx 3.5\text{ jumps/year}$ with $\pm 3\%$ to $\pm 4.3\%$ shock size), while long-tenor options are driven by continuous volatility diffusion. Short-dated premium harvesters are thus predominantly selling crash insurance rather than diffusive volatility.
2. **Structural Basis for Volatility-of-Volatility ($\eta$) Markups**: The 2x markup of risk-neutral vol-of-vol over physical vol-of-vol provides the theoretical underpinning for why delta-neutral and OTM short options carry persistent positive alpha, while highlighting the need for strike selection safeguards and tail-loss buffers in backtest pipelines (`lab/report.py`, `08_rolling.py`).

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** Validates the core theoretical premise that option sellers earn premia by bearing both continuous diffusive volatility and discrete jump risk, while demonstrating that short-tenor volatility smirks are driven primarily by jump components. However, its primary focus is on continuous-time econometric model estimation (EMM) rather than actionable trading rules or discrete strategy backtests.

## Notable Citations to Follow Up

1. **Bakshi, Gurdip, and Nikunj Kapadia (2001)** — *Delta-Hedged Gains and the Negative Market Volatility Risk Premium* (Working Paper, University of Maryland).
   - Directly examines why delta-hedged short option portfolios generate positive excess returns and quantifies the economic magnitude of market volatility risk premia.
2. **Chernov, Mikhail, and Eric Ghysels (2000)** — *A Study towards a Unified Approach to the Joint Estimation of Objective and Risk Neutral Measures for the Purpose of Options Valuation* (Journal of Financial Economics, 56, 407-458).
   - Explores the joint estimation of physical and risk-neutral dynamics, valuable for modeling the divergence between realized index volatility and implied volatility surfaces.
3. **Das, Sanjiv R., and Rangarajan K. Sundaram (1999)** — *Of Smiles and Smirks: A Term-Structure Perspective* (Journal of Financial and Quantitative Analysis, 34, 211-239).
   - Provides analytical and empirical foundations for how stochastic volatility versus discrete jump processes generate distinct term structures of implied volatility skew.
