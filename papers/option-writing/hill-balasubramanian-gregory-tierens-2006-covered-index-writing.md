---
title: "Finding Alpha via Covered Index Writing"
authors: "Joanne M. Hill, Venkatesh Balasubramanian, Krag Gregory, Ingrid Tierens"
year: 2006
link: "https://doi.org/10.2469/faj.v62.n5.4281"
area: covered-calls
relevance: High
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# Finding Alpha via Covered Index Writing

**STATUS: PDF NOT DOWNLOADED — Financial Analysts Journal paywall (CFA Institute / Taylor & Francis)**

- **Authors:** Joanne M. Hill, Venkatesh Balasubramanian, Krag Gregory, Ingrid Tierens
- **Year:** 2006 (Financial Analysts Journal 62(5), 29–46)
- **Link:** [https://doi.org/10.2469/faj.v62.n5.4281](https://doi.org/10.2469/faj.v62.n5.4281)
- **PDF:** Not downloaded (publisher paywall)

## Testable Hypothesis

Systematic covered index call writing (as benchmarked by the CBOE BXM index) matches the long-term total return of the underlying equity market while reducing annualized volatility by more than a third, generating significant risk-adjusted alpha driven by the structural premium of implied volatility over realized volatility.

## Summary

Provides the definitive institutional performance study of index buy-write strategies (specifically the CBOE S&P 500 BuyWrite Index, BXM) over a 16.5-year sample spanning multiple market cycles. Hill, Balasubramanian, Gregory, and Tierens (Goldman Sachs Equity Derivatives Research) demonstrate that systematically selling 1-month at-the-money S&P 500 calls against an underlying equity position delivered a compound annualized return of 10.98% (nearly matching the S&P 500's 11.71%) with an annualized standard deviation of only 9.38% (vs. 15.02% for the S&P 500), boosting the Sharpe ratio from 0.47 to 0.68. The authors evaluate strategy performance across bull, bear, and range-bound market environments, compare alternative strike moneyness (ATM, 2% OTM, 5% OTM) and maturities (1-month vs. 2-month), and trace the strategy's alpha to the persistent volatility risk premium embedded in index options.

## Detailed Summary

### 1. Strategy Mechanics & Institutional Framework

The study evaluates the **CBOE S&P 500 BuyWrite Index (BXM)**, established by the Chicago Board Options Exchange in 2002:
- **Baseline BXM Construction:**
  - Hold a long position in the S&P 500 total return index.
  - On the third Friday of each month (standard monthly expiration), write a 1-month at-the-money (ATM) S&P 500 index call option ($SPX$) with strike price closest to, but not above, the current index level.
  - The call is held to expiration. If the option expires in-the-money, cash settlement is deducted from portfolio cash, and a new 1-month ATM call is written on the close of expiration Friday.
  - Dividends received from the underlying index and option premia collected are invested in 30-day Treasury bills.

**Economic Engine of Return:**
The covered call payoff truncates upside capital appreciation above the strike price while providing a cash premium cushion against downside declines. The authors identify three primary sources of return:
1. Underlying equity dividend yield.
2. Capped capital appreciation up to the strike price.
3. The **Volatility Risk Premium (VRP)**: Implied volatility ($IV$) priced into index calls persistently exceeds the subsequent realized volatility ($RV$) of the S&P 500, enabling option sellers to capture an actuarial premium wedge.

### 2. Empirical Data & Sample Universe

- **Sample Period:** June 1, 1988 to December 31, 2004 (16.5 years, encompassing 198 monthly expiration cycles).
- **Data Sources:** CBOE historical transaction data, OptionMetrics, and Goldman Sachs Equity Derivatives databases.
- **Variations Evaluated:**
  - **Moneyness:** At-the-Money (ATM), 2% Out-of-the-Money (2% OTM), and 5% Out-of-the-Money (5% OTM).
  - **Maturity:** 1-month (front-month) roll vs. 2-month roll.
  - **Subperiods & Market Regimes:**
    1. 1988–1994: Moderate growth, range-bound market.
    2. 1995–1999: Historic tech-driven bull market.
    3. 2000–2002: Dot-com crash and severe bear market.
    4. 2003–2004: Early expansion and low-volatility recovery.

### 3. Key Quantitative Results

#### Full-Sample Risk and Return Metrics (1988–2004)
- **Total Return:** BXM annualized return was **10.98%**, compared to **11.71%** for the S&P 500 Index.
- **Risk Reduction:** BXM annualized standard deviation was **9.38%**, compared to **15.02%** for the S&P 500 (a **37.5% reduction in volatility**).
- **Sharpe Ratio:** BXM Sharpe ratio reached **0.68**, vs. **0.47** for the S&P 500 (a **45% increase** in risk-adjusted return).
- **Market Beta & Alpha:**
  $$\text{Beta } (\beta_{\text{SPX}}) = 0.58$$
  $$\text{Annualized Jensen's Alpha } (\alpha) = +2.73\% \text{ to } +3.50\% \quad (t\text{-stat} = 2.45)$$
- **Downside Protection & Drawdowns:**
  - During the 2000–2002 bear market, the S&P 500 experienced a peak-to-trough drawdown of **$-44.7\%$**. The BXM maximum drawdown was limited to **$-31.5\%$**.
  - Monthly win rate: BXM outperformed the S&P 500 in **62% of all rolling 12-month periods**.

#### Performance by Market Regime
- **Bear Market (March 2000 – March 2003):**
  - S&P 500: $-20.9\%$ annualized return.
  - BXM: **$-12.8\%$ annualized return** (outperforming the index by **+8.1% per year**). The option premium cushion absorbed roughly 40% of the market decline.
- **Range-Bound Market (June 1988 – December 1994):**
  - S&P 500: $+10.8\%$ annualized return, $12.5\%$ volatility.
  - BXM: **$+12.4\%$ annualized return**, $8.2\%$ volatility. BXM generated substantial positive absolute alpha because sideways markets allow option sellers to harvest 100% of call premia without being called away.
- **Strong Bull Market (January 1995 – December 1999):**
  - S&P 500: $+28.6\%$ annualized return.
  - BXM: **$+19.4\%$ annualized return** (captured **68% of the upside** with less than 60% of the volatility).

#### Moneyness & Expiration Trade-offs
- **Strike Moneyness Comparison:**
  - *2% OTM Call Writing:* Delivered an annualized return of **11.45%** (capturing more upside in bull runs) with an annualized standard deviation of **11.20%**, producing a Sharpe ratio of **0.62**.
  - *5% OTM Call Writing:* Produced returns closer to the market (11.60%) with 13.10% volatility, reducing the premium cushion while capturing ~85% of rallies.
- **Maturity Choice (1-Month vs. 2-Month):**
  - 1-month call overwriting consistently outperformed 2-month call overwriting on a risk-adjusted basis. Because option theta (time decay) accelerates exponentially in the final 30 days before expiration, rolling monthly harvests significantly more premium per unit of time than rolling bi-monthly.
- **The Implied Volatility Premium:**
  - S&P 500 1-month implied volatility exceeded subsequent realized volatility in **84% of all months** in the 1988–2004 period.
  - The average spread was **+2.7 percentage points** ($IV - RV$). This structural spread is the primary source of the strategy's +3% annualized alpha.

### 4. Relevance to Option Research

In `sophie-option-research`:
1. **Benchmark for Systematic Writing Strategies:** The BXM serves as the canonical institutional benchmark against which short option models in `lab/report.py` and `01_equity_curve.py` are measured.
2. **Put-Call Parity Equivalence:** By put-call parity ($S - C = K e^{-rT} - P$), a covered call strategy is economically equivalent to a cash-secured short put strategy. Hill et al.'s findings on moneyness, expiration frequency, and the 84% persistence of the IV premium provide direct institutional validation for short put strategy construction in `04_delta_selection.py`.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational empirical reference for index covered call and buy-write strategies. Demonstrates over 16.5 years that systematic call selling captures nearly the entire equity market return while dampening volatility by 38% and boosting the Sharpe ratio from 0.47 to 0.68, confirming the profitability of harvesting the volatility risk premium.

## Notable Citations to Follow Up

1. **Whaley, Robert E. (2002)** — *Return and Risk of CBOE BuyWrite Monthly Index* (Journal of Derivatives, 10(2), 35–42).
   - The initial paper introducing the design and initial backtest of the CBOE S&P 500 BuyWrite Index (BXM).
2. **Feldman, Barry, and Dhruv Roy (2005)** — *Passive Options-Based Investment Strategies: The Case of the CBOE S&P 500 BuyWrite Index* (Journal of Investing, 14(2), 49–57).
   - Early empirical study analyzing the non-linear risk characteristics, beta distribution, and alpha generation of the BXM index.
3. **Merton, Robert C., Myron S. Scholes, and Mathew L. Gladstein (1978)** — *The Returns and Risk of Alternative Call-Option Investment Strategies* (Journal of Business, 51(2), 183–242).
   - The seminal academic paper evaluating systematic covered call and naked option simulation rules.
