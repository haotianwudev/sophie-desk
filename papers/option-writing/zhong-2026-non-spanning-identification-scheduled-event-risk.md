---
title: "Non-Spanning Identification of Scheduled Event Risk in Option Pricing"
authors: "Tenghan Zhong"
year: 2026
link: "https://arxiv.org/abs/2606.12872"
area: event-risk
relevance: Medium
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Non-Spanning Identification of Scheduled Event Risk in Option Pricing

- **Authors:** Tenghan Zhong
- **Year:** 2026 (arXiv:2606.12872, June 2026)
- **Link:** [https://arxiv.org/abs/2606.12872](https://arxiv.org/abs/2606.12872)
- **PDF:** zhong-2026-non-spanning-identification-scheduled-event-risk.pdf (open-access copy, arXiv)

## Testable Hypothesis

Separating the continuous no-event implied volatility surface from scheduled event jumps via a non-spanning expiry identification protocol isolates macroeconomic announcement variance markups (FOMC, CPI, NFP) in short-dated SPX options and improves out-of-sample pricing of event-volatility option combinations.

## Summary

Examines short-dated S&P 500 index options (SPXW) from May 2022 to August 2025 around major scheduled macroeconomic announcements (FOMC, CPI, Non-Farm Payrolls). Formulates a non-spanning identification protocol where non-spanning expiries identify the baseline continuous volatility surface while event-spanning quotes calibrate the scheduled deterministic event jump. Demonstrates that explicit scheduled event-jump specifications consistently improve held-out event-spanning option pricing and event-volatility straddle/strangle pricing over standard surface smoothing, preventing continuous volatility models from misattributing event markups to baseline diffusion variance.

## Detailed Summary

### 1. Methodology & Non-Spanning Identification Protocol

Zhong investigates the pricing of scheduled macroeconomic announcements in short-dated S&P 500 index options (SPX/SPXW) and resolves an identification problem in option surface calibration: flexible continuous volatility surfaces (e.g. polynomial, SSVI) fitted across all expiries artificially absorb discrete event markups, obscuring the true magnitude of scheduled jump risk.

**The Non-Spanning Protocol:**
For a scheduled announcement date $e$ observed at pre-event quote date $t < e$:
1. **Non-Spanning Contracts ($\mathcal{D}_{t,e}^0, T_i < e$)**: Expiring strictly before the announcement; used exclusively to fit the continuous no-event variance-rate surface:
   $$w_c(k, \tau) = \tau \sigma_c^2(k, \tau), \quad \log \sigma_c^2(k, \tau) = b(k, \tau)^\top \beta$$
2. **Event-Spanning Training Contracts ($\mathcal{D}_{t,e}^{1,tr}, T_i \ge e$)**: Spanning the announcement; used exclusively to calibrate the deterministic-time scheduled jump $J_{e,t}$.
3. **Held-Out Event-Spanning Contracts ($\mathcal{D}_{t,e}^{1,ho}$)**: 25% stratified held-out sample per event, used solely to evaluate out-of-sample pricing performance without data contamination.

**Scheduled Event-Jump Specifications:**
- **Event Gaussian**: $J_{e,t} \sim N(-s_e^2/2, s_e^2)$ with single jump scale $s_e > 0$.
- **Event Mixture**: 2-component Gaussian mixture $\sum_{m=1}^2 p_m N(\mu_m, \sigma_m^2)$, martingale-normalized by $A_e = \log \sum p_m \exp(\mu_m + \sigma_m^2/2)$.
- **Event Neural-MDN**: 4-component Mixture Density Network predicting mixture weights, means, and scales from non-spanning pre-event conditioning features (leave-one-event-out).
- **Event Neural-MDN-Calibrated**: Neural mixture shape with target-event single scale parameter $\gamma_e \in [0, 5]$.

### 2. Data & Sample Panel

- **Sample Period**: May 1, 2022 to August 29, 2025 (post-daily expiration introduction on SPXW).
- **Universe**: PM-settled SPX index options from OptionMetrics Ivy DB, filtered for positive bids, relative spreads $\le 0.60$, and log-moneyness $k \in [-0.35, 0.35]$ using out-of-the-money puts/calls plus near-ATM representatives.
- **Event Panel**: 101 usable scheduled macroeconomic announcements (39 CPI releases, 23 FOMC rate decisions, 39 Non-Farm Payroll reports) yielding **11,135 held-out event-spanning quotes**.

### 3. Key Quantitative Results

#### Held-Out Pricing Performance Across Specifications (Table 1 & Figure 2)
- **No-Event Baseline (No-Event Poly)**: Price MAE $=\$7.917$, Spread-normalized MAE $= 69.231$, Median Spread MAE $= 14.008$, Bid-Ask Containment $= 1.58\%$, IV MAE $= 0.1080$, Median IV Error $= 0.0561$.
- **Event Gaussian**: Price MAE $=\$7.299$, Spread MAE $= 66.918$, Median Spread MAE $= 9.417$, Bid-Ask Containment $= 3.45\%$, IV MAE $= 0.0970$, Median IV Error $= 0.0370$.
- **Event Mixture**: Best overall pricing accuracy across all metrics:
  - Price MAE $=\mathbf{\$7.255}$, Spread MAE $=\mathbf{66.601}$, Median Spread MAE $=\mathbf{8.915}$, Bid-Ask Containment $=\mathbf{4.62\%}$, IV MAE $=\mathbf{0.0926}$, Median IV Error $=\mathbf{0.0305}$.
  - Event-level paired bootstrap (Figure 2) confirms statistically significant reductions over No-Event Poly: Price difference $-\$0.743$, Spread difference $-3.074$, and IV difference $-0.0179$ ($p < 0.05$).

#### Contaminated-Surface Diagnostic Failure Mode (Table 2 Panel B)
- When event-spanning training quotes are allowed into the continuous surface fit, held-out price MAE artificially collapses from $\$7.255$ to **$\$0.380$** and spread MAE collapses to **$2.962$**.
- This proves that standard surface smoothing simply overfits local interpolation and absorbs event premia rather than identifying the structural scheduled jump.

#### Announcement Heterogeneity & Jump Scale (Table 3)
- **CPI Releases ($N=39$)**: Largest priced event risk. Median spread $\Delta = 5.793$, IV MAE $\Delta = 0.0205$, Bid-Ask lift $+3.66\%$, jump standard deviation $= \mathbf{0.91\%}$, lower-bound share only $20.5\%$.
- **FOMC Decisions ($N=23$)**: Strong priced event risk. Median spread $\Delta = 7.197$, IV MAE $\Delta = 0.0150$, Bid-Ask lift $+4.34\%$, jump standard deviation $= \mathbf{0.81\%}$, lower-bound share $30.4\%$.
- **NFP Reports ($N=39$)**: Substantially weaker priced event risk. Median spread $\Delta = 2.903$, IV MAE $\Delta = 0.0094$, Bid-Ask lift $+1.49\%$, jump standard deviation $= \mathbf{0.10\%}$, with **$66.7\%$ of events hitting the lower bound**. Options market prices minimal discrete event jump for employment reports compared to CPI and FOMC.

#### Option-Combination Errors & Skew vs. Volatility (Figure 3)
- Explicit scheduled jumps dramatically reduce pricing errors in **ATM straddles** and **25-delta strangles** (pure volatility and convexity exposure).
- Jumps provide **zero pricing improvement in 25-delta risk reversals**, demonstrating that short-dated macro announcement pricing is driven by direction-agnostic event variance rather than directional skew.

#### Scale vs. Shape Transfer in Neural Benchmarks (Table 4 & Figure 4)
- Pure cross-event shape amortization (Neural-MDN) reduces IV error by only $0.0048$.
- Target-event scale calibration ($\gamma_e$) provides the majority of the gain ($0.0138$), confirming that event jump scale cannot be purely amortized and must be identified from target-event options quotes.

### 4. Relevance to Option Research

Zhong's findings provide actionable guidelines for macro calendar event-gating and short-tenor strategy execution in `sophie-option-research`:
1. **Macro Calendar Event Gating**: CPI releases ($0.91\%$ jump std) and FOMC meetings ($0.81\%$ jump std) embed significant unhedgeable jump variance that cannot be absorbed by continuous delta-hedging. Systematic option selling strategies (0–7 DTE short puts, straddles, and iron condors in `08_rolling.py` / `lab/features.py`) should systematically **gate/pause new entries or widen wing widths** on days crossing CPI and FOMC releases.
2. **NFP Low-Risk Exemption**: Non-Farm Payrolls exhibit a $66.7\%$ lower-bound share and only $0.10\%$ jump std, indicating that employment releases do not warrant the same restrictive hedging suspensions as inflation and central bank decisions.
3. **Volatility vs. Directional Hedging**: Because announcement premia are concentrated entirely in straddles/strangles rather than risk reversals, traders should manage gamma/vega size rather than attempting directional delta-tilt adjustments ahead of macro events.

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** Econometric identification framework that isolates scheduled macroeconomic event risk (FOMC, CPI, NFP) from continuous baseline diffusion variance. Demonstrates that CPI and FOMC carry substantial priced event jump variance concentrated in direction-agnostic volatility combinations (straddles/strangles) rather than directional skew, directly supporting macro calendar event-gating in `sophie-option-research`.

## Notable Citations to Follow Up

1. **Londono, Juan M., and Mehrdad Samadi (2023)** — *The Price of Macroeconomic Uncertainty: Evidence from Daily Options* (Federal Reserve Board IFDP 1376).
   - Uses same-day and 1-day SPX expirations to estimate release-specific volatility premia across major macroeconomic announcements.
2. **Wright, Jonathan H. (2020)** — *Event-Day Options* (NBER Working Paper 28306).
   - Formulates option-implied variance risk premium dynamics and jump risk compensation specifically spanning FOMC and employment report release days.
3. **Alexiou, Lykourgos, Amit Goyal, Alexandros Kostakis, and Leonidas Rompolis (2025)** — *Pricing Event Risk: Evidence from Concave Implied Volatility Curves* (Review of Finance, 29(4), 963-1007).
   - Demonstrates that scheduled event announcements induce distinct concavity, bimodality, and elevated crash premia in short-term risk-neutral state-price densities.
