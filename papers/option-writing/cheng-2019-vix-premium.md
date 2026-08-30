---
title: "The VIX Premium"
authors: "Ing-Haw Cheng"
year: 2019
link: "https://utoronto.scholaris.ca/items/1cfdb03f-e696-46b1-959c-15bcb51163d5"
area: vrp-timing
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The VIX Premium

- **Authors:** Ing-Haw Cheng
- **Year:** 2019 (Review of Financial Studies 32(1), 180-227; working paper May 2018)
- **Link:** [https://utoronto.scholaris.ca/items/1cfdb03f-e696-46b1-959c-15bcb51163d5](https://utoronto.scholaris.ca/items/1cfdb03f-e696-46b1-959c-15bcb51163d5)
- **PDF:** `cheng-2019-vix-premium.pdf` (open-access post-print, University of Toronto TSpace repository)

## Testable Hypothesis

The premium embedded in rolling one-month VIX futures (the "VIX premium") is driven by time-varying hedging demand rather than compensation for realized risk, so it counterintuitively falls or flattens exactly when ex-ante risk rises — meaning a systematic short-VIX-futures roll strategy is harvesting a hedging-demand premium that shrinks precisely when the position is most exposed, not a premium that scales with the risk being borne.

## Summary

Estimates a daily time series of the premium earned by rolling short-dated VIX futures each month and shows it reliably predicts ex-post VIX futures returns with a coefficient near one. Ties the puzzle — premiums falling as risk rises — to declining hedging demand from market participants during risk shocks, using futures positioning data. Offers a distinct instrument (VIX futures roll, rather than SPX index options) and a distinct mechanism (hedging-demand dynamics, rather than tail/jump risk pricing) for harvesting the volatility risk premium versus the SPX-option-writing angle already covered by `wysocki-slepaczuk-2024-construction-hedging` and `wysocki-2025-sizing-risk`.

## Detailed Summary

### 1. Methodology & The VIX Premium Definition

Cheng investigates the risk premium embedded in the VIX futures market, defined as the risk-neutral expected value of the future VIX minus its physical expectation:

$$VIXP_t \equiv \mathbb{E}_t^\mathbb{Q}[VIX_{T(t)}] - \mathbb{E}_t^\mathbb{P}[VIX_{T(t)}]$$

1. **Measurement and Strategy Construction**:
   - Examines a systematic 1-month rolling VIX futures investment strategy. On any date $t$, the strategy holds the 1-month-ahead contract expiring at $T(t)$, rolling into the 2-month contract on the last trading day of each month.
   - Under no-arbitrage, $\mathbb{E}_t^\mathbb{Q}[VIX_{T(t)}] = F_t^{T(t)}$ (the futures settlement price).
   - The physical expectation $\mathbb{E}_t^\mathbb{P}[VIX_{T(t)}] = \widehat{VIX}_t^{T(t)}$ is estimated strictly out-of-sample using a baseline $ARMA(2,2)$ model parameterized exclusively on pre-2004 daily data:
     $$VIX_t = 20.083 + 1.651(VIX_{t-1} - 20.083) - 0.654(VIX_{t-2} - 20.083) - 0.714 \varepsilon_{t-1} - 0.064 \varepsilon_{t-2} + \varepsilon_t$$
   - Scaled to a 1-month horizon (21 trading days), the dollar premium is:
     $$VIXP_t = \frac{21}{T(t) - t} \left[ F_t^{T(t)} - \widehat{VIX}_t^{T(t)} \right]$$
   - In return space, the ex-ante expected monthly excess return is:
     $$VIXR_{t-1} = \left[ \frac{\widehat{VIX}_{t_1}^{T(t_1)}}{F_{t_1}^{T(t_1)}} \right]^{\frac{21}{T(t_1) - t_1}} - 1$$

2. **The Low Premium-Response Puzzle**:
   - Evaluates how monthly changes in $VIXP_t$ react to changes in ex-ante and realized risk measures $X_t$ (Realized Volatility, $VVIX$, SPX IV Skew, spot $VIX$, CBOE $SKEW$):
     $$\Delta VIXP_t = \alpha + \beta \Delta X_t + \sum_{k=1}^3 (\gamma_k \Delta X_{t-k} + \delta_k \Delta VIXP_{t-k}) + \varepsilon_t$$
   - Standard asset pricing models (e.g., Bollerslev, Tauchen, and Zhou 2009; Drechsler and Yaron 2011) predict $\beta > 0$ (premiums rise with risk). Instead, empirical estimates find $\beta < 0$ (premiums fall or stay flat contemporaneously when risk surges).

3. **Equilibrium Demand-Supply Channel**:
   - Uses CFTC Traders in Financial Futures (TFF) data to decompose positioning between long hedgers (commercial dealers hedging retail VXX notes and public long-VIX call options) and short liquidity suppliers (leveraged hedge funds).
   - Proves that falling premiums co-moving with declining dealer long positions reflect a collapse in customer hedging demand during market stress, rather than mismeasurement.

### 2. Data & Universe

- **Sample Period**: March 2004 – May 2016 (2,940 daily trading sessions, 608 trading weeks, 141 monthly cycles).
- **Data Sources**: Bloomberg (VIX futures settlements across 1- to 5-month expiries, spot VIX, VVIX), TickData (5-minute intraday SPX prices), OptionMetrics Ivy DB (SPX implied volatility surfaces), CFTC TFF weekly reports (dealer, asset manager, and hedge fund net positions), and Kenneth French factor data.

### 3. Key Quantitative Results

#### Summary Statistics & Baseline Return (Table 1)
- **VIX Futures Rolling Return**: Fully collateralized 1-month rolling short-term VIX futures earned an average monthly excess return of **-3.46%** (monthly standard deviation 17.50%, annualized 61%), yielding an annualized Sharpe ratio of **-0.68** (vs. +0.51 for the S&P 500).
- **Average VIX Premium**: The dollar premium $VIXP$ averaged **+$0.70 points** ($SD = 1.41$, range $-4.62$ to $+4.20$), corresponding to an expected monthly futures return $VIXR$ of **-2.51%** ($SD = 5.65\%$).

#### The Low Premium-Response Puzzle (Table 2 & Table 3)
- **Contemporaneous Negative Sensitivity**:
  - A 1-SD increase in realized volatility (6.4 percentage points) causes an immediate **-0.45-point drop** in the VIX premium (-0.43 SDs, $\beta = -0.070, t = -3.50$).
  - A 1-SD increase in VVIX (14.0 points) triggers a **-0.36-point decline** in premium (-0.35 SDs, $\beta = -0.026, t = -2.89$).
  - A 1-SD increase in SPX IV skew triggers a **-0.46 SD decline** in premium ($\beta = -0.230, t = -4.42$).
  - Decompositions show futures prices rise by *less* than physical conditional forecasts during volatility shocks.
- **Robustness Across Models & Subsamples**: Holds in the post-2010 subsample (excluding GFC; realized vol $\beta = -0.026, t = -1.30$; VVIX $\beta = -0.016, t = -2.29$) and across 10 alternative HAR/bi-power realized volatility forecast specifications (Table 3, Panel C).

#### Return Predictability & Ex-Post Risk (Tables 4 & 5)
- **Predictive Slope Near One**: Regressing realized monthly futures excess return $r_{t+1}$ on ex-ante expected return $VIXR_t$ yields:
  $$r_{t+1} = \alpha + \beta VIXR_t + \varepsilon_{t+1} \implies \beta = \mathbf{0.917} \; (s.e. = 0.289, \; R^2 = 8.8\%)$$
  The coefficient is statistically indistinguishable from 1.0, confirming that low estimated premiums accurately reflect low ex-post realized returns rather than model error.
- **Predicting Higher Volatility**: A 1-SD decline in $VIXP$ predicts a **+16 percentage-point increase** in future annualized futures return volatility ($\beta_1 = -15.14, t = -3.32$) and a **+3.0 percentage-point rise** in market realized volatility ($\beta_1 = -2.77, t = -2.59$).

#### Trading Strategy Performance & Alpha (Table 6 & Table 7)
- **Always-Short VIX Futures (S/S)**: Annualized excess return +12.3%, standard deviation 21.5%, Sharpe ratio **+0.572**, 4-factor alpha +4.1%/yr, Maximum Drawdown **-55.3%** (heavy left skew -0.825).
- **Cash/Short Timing Strategy (C/S)** (short futures when $VIXR < 0$, hold cash when $VIXR \ge 0$):
  - Annualized excess return **+16.6%** ($s.e. = 4.9\%$).
  - Standard deviation **19.0%** (delevered to match SPX vol).
  - Annualized Sharpe ratio **+0.874** (vs. +0.572 for S/S and +0.413 for SPX).
  - Maximum Drawdown dramatically reduced from **-55.3% to -26.4%**.
  - Four-factor alpha increases to **+11.6% per year** ($t = 2.58$).
- **Long/Short Timing Strategy (L/S)**: Earns **+14.6% annualized alpha** ($t = 2.43$) and a Sharpe ratio of **+0.790**, but higher volatility when long due to elevated ex-post uncertainty.

#### Hedging Demand Mechanics (Tables 8, 9, 10)
- **CFTC Positions**: Post-2010, commercial dealers held an average net long position of **+22,200 contracts** ($+\$22.2M$ notional per VIX point), while leveraged hedge funds held net short positions of **-32,600 contracts**.
- **Hedging Contraction**: In response to a 1-SD increase in realized volatility, dealers reduce long futures positions by **-0.25 SDs** ($\beta = -0.525, t = -2.82$), driven by sharp contractions in retail VXX creation flows and public net long VIX option demand.

### 4. Relevance to Option Research

In `sophie-option-research`, Cheng (2019) delivers crucial structural insights for designing and risk-managing volatility-harvesting systems:
1. **The Fallacy of Constant / Expanding VRP in Crises**: Systematic option sellers often assume that premium spreads widen during market selloffs. Cheng demonstrates that because dealer hedging demand dries up during volatility shocks, the ex-ante VIX premium compresses or turns negative, making naked short positions poorly compensated precisely when left-tail risk is highest.
2. **Dynamic Regimes & Gating Signals**: Directly informs the filter rules tested in `notebooks/09_vrp_study.ipynb` and `notebooks/05_walk_forward.ipynb`. Implementing a simple sign-gated filter (shutting off short option/futures exposure when $VIXR \ge 0$ or when the front-month VIX futures curve inverts into backwardation) cuts strategy drawdown in half (from -55% to -26%) and lifts Sharpe ratios from 0.57 to 0.87.
3. **VVIX and Skew Conditioning**: Confirms that monitoring second-order volatility features (`VVIX` and OTM put skew in `notebooks/02_features.ipynb`) captures dealer risk aversion shifts, providing an early-warning indicator before volatility spikes materialize into catastrophic assignment losses.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Vital empirical study uncovering the "low premium-response puzzle," where volatility risk premia compress or invert during acute market shocks due to dealer hedging retrenchment. Demonstrates that a rule-based cash/short timing filter (disabling short exposure when estimated premium turns negative or backwardated) cuts drawdowns by half (-55% to -26%) and lifts Sharpe ratios from 0.57 to 0.87.

## Notable Citations to Follow Up

1. **Constantinides, George M., Jens C. Jackwerth, and Alexi Savov (2013)** — *The Puzzle of Index Option Returns* (Review of Asset Pricing Studies, 3(2), 229-257).
   - Shows that standard equilibrium asset pricing models with jumps and stochastic volatility cannot explain the cross-section of S&P 500 option returns.
2. **Mencía, Javier, and Enrique Sentana (2013)** — *Valuation of VIX Derivatives* (Journal of Financial Economics, 108(2), 367-391).
   - Establishes a comprehensive structural framework for pricing VIX futures and options with stochastic mean reversion and discrete volatility jumps.
3. **Moreira, Alan, and Tyler Muir (2017)** — *Volatility-Managed Portfolios* (Journal of Finance, 72(4), 1611-1644).
   - Documents that dynamically scaling back exposure during volatile regimes dramatically improves Sharpe ratios and alphas without sacrificing long-term returns.
