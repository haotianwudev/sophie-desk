---
title: "Downside Variance Risk Premium"
authors: "Bruno Feunou, Mohammad R. Jahan-Parvar, Cédric Okou"
year: 2018
link: "https://www.oar-rao.bank-banque-canada.ca/record/6595/files/wp2015-36.pdf"
area: vrp-measurement
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Downside Variance Risk Premium

- **Authors:** Bruno Feunou, Mohammad R. Jahan-Parvar, Cédric Okou
- **Year:** 2018 (Journal of Financial Econometrics 16(3), 341-383; working paper 2015)
- **Link:** [https://www.oar-rao.bank-banque-canada.ca/record/6595/files/wp2015-36.pdf](https://www.oar-rao.bank-banque-canada.ca/record/6595/files/wp2015-36.pdf) (Bank of Canada Staff Working Paper 2015-36)
- **PDF:** `feunou-jahan-parvar-okou-2018-downside-variance-risk-premium.pdf` (open-access copy, Bank of Canada repository)

## Testable Hypothesis

Decomposing the aggregate variance risk premium into downside and upside semi-variances reveals that the downside variance risk premium (compensation for bearing adverse price fluctuations) accounts for virtually all equity return predictability, whereas the difference between upside and downside components (skewness risk premium) is negatively associated with future stock returns.

## Summary

Proposes a model-free decomposition of total variance risk premium into downside variance risk premium (DVRP) and upside variance risk premium (UVRP) based on semi-variance corridor contracts. Shows empirically that DVRP is the economically dominant component of the total variance premium and drives the predictive power of option-implied variance for subsequent excess stock market returns. In contrast, UVRP has negligible predictive power. This asymmetry demonstrates that option market participants exhibit strong aversion to downside market turmoil while treating upside volatility neutrally, providing direct structural justification for why short out-of-the-money put options command a disproportionately higher premium than symmetrical out-of-the-money calls.

## Detailed Summary

### 1. Methodology & Semi-Variance Decomposition

Feunou, Jahan-Parvar, and Okou propose a non-parametric model-free framework to decompose the aggregate Variance Risk Premium ($VRP$) into directional components:
$$VRP_{t,h} \equiv VRP_{t,h}^U + VRP_{t,h}^D$$
where:
- **Downside Variance Risk Premium ($VRP^D$ or $DVRP$)**: $E_t^\mathbb{Q}[RV_{t,h}^D] - E_t^\mathbb{P}[RV_{t,h}^D]$, measuring the compensation demanded by investors to bear bad (downside) volatility.
- **Upside Variance Risk Premium ($VRP^U$ or $UVRP$)**: $E_t^\mathbb{Q}[RV_{t,h}^U] - E_t^\mathbb{P}[RV_{t,h}^U]$, measuring the price/discount investors are willing to pay for exposure to good (upside) volatility.
- **Skewness Risk Premium ($SRP$)**:
  $$SRP_{t,h} \equiv VRP_{t,h}^U - VRP_{t,h}^D = E_t^\mathbb{Q}[RSV_{t,h}] - E_t^\mathbb{P}[RSV_{t,h}]$$
  where $RSV_{t,h} = RV_{t,h}^U - RV_{t,h}^D$ is realized skewness (signed jump variation).

**Construction of Realized & Risk-Neutral Measures:**
- **Realized Semi-Variances**: Computed from 5-minute intraday returns of the S&P 500 separated by threshold $\kappa = 0$:
  $$RV_t^U = \sum_{j=1}^{n_t} r_{j,t}^2 1_{\{r_{j,t} > 0\}}, \quad RV_t^D = \sum_{j=1}^{n_t} r_{j,t}^2 1_{\{r_{j,t} \le 0\}}$$
- **Risk-Neutral Semi-Variances ($IV^U, IV^D$)**: Constructed from OptionMetrics S&P 500 options across 1,000 finely discretized strike prices using Andersen-Bondarenko (2007) corridor integrals:
  $$IV_t^U \approx 2 \int_{F_t}^\infty \frac{\min(P_t(S), C_t(S))}{S^2} dS, \quad IV_t^D \approx 2 \int_0^{F_t} \frac{\min(P_t(S), C_t(S))}{S^2} dS$$

**Theoretical Model:**
The authors solve an equilibrium consumption-based asset pricing model with Epstein-Zin recursive preferences and asymmetric Gamma-distributed consumption shocks with separate upside/downside time-varying volatility-of-volatility ($q_{u,t}, q_{d,t}$). The model proves analytically that $VRP^D > 0$, $VRP^U < 0$, and $SRP < 0$.

### 2. Data & Sample Period

- **Primary Sample**: September 1996 to December 2010 ($N = 3,608$ daily observations).
- **Options Data**: 536,443 out-of-the-money S&P 500 European call and put contracts from OptionMetrics Ivy DB across maturities from 1 to 24 months.
- **High-Frequency Data**: 5-minute intraday S&P 500 index prices from the Institute of Financial Markets (IFM).
- **Subsample for Pre-Crisis Robustness**: September 1996 to December 2007 ($N = 2,852$).

### 3. Key Quantitative Results

#### Empirical Magnitudes & Asymmetry (Table 1, Panel D)
- **Downside VRP ($DVRP$)**: Annualized mean is **$+5.21\%$** (median $4.87\%$, Std Dev $3.82\%$).
- **Upside VRP ($UVRP$)**: Annualized mean is **$-2.60\%$** (median $-2.57\%$, Std Dev $2.59\%$).
- **Total VRP**: Annualized mean is **$+2.64\%$** ($5.21\% - 2.60\%$).
- **Skewness Risk Premium ($SRP$)**: Annualized mean is **$-7.81\%$** (median $-6.99\%$, Std Dev $3.06\%$).
- **Economic Takeaway**: Downside variance risk compensation accounts for **more than $80\%$ of total gross variance risk premia**. Investors demand large positive compensation for downside crash exposure, while accepting a negative premium (discount) for exposure to upside gains.

#### Equity Excess Return Predictability (Tables 3 & 6)
- **Short-Horizon Predictability ($k = 3$ months, Table 3)**:
  - Total $VRP$: $t\text{-stat} = 4.11, \text{Adj. } R^2 = 8.13\%$.
  - Downside $VRP^D$: $t\text{-stat} = \mathbf{4.76}, \text{Adj. } R^2 = \mathbf{10.72\%}$ (subsumes and outperforms total $VRP$).
  - Upside $VRP^U$: $t\text{-stat} = 3.05, R^2 = 4.41\%$.
  - Joint Model ($VRP^U + VRP^D$, Table 6 Panel A): $t_{down} = 3.79, t_{up} = -1.28, \text{Adj. } R^2 = \mathbf{11.04\%}$.
- **Intermediate & Long-Horizon Predictability ($SRP$, Table 3 Panel D)**:
  - While $VRP$ and $VRP^D$ predictability peaks at 3–6 months and declines, $SRP$ predictability **peaks at 6 to 12 months**:
    - At $k = 6$ months: $t = 4.05, \text{Adj. } R^2 = 8.00\%$ ($h=6$).
    - At $k = 9$ months: $t = 4.20, \text{Adj. } R^2 = \mathbf{10.59\%}$ ($h=12$).
    - At $k = 12$ months: $t = 4.07, \text{Adj. } R^2 = 8.34\%$ ($h=12$).
  - Proves that $SRP$ acts as the missing bridge between short-run option VRP predictability (1–3 months) and long-run valuation ratios ($P/E, P/D, CAY$).

#### Multivariate Robustness & Out-of-Sample Performance (Tables 8, 10, 11)
- In multivariate semi-annual regressions ($h=6$, Table 8), $DVRP$ maintains robust significance ($t = 2.49$ to $3.76$) alongside $P/D, P/E$, term spread, default spread, inflation, and Kelly-Pruitt cross-sectional index ($\text{Adj. } R^2$ reaches $25.71\%$).
- Pre-crisis sample ($1996\text{--}2007$, Table 10): $DVRP$ multivariate $R^2$ reaches **$41.8\%\text{--}49.4\%$** ($t = 5.78\text{--}8.47$).
- Diebold-Mariano out-of-sample tests (Table 11) confirm that $DVRP$ and $SRP$ outperform classical predictors out-of-sample across 1, 3, and 6-month horizons.

### 4. Relevance to Option Research

The insights from Feunou, Jahan-Parvar, and Okou directly shape option strategy design and quantitative risk modeling in `sophie-option-research`:
1. **Structural Rationale for Short Put Bias**: Provides mathematical and empirical proof for why systematic option writing should focus on short OTM puts (or bull put spreads) rather than symmetrical call selling or straddles: investors pay **$+5.21\%$** for downside protection but discount upside volatility by **$-2.60\%$**. Short call strategies are structurally undercompensated relative to put selling.
2. **Directional Feature Engineering**: Replaces aggregate $VRP$ with directional semi-variance metrics ($DVRP = IV^D - RV^D$ and $SRP = IV^U - IV^D - (RV^U - RV^D)$) in `lab/features.py`.
3. **Multi-Horizon Signal Layering**:
   - **Tactical (1–3 Months)**: High $DVRP$ indicates rich put option premiums and strong short-term mean-reversion upside for equities, signaling aggressive short put deployment.
   - **Strategic (6–12 Months)**: Deeply negative $SRP$ indicates elevated left-tail skewness pricing, forecasting favorable risk-adjusted equity returns over semi-annual to annual holding periods.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Crucial structural study decomposing total VRP into Downside Variance Risk Premium (DVRP) and Upside Variance Risk Premium (UVRP), proving that >80% of option premium compensation stems exclusively from downside variance ($DVRP \approx +5.2\%$, $UVRP \approx -2.6\%$). Directly justifies concentrating option selling on short OTM put strategies over call writing and provides actionable semi-variance/skewness feature metrics.

## Notable Citations to Follow Up

1. **Barndorff-Nielsen, Ole E., Silja Kinnebrock, and Neil Shephard (2010)** — *Measuring Downside Risk: Realised Semivariance* (in Volatility and Time Series Econometrics: Essays in Honor of Robert F. Engle, Oxford University Press, 117-136).
   - Establishes the mathematical theory of realized semi-variances for decomposing intraday high-frequency return variation into directional components.
2. **Kozhan, Roman, Anthony Neuberger, and Paul Schneider (2013)** — *The Skew Risk Premium in the Equity Index Market* (Review of Financial Studies, 26(9), 2174-2203).
   - Characterizes the pricing and tradeable replication of the skewness risk premium using model-free option portfolios and cubic swap contracts.
3. **Patton, Andrew J., and Kevin Sheppard (2015)** — *Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility* (Review of Economics and Statistics, 97(3), 683-697).
   - Demonstrates that downside semi-variance and negative signed jumps provide vastly superior forecasting power for future market volatility compared to upside semi-variance.
