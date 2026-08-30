# Embedded Leverage

- **Authors:** Andrea Frazzini, Lasse Heje Pedersen
- **Year:** 2012
- **Link:** [https://www.nber.org/papers/w18558](https://www.nber.org/papers/w18558)
- **PDF:** `frazzini-pedersen-2012-embedded-leverage.pdf` (open-access copy)

## Testable Hypothesis

Because leverage-constrained investors overpay for high-beta and high-embedded-leverage assets like out-of-the-money options, writing high-embedded-leverage options and holding low-leverage underlyings systematically generates positive risk-adjusted alpha.

## Summary

Documents how borrowing constraints create demand for instruments with embedded leverage (options, leveraged ETFs), causing them to trade at rich valuations and offer low expected returns. Demonstrates that selling high-embedded-leverage options captures the resulting premium.

## Detailed Summary

### 1. Methodology & Embedded Leverage Theory

Frazzini and Pedersen propose that a central economic characteristic driving derivative pricing is **embedded leverage**—the amount of market exposure provided per unit of committed capital.

1. **Embedded Leverage Definition ($\Omega$)**:
   The embedded leverage (option elasticity) of a derivative security with price $F$ and delta $\Delta = \partial F / \partial S$ relative to underlying spot price $S$ is defined as:
   $$\Omega \equiv \left| \frac{\partial F}{\partial S} \frac{S}{F} \right| = \left| \Delta \frac{S}{F} \right|$$
   - Investors facing borrowing or regulatory leverage constraints (e.g. retail traders, pension funds, mutual funds) cannot apply outright margin leverage. To increase return potential, they bid up securities that embed leverage (out-of-the-money options, short-dated options, and leveraged ETFs).
   - High demand makes high-$\Omega$ assets trade at expensive valuations, driving down their required risk-adjusted returns (producing negative alphas).
2. **Betting-Against-Beta ($BAB$) Construction in Options & ETFs**:
   - To exploit this mispricing without taking directional equity risk, the authors construct self-financing Betting-Against-Beta ($BAB$) portfolios.
   - For each underlying asset $i$, options are sorted into low ($\Omega^{L,i}$) and high ($\Omega^{H,i}$) embedded leverage portfolios relative to median $\Omega$. Position sizes are rescaled by $1/\Omega$ so both legs have unit exposure to the underlying (net delta = 0 ex-ante):
     $$BAB_t^i = \left(\frac{1}{\Omega_{t-1}^{L,i}}\right) r_t^{L,i} - \left(\frac{1}{\Omega_{t-1}^{H,i}}\right) r_t^{H,i}$$
   - For leveraged ETFs, $BAB_t = r_t^{1\times} - 0.5 \cdot r_t^{2\times}$.
   - Portfolios are evaluated on monthly delta-hedged excess returns, Fama-French 3-factor, Carhart 4-factor, and a 5-factor model that adds the Coval-Shumway (2001) zero-beta ATM S&P 500 straddle factor.

### 2. Data & Universe

- **Sample Period**: January 1996 – December 2010 (15 years of OptionMetrics Ivy DB closing quotes; 2006–2010 for ETFs via Yahoo Finance).
- **Universe**:
  - *Equity Options*: 11,327,382 option-months across 7,179 individual stocks (averaging ~2,920 stocks/year with 62 options per stock-month).
  - *Index Options*: 290,125 option-months across 12 major indices (`SPX`, `OEX`, `NDX`, `MNX`, `DJX`, `RUT`, `MID`, `SML`, `XMI`, `TYX`, `NYZ`, `WSX`; averaging 371 options per index-month).
  - *Leveraged ETFs*: 7 major index pairs (SPY/SSO, QQQ/QLD, DIA/DDM, IWM/UWM, IWV/UWC, MDY/MVV, IJR/SAA).
- **Option Buckets**: 30 portfolios sorted on 5 delta moneyness bins (DOTM, OTM, ATM, ITM, DITM) $\times$ 6 maturity bins (1, 2, 3, 6, 12, >12 months).

### 3. Key Quantitative Results

#### Dispersion of Embedded Leverage (Table II, Table III)
- **Equity Options**: Embedded leverage averages $\Omega = 6.48$ ($SD = 4.79$, range 0.14 to 43.94). Short-dated (1-month) DOTM options have $\Omega = 16.48$, whereas long-dated (>12m) DITM options have $\Omega = 2.42$.
- **Index Options**: Embedded leverage averages $\Omega = 12.14$ ($SD = 10.15$, range 0.72 to 120.60). 1-month DOTM index options reach an extreme $\Omega = 36.14$, compared to $\Omega = 3.27$ for long-dated DITM.

#### Low Returns to High Embedded Leverage (Table IV, Table V)
- **Overall Asset Class Alphas (Table IV)**:
  - Equal-weighted delta-hedged equity options earn a 4-factor alpha of **-3.25% per month** ($t = -3.04$). Index options earn **-2.37% per month** ($t = -3.18$).
- **Maturity-Sorted Portfolios (Table V)**:
  - 1-month equity options earn an excess return of **-11.54%/month** (4-factor alpha **-10.39%**, $t = -9.45$), while >12-month options earn **+0.25%/month** (alpha **+1.03%**, $t = 1.97$).
  - Long low-$\Omega$ / short high-$\Omega$ maturity spread ($P6 - P1$) generates a massive alpha of **+11.08% per month** ($t = 12.08$).
  - For index options, the $P6 - P1$ spread earns **+11.52% per month** alpha ($t = 7.29$).
- **Moneyness-Sorted Portfolios (Table V)**:
  - Deep OTM equity options lose **-7.70%/month** (alpha **-5.25%**, $t = -2.95$), while Deep ITM options lose only -0.33% (alpha -0.12%). The $P5 - P1$ moneyness spread yields **+5.13%/month** alpha ($t = 3.11$).

#### BAB Portfolio Performance & Sharpe Ratios (Table VI, Figures 2 & 3)
- **Equity Options BAB**:
  - Monthly excess return **+0.36%** ($t = 8.57$), 5-factor alpha **+0.33% per month** ($t = 7.60$, ~4.0% annualized alpha).
  - Annualized volatility is only **1.95%**, resulting in an extraordinary annualized Sharpe ratio of **2.22** (Sortino 1.11).
  - 78% of all individual equity option BABs generate positive alphas.
- **Index Options BAB**:
  - Monthly excess return **+0.33%** ($t = 6.26$), 5-factor alpha **+0.26% per month** ($t = 4.95$, ~3.1% annualized alpha).
  - Annualized volatility is **2.42%**, yielding an annualized Sharpe ratio of **1.62**.
  - **100% of the 12 individual index option BABs** generate positive alphas.
- **Leveraged ETF BAB**:
  - Earns a 5-factor alpha of **+0.07% to +0.09% per month** ($t = 2.52$ to $3.43$), with annualized Sharpe ratios between **1.18 and 1.63**.
- **Distributional Properties (Table VIII, Figure 3)**:
  - Rescaling by $1/\Omega$ dynamically stabilizes volatility. BAB factor returns exhibit mild skewness (-0.87 to +0.41) and low excess kurtosis (1.16 to 4.57), behaving far better than raw option strategies.

#### Cross-Sectional Fama-MacBeth Regressions (Table VII)
- Across 11.3M equity option observations, controlling for open interest, maturity, moneyness, IV, vega, gamma, and stock returns, lagged embedded leverage $\Omega_{t-1}$ enters with a large, highly significant negative coefficient of **-1.28 to -1.57** ($t = -10.08$ to $-10.83$).
- For index options, the coefficient on $\Omega_{t-1}$ is **-1.30 to -1.51** ($t = -7.99$ to $-9.20$).

#### Crisis & Bear Market Robustness (Table IX)
- During NBER recessions, equity option BAB alpha remains robust at **+0.38%/month** ($t = 2.41$).
- In severe bear markets (12-month market return <-25%), equity BAB alpha jumps to **+0.92%/month** ($t = 7.24$) and index BAB alpha surges to **+1.30%/month** ($t = 4.40$), confirming the strategy does not rely on hidden catastrophic tail risk.

### 4. Relevance to Option Research

In `sophie-option-research`, Frazzini and Pedersen (2012) provides the foundational theoretical mechanism explaining why systematic option selling works and how to optimize strike and maturity selection:
1. **The Structural Driver of Option Alpha**: Explains that the rich pricing of short-dated OTM options is fundamentally driven by retail/institutional leverage constraints and demand for embedded leverage ($\Omega = |\Delta S/F|$). Selling options is not just "picking up pennies in front of a steamroller," but systematically supplying leverage to constrained investors.
2. **Strike & Moneyness Optimization**: Confirms why writing 10–25 delta OTM options (`notebooks/04_param_sweep.ipynb` and `lab/strategy.py`) harvests maximum mispricing: high-$\Omega$ options lose -5% to -10%/month on a delta-hedged basis, whereas deep ITM options trade close to fair value.
3. **Risk-Weighted Sizing ($1/\Omega$)**: The paper's insight on scaling position sizes inversely with embedded leverage ($1/\Omega$) provides an effective sizing framework for backtests in `lab/engine.py` to prevent short-dated OTM options from dominating portfolio variance and tail risk.
