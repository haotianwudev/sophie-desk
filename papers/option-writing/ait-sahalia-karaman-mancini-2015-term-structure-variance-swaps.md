---
title: "The Term Structure of Variance Swaps and Risk Premia"
authors: "Yacine Aït-Sahalia, Mustafa Karaman, Loriano Mancini"
year: 2015
link: "https://doi.org/10.1016/j.jeconom.2020.03.002"
area: vrp-measurement
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The Term Structure of Variance Swaps and Risk Premia

- **Authors:** Yacine Aït-Sahalia, Mustafa Karaman, Loriano Mancini
- **Year:** 2015 (Published in *Journal of Econometrics* 219(2), 2020, 204–230; Swiss Finance Institute Research Paper No. 18-37; circulated as *The Term Structure of Variance Swaps, Risk Premia and the Expectations Hypothesis*, 2012–2015)
- **Link:** [https://doi.org/10.1016/j.jeconom.2020.03.002](https://doi.org/10.1016/j.jeconom.2020.03.002)
- **PDF:** `ait-sahalia-karaman-mancini-2015-term-structure-variance-swaps.pdf` (Open-access AEA/seminar manuscript)

## Testable Hypothesis

Variance swap rates across different maturities embed separate diffusive volatility and discrete jump risk premia; the integrated variance risk premium (IVRP) is structurally negative and downward-sloping across the maturity curve, with short-term variance risk premia dominated by tail jump fears that spike following market drops, while long-term variance risk premia reflect persistent diffusive economic uncertainty.

## Summary

This paper investigates the term structure of over-the-counter variance swaps (VS) written on the S&P 500 across 2-, 3-, 6-, 12-, and 24-month maturities from 1996 to 2010. Using both model-free diagnostics and a continuous-time two-factor stochastic volatility model with co-jumps in asset prices and variance (SV2F-PJ-VJ), the authors estimate objective and risk-neutral dynamics via closed-form likelihood approximations. They show that two principal components (level and slope) explain 99.8% of variance swap curve variation. The ex-ante integrated variance risk premium ($IVRP_t = E_t^{\mathbb{P}}[QV_{t, t+\tau}] - E_t^{\mathbb{Q}}[QV_{t, t+\tau}]$) is unconditionally negative across all maturities, averaging -2.9% to -5.0% in annualized variance units for 24-month contracts against a baseline spot variance of 4.0%. Downside price jumps account for the sharp spikes in short-term variance risk premia following market crashes, while long-term variance premia are more persistent. Finally, a rule-based trading strategy conditioning short variance swap positions on model-implied Sharpe ratios avoids crisis drawdowns and achieves out-of-sample Sharpe ratios between 1.84 and 2.98 across 6- to 24-month horizons.

## Detailed Summary

### 1. Theoretical Framework & Jump-Diffusion Term Structure Model

The underlying equity index price $S_t$ and its continuous variance state vector follow a continuous-time jump-diffusion on a filtered probability space $(\Omega, \mathcal{F}, (\mathcal{F}_t), \mathbb{P})$:
$$d\ln S_t = \left( r_t - \delta_t - \lambda_t \mu_J^\mathbb{P} + \eta_t \right) dt + \sqrt{v_t} dW_{1,t}^\mathbb{P} + J_t dN_t$$
where $r_t$ is the risk-free rate, $\delta_t$ is the dividend yield, $N_t$ is a Poisson process with state-dependent arrival intensity $\lambda_t = \lambda_0 + \lambda_1 v_t$, and $J_t$ is the jump size distributed with mean $\mu_J^\mathbb{P} = E^\mathbb{P}[e^{J_t} - 1]$.

To capture both high-frequency transient volatility bursts and long-term persistent regime shifts, total diffusive variance $v_t$ is modeled as a two-factor process:
$$v_t = v_{1,t} + v_{2,t}$$
$$dv_{1,t} = \kappa_1 (\theta_1 - v_{1,t}) dt + \sigma_1 \sqrt{v_{1,t}} dW_{2,t}^\mathbb{P} + J_{v,t} dN_t$$
$$dv_{2,t} = \kappa_2 (\theta_2 - v_{2,t}) dt + \sigma_2 \sqrt{v_{2,t}} dW_{3,t}^\mathbb{P}$$
where $W_{1,t}^\mathbb{P}, W_{2,t}^\mathbb{P}, W_{3,t}^\mathbb{P}$ are standard Brownian motions with contemporaneous leverage correlations $\text{Corr}(dW_{1,t}^\mathbb{P}, dW_{2,t}^\mathbb{P}) = \rho_1$ and $\text{Corr}(dW_{1,t}^\mathbb{P}, dW_{3,t}^\mathbb{P}) = \rho_2$. Negative jumps in stock prices $J_t < 0$ are accompanied by simultaneous positive variance jumps $J_{v,t} > 0$.

Under the risk-neutral pricing measure $\mathbb{Q}$, the variance swap rate $VS_{t, t+\tau}$ equals the risk-neutral expected quadratic variation over horizon $\tau$:
$$VS_{t, t+\tau} = \frac{1}{\tau} E_t^\mathbb{Q} \left[ \int_t^{t+\tau} v_s ds + \sum_{t < s \le t+\tau} J_s^2 \right] = \alpha(\tau) + \beta_1(\tau) v_{1,t} + \beta_2(\tau) v_{2,t}$$
Because the model is affine, the term structure of variance swap rates is an exact linear function of the latent volatility factors. The Integrated Variance Risk Premium over horizon $\tau$ is defined as:
$$IVRP_{t, t+\tau} = E_t^\mathbb{P}[QV_{t, t+\tau}] - E_t^\mathbb{Q}[QV_{t, t+\tau}] = E_t^\mathbb{P}[QV_{t, t+\tau}] - \tau \cdot VS_{t, t+\tau}$$

### 2. Data, Sample Period & Model-Free Empirical Facts

- **Sample Period**: January 4, 1996 to September 2, 2010 (3,624 daily observations).
  - In-sample estimation: January 4, 1996 to April 2, 2007 (2,823 days).
  - Out-of-sample evaluation: April 3, 2007 to September 2, 2010 (801 days, spanning the 2007–2009 Global Financial Crisis).
- **Asset Universe**: Actual OTC variance swap quotes on the S&P 500 across five fixed tenors: 2, 3, 6, 12, and 24 months, matched with daily S&P 500 total returns, CBOE VIX, and Treasury zero curves.
- **Model-Free Stylized Facts**:
  1. **Term Structure Level & Persistence**: Average variance swap rates increase monotonically with maturity: 2-month rates average 20.89% (vol units), 3-month averages 21.05%, 6-month averages 21.43%, 12-month averages 21.89%, and 24-month averages 22.42%. First-order daily autocorrelation rises from 0.984 (2-month) to 0.993 (24-month).
  2. **Volatility of Volatility & Skewness Decay**: Volatility of variance swap rates declines monotonically across horizons: standard deviation falls from 7.91% at 2 months to 5.76% at 24 months; skewness drops from 2.05 to 1.48; kurtosis declines from 9.94 to 6.30.
  3. **Principal Component Analysis**: The first principal component (level) explains 94.6% of the variance across maturities, and the second component (slope) explains an additional 5.2%. Together, two factors explain **99.8%** of the entire variance swap term structure.
  4. **Model-Free Jump Identification**: Discrepancies between synthetic log-contract replicating portfolios (VIX-style indices) and realized swap rates reveal that jump risk accounts for substantial pricing wedges, especially during volatile periods.

### 3. Key Quantitative Results

#### Term Structure of the Variance Risk Premium
- **Persistent Downward Slope**: Unconditional $IVRP_{t, t+\tau}$ is negative across all horizons and deepens with maturity. In out-of-sample data (2007–2010), annualized average IVRP is **-2.9%** (variance units) for 24-month contracts, reaching as deep as **-5.0%** during market turmoil. This represents an enormous premium relative to the sample average spot variance of 4.0% (corresponding to 20% annualized vol).
- **Asymmetric Crash Response**: Following market crashes (e.g., Autumn 1998 LTCM, September 2008 Lehman collapse), short-term IVRP plunges violently into deep negative territory as investors frantically buy short-dated crash insurance. The jump risk component accounts for over 70% of the IVRP movement at 2-month horizons during stress events. For long horizons (12- to 24-month), the IVRP shift is more gradual but significantly more persistent.

#### Macroeconomic & Factor Determinants of the Term Structure (Table 6)
- Regressing $IVRP_{t, t+\tau}$ on market state variables reveals distinct transmission mechanisms:
  - **S&P 500 Return**: A contemporaneous negative market return widens (makes more negative) the IVRP sharply at the short end ($\beta = 0.28, t = 4.1$ at 2 months), but this effect decays to near zero and becomes statistically insignificant past 12 months.
  - **VIX Level**: VIX increases uniformly shift the entire IVRP term structure downward across all tenors ($\beta \approx -0.15$ to $-0.18$, all $t < -6.0$), acting as a classic level factor.
  - **Corporate Credit Spread ($CS_{\text{corp}}$)**: Corporate credit widening significantly deepens the negative IVRP, reinforcing the procyclical nature of variance risk compensation.

#### Trading Performance & Timing Strategies (Table 7)
- **Unconditional Short Variance Swap Strategy**:
  - In-sample (1996–2007), unconditionally shorting variance swaps yields annualized Sharpe ratios of **0.59** (2-mo), **0.61** (3-mo), **0.68** (6-mo), **0.85** (12-mo), and **0.67** (24-mo), vastly outperforming long S&P 500 buy-and-hold (Sharpe 0.13 to 0.27).
  - Out-of-sample (2007–2010), unconditional shorting suffers severe drawdown during the 2008 crash, dropping Sharpe ratios to 0.03–0.23.
- **Conditional Model-Timed Short Strategy (Threshold $n = 1.0$)**:
  - Conditioning short positions on model-implied expected profits ($VS_{t, t+\tau} - E_t^\mathbb{P}[QV_{t, t+\tau}] \ge 1.0 \times \sigma$):
  - In-sample Sharpe ratios surge to **1.47** (2-mo), **3.16** (3-mo), **2.05** (6-mo), **2.21** (12-mo), and **2.64** (24-mo).
  - Out-of-sample (2007–2010), conditional timing successfully gates exposure during the height of the crisis, generating stellar Sharpe ratios of **1.84** (6-mo), **2.47** (12-mo), and **2.98** (24-mo).

### 4. Relevance to Option Research

Aït-Sahalia, Karaman, and Mancini's findings directly support and validate several architectural components in `sophie-option-research`:
1. **Term Structure Selection for Systematic Harvesting**: The empirical fact that long-dated variance swaps (12- to 24-month) carry larger and more stable annualized IVRP (-2.9% to -5.0%) than short-dated contracts explains why pure unhedged short-dated option selling is prone to jump-shock blowouts. In backtests (`lab/engine.py`, `04_delta_selection.py`), managing the term-structure dimension rather than treating all tenors identically is critical to surviving regime switches.
2. **Conditional Variance Timing & Gating**: Validates the regime-filtering and skip mechanisms implemented in `01_equity_curve.py` and `lab/features.py`. Timing short-volatility exposure based on the spread between implied variance and objective forecasted variance ($E^\mathbb{P}[QV]$) prevents catastrophic drawdowns during market crashes, turning crisis-period out-of-sample Sharpe ratios from near zero (0.03) into 2.47–2.98.
3. **Decomposition of Jump vs Diffusive Risk**: Confirms that short-dated OTM put pricing reflects jump-tail risk compensation ($\lambda_1 v_t J_t$) rather than diffusive volatility alone, supporting tail-risk hedging models and sizing algorithms in `wysocki-2025-sizing-risk.md`.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Canonical empirical study of the variance swap term structure, proving that the variance risk premium is structurally negative, upward-sloping in price (downward-sloping in payoff), and driven by distinct jump versus diffusive components. Most importantly, it demonstrates that rule-based conditioning on model-forecasted IVRP avoids crash blowups and delivers out-of-sample Sharpe ratios above 2.0 through severe financial crises.

## Notable Citations to Follow Up

1. **Egloff, Daniel, Markus Leippold, and Liuren Wu (2010)** — *The Term Structure of Variance Swap Rates and Optimal Variance Swap Investments* (Journal of Financial and Quantitative Analysis, 45(5), 1279–1310).
   - Develops a structural dynamic asset allocation framework identifying two stochastic variance factors (fast-mean-reverting short end and slow-moving long end) that dictate optimal variance swap harvesting portfolios.
2. **Todorov, Viktor (2010)** — *Variance Risk-Premium Dynamics: The Role of Jumps* (Review of Financial Studies, 23(1), 345–383).
   - Formulates non-parametric high-frequency econometric tests isolating the discrete jump component of the variance risk premium over a one-month horizon.
3. **Carr, Peter, and Liuren Wu (2009)** — *Variance Risk Premia* (Review of Financial Studies, 22(3), 1311–1341).
   - Establishes the synthetic replication of variance swaps using static option portfolios and confirms the persistence of negative variance risk premia across equity indices.
