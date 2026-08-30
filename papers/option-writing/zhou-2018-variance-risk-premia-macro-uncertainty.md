---
title: "Variance Risk Premia, Asset Predictability Puzzles, and Macroeconomic Uncertainty"
authors: "Hao Zhou"
year: 2018
link: "https://www.federalreserve.gov/pubs/feds/2010/201014/201014pap.pdf"
area: cross-asset
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Variance Risk Premia, Asset Predictability Puzzles, and Macroeconomic Uncertainty

- **Authors:** Hao Zhou
- **Year:** 2018 (Annual Review of Financial Economics 10, 481-497; working paper 2010)
- **Link:** [https://www.federalreserve.gov/pubs/feds/2010/201014/201014pap.pdf](https://www.federalreserve.gov/pubs/feds/2010/201014/201014pap.pdf) (Federal Reserve Board FEDS 2010-14)
- **PDF:** `zhou-2018-variance-risk-premia-macro-uncertainty.pdf` (open-access copy, Federal Reserve Board repository)

## Testable Hypothesis

The variance risk premium is a unified proxy for macroeconomic uncertainty and time-varying risk aversion that simultaneously resolves short-horizon return predictability puzzles across equity, Treasury bond, foreign exchange, and credit default swap markets.

## Summary

Surveys and synthesizes theoretical and empirical research on the variance risk premium across major financial asset classes. Highlights that while traditional valuation factors predict asset returns only at multi-year horizons, the variance risk premium consistently predicts excess returns at short-to-intermediate horizons (1 to 6 months) across equities, government bonds, exchange rates, and credit spreads. Demonstrates how structural asset pricing models incorporating consumption jump risk, time-varying economic uncertainty, and Knightian ambiguity explain both the magnitude of the variance risk premium and its widespread cross-market predictive power.

## Detailed Summary

### 1. Unified Framework & Economic Uncertainty Model

Hao Zhou develops an integrated general equilibrium framework that positions the Variance Risk Premium ($VRP_t$) as a fundamental macroeconomic uncertainty proxy that simultaneously resolves short-horizon asset predictability puzzles across equities, Treasury bonds, and corporate credit markets.

**VRP Measurement:**
$$VRP_t \equiv E_t^\mathbb{Q}[\text{Var}_{t,t+1}] - E_t^\mathbb{P}[\text{Var}_{t,t+1}] \approx VIX_t^2 - \widehat{E}_t^\mathbb{P}[RV_{t,t+1}]$$
where $VIX_t^2$ is the CBOE model-free risk-neutral implied variance and $\widehat{E}_t^\mathbb{P}[RV_{t,t+1}]$ is the physical conditional expectation of 5-minute S&P 500 realized variance estimated via an $AR(12)$ time-series model.

**Consumption-Based General Equilibrium Model:**
The representative agent possesses Epstein-Zin-Weil recursive preferences with risk aversion $\gamma = 2$, elasticity of intertemporal substitution $\psi = 1.5$ ($\theta = \frac{1-\gamma}{1-1/\psi} < 0$), and time preference $\delta = 0.997$.
- Log consumption growth: $g_{t+1} = \mu_g + \sigma_{g,t} z_{g,t+1}$.
- Consumption volatility: $\sigma_{g,t+1}^2 = a_\sigma + \rho_\sigma \sigma_{g,t}^2 + \sqrt{q_t} z_{\sigma,t+1}$.
- **Stochastic Volatility-of-Volatility ($q_t$)**: $q_{t+1} = a_q + \rho_q q_t + \phi_q \sqrt{q_t} z_{q,t+1}$, representing pure macroeconomic economic uncertainty.

**Analytical Solutions for Market Risk Premia (Equations 12–14):**
- **Equity Risk Premium**: $\text{ERP}_t = \gamma \sigma_{g,t}^2 + (1-\theta)\kappa_1^2 (A_q^2 \phi_q^2 + A_\sigma^2) q_t > 0$.
- **Variance Risk Premium**: $VRP_t \approx (\theta - 1)\kappa_1 \left[ A_\sigma + A_q \kappa_1^2 (A_\sigma^2 + A_q^2 \phi_q^2) \phi_q^2 \right] q_t > 0$.
- **Bond Risk Premium**: $rp_t^n = \left[ B(n-1)(\theta-1)\kappa_1 A_\sigma + C(n-1)(\theta-1)\kappa_1 A_q \phi_q^2 \right] q_t > 0$.
Because equity, variance, and bond risk premia all load positively on the same latent state variable $q_t$, $VRP_t$ serves as a direct proxy for time-varying macroeconomic uncertainty across financial markets.

### 2. Data & Sample Period

- **Primary Sample**: Monthly observations from January 1990 to December 2008 ($N = 228$ months, spanning the 1990/2001 recessions, 1998 LTCM/Russian crisis, and 2008 Global Financial Crisis).
- **Equity Market**: S&P 500 monthly excess returns, $\log(P/E)$.
- **Treasury Market**: CRSP Fama zero-coupon Treasury bills with maturities of 1 to 6 months and holding periods of 1 to 5 months.
- **Credit Market**: Moody's AAA and BAA corporate bond yield indices and CRSP Fama-Bliss risk-free rates.

### 3. Key Quantitative Results

#### Summary Statistics & Properties of VRP (Table 1)
- **Mean Level**: Full-sample $AR(12)$ $VRP$ mean is **$18.30$ (% squared)**, Std Dev $= 22.69$, Skewness $= 2.79$, Kurtosis $= 16.62$.
- **Stationarity & Low Correlation**: $AR(1) = 0.26$, showing that $VRP$ is a stationary, non-persistent variable.
- **Orthogonality to Macro Ratios**: Correlation with $P/E$ is $0.07$, with forward spreads is $0.04\text{--}0.06$, and with the short rate is $-0.09$, proving that $VRP$ provides independent, uncrowded information.

#### Cross-Market Short-Horizon Return Predictability (Tables 2–6)
- **Equity Market (Table 2 & Figure 3)**:
  - Displays a distinctive tent-shaped predictability pattern peaking at **4 months**:
    - 1 month: $R^2 = -0.43\%$
    - 4 months: $\beta = 0.40$ ($t = 3.56, \text{Adj. } R^2 = \mathbf{8.11\%}$).
    - 12 months: $R^2 = 1.51\%$ ($t = 2.38$).
  - Combined with $\log(P/E)$ at 4 months: $\text{Adj. } R^2$ surges to **$12.59\%$** ($\beta_{VRP} = 0.42, t = 3.61; \beta_{P/E} = -22.83, t = -1.60$).
- **Treasury Bond Market (Tables 3 & 5, Figure 4)**:
  - $VRP$ significantly predicts 1-month holding period excess returns across 2- to 6-month T-bills:
    - 2-month bill: $\beta = 5.96 \times 10^{-3}$ ($t = 2.38, R^2 = 4.20\%$).
    - 6-month bill: $\beta = 13.12 \times 10^{-3}$ ($t = 3.23, R^2 = \mathbf{4.57\%}$).
    - Translates to an average variance-induced bond risk premium of **$11\text{ to }24\text{ bps}$**.
  - Combining $VRP$ with Fama forward spreads boosts 1-month predictive $R^2$ to **$33.23\%$** for 3-month bills and **$22.98\%$** for 2-month bills.
- **Corporate Credit Market (Table 6 & Figure 5)**:
  - $VRP$ predicts 1-month ahead credit spreads: $\beta = 4.68 \times 10^{-3}$ ($t = 2.49, R^2 = 5.19\%$) for AAA; $\beta = 7.99 \times 10^{-3}$ ($t = 2.35, R^2 = 6.64\%$) for BAA (average impact 9–15 bps).
  - Combined with short rate $r_{f,t}$, joint $R^2$ reaches **$41.13\%$** for AAA ($\beta_{VRP} = 5.85 \times 10^{-3}, t = 4.26$) and **$42.37\%$** for BAA ($\beta_{VRP} = 9.76 \times 10^{-3}, t = 3.77$).

#### Equilibrium Calibration (Tables 8 & 9)
- By calibrating volatility-of-volatility persistence $\rho_q = 0.95$ and vol-of-vol shock $\phi_q = 0.008$ with moderate risk aversion $\gamma = 2$, the model matches the empirical $VRP$ mean ($18.30$), standard deviation ($25.12$ vs. $22.69$), skewness ($2.48$ vs. $2.79$), and kurtosis ($13.18$ vs. $16.62$) without needing exogenous jump processes.

### 4. Relevance to Option Research

Zhou's cross-asset synthesis expands the scope of volatility selling research in `sophie-option-research`:
1. **Macro Uncertainty Foundation**: Reaffirms that the variance risk premium is not a localized option quirk but the market-wide price of macroeconomic uncertainty ($q_t$). Option writers are systematically compensated for providing capital insurance during uncertainty spikes.
2. **Cross-Asset Signal Integration**: In `lab/features.py`, VRP can be utilized not only for equity option strike timing but as a macro risk factor that predicts short-term yield curve shifts (T-bill excess returns) and credit spread widenings.
3. **Short-Horizon Complementarity**: Validates why short-horizon option strategies (30–60 DTE) pair synergistically with long-horizon equity or fixed-income portfolios: VRP captures rapid 1- to 4-month risk-premia mean-reversion that is uncorrelated with traditional multi-year valuation factors ($P/E, P/D$).

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Comprehensive synthesis of the Variance Risk Premium ($VRP = IV - \mathbb{E}[RV]$) across asset classes; establishes that model-free VRP is a robust short-horizon predictor (peaking at 1–4 months) of excess returns across equities, Treasury bonds, and credit spreads. Directly justifies the core economic thesis of `sophie-option-research` that selling volatility systematically harvests compensation for macroeconomic uncertainty and time-varying risk aversion.

## Notable Citations to Follow Up

1. **Drechsler, Itamar, and Amir Yaron (2011)** — *What's Vol Got to Do With It* (The Review of Financial Studies, 24(1), 1-45).
   - Demonstrates how time-varying economic uncertainty and non-Gaussian jump risks under recursive preferences generate large, volatile variance risk premia.
2. **Bansal, Ravi, and Amir Yaron (2004)** — *Risks for the Long Run: A Potential Resolution of Asset Pricing Puzzles* (The Journal of Finance, 59(4), 1481-1509).
   - Seminal long-run risk framework establishing how stochastic volatility and recursive utility price macroeconomic consumption uncertainty into asset risk premia.
3. **Jiang, George, and Yisong Tian (2005)** — *Model-Free Implied Volatility and Its Information Content* (The Review of Financial Studies, 18(4), 1305-1342).
   - Derives the model-free implied volatility formulation (the mathematical basis for the modern CBOE VIX) and proves its superior information content over Black-Scholes IV.
