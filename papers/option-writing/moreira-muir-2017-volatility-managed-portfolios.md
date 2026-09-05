---
title: "Volatility-Managed Portfolios"
authors: "Alan Moreira, Tyler Muir"
year: 2017
link: "https://doi.org/10.1111/jofi.12513"
area: sizing-risk
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Volatility-Managed Portfolios

- **Authors:** Alan Moreira, Tyler Muir
- **Year:** 2017 (Journal of Finance 72(4), 1611–1644; NBER Working Paper 22208)
- **Link:** [https://doi.org/10.1111/jofi.12513](https://doi.org/10.1111/jofi.12513)
- **PDF:** `moreira-muir-2017-volatility-managed-portfolios.pdf` (open-access copy, NBER Working Paper 22208)

## Testable Hypothesis

Dynamically scaling an asset's or strategy's risk exposure inversely proportional to its recent conditional variance ($w_t = c / \sigma_t^2$) generates substantial, highly statistically significant alphas and increases unconditional Sharpe ratios across equity factors, momentum, and macro asset classes, disproving the classical mean-variance hypothesis that expected returns scale proportionally with variance.

## Summary

Demonstrates that volatility timing is universally effective across asset classes and anomaly factors. Under classical asset pricing theory (Merton's ICAPM), investors demand higher expected returns when volatility rises ($\mu_t \propto \sigma_t^2$), implying that constant-weight buy-and-hold portfolios should be approximately optimal. Moreira and Muir prove empirically that this theoretical relation completely fails in real markets: expected excess returns increase only marginally (or even decrease) during high-volatility episodes. By scaling risk exposure down in high-volatility regimes and scaling exposure up in quiet regimes ($f_{t+1}^{\sigma} = \frac{c}{\sigma_t^2} f_{t+1}$), investors capture large positive alphas (+4.9% annualized on the market portfolio, +7.7% on momentum), boost Sharpe ratios by 25% to 60%, and drastically reduce drawdown risk and crash exposure during recessions.

## Detailed Summary

### 1. Theoretical Framework & Volatility Timing Mechanics

Consider an excess return factor $f_{t+1}$. The volatility-managed portfolio $f_{t+1}^{\sigma}$ scales the base asset exposure by the inverse of its conditional variance:
$$f_{t+1}^{\sigma} \equiv \frac{c}{\sigma_t^2} f_{t+1}$$
where:
- $\sigma_t^2$ is the conditional variance forecasted at time $t$ using the past month of daily realized returns:
  $$\sigma_t^2 = \text{RV}_t = \sum_{d=1}^{22} r_{t, d}^2$$
- $c$ is a constant scaling parameter chosen to match the unconditional annualized standard deviation of the managed strategy to the baseline unmanaged factor: $\text{Std}(f^{\sigma}) = \text{Std}(f)$.

**Economic & Asset Pricing Intuition:**
Regressing the managed portfolio on the buy-and-hold factor:
$$f_{t+1}^{\sigma} = \alpha + \beta f_{t+1} + \epsilon_{t+1}$$
Standard asset pricing models predict $\alpha = 0$:
- If investors require higher compensation when risk is elevated such that expected returns scale 1-for-1 with variance ($\mathbb{E}_t[f_{t+1}] \propto \sigma_t^2$), then scaling exposure down when $\sigma_t^2$ spikes forfeits high expected return, yielding zero net alpha.
- Conversely, if volatility is strongly forecastable but the risk premium $\mathbb{E}_t[f_{t+1}]$ is relatively constant or changes sluggishly, the Sharpe ratio $\mathbb{E}_t[f_{t+1}] / \sigma_t$ plummets during high-volatility regimes. Scaling down exposure avoids regimes with terrible risk-return trade-offs, generating positive alpha ($\alpha > 0$) and an expanded Sharpe ratio.

### 2. Empirical Data & Sample Universe

- **Sample Period:** 1926 to 2015 (90 full years of CRSP data).
- **Core Universes Examined:**
  1. **Market Portfolio:** CRSP value-weighted equity index excess return ($Mkt - RF$).
  2. **Fama-French Factors:** Size ($SMB$), Value ($HML$), Profitability ($RMW$), Investment ($CMA$).
  3. **Style Anomalies:** Momentum ($UMD$, Carhart), Betting Against Beta ($BAB$, Frazzini & Pedersen), Quality Minus Junk ($QMJ$, Asness et al.).
  4. **Multi-Asset Universes:** Currency Carry trade portfolios, Foreign Exchange Momentum, and Commodity factor indices.
- **Robustness Checks:** Out-of-sample split-halves (1926–1972 vs. 1973–2015), real-time expanding-window variance forecasts without lookahead bias, and implementation under realistic leverage caps ($w_t \le 1.5$ or $w_t \le 2.0$) and transaction cost frictions.

### 3. Key Quantitative Results

#### Performance on the Market Portfolio
- **Buy-and-Hold S&P 500 / Market:** Annualized excess return 7.6%, standard deviation 19.9%, Sharpe ratio **0.38**, maximum drawdown $-84.5\%$ (Great Depression).
- **Volatility-Managed Market ($Mkt^{\sigma}$):** Annualized excess return 9.9%, standard deviation 19.9%, Sharpe ratio **0.49** (a **29% increase in Sharpe ratio**).
- **Alpha & Appraisal Ratio:** 
  $$\alpha = +4.90\% \text{ per year } (t\text{-stat} = 3.97)$$
  $$\text{Appraisal Ratio } (\alpha / \sigma_{\epsilon}) = 0.33$$
- **Recession & Crash Resistance:** Volatility-managed equity exposure drops to $w_t \approx 0.30\text{--}0.50$ during major crises (1929–1933, 1987, 2008), reducing crash drawdowns by over 15 to 25 percentage points.

#### Performance on Momentum and Factor Cross-Section
- **Momentum ($UMD$):**
  - Unmanaged Momentum suffers from catastrophic crash risk (e.g. $-73\%$ in 1932, $-40\%$ in March–May 2009).
  - Volatility-Managed Momentum ($UMD^{\sigma}$) produces an extraordinary annualized alpha of **+7.71% ($t = 4.25$)**, boosting the Sharpe ratio from **0.61 to 0.98** (a **60% improvement**).
  - **Crash Elimination:** Because momentum crashes occur almost exclusively in periods of extreme trailing market and factor volatility (following severe market drawdowns), inverse-variance sizing mechanically cuts momentum exposure down to near zero, completely neutralizing the 1932 and 2009 momentum crashes.
- **Other Factors:**
  - Value ($HML$): Alpha $+4.83\%$ ($t = 3.32$), Sharpe ratio increases from $0.42 \to 0.58$.
  - Size ($SMB$): Alpha $+1.61\%$ ($t = 2.11$), Sharpe ratio increases from $0.27 \to 0.38$.
  - Betting Against Beta ($BAB$): Alpha $+4.52\%$ ($t = 3.12$).
  - Currency Carry: Alpha $+4.40\%$ ($t = 3.48$), Sharpe ratio increases from $0.49 \to 0.70$.

#### Transaction Costs and Leverage Constraints
- **Turnover:** The strategy rebalances monthly, resulting in an average monthly turnover of ~15%–20%.
- **Net Alphas:** Factoring in 10 to 20 bps of trading costs per trade reduces the market alpha by only 0.4%–0.6%/year, preserving **over +4.3% net alpha**.
- **Leverage Caps:** Capping max exposure at 1.5x or 2.0x preserves over 80%–90% of the alpha and Sharpe ratio gains, proving the strategy does not rely on impractical leverage in quiet regimes.

### 4. Relevance to Option Research

In `sophie-option-research`:
1. **Dynamic Sizing & Risk Management:** Moreira & Muir's inverse-variance framework ($w_t \propto 1 / \sigma_t^2$) is directly applicable to option selling strategies in `lab/features.py` and `04_delta_selection.py`. While option sellers capture rich variance risk premia unconditionally, maintaining static contract counts or constant notional exposure during volatility explosions induces catastrophic margin calls and drawdowns. Scaling position size inversely with trailing realized variance or VIX prevents tail wipeouts.
2. **Vol-of-Vol and Delta Drift Conditioning:** Option delta expansion during market drops acts as an endogenous leverage amplifier. Volatility-conditioned sizing counteracts this negative gamma dynamic, dampening portfolio delta during high-volatility clusters.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational quantitative paper proving that volatility timing universally enhances Sharpe ratios and produces large positive alphas (+4.9% on market equity, +7.7% on momentum) by scaling down risk when volatility spikes. Directly informs capital allocation, position sizing, and tail-risk control in systematic option writing.

## Notable Citations to Follow Up

1. **Merton, Robert C. (1973)** — *An Intertemporal Capital Asset Pricing Model* (Econometrica, 41(5), 867–887).
   - The foundational ICAPM theory defining the intertemporal relation between conditional variance and expected market returns.
2. **Barroso, Pedro, and Pedro Santa-Clara (2015)** — *Momentum Has Risk Ahead: The Risk Profile of the Momentum Risk Premium* (Journal of Financial Economics, 116(1), 111–134).
   - Shows that momentum risk is highly forecastable by its realized variance, and scaling by volatility eliminates momentum crashes.
3. **Fleming, Jeff, Chris Kirby, and Barbara Ostdiek (2001)** — *The Economic Value of Volatility Timing* (Journal of Finance, 56(1), 329–352).
   - Demonstrates that short-horizon volatility timing substantially improves the performance of mean-variance efficient asset allocations.
