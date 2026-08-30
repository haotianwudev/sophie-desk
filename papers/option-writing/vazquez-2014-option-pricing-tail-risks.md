# Option Pricing, Historical Volatility and Tail Risks

- **Authors:** Samuel E. Vazquez
- **Year:** 2014
- **Link:** [https://arxiv.org/abs/1402.1255](https://arxiv.org/abs/1402.1255)
- **PDF:** `vazquez-2014-option-pricing-tail-risks.pdf` (open-access copy)

## Testable Hypothesis

Pricing equity index options using historical volatility plus explicit risk premia for tail events (skew and kurtosis) accurately reconstructs the SPX implied volatility surface, indicating that premium sellers are primarily compensated for unhedged jump/kurtosis risk rather than diffusion volatility.

## Summary

Formulates an option pricing model that decomposes the volatility risk premium into distinct premiums for convexity, skew, and kurtosis. Shows that index option skew and elevated implied volatility are driven by market-wide aversion to large tail drops, which systematic premium sellers absorb.

## Detailed Summary

### 1. Methodology & Tail Risk Pricing Framework

Vazquez formulates an option pricing architecture that directly connects time-series historical volatility forecasts (under the physical/real-world measure $\mathbb{P}$) to the market volatility surface (under the risk-neutral/martingale pricing measure $\mathbb{Q}$) by explicitly pricing unhedgable tail risks.

1. **Economic Origin of Tail Premia**:
   - Option traders mark to market in discrete time, face capital and margin constraints, and cannot continuously delta-hedge large discrete shocks (3–5 sigma tail moves).
   - A short-gamma or short-higher-moment position suffers severe non-linear losses during tail drops ($\lim_{|\epsilon_t| \to \infty} \Delta P_t \propto -\epsilon_t^2, -\epsilon_t^3, -\epsilon_t^4$). To induce market makers and option sellers to supply liquidity, option P&L under $\mathbb{P}$ must earn positive drift governed by the market prices of tail risk:
     $$\mathbb{E}_t[\Delta P_{t+\Delta t}^{(2)}] = -\lambda_2 \quad (\text{Convexity / Gamma Risk Premium})$$
     $$\mathbb{E}_t[\Delta P_{t+\Delta t}^{(3)}] = \lambda_3 \quad (\text{Skew Risk Premium})$$
     $$\mathbb{E}_t[\Delta P_{t+\Delta t}^{(4)}] = -\lambda_4 \quad (\text{Kurtosis Risk Premium})$$
2. **Multi-Timescale Asymmetric GARCH & Martingale Mapping**:
   - The underlying asset dynamics are modeled via multi-scale asymmetric GARCH with exponential moving average (EMA) filters to capture long memory in volatility.
   - Using the Feynman-Kac theorem, the real-world PDE is mapped into a continuous-time stochastic volatility model under $\mathbb{Q}$.
3. **Bergomi-Guyon Vol-of-Vol Expansion Calibration**:
   - Closed-form approximations for implied moments up to second order in volatility-of-volatility (vol-of-vol) are derived via the Bergomi-Guyon (2011) expansion.
   - This allows independent and fast calibration: $\lambda_2$ is calibrated to the variance swap term structure, $\lambda_3$ to the implied skew across maturities, and $\lambda_4$ to the implied kurtosis.
   - The kurtosis premium $\lambda_4$ empirically saturates a theoretical consistency bound, reducing the required free calibration parameters to just two: convexity ($\lambda_2$) and skew ($\lambda_3$).

### 2. Data & Universe

- **Sample Period**: 2005 – 2014 (encompassing the 2008 Global Financial Crisis and the post-crisis recovery).
- **Universe & Data Sources**:
  - Daily closing mid-prices of European S&P 500 index options (`SPX`) from OptionMetrics / CBOE across the entire moneyness spectrum ($|\Delta| \in [0.001, 0.999]$) and maturities ranging from 26 days to 2.5 years.
  - S&P 500 E-mini futures (`SPMINI`) and CBOE VIX futures (`VIX`) closing prices for empirical P&L and risk attribution comparisons.

### 3. Key Quantitative Results

#### VIX Futures vs. Equities Risk Premium (Figure 1, Figure 2)
- Short front-month VIX futures deliver an annualized Sharpe ratio of **0.96** compared to **0.57** for long SPMINI futures when both are risk-managed to maintain a constant $1.00 daily risk on a 20-day rolling scale.
- Non-linear residual conditioning reveals that the outperformance of short VIX futures is directly driven by bearing quadratic negative gamma exposure to large negative equity shocks.

#### Skew Risk Premium ($\lambda_3$) & Implied Skew Calibration (Figure 4, Figure 14)
- A pure physical GARCH model without tail premia ($\lambda_2 = \lambda_3 = 0$) completely fails to explain the market implied volatility skew, because physical standardized return innovations exhibit negligible skewness ($\mathbb{E}[\epsilon^3] \approx 0$).
- Empirically, the skew risk premium $\lambda_3$ is **persistently positive and stable over time** throughout 2005–2014, demonstrating that the steepness of OTM index put volatility is an asset pricing compensation for crash aversion rather than statistical physical return asymmetry.

#### Convexity Risk Premium ($\lambda_2$) Dynamics (Figure 13)
- The convexity/gamma premium $\lambda_2$ is positive on average during calm and trending bull markets, but exhibits strong regime shifts, compressing and turning negative during major volatility spikes and liquidity crises (e.g. 2008 GFC).

#### Kurtosis Bound Saturation & Parameter Reduction (Figure 5, Figure 15)
- The kurtosis risk premium $\lambda_4$ saturates its theoretical inequality bound across almost all trading dates. This confirms that implied kurtosis (vol-of-vol) is structurally bound to $\lambda_2$ and $\lambda_3$, allowing full surface generation using only two calibrated risk premia parameters.
- Monte Carlo simulations with calibrated $(\lambda_2, \lambda_3)$ accurately reconstruct the full SPX implied volatility smile across 26-day and 54-day expiries (Figures 6–8).

### 4. Relevance to Option Research

In `sophie-option-research`, Vazquez (2014) provides the foundational theoretical and econometric bridge between physical volatility forecasting and option-selling strategy design:
1. **Multi-Component Edge Attribution**: Proves that the profitability of systematic option writing (`src/lab/backtest.py` and `src/lab/strategy.py`) does not stem merely from flat variance harvesting ($\lambda_2$), but is heavily anchored by the persistent skew premium ($\lambda_3$) and bound kurtosis premium ($\lambda_4$). This explains why OTM put writing generates higher risk-adjusted returns than ATM straddles.
2. **GARCH & Volatility Feature Engineering**: Directly informs feature extraction in `src/lab/features.py` and `src/lab/market_data.py`, demonstrating how multi-timescale EMA filters and asymmetric return conditioning can be combined with implied moments (VIX / variance swap term structure) to generate accurate strike-specific pricing signals.
3. **Regime-Aware Strategy Selection**: Because the convexity premium $\lambda_2$ collapses during crises while the skew premium $\lambda_3$ remains elevated, strategy engines in `src/lab/experiments.py` can dynamically transition from short-dated ATM structures to deep OTM vertical credit spreads when market stress alters the relative pricing of $\lambda_2$ vs. $\lambda_3$.

