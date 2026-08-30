# Sizing the Risk: Kelly, VIX, and Hybrid Approaches in Put-Writing on Index Options

- **Authors:** Maciej Wysocki
- **Year:** 2025
- **Link:** [https://arxiv.org/abs/2508.16598](https://arxiv.org/abs/2508.16598)
- **PDF:** `wysocki-2025-sizing-risk.pdf` (open-access copy)

## Testable Hypothesis

Dynamic position sizing combining Kelly growth criteria with VIX regime scaling significantly reduces tail drawdown risk in short-dated SPX put-writing while preserving excess returns from the volatility risk premium.

## Summary

Evaluates systematic put-writing strategies on S&P 500 index options (SPXW) across various moneyness and sizing models. Finds that ultra-short-dated, far out-of-the-money short puts sized via hybrid Kelly/VIX scaling achieve optimal risk-adjusted growth without catastrophic blowup during market crashes.

## Detailed Summary

### 1. Methodology & Dynamic Sizing Framework

Wysocki investigates how systematic position sizing techniques can harvest the Volatility Risk Premium (VRP) in ultra-short-dated S&P 500 options (SPXW) while mitigating catastrophic left-tail liquidation risk.

1. **Position Sizing Architectures**:
   - **Monte Carlo Kelly Criterion Sizing**:
     Simulates forward paths of the underlying asset using historical volatility estimators (Close-to-Close, Garman-Klass, Yang-Zhang) to estimate the empirical probability of profit $p = \frac{1}{N}\sum \mathbf{1}_{r_i > 0}$, conditional expected gains $b = \mathbb{E}[r_i | r_i > 0]$, and conditional expected losses $a = \mathbb{E}[r_i | r_i \le 0]$. Position size in contracts $Q_t$ is computed via:
     $$Q_t = \left\lfloor \frac{PV_t}{M(P_t, S_t, K)} \cdot f(p, a, b) \right\rfloor$$
     incorporating broker margin requirements $M(P_t, S_t, K) = [P_t + \max(0.15 S_t - \max(0, K - S_t), 0.10 S_t)] \times 100$.
   - **VIX Percentile / Regime Sizing**:
     Scales position leverage dynamically based on the rolling percentile rank of implied volatility (standard 30-day VIX or 9-day VIX9D) over memory lookback horizons $L \in \{21, 42, 63, 126, 252\}$ trading days.
   - **Hybrid Kelly-VIX Sizing**:
     Blends the forward-looking Monte Carlo Kelly fraction with the real-time VIX percentile scaling factor to adjust exposure dynamically to prevailing volatility regimes.

2. **Strategy Grid & Execution**:
   - **Tenors**: 0, 1, 3, and 5 Days to Expiration (DTE) using daily-expiring SPXW options.
   - **Moneyness**: At-The-Money (ATM / 0%), 5% OTM, and 10% OTM.
   - **Execution & Evaluation**: High-frequency 1-minute intraday execution with explicit bid-ask spread friction. Evaluated using Annualized Return, Volatility, Information Ratio (IR), Maximum Drawdown, Value at Risk (VaR), Expected Shortfall (CVaR), and the Probabilistic Sharpe Ratio (PSR; Bailey & Lopez de Prado, 2012).

### 2. Data & Universe

- **Sample Period**: 2018 – 2024 (7 years total).
  - *In-Sample (IS)*: January 1, 2018 – December 31, 2023 (encompassing 2018 Volmageddon, Q4 2018 sell-off, 2020 COVID crash, and the 2022 bear market).
  - *Out-of-Sample (OOS)*: January 1, 2024 – December 31, 2024 (strong trending bull market).
- **Instruments & Data Sources**:
  - CBOE PM-settled SPXW weekly index options with 1-minute intraday OHLC bid/ask quotes and trades.
  - S&P 500 Index (`SPX`), CBOE Volatility Index (`VIX`), and CBOE 9-Day Volatility Index (`VIX9D`).
  - U.S. 3-Month Treasury Bill rate from FRED as the risk-free benchmark.
  - Reference Benchmarks: S&P 500 Buy & Hold (B&H) and the CBOE S&P 500 PutWrite Index (`PUT`).

### 3. Key Quantitative Results

#### Benchmark Baseline Performance (Table 1, Section 6)
- **In-Sample Characteristics (2018–2023)**: VIX9D daily return standard deviation is 0.1492 (skew 3.47, kurtosis 33.61) vs. VIX at 0.0875 (skew 2.89, kurtosis 24.78) and S&P 500 index at 0.0130 (skew –0.51, kurtosis 12.88).
- **Out-of-Sample Benchmarks (2024)**:
  - *S&P 500 Buy & Hold*: Annualized return **24.00%**, volatility 12.63%, Information Ratio **1.90**, Max Drawdown **-8.5%**.
  - *CBOE PUT Index*: Annualized return **17.93%**, volatility **6.52%**, Information Ratio **2.75**, Max Drawdown **-3.1%**.

#### In-Sample Strategy Dynamics (2018–2023, Tables 3–8)
- **Volatility Estimators**: Advanced intraday range estimators (Garman-Klass and Yang-Zhang) consistently outperform standard close-to-close estimators in short-dated Kelly simulations by incorporating intraday extreme prices and overnight jump effects.
- **VIX9D vs. VIX30D Tenor Alignment**: For ultra-short-dated options (0–1 DTE), VIX9D delivers systematically superior Information Ratios compared to the 30-day VIX, as the 30-day index carries longer-term noise that dilutes short-term regime responsiveness.

#### Out-of-Sample Performance (2024 Bull Market, Table 2)
- **Kelly Sizing Performance (0–1 DTE)**:
  - 1 DTE, 5% OTM configurations using Garman-Klass volatility with 63-day memory achieved **14.35% to 17.24% annualized return** with low volatility (~8.5%) and strict drawdown control.
- **VIX-Rank Sizing Performance**:
  - Wide dispersion across parameters: returns range from 0.95% up to **52.77%**.
  - Top performer: Aggressive 5 DTE ATM configuration using VIX9D with a 21-day memory achieved **52.77% annualized return**, 21.59% volatility, and a maximum drawdown of **9.91%**, outperforming the S&P 500 B&H Information Ratio.
  - Conservative 10% OTM setups with longer memory lookbacks (126–252 days) produced steady, low-volatility returns with minimal drawdowns.
- **Hybrid Kelly-VIX Performance**:
  - Achieved up to **23.13% annualized return** (using VIX30D with 63-day memory and short-memory GK estimator).
  - Maximum drawdowns across all hybrid configurations remained strictly **under 11%**, providing superior tail protection without sacrificing growth.

### 4. Relevance to Option Research

In `sophie-option-research`, Wysocki (2025) provides modern, high-frequency empirical validation for short-dated SPX option trading and portfolio construction:
1. **Dynamic Sizing Integration**: Directly validates the mathematical sizing engines in `src/lab/sizing.py`, demonstrating the practical effectiveness of blending Monte Carlo Kelly fractional sizing with real-time VIX percentile regime filters to maximize compound growth while avoiding ruin.
2. **Ultra-Short DTE (0–5 DTE) Exploitation**: Informs trade generation and scheduling in `src/lab/backtest.py` and `notebooks/01_backtest_baseline.ipynb`, confirming that SPXW daily expirations offer rapid theta decay that can be harvested with high Information Ratios when sized appropriately.
3. **Signal Selection & Estimator Upgrades**: Recommends using Garman-Klass and Yang-Zhang range estimators in `src/lab/features.py` for volatility inputs, and utilizing VIX9D for near-term option filtering rather than standard 30-day VIX.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Highly practical and directly actionable for `sophie-option-research`; evaluates Monte Carlo fractional Kelly sizing, rolling VIX/VIX9D percentile rank scaling, and hybrid architectures on short-dated (0–5 DTE) SPXW short puts. Proves that hybrid Kelly-VIX sizing achieves strong compounding (14%–23% annualized) while capping max drawdowns below 11% across bull and bear regimes.

## Notable Citations to Follow Up

1. **Maclean, Leonard C., Edward O. Thorp, and William T. Ziemba (2010)** — *Long-Term Capital Growth: The Good and Bad Properties of the Kelly and Fractional Kelly Capital Growth Criteria* (Quantitative Finance, 10(7), 681-689).
   - Establishes mathematical properties of fractional Kelly betting, demonstrating how scaling down bet size dramatically curtails drawdown duration and volatility with minimal sacrifice in asymptotic growth.
2. **Malkiel, Burton G., Alexis Rinaudo, and Atanu Saha (2018)** — *Option Writing: Using VIX to Improve Returns* (The Journal of Derivatives, 26(2), 38-49).
   - Demonstrates that dynamically adjusting option writing allocations based on VIX levels and percentiles boosts risk-adjusted returns over static index strategies.
3. **Beckmeyer, Heiner, Nicole Branger, and Leander Gayda (2023)** — *Retail Traders Love 0DTE Options... But Should They?* (SSRN Working Paper 4554316).
   - Detailed empirical study on volume, market maker inventory imbalances, and intraday pricing dynamics of same-day expiration (0DTE) SPX contracts.
