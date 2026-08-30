---
title: "Variance Risk Premia"
authors: "Peter Carr, Liuren Wu"
year: 2009
link: "https://engineering.nyu.edu/sites/default/files/2019-01/CarrReviewofFinStudiesMarch2009-a.pdf"
area: vrp-measurement
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Variance Risk Premia

- **Authors:** Peter Carr, Liuren Wu
- **Year:** 2009 (RFS 22(3), 1311-1341; first draft 2004)
- **Link:** [https://engineering.nyu.edu/sites/default/files/2019-01/CarrReviewofFinStudiesMarch2009-a.pdf](https://engineering.nyu.edu/sites/default/files/2019-01/CarrReviewofFinStudiesMarch2009-a.pdf)
- **PDF:** `carr-wu-2009-variance-risk-premia.pdf` (open-access copy, NYU Tandon faculty page)

## Testable Hypothesis

A synthetic variance-swap rate built from a cross-section of options robustly measures the variance risk premium, and this premium is negative and statistically significant not just for the S&P 500 index but across a broad cross-section of 35 individual stocks, implying that pure volatility-selling compensation is a pervasive, near-universal feature of equity options rather than an index-specific phenomenon.

## Summary

Proposes a model-free method for quantifying the variance risk premium as the difference between realized variance and a synthetic variance swap rate replicated from a portfolio of options. Applying it to five stock indexes and 35 individual stocks, finds variance risk premia are uniformly negative (i.e., variance sellers are paid), but the premium is markedly larger in magnitude and more statistically robust for index variance than for the average single-stock variance, pointing to a common, systematic (rather than idiosyncratic) source of the risk being compensated. Distinct from `coval-shumway-2001-expected-option-returns` in scope: rather than aggregate-index option returns alone, this establishes the cross-sectional breadth of the volatility risk premium across single names, and separates the systematic index-level component from idiosyncratic single-stock variance risk.

## Detailed Summary

### 1. Methodology & Model-Free Variance Swap Synthesis

Carr and Wu develop a model-free replication framework to quantify the return variance risk premium ($VRP$) on financial assets without requiring parametric assumptions on underlying return volatility dynamics.

1. **Synthetic Variance Swap Rate ($\mathbb{E}^\mathbb{Q}[RV_{t,T}]$)**:
   A variance swap pays the difference between annualized realized return variance $RV_{t,T}$ and a fixed swap rate $SW_{t,T}$. Under no-arbitrage, $SW_{t,T} = \mathbb{E}_t^\mathbb{Q}[RV_{t,T}]$. By applying Itô's lemma for semi-martingales to $\ln F_T$ (where $F$ is the forward/futures price), the annualized quadratic variation is replicated by a static portfolio of out-of-the-money European options plus dynamic futures trading:

   $$\mathbb{E}_t^\mathbb{Q}[RV_{t,T}] = \frac{2}{T - t} \int_0^\infty \frac{\Theta_t(K,T)}{B_t(T) K^2} dK + \varepsilon$$

   where $\Theta_t(K,T)$ is the out-of-the-money option price (put for $K \le F_t$, call for $K > F_t$), $B_t(T)$ is the discount bond, and $\varepsilon$ is the replication approximation error.
   - Under continuous price paths, $\varepsilon = 0$ exactly.
   - When jumps are present, the instantaneous approximation error is third order in jump size, $\mathcal{O}((dF_t/F_{t-})^3)$, and numerical simulations under Merton Jump-Diffusion (MJD) and Bates Stochastic Volatility with Jumps (MJDSV) confirm that jump and strike discretization errors are negligible ($\sim 0.0021$, or $<1.5\%$ of total variance).

2. **Volatility Swap Approximation & Variance of Volatility**:
   - The volatility swap rate $VS_{t,T} = \mathbb{E}_t^\mathbb{Q}[\sqrt{RV_{t,T}}]$ is accurately approximated by the at-the-money implied volatility ($ATMV_{t,T}$) with third-order accuracy $\mathcal{O}((T-t)^{3/2})$ (Carr and Lee, 2003a).
   - By Jensen's inequality, $SW_{t,T} \ge VS_{t,T}^2$. The difference $SW_{t,T} - VS_{t,T}^2 = \text{Var}_t^\mathbb{Q}(\sqrt{RV_{t,T}})$ provides a direct, observable, model-free measure of the risk-neutral *variance of return volatility* (vol-of-vol).

3. **Expectation Hypothesis & Asset Pricing Framework**:
   - Variance risk premium is evaluated both in levels $RP_{t,T} = RV_{t,T} - SW_{t,T}$ and log excess returns $LRP_{t,T} = \ln(RV_{t,T} / SW_{t,T})$.
   - Tested against classical CAPM ($\ln(RV/SW) = \alpha + \beta ER^m$), Fama-French three-factor ($\alpha + \beta ER^m + s SMB + h HML$), and volatility-of-volatility controls ($\ln RV = a + b \ln SW + c \ln(SW/VS^2)$) using GMM with Newey-West serial dependence corrections.

### 2. Data & Universe

- **Sample Period**: January 1996 – February 2003 (daily closing quotes, matched with monthly CRSP / Kenneth French factor libraries).
- **Data Source**: OptionMetrics Ivy DB (implied volatility surfaces, bid-ask quotes, interest rates, dividend yields) and CBOE.
- **Assets Analyzed**:
  - 5 stock indexes / baskets: S&P 500 (`SPX`, European), S&P 100 (`OEX`, American), Dow Jones Industrial Average (`DJX`, European), Nasdaq-100 (`NDX`, European), and Nasdaq-100 tracker (`QQQ`, American).
  - 35 actively traded individual equities (e.g., MSFT, INTC, IBM, GE, CSCO, AMZN, YHOO, DELL, ORCL, PFE, AMGN).
- **Construction Details**: Constant 30-day maturity constructed by linear interpolation between the two nearest expiries (>8 DTE to avoid microstructure distortions). Option surfaces interpolated across 2,000 strike points covering $\pm 8$ standard deviations from ATM.

### 3. Key Quantitative Results

#### Pervasive Negative Variance Risk Premia (Tables 4 & 5)
- **Synthetic Swap Rate vs. Realized Volatility**: Across all 5 indexes, implied swap rates $\sqrt{SW}$ systematically exceed realized volatility $\sqrt{RV}$:
  - *SPX*: $\sqrt{SW} = 24.41\%$ vs. $\sqrt{RV} = 18.82\%$ (implied exceeds realized by $+5.59\%$ annualized).
  - *OEX*: $\sqrt{SW} = 24.61\%$ vs. $\sqrt{RV} = 19.88\%$.
  - *DJX*: $\sqrt{SW} = 24.71\%$ vs. $\sqrt{RV} = 19.67\%$.
  - *NDX*: $\sqrt{SW} = 40.19\%$ vs. $\sqrt{RV} = 37.54\%$.
- **Statistical Significance of Log VRP ($LRP = \ln(RV/SW)$)**:
  - Broad index options show massive, highly significant negative excess returns to variance buyers: SPX $LRP = -0.594$ ($t = -9.48$), OEX $LRP = -0.509$ ($t = -7.83$), DJX $LRP = -0.525$ ($t = -7.03$). This represents an average loss of over **50% per month** for long variance swap buyers.
  - For individual equities, $LRP$ is negative for almost all 35 stocks (e.g., MSFT $-0.277, t=-5.90$; GE $-0.237, t=-5.49$; IBM $-0.232, t=-3.90$) and statistically significant in 21 of 35 names, but notably smaller in magnitude than index VRP.

#### Systematic vs. Idiosyncratic Variance Pricing (Figure 1 & Eq. 54)
- Regressing individual stock log risk premia ($LRP_j$) on their index variance beta $\beta_j^V = \text{Cov}(RV_j, RV_{SPX}) / \text{Var}(RV_{SPX})$ yields:
  $$LRP_j = 0.0201 + 0.2675 \beta_j^V \quad (R^2 = 15.9\%, \; t = 2.72)$$
- The market does not compensate investors for total firm-specific variance, but specifically prices the covariance of return variance with systematic market variance.

#### Inability of CAPM and Fama-French Factors to Explain VRP (Tables 6 & 7)
- **CAPM Regressions**: While index variance swaps exhibit heavy negative market betas ($\beta = -4.59$ for SPX, $t = -5.88$), the abnormal excess return intercept $\alpha$ remains deeply negative and significant: SPX $\alpha = -0.577$ ($t = -12.30$), OEX $\alpha = -0.492$ ($t = -10.29$).
- **Fama-French 3-Factor Model**: Controlling for Market ($ER^m$), Size ($SMB$), and Value ($HML$), the SPX intercept is $\alpha = -0.561$ ($t = -8.37$), with $SMB$ loading $s = -2.83$ ($t = -2.13$) and $HML$ loading $h = -0.29$ ($t = -0.34$, insignificant).
- **Conclusion**: The variance risk premium cannot be explained away by equity factor exposures and represents a heavily priced independent risk factor.

#### Dynamic Structure & Variance of Volatility (Tables 8, 9 & 10)
- **Expectation Hypothesis**: Regressing level realized variance on swap rate ($RV = a + b SW$) yields slope coefficients significantly below 1 for indexes (SPX $b = 0.526, t = -3.98$), consistent with Heston model dynamics under a negative market price of volatility risk ($\gamma < 0$).
- **Controlling for Vol-of-Vol**: When adding the log variance-of-volatility term $\ln(SW/VS^2)$ into the expectation regression ($\ln RV = a + b \ln SW + c \ln(SW/VS^2)$), the slope $b$ on $\ln SW$ converges almost perfectly to $1.00$ across all 5 indexes (SPX: $b = 1.007, t = 0.06$; OEX: $b = 1.001, t = 0.01$; NDX: $b = 1.076, t = 1.11$) and 30 of 35 individual stocks, while the vol-of-vol loading $c$ is strongly negative (SPX: $c = -1.146, t = -6.09$).

### 4. Relevance to Option Research

In `sophie-option-research`, Carr and Wu (2009) provides the foundational theoretical and empirical justification for systematic option-selling strategies (e.g. short SPX puts, covered strangles, and credit spreads):
1. **Index vs. Single-Stock Edge**: The finding that index VRP ($LRP \approx -0.59$) is vastly larger and more statistically robust than single-stock VRP proves that the primary premium in option writing comes from underwriting systematic, market-wide downside risk rather than idiosyncratic single-name volatility. This strongly validates focusing backtesting engines on `SPX`/`NDX` index products (`lab/strategy.py`).
2. **VRP Feature Engineering**: The formula for risk-neutral variance of volatility ($SW - VS^2 \approx \text{VIX}^2 - \text{ATMV}^2$) provides a model-free feature for `notebooks/02_features.ipynb` and `notebooks/09_vrp_study.ipynb` to predict time-varying variance risk premia and optimize trade entry sizing.
3. **Pure Premium Benchmarking**: Synthetic variance swap replication serves as the theoretical upper bound / pure benchmark for delta-hedged options trading against which discrete option writing and rolling strategies can be compared.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational empirical study proving that selling index volatility (SPX, OEX, DJX) earns substantial negative risk premia (variance sellers capture ~50% annualized excess returns) that cannot be explained by CAPM or Fama-French factors. Demonstrates that index option premium selling exploits priced market-wide covariance risk, whereas single-stock idiosyncratic variance is largely uncompensated.

## Notable Citations to Follow Up

1. **Carr, Peter, and Roger Lee (2003)** — *Robust Replication of Volatility Derivatives* (Working Paper, Bloomberg LP / Cornell University).
   - Derives model-free replication and pricing bounds for volatility swaps using at-the-money implied volatility.
2. **Bakshi, Gurdip, and Nikunj Kapadia (2003)** — *Delta-Hedged Gains and the Negative Market Volatility Risk Premium* (Review of Financial Studies, 16(2), 527-566).
   - Demonstrates that delta-hedged call and put positions earn systematically negative returns, isolating the pure market volatility risk premium.
3. **Blair, Benjamin J., Ser-Huang Poon, and Stephen J. Taylor (2001)** — *Forecasting S&P 100 Volatility: The Incremental Information Content of Implied Volatilities and High-Frequency Index Returns* (Journal of Econometrics, 105(1), 5-26).
   - Tests whether implied volatility subsumes high-frequency intraday realized volatility in out-of-sample volatility forecasting.
