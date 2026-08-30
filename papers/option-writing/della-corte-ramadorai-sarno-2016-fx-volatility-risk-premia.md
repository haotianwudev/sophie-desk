---
title: "Volatility Risk Premia and Exchange Rate Predictability"
authors: "Pasquale Della Corte, Tarun Ramadorai, Lucio Sarno"
year: 2016
link: "https://www.aeaweb.org/conference/2014/retrieve.php?pdfid=554"
area: cross-asset
relevance: Medium
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Volatility Risk Premia and Exchange Rate Predictability

- **Authors:** Pasquale Della Corte, Tarun Ramadorai, Lucio Sarno
- **Year:** 2016 (Journal of Financial Economics 120(1), 21-40; working paper 2013)
- **Link:** [https://www.aeaweb.org/conference/2014/retrieve.php?pdfid=554](https://www.aeaweb.org/conference/2014/retrieve.php?pdfid=554)
- **PDF:** `della-corte-ramadorai-sarno-2016-fx-volatility-risk-premia.pdf` (open-access working-paper copy, AEA conference archive)

## Testable Hypothesis

Selling volatility insurance in the currencies with the highest volatility risk premium (implied minus realized volatility) and buying it in the lowest generates a systematic cross-sectional strategy whose returns come mainly from spot exchange-rate movements rather than interest-rate differentials, and which carries more portfolio weight than the classic FX carry or momentum factors.

## Summary

Constructs a currency-by-currency volatility risk premium (implied vol from FX options minus subsequently realized vol) and forms a cross-sectional strategy that is short options / short insurance in high-premium currencies and long in low-premium ones. Finds the strategy earns significant, largely uncorrelated returns relative to carry and momentum, and traces the return source to exchange-rate spot moves rather than rate differentials. This is the folder's first genuinely cross-asset (FX rather than equity-index) test of systematic premium selling, directly answering the "cross-asset premium comparison" gap relative to the SPX/VIX-only papers already collected.

## Detailed Summary

### 1. Methodology & Currency VRP Construction

Della Corte, Ramadorai, and Sarno examine the pricing and predictive power of volatility risk premia ($VRP$) in the global foreign exchange (FX) market by constructing a cross-sectional currency trading strategy sorted by the cost of volatility insurance.

1. **Model-Free Implied Volatility & Volatility Swaps**:
   - A volatility swap delivers payoff $VP_{t,\tau} = RV_{t,\tau} - SW_{t,\tau}$, where under risk-neutral pricing $SW_{t,\tau} = \mathbb{E}_t^\mathbb{Q}[RV_{t,\tau}]$.
   - Synthesizes the model-free implied variance using the Britten-Jones and Neuberger (2000) / Jiang and Tian (2005) formulation by integrating over a cubic spline of Garman-Kohlhagen (1983) option prices across 5 standardized delta quotes (10-delta put, 25-delta put, ATM straddle, 25-delta call, 10-delta call):
     $$\mathbb{E}_t^\mathbb{Q}[RV_{t,\tau}^2] = \kappa \left( \int_0^{F_{t,\tau}} \frac{1}{K^2} P_{t,\tau}(K) dK + \int_{F_{t,\tau}}^\infty \frac{1}{K^2} C_{t,\tau}(K) dK \right)$$
   - Model-free implied volatility is defined as $SW_{t,\tau} = \sqrt{\mathbb{E}_t^\mathbb{Q}[RV_{t,\tau}^2]}$.
2. **Measuring Currency-Specific VRP**:
   - Following Bollerslev, Tauchen, and Zhou (2009) and Carr and Wu (2009), the $\tau$-period volatility risk premium is defined as:
     $$VRP_{t,\tau} \equiv \mathbb{E}_t^\mathbb{P}[RV_{t,\tau}] - \mathbb{E}_t^\mathbb{Q}[RV_{t,\tau}] \approx RV_{t-\tau,t} - SW_{t,\tau}$$
   - Currencies with high $VRP$ (realized volatility exceeds option implied volatility) have relatively *cheap* volatility insurance; currencies with low $VRP$ (implied volatility significantly exceeds realized) have *expensive* volatility insurance.
3. **Cross-Sectional Portfolio Construction**:
   - At the end of each month $t$, currencies are sorted into 5 quintile portfolios based on their 1-year $VRP$.
   - The long-short strategy ($VRP = P_L - P_S$) goes long $P_L$ (top 20% cheapest insurance) and short $P_S$ (top 20% most expensive insurance).
   - Decomposes excess returns $RX_{t+1} \approx \frac{S_{t+1} - S_t}{S_t} - (i_t - i_t^*)$ into spot exchange rate changes (FX return) and interest rate differentials (yield).

### 2. Data & Universe

- **Sample Period**: January 1996 – August 2011 (187 monthly rebalancing periods).
- **Data Sources**: JP Morgan (daily OTC currency option implied volatilities, risk reversals, butterfly spreads, and deposit interest rates), Barclays/Reuters via Datastream (daily spot and forward exchange rates), CFTC Commitments of Traders (commercial vs. financial net positions), and consolidated hedge fund database (634 macro/currency hedge funds managing $1.5T AUM from HFR, CISDM, TASS, Morningstar, Barclay-Hedge).
- **Universe**: 20 currency pairs against USD:
  - *Developed (G10)*: AUD, CAD, CHF, DKK, EUR, GBP, JPY, NOK, NZD, SEK.
  - *Emerging (G10)*: BRL, CZK, HUF, KRW, MXN, PLN, SGD, TRY, TWD, ZAR.
  - Contract horizon: 1-year constant maturity.

### 3. Key Quantitative Results

#### Summary Statistics of FX Volatility Risk Premia (Table 1, Table A.1)
- **Developed Currencies**: Average 1-year realized volatility $RV = 10.68\%$ ($SD = 2.88\%$), synthetic swap rate $SW = 11.31\%$ ($SD = 2.75\%$), and average $VRP = -0.62\%$ ($SD = 1.58\%$).
- **Developed & Emerging**: Average $RV = 10.82\%$, $SW = 11.74\%$, and $VRP = -0.92\%$ ($SD = 1.78\%$).
- **Country Breakdown**: $VRP$ is negative for almost every individual currency: MXN ($-5.47\%$), TRY ($-4.59\%$), BRL ($-3.78\%$), ZAR ($-2.57\%$), TWD ($-2.34\%$), EUR ($-1.16\%$), GBP ($-1.15\%$), CAD ($-0.59\%$), CHF ($-0.51\%$), JPY ($-0.45\%$), AUD ($+0.39\%$).

#### VRP Strategy Performance & Spot Return Driver (Tables 2 & 3)
- **Excess Returns (Panel A)**:
  - Developed Sample: Annualized excess return **+4.03%** ($SD = 8.33\%$, Sharpe ratio **0.48**, Sortino **0.87**, Maximum Drawdown **-18%**).
  - Developed & Emerging: Annualized excess return **+2.34%** (Sharpe **0.29**, Drawdown **-18%**).
- **Dominance of Spot Predictability (Panel B)**:
  - Unlike the carry trade ($CAR$), where 95%+ of return is driven by interest differentials while spot FX return is near zero or negative (+0.34% Developed, -0.65% full sample), the $VRP$ strategy return is **100% generated by spot exchange rate moves**:
  - Developed Spot FX Return: **+4.40% per year** (Sharpe **0.53**, Sortino **0.93**, Drawdown **-19%**).
  - Full Sample Spot FX Return: **+3.72% per year** (Sharpe **0.46**, Sortino **0.75**, Drawdown **-18%**).
  - Currencies with cheap volatility insurance appreciate, while those with expensive volatility insurance depreciate.

#### Uncorrelated Returns & Optimal Allocation (Table 3, Figure 3)
- **Low/Negative Correlation**: VRP strategy excess returns are negatively correlated with Carry ($r = -0.18$ Developed, $-0.21$ full sample) and virtually orthogonal to Momentum ($r = +0.09$), Value ($r = +0.23$), and Risk Reversals ($r = -0.01$).
- **Global Minimum Variance Portfolio (MVP)**: In an optimal mean-variance portfolio combining all 5 currency strategies ($CAR, MOM, VAL, RR, VRP$), $VRP$ receives the **largest weight of any strategy at 33%** (a full one-third of the portfolio), lifting the overall portfolio Sharpe ratio from **0.79 to 0.92** for developed currencies.

#### Recession & Crisis Resilience (Table 4)
- **NBER Recessions (Panel A)**: VRP delivers an annualized return of **+11.54%** (Sharpe **1.14**, max drawdown -9%), while the Carry trade crashes at **-9.59%** (Sharpe **-0.56**, max drawdown -40%).
- **2007–2009 Financial Crisis (Panel D)**: VRP returned **+9.61% per year** (Sharpe **1.06**, max drawdown -8%), confirming it serves as an effective crisis hedge.

#### Mechanism: Limits to Arbitrage & Intermediary Constraints (Table 8, Figures 4 & 5)
- **Macro Conditioning**: Interacting the TED spread with 12-month rolling $\Delta VIX$ strongly predicts higher VRP spot returns ($\beta = 0.09, t = 4.5$), indicating that when dealer funding liquidity tightens and risk aversion rises, mispricing spreads widen.
- **Hedge Fund Capital Flows**: When capital flows into macro/currency hedge funds are high (relaxing speculator capital constraints), subsequent VRP strategy returns fall ($\beta = -1.50, t = -2.08$).
- **CFTC Positioning (Figure 5)**: Commercial hedgers consistently sell expensive-insurance currencies and buy cheap-insurance currencies, while financial traders take the opposite side as market-makers.
- **Return Reversals (Figure 4)**: Cumulative post-formation returns peak at 3–4 months and mean-revert thereafter, reflecting the multi-month redeployment horizon of speculative arbitrage capital.

### 4. Relevance to Option Research

In `sophie-option-research`, Della Corte et al. (2016) provides key empirical lessons for cross-asset volatility modeling and portfolio construction:
1. **Cross-Asset Volatility Arbitrage**: Demonstrates that the volatility risk premium is not an isolated quirk of equity index options, but a universal market pricing phenomenon present across global currency pairs.
2. **Asymmetric Hedging & Crisis Decoupling**: While short equity index options and currency carry trades suffer severe left-tail crashes during market crises, cross-sectional VRP ranking strategies produce massive positive returns during recessions (+11.54%/yr, Sharpe 1.14 during NBER downturns), offering a blueprint for constructing hedged volatility overlays in `notebooks/09_vrp_study.ipynb` and `lab/strategy.py`.
3. **Multi-Horizon Capital Flow Filters**: Incorporating macro liquidity indicators (such as TED spreads and funding constraints) as regime switches helps identify when options pricing diverges from fundamental realized volatility due to intermediary capacity limits.

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** Valuable cross-asset demonstration that the volatility risk premium is a universal phenomenon whose cross-sectional sorting provides strong downside protection and crisis alpha (+11.5% in recessions). However, because `sophie-option-research` is dedicated to SPX/US equity options, its specific FX spot-predictability mechanisms and currency-option-space tools are informative conceptually rather than directly actionable for our equity index execution pipeline.

## Notable Citations to Follow Up

1. **Menkhoff, Lukas, Lucio Sarno, Maik Schmeling, and Andreas Schrimpf (2012)** — *Carry Trades and Global FX Volatility* (Journal of Finance, 67(2), 681-718).
   - Establishes how global volatility innovations act as a priced risk factor across currency strategies, explaining why high-yielding assets crash during volatility spikes.
2. **Lustig, Hanno, Nikolai Roussanov, and Adrien Verdelhan (2011)** — *Common Risk Factors in Currency Markets* (Review of Financial Studies, 24(11), 3731-3777).
   - Seminal empirical work defining the cross-sectional factor structure of currency returns and quantifying global currency risk premia.
3. **Buraschi, Andrea, Fabio Trojani, and Andrea Vedolin (2014)** — *When Uncertainty Blows in the Orchard: Comovement and Equilibrium Volatility Risk Premia* (Journal of Finance, 69(1), 101-137).
   - Models how belief dispersion and economic uncertainty drive the comovement and cross-sectional pricing of volatility risk premia across derivative markets.
