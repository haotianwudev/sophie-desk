# Construction and Hedging of Equity Index Options Portfolios

- **Authors:** Maciej Wysocki, Robert Ślepaczuk
- **Year:** 2024
- **Link:** [https://arxiv.org/abs/2407.13908](https://arxiv.org/abs/2407.13908)
- **PDF:** `wysocki-slepaczuk-2024-construction-hedging.pdf` (open-access copy)

## Testable Hypothesis

Systematic SPX option writing combined with periodic delta hedging (at ~130-minute intraday intervals) provides superior risk-adjusted returns over unhedged writing and buy-and-hold equity benchmarks by capturing the volatility risk premium while limiting directional market exposure.

## Summary

Analyzes systematic index option-writing portfolios on S&P 500 options from 2018 to 2023 using high-frequency 1-minute data. Compares Black-Scholes-Merton and Variance-Gamma hedging models and identifies the optimal intraday hedging frequency to minimize transaction costs while retaining positive volatility risk premium capture.

## Detailed Summary

### 1. Methodology & Intraday Hedging Framework

Wysocki and Ślepaczuk investigate the empirical construction, sizing, and dynamic delta-hedging of systematic S&P 500 option-writing portfolios to isolate and harvest the Volatility Risk Premium (VRP) under realistic high-frequency market conditions.

1. **Option Pricing & Hedging Models**:
   - **Black-Scholes-Merton (BSM)**: Standard closed-form model with implied volatility calibrated directly from option market quotes.
   - **Variance-Gamma (VG)**: Three-parameter stochastic jump model (Madan et al., 1998) capturing finite jump activity, skewness, and fat tails, calibrated to market option strips.
   - **Rehedging Frequencies**:
     - *30-Minute Rehedging*: High-frequency intraday delta adjustments (~13 rebalances/day).
     - *130-Minute Rehedging*: Moderate intraday delta adjustments (3 rebalances/day, at 10:00, 12:10, 14:20 ET).
     - *Daily (Single) Rehedging*: End-of-day delta adjustment.
     - *Naked (Unhedged)*: Fixed unhedged baseline holding option positions to expiry.

2. **Position Sizing Methodologies**:
   - **Delta-Based Sizing**: Positions scaled inversely to option delta to maintain standardized directional exposure across moneyness.
   - **VIX-Rank Sizing**: Sizing scaled dynamically by the percentile rank of the VIX index, reducing position sizes during high-volatility regimes to avert tail drawdowns.

3. **Strategy Structures & Evaluation Metrics**:
   - Evaluates Short Calls, Short Puts, Short Straddles (0% ATM), and Short Strangles (2%, 5%, 10% OTM).
   - Metrics include Annualized Return ($aRC$), Annualized Volatility ($aSD$), Maximum Drawdown ($MD$), Maximum Loss Duration ($MLD$), Information Ratio ($IR = (aRC - r_f)/aSD$), drawdown-penalized metrics ($IR^{**}$ and $IR^{***}$), 99% Value at Risk ($VaR$), and 99% Conditional Value at Risk ($CVaR$).

### 2. Data & Universe

- **Sample Period**: January 1, 2018 – December 31, 2023 (6 years / ~1,500 trading days, including 2018 Volmageddon, Q4 2018 equity correction, 2020 COVID crash, and 2022 bear market).
- **Instruments & Data**:
  - High-frequency 1-minute intraday OHLC quotes and bid-ask spreads for S&P 500 Index options (`SPX`) and underlying index quotes from CBOE.
  - SPDR S&P 500 ETF Trust (`SPY`) 1-minute quotes for delta hedge execution.
  - CBOE Volatility Index (`VIX`) and FRED 3-Month US Treasury bills.
- **Benchmark**: S&P 500 Buy & Hold (B&H: $aRC = 9.89\%$, $aSD = 20.60\%$, $MD = 34.00\%$, $IR = 0.48$).

### 3. Key Quantitative Results

#### Hedging Model Comparison: BSM vs. Variance-Gamma (VG) (Table 4, Table 5)
- **BSM Dominance in Hedging**: In delta-sized hedged short put configurations, the BSM model achieves superior risk-adjusted performance ($IR^{***}$) in **10 out of 12 cases** compared to the VG model.
- **Tail Risk Containment**: BSM delta hedging systematically delivers lower 99% $VaR$ and $CVaR$ losses than VG hedging, confirming that BSM implied-volatility delta tracking provides better protection against large market swings.
- **VG as a Sizing Signal**: While VG is less effective for continuous hedging, naked strategies sized via VG parameters occasionally produce higher raw returns ($aRC$), albeit with significantly higher volatility and drawdowns.

#### Optimal Intraday Hedging Frequency (Section 4.2, Table 5)
- **The 130-Minute Sweet Spot**: Rehedging every **130 minutes** (3 times per trading session) delivers the optimal trade-off between downside protection and execution cost.
  - *30-minute rehedging*: Generates excessive turnover and bid-ask slippage that erode net profitability without meaningfully improving drawdown protection over 130-minute rehedging.
  - *Daily (single) rehedging*: Fails to protect against sharp intra-day equity crashes (e.g. March 2020), exhibiting severe drawdown spikes.
  - *130-minute BSM hedged short puts*: Successfully curb maximum drawdowns and volatility while preserving positive net returns from VRP capture.

#### Strategy Performance: Puts vs. Strangles (Table 5, Table 6)
- **Short Strangles (Table 6)**:
  - 5% OTM Short Strangles using BSM delta sizing achieved an annualized return of **10.27%**, volatility of **13.00%**, and an extraordinary $IR^{***}$ of **64.16** (outperforming the S&P 500 Buy & Hold benchmark).
  - VIX-sized ATM Straddles delivered steady income of **3.04%** annualized return with only **7.10%** volatility and $IR^{***}$ of **1.77**.
- **Short Puts (Table 5)**:
  - 5% OTM short puts delivered the strongest standalone performance ($aRC = 6.40\%$, $aSD = 26.00\%$, $MD = 35.10\%$, $IR^{***} = 5.11$).
  - VIX-rank sizing sharply reduced volatility ($aSD$ down to 3.8%–7.5%) and drawdowns ($MD$ contained under 10%), transforming naked option selling into a conservative, steady yield stream.

### 4. Relevance to Option Research

In `sophie-option-research`, Wysocki and Ślepaczuk (2024) provides essential practical guidance for delta hedging, sizing, and intraday rebalancing schedules:
1. **Intraday Hedging Cadence**: Directly justifies the rebalancing frequency in `src/lab/backtest.py` and `src/lab/rolling.py`, demonstrating that periodic intraday hedging (e.g., 2–3 checks per session / ~130 minutes) captures the bulk of theoretical continuous delta hedging benefits while avoiding transaction cost drag.
2. **Hedging Model Selection**: Confirms that BSM implied-volatility delta hedging remains the most robust and computationally efficient model for practical tail-risk control in `src/lab/engine.py`, outperforming complex stochastic jump models like Variance-Gamma.
3. **VIX-Rank Sizing Architecture**: Supports the volatility percentile scaling modules in `src/lab/sizing.py`, confirming that scaling contract sizes inversely with VIX ranks drastically reduces max drawdown depth and duration across market stress periods (2018 Volmageddon, 2020 COVID).

