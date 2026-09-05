---
title: "Tails, Fears, and Risk Premia"
authors: "Tim Bollerslev, Viktor Todorov"
year: 2011
link: "https://doi.org/10.1111/j.1540-6261.2011.01695.x"
area: tail-risk
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Tails, Fears, and Risk Premia

- **Authors:** Tim Bollerslev, Viktor Todorov
- **Year:** 2011 (Journal of Finance 66(6), 2165–2211)
- **Link:** [https://doi.org/10.1111/j.1540-6261.2011.01695.x](https://doi.org/10.1111/j.1540-6261.2011.01695.x)
- **PDF:** `bollerslev-todorov-2011-tails-fears-risk-premia.pdf` (open-access copy, Duke University / author faculty archive)

## Testable Hypothesis

The historically large magnitude of both the equity risk premium (ERP) and the variance risk premium (VRP) is primarily driven by compensation for rare, catastrophic jump events (tail risk) rather than continuous Gaussian diffusive volatility; separating the jump tail component non-parametrically reveals an "Investor Fears" index that accounts for the vast majority of the time-varying variance risk premium.

## Summary

Develops a non-parametric Extreme Value Theory (EVT) framework that decomposes financial market price movements into continuous diffusion and discontinuous jumps under both the objective physical measure $\mathbb{P}$ (using high-frequency intraday S&P 500 futures) and the risk-neutral measure $\mathbb{Q}$ (using short-maturity out-of-the-money S&P 500 options). Under the physical measure $\mathbb{P}$, intraday return jumps are approximately symmetric between positive and negative moves. In stark contrast, under the risk-neutral measure $\mathbb{Q}$, negative jump intensities are priced with an extreme, time-varying premium. Bollerslev and Todorov construct an "Investor Fears" index that isolates this disaster compensation. They find that jump tail risk accounts for **over 60% to 80% of the total variance risk premium** and roughly two-thirds of the equity risk premium. Once tail risk is removed, the remaining diffusive risk premia align closely with standard consumption-based equilibrium models with modest, conventional risk aversion.

## Detailed Summary

### 1. Theoretical & Econometric Framework

The logarithmic price of the aggregate equity index $p_t = \ln S_t$ follows an Itô semi-martingale on $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}, \mathbb{P})$:
$$dp_t = \mu_t dt + \sigma_t dW_t + \int_{\mathbb{R}} x \, (\mu(dt, dx) - \nu_t(dx) dt)$$
where $W_t$ is a standard Brownian motion, $\sigma_t$ is the stochastic volatility process, and $\mu(dt, dx)$ is a Poisson random measure with compensator $\nu_t(dx) dt$ governing jump arrivals.

**Extreme Value Theory (EVT) Jump Tail Specification:**
Bollerslev and Todorov apply EVT to the jump compensators under both measures $\mathbb{P}$ and $\mathbb{Q}$. For large jumps $|x| > k$:
- Under $\mathbb{P}$ (Physical):
  $$\nu_t(dx) = \left( \phi_t^+ \alpha^+ e^{-\alpha^+ x} \mathbf{1}_{\{x > 0\}} + \phi_t^- \alpha^- e^{-\alpha^- |x|} \mathbf{1}_{\{x < 0\}} \right) dx$$
- Under $\mathbb{Q}$ (Risk-Neutral):
  $$\nu_t^{\mathbb{Q}}(dx) = \left( \psi_t^+ \alpha_{\mathbb{Q}}^+ e^{-\alpha_{\mathbb{Q}}^+ x} \mathbf{1}_{\{x > 0\}} + \psi_t^- \alpha_{\mathbb{Q}}^- e^{-\alpha_{\mathbb{Q}}^- |x|} \mathbf{1}_{\{x < 0\}} \right) dx$$

Here, $\phi_t^{\pm}$ and $\psi_t^{\pm}$ capture time-varying jump arrival intensities, while $\alpha^{\pm}$ and $\alpha_{\mathbb{Q}}^{\pm}$ govern the steepness (decay rate) of the jump tails.

**The Investor Fears Index:**
The wedge between the risk-neutral jump tail and the physical jump tail isolates the pricing of catastrophic events:
$$\text{Fear}_t \equiv \frac{\psi_t^-}{\phi_t^-}$$
Because option prices in the deep left tail reflect both physical crash probability and the marginal utility in crash states, the ratio $\psi_t^- / \phi_t^-$ represents the pure "fear markup" demanded by investors to absorb downside jump risk.

### 2. Empirical Data & High-Frequency Filtering

- **Physical Measure Data ($\mathbb{P}$):**
  - High-frequency tick data for S&P 500 futures (CME, Tick Data Inc.) spanning January 1990 to December 2008 (19 years, 4,751 trading days).
  - Sampled at 5-minute intervals (81 intraday observations per day, 8:35 to 15:15 CST).
  - Bipower variation and threshold techniques are used to separate continuous path variation from discrete intraday jumps.
- **Risk-Neutral Measure Data ($\mathbb{Q}$):**
  - Short-maturity out-of-the-money S&P 500 index options (OptionMetrics IvyDB, 1996–2008).
  - Focused on short horizons ($\tau \in [8, 45]$ days) and out-of-the-money puts ($K/S_t \le 0.95$) and calls ($K/S_t \ge 1.05$) to isolate pure tail behavior without at-the-money diffusive contamination.

