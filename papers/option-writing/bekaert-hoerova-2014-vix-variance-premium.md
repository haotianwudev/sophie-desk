# The VIX, the Variance Premium and Stock Market Volatility

- **Authors:** Geert Bekaert, Marie Hoerova
- **Year:** 2014 (Journal of Econometrics 183(2), 181-192; working paper 2013)
- **Link:** [https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1675.pdf](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1675.pdf) (ECB Working Paper Series No. 1675)
- **PDF:** `bekaert-hoerova-2014-vix-variance-premium.pdf` (open-access copy, European Central Bank repository)

## Testable Hypothesis

Decomposing the squared VIX into conditional physical variance and the equity variance risk premium isolates investor risk aversion from physical uncertainty, showing that the variance premium alone drives stock return predictability while conditional stock variance predicts real economic activity and financial instability.

## Summary

Develops a framework using high-frequency realized volatility and flexible forecasting models to decompose the squared VIX into two unobservable components: the conditional expectation of actual future stock market variance (physical volatility) and the variance risk premium (a proxy for risk aversion). Shows that while the variance risk premium reliably predicts future stock market excess returns at short-to-intermediate horizons, the conditional variance component is the primary driver forecasting macro-economic activity and banking sector stress. This separation resolves the ambiguity in index option-selling literature regarding whether high implied volatility reflects rising physical risk or surging risk compensation.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Crucial for systematic VRP feature engineering and trade filtering; demonstrates that decomposing $VIX^2$ into conditional physical variance ($CV$) and variance risk premium ($VP = VIX^2 - CV$) isolates risk compensation from physical uncertainty. Shows that $VP$ drives future equity returns and option-writing profitability, while $CV$ acts as an economic danger signal.

## Notable Citations to Follow Up

1. **Corsi, Fulvio (2009)** — *A Simple Approximate Long Memory Model of Realized Volatility* (Journal of Financial Econometrics, 7(2), 174-196).
   - Introduces the HAR-RV framework (daily, weekly, monthly realized variance cascades), which serves as the premier benchmark for estimating physical conditional volatility $CV$.
2. **Corsi, Fulvio, and Roberto Renò (2012)** — *Discrete-Time Volatility Forecasting with Persistent Leverage Effect and the Link with Continuous-Time Volatility Modeling* (Journal of Business & Economic Statistics, 30(4), 468-480).
   - Enhances HAR models with multi-frequency asymmetric returns (leverage effect) and jump components (LHAR-CJ), directly applicable to short-term option pricing features.
3. **Andersen, Torben G., Tim Bollerslev, and Francis X. Diebold (2007)** — *Roughing It Up: Including Jump Components in the Measurement, Modeling, and Forecasting of Return Volatility* (Review of Economics and Statistics, 89(4), 701-720).
   - Establishes bipower variation techniques to decompose realized quadratic variation into continuous diffusion versus discrete jump components.
