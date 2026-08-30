# The Cost of Capital for Alternative Investments

- **Authors:** Jakub W. Jurek, Erik Stafford
- **Year:** 2015
- **Link:** [https://www.nber.org/papers/w17376](https://www.nber.org/papers/w17376)
- **PDF:** `jurek-stafford-2015-cost-of-capital-alternative-investments.pdf` (open-access copy)

## Testable Hypothesis

The pre-fee risk and return distribution of diversified hedge funds can be largely replicated by a simple mechanical rule of selling out-of-the-money S&P 500 put options to harvest the downside volatility risk premium.

## Summary

Shows that broad hedge fund index returns have significant non-linear downside market exposure resembling out-of-the-money put writing. Concludes that much of aggregate hedge fund 'alpha' reflects compensation for bearing tail risk and harvesting the equity index volatility risk premium.

## Detailed Summary

### 1. Methodology & Non-Linear Replication Framework

Jurek and Stafford investigate whether the economic performance of the aggregate hedge fund universe represents genuine managerial alpha or uncompensated/compensated exposures to non-linear market risks (specifically the volatility risk premium and downside tail risk).

1. **State-Contingent Put-Writing Replication**:
   - The authors model hedge fund returns as a combination of linear equity exposure and short positions in out-of-the-money (OTM) S&P 500 index put options.
   - Put-writing portfolios are parameterized by $[Z, L]$, where $Z$ defines the moneyness strike threshold:
     $$K/S_t = 1 + Z \cdot \sigma_t \sqrt{\tau}$$
     with $Z \in \{-0.5, -1.0, -1.5, -2.0\}$, maturity $\tau = 1\text{ month}$, and $L$ is the leverage/notional multiplier chosen to match the sample mean return of the target hedge fund index.
   - An equal-weighted **Put Writing Composite** is constructed across the four moneyness tiers.
   - Replicating returns and feasible residuals are compared against standard linear factor models: the CAPM, the Fama-French/Carhart 4-factor model, and the Fung-Hsieh 9-factor hedge fund model.

2. **Generalized Cost of Capital Model**:
   - Linear asset pricing models (e.g. CAPM beta) fail for non-linear payoffs because they only evaluate covariance, ignoring higher-order moments and tail dependence.
   - The authors develop a state-dependent utility framework (CRRA risk aversion $\gamma = 3.3$) to determine the true required rate of return (cost of capital) for institutional investors with large allocations to alternative investments (e.g., an endowment model with 35% or 50% allocation to alternatives alongside a baseline 60/40 equity/bond mix).
   - Time-varying required risk premia are computed dynamically using market volatility estimated from $0.8 \times \text{VIX}_t$.

### 2. Data & Universe

- **Sample Period**: January 1996 – December 2010 (15 years, 60 quarters / 180 months).
- **Hedge Fund Indices**: 
  - *Aggregates*: HFRI Fund-Weighted Composite Index (equal-weighted) and Dow Jones/Credit Suisse Broad Hedge Fund Index (value-weighted).
  - *Sub-indices*: Event Driven, Distressed, Merger Arbitrage, Equity Hedge, Long/Short Equity, Relative Value, Convertible Arbitrage, Macro, and Managed Futures.
- **Pre-Fee Adjustment**: Pre-fee series are constructed assuming a representative fund at its high-water mark charging a 2% management fee and 10% incentive fee payable monthly (all-in annual fees average ~3.1% to 5.0%; 4.0% for HFRI).
- **Option & Market Data**: S&P 500 options from OptionMetrics and CBOE; CRSP S&P 500 index; 1-month U.S. Treasury bills from Ken French's data library.

### 3. Key Quantitative Results

#### Pre-Fee Hedge Fund Performance (Table I)
- **HFRI Fund-Weighted Composite**: Annualized pre-fee mean return of **13.6%** (excess return 10.5%), annualized volatility **9.8%**, Sharpe ratio **1.07**, CAPM alpha $\hat{\alpha} = \mathbf{8.0\%}$, CAPM $\beta = 0.45$, maximum drawdown **-18.8%**, all-in fee **4.0%**.
- **DJ/CS Broad Index**: Pre-fee mean return **13.6%**, volatility **9.2%**, Sharpe ratio **1.15**, CAPM $\hat{\alpha} = \mathbf{8.6\%}$, CAPM $\beta = 0.35$, max drawdown **-18.8%**, all-in fee **3.9%**.
- **S&P 500 Index**: Mean return 8.5%, volatility 18.1%, Sharpe ratio 0.30, max drawdown -50.2%.

#### Put-Writing vs. Linear Factor Replication (Table II & Table III)
- **Residual Distribution & Non-Linear Fit (Table III)**:
  - Linear models produce residuals with extreme non-normality and substantial unexplained mean alpha:
    - *CAPM*: Feasible residual mean 5.76% ($t = 3.5$), Jarque-Bera $JB = 3.5$ ($p = 0.09$), Joint test $JS = 36.7$ ($p < 0.001$).
    - *Fama-French/Carhart 4-factor*: Residual mean 6.88% ($t = 7.0$), $JB = 16.3$ ($p = 0.01$), Joint test $JS = 63.6$ ($p < 0.001$).
    - *Fung-Hsieh 9-factor*: Residual mean 9.46% ($t = 10.1$), $JB = 9.6$ ($p = 0.02$), Joint test $JS = 99.1$ ($p < 0.001$).
  - *Put Writing Composite*: Feasible residual mean is virtually zero (**0.1%**, $t = 0.06$), $JB = 1.9$ ($p = 0.27$), Joint test $JS = 1.9$ (**$p = 0.52$**, failing to reject zero mean and normality).
- **Drawdown Matching**: The Put Writing Composite matches the historical drawdown trajectory of the HFRI Composite with a Root Mean Squared Error (RMSE) of only **1.4%**, compared to **5.5%** for CAPM, **4.7%** for FF-4, and **7.0%** for Fung-Hsieh.

#### Required Cost of Capital & Investor Alphas (Table VI)
- **Hedge Fund After-Fee Alphas**:
  - Realized excess return of after-fee HFRI Composite is **6.3%** ($t = 3.2$).
  - Linear CAPM required return is only **3.0%**, suggesting an apparent alpha of **+3.3%** ($t = 1.7$).
  - Generalized non-linear cost of capital for an endowment investor is **6.9%** (at 35% allocation) and **8.7%** (at 50% allocation).
  - Evaluated against the proper cost of capital, after-fee hedge fund alpha is **negative**: **-0.6%** ($t = -0.3$) at 35% allocation and **-2.5%** ($t = -1.2$) at 50% allocation.
- **Put-Writing Strategy Performance**:
  - Pre-fee Put Writing Composite achieves an annualized realized excess return of **10.2%** ($t = 5.4$)—beating the after-fee HFRI by **~3.9% per year**.
  - Net alpha relative to the endowment cost of capital remains positive: **+3.3%** ($t = 1.8$) at 35% allocation and **+1.5%** ($t = 0.8$) at 50% allocation.

#### Out-of-Sample Validation & Sub-Strategies (Table IV, Table V, Table VII)
- In out-of-sample split tests (1996–2003 in-sample vs. 2003–2010 out-of-sample), put writing models consistently match the non-linear risk profiles across Equity Hedge, Event Driven, and Relative Value styles, whereas linear factor models fail in out-of-sample drawdown tracking.

### 4. Relevance to Option Research

In `sophie-option-research`, Jurek and Stafford (2015) provides critical empirical and theoretical justification for short put / VRP harvesting strategies:
1. **Option Selling as the Engine of Alternative Alpha**: Proves that the non-linear payoff structure and returns of the entire multibillion-dollar hedge fund industry are essentially equivalent to systematic short put options on the S&P 500. This validates that systematic option selling in `src/lab/backtest.py` directly extracts the fundamental risk premium driving institutional alternative performance.
2. **Parametric Strike & Leverage Framework ($[Z, L]$)**: The paper's formulation of moneyness in volatility units ($K = S(1 + Z \sigma \sqrt{\tau})$) and leverage scaling ($L$) provides a mathematically rigorous blueprint for strike grid definitions in `src/lab/strategy.py` and parameter sweep notebooks (`notebooks/04_param_sweep.ipynb`).
3. **Risk Metrics & Benchmark Attribution**: Demonstrates that linear risk models (beta, linear alpha) severely underestimate downside tail risk. This motivates the implementation of non-linear risk metrics in `src/lab/metrics.py` and `src/lab/report.py`, including drawdown RMSE matching, shortfall distributions, and state-contingent cost of capital benchmarking against naive linear CAPM models.