### 3. Key Quantitative Results

#### Physical vs. Risk-Neutral Jump Asymmetry
- **Physical Symmetry ($\mathbb{P}$):** Under the actual data-generating process, the distribution of positive and negative jumps is nearly symmetric:
  - Left tail decay parameter: $\alpha^- \approx 32.5$.
  - Right tail decay parameter: $\alpha^+ \approx 34.0$.
  - Jump intensity ratio $\phi_t^- / \phi_t^+ \approx 1.05$. In reality, sharp upward market rallies and sharp downward market drops occur with comparable frequency and magnitude.
- **Risk-Neutral Distortion ($\mathbb{Q}$):** In the options market, this symmetry collapses completely:
  - Risk-neutral left tail decay: $\alpha_{\mathbb{Q}}^- \approx 18.2$ (much fatter tail than $\alpha^- = 32.5$).
  - Negative jump intensity is marked up dramatically: $\psi_t^- / \phi_t^-$ averages **between 3.5 and 6.0**, spiking to **over 10.0 to 15.0 during severe crisis episodes** (e.g. 1998 LTCM, September 2008 Lehman collapse).
  - Conversely, positive jump intensity is barely marked up: $\psi_t^+ / \phi_t^+ \approx 1.1\text{--}1.3$.

#### Decomposition of the Variance Risk Premium (VRP)
- Total variance risk premium is decomposed into continuous diffusive premium ($VRP_t^c$) and jump tail premium ($VRP_t^j$):
  $$VRP_t = \mathbb{E}_t^{\mathbb{Q}}[QV_{t, t+\tau}] - \mathbb{E}_t^{\mathbb{P}}[QV_{t, t+\tau}] = VRP_t^c + VRP_t^j$$
- **Jump Share of VRP:** Compensation for jump tail risk accounts for **over 65% to 80% of the unconditional average VRP**, with the left jump tail (crash risk) representing over **85% of the jump component**.
- Continuous diffusive volatility risk ($VRP_t^c$) accounts for only **20% to 35%** of the premium.
- The massive spike in the VIX during market panics is predominantly an explosion in the Investor Fears index ($\psi_t^- / \phi_t^-$) rather than an explosion in objective physical jump arrival intensity $\phi_t^-$.

#### Resolution of the Equity Risk Premium Puzzle
- Tail jump risk explains roughly **two-thirds (~65%) of the historical 6%–7% annualized equity risk premium**.
- When the jump tail component is subtracted, the residual diffusive equity risk premium is approximately **2.0% per year**, which is easily reconciled by standard CRRA utility with modest risk aversion parameters ($R \approx 2\text{--}3$), resolving the Mehra-Prescott equity premium puzzle.

### 4. Relevance to Option Research

In `sophie-option-research`:
1. **Targeting the Right Risk in Option Selling:** Directly explains why short put strategies (`01_equity_curve.py`, `04_delta_selection.py`) generate superior risk-adjusted alpha compared to delta-hedged straddles. The edge does not come from selling continuous variance; it comes from underwriting **catastrophic jump tail insurance** that investors overpay for due to time-varying "crash-o-phobia."
2. **Delta Selection & Tail Asymmetry:** Validates why 10–25 delta out-of-the-money puts carry the highest ratio of implied-to-realized variance: the risk-neutral left tail decay ($\alpha_{\mathbb{Q}}^- = 18.2$) is dramatically flatter than the physical tail ($\alpha^- = 32.5$), creating an expanding premium wedge as moneyness moves further out of the money.
3. **Regime Conditioning:** Demonstrates that monitoring the Investor Fears index ($\psi_t^- / \phi_t^-$) is vital for dynamic sizing rules: when Fear spikes above historical 90th percentiles, option writers must manage tail leverage to survive discontinuous drawdowns.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Crucial empirical proof that the Volatility Risk Premium is overwhelmingly a Jump Tail Risk Premium (65%–80% jump-driven). Explains why out-of-the-money put options command structural excess premia: option sellers are not earning compensation for day-to-day volatility fluctuations, but for providing liquidity against rare catastrophic crashes.

## Notable Citations to Follow Up

1. **Barndorff-Nielsen, Ole E., and Neil Shephard (2004)** — *Power and Bipower Variation with Quantum Jumps and Stochastic Volatility* (Econometrica, 72(4), 1163–1191).
   - Introduces the mathematical framework of realized bipower variation to separate continuous diffusion from discrete jumps.
2. **Rietz, Thomas A. (1988)** — *The Equity Risk Premium: A Solution* (Journal of Monetary Economics, 22(1), 117–131).
   - Pioneering economic theory proposing that disaster risk explains the equity risk premium puzzle.
3. **Bollerslev, Tim, Michael Gibson, and Hao Zhou (2011)** — *Dynamic Estimation of Volatility Risk Premia and Investor Risk Aversion from Option-Implied and Realized Volatilities* (Journal of Econometrics, 160(1), 235–245).
   - Explores the continuous time-series dynamics of the volatility risk premium and time-varying risk aversion.
