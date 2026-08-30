---
title: "The Price of Variance Risk"
authors: "Ian Dew-Becker, Stefano Giglio, Anh Le, Marius Rodriguez"
year: 2017
link: "https://www.nber.org/system/files/working_papers/w21182/w21182.pdf"
area: vrp-measurement
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The Price of Variance Risk

- **Authors:** Ian Dew-Becker, Stefano Giglio, Anh Le, Marius Rodriguez
- **Year:** 2017 (Journal of Financial Economics 123(2), 225-250; working paper 2015)
- **Link:** [https://www.nber.org/system/files/working_papers/w21182/w21182.pdf](https://www.nber.org/system/files/working_papers/w21182/w21182.pdf) (NBER Working Paper No. 21182)
- **PDF:** `dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk.pdf` (open-access copy, NBER repository)

## Testable Hypothesis

The market price of variance risk is concentrated entirely at the ultra-short end (1-2 month maturities), while forward variance claims with maturities beyond two months carry an expected return of zero, proving that financial markets only price transient, immediate volatility shocks rather than persistent long-run variance uncertainty.

## Summary

Estimates the term structure of variance risk premia across horizons from 1 to 24 months using a rich panel of variance swaps and synthetic forward variance swaps on the S&P 500. Documents that while spot (1-month) variance swaps carry large negative returns (-20% to -30% annualized, compensating variance sellers), forward variance swaps settling on volatility beyond the front two months earn zero risk premium on average. This establishes that investors pay a steep premium exclusively to hedge short-term volatility spikes rather than innovations to long-term expected variance, challenging leading macro-finance asset pricing models (e.g., long-run risk models) that rely on persistent variance risk pricing.

## Detailed Summary

### 1. Methodology & Data Panel

Dew-Becker, Giglio, Le, and Rodriguez provide the first comprehensive empirical investigation of the entire term structure of variance risk premia, spanning maturities from 1 month to 14 years.

**Variance Swaps & Forward Variance Claims:**
- An $m$-day variance swap pays the difference between realized variance and the contract strike: $\text{Payoff}_\tau^m = \sum_{j=\tau+1}^{\tau+m} r_j^2 - VS_\tau^m$.
- To isolate risk pricing at specific forward horizons, the authors define $n$-month **zero-coupon variance claims**:
  $$Z_t^n \equiv E_t^\mathbb{Q}[RV_{t+n}] = VS_t^n - VS_t^{n-1}$$
  where $Z_t^0 = RV_t$ and $Z_t^1 = VS_t^1$ (the standard 1-month variance swap).
- Monthly holding return on an $n$-month claim rolled each month: $R_{t+1}^n = \frac{Z_{t+1}^{n-1} - Z_t^n}{Z_t^n}$.

**Novel Dataset (1996–2014):**
- Two proprietary S&P 500 variance swap datasets: Dataset 1 (monthly fixed maturities 1–24 months, Dec 1995–Oct 2013) and Dataset 2 (Markit Totem dealer quotes across 11 market makers up to 14-year maturities, Aug 2007–Feb 2014, verified against DTCC repository transaction records).
- Synthetic option-implied variance curves constructed for international indexes: S&P 500, Euro Stoxx 50, FTSE 100, DAX, and CAC 40.
- Risk prices estimated via Fama-MacBeth two-pass regressions and continuous-time affine no-arbitrage term structure models (CIR, Constant Variance, Flexible specifications).

### 2. Key Quantitative Results

#### Sharpe Ratios Across the Term Structure (Table 2 & Figure 4)
- **1-Month Variance Swap ($Z_t^1$)**: Average monthly return is **$-25.6\%$** (Std Dev $69.0\%$, skew $6.1$, excess kurtosis $54.3$). This translates to an **annualized Sharpe ratio of $-1.40$ to $-1.70$** (four times larger in magnitude than the S&P 500 equity Sharpe ratio of $+0.43$).
- **2-Month Claim ($Z_t^2$)**: Average monthly return is **$-5.6\%$** (Std Dev $47.8\%$), yielding an annualized Sharpe ratio of $\approx -0.50$.
- **3-Month to 12-Month Forward Claims ($Z_t^3$ to $Z_t^{12}$)**: Average monthly returns turn positive ($+0.8\%$ at 3m, $+0.5\%$ at 6m, $+1.8\%$ at 12m), and annualized Sharpe ratios are **statistically indistinguishable from zero** (Figure 4, range $0.0$ to $+0.35$).
- Investors pay an enormous premium to hedge 30-day realized variance, but **zero premium** to hedge variance shocks occurring beyond 2 months.

#### Pricing of Shocks & Factor Risk Prices (Tables 3, 4, 7 & Table A.6)
- Principal component analysis shows that two factors explain **$99.9\%$ of the term structure** ($97.1\%$ level $s_t^2$, $2.7\%$ slope $l_t^2$).
- Using a 3-variable VAR ($s^2, l^2, RV$) rotated via Cholesky decomposition:
  - Level shock ($s_t^2$) risk price: $-0.11$ ($t = -0.35$, statistically insignificant).
  - Slope shock ($l_t^2$) risk price: $-0.18$ ($t = -1.50$, statistically insignificant).
  - **Pure Transitory Realized Variance Shock ($RV$)**: Annualized risk price is **$-1.70$ ($t = -3.54, p < 0.001$)** in the no-arbitrage model (and $-2.72$ in Fama-MacBeth).
  - Adding the pure $RV$ shock to CAPM increases the cross-sectional $R^2$ from **$37.7\%$ to $99.7\%$** (Table 4).

#### Downside vs. Upside Semivariance Decomposition (Figure 8)
- Decomposing total implied variance into downside and upside components: $VIX_t^2 = (VIX_t^D)^2 + (VIX_t^U)^2$.
- The steep negative return on short variance claims is driven entirely by downside semivariance $VIX^D$ (**$-30\%$ per month**), while $VIX^U$ return is close to zero. Investors are specifically buying crash insurance rather than general volatility insurance.

#### International Evidence & Disaster Dynamics (Table 8 & Figure 11)
- Global consistency: Term structures for Euro Stoxx 50, FTSE 100, DAX, and CAC 40 display the identical ultra-steep front end and flat forward curve.
- 28 disaster events across 17 countries show that realized volatility spikes to $25.2\%$–$83.1\%$ during disasters but is highly transitory: **volatility peaks for only 1 month**, dropping by $40\%$ one month after and $50\%$ three months out.

#### Rejection of Macro-Finance Models
- The empirical flat forward Sharpe curve decisively rejects standard Epstein-Zin long-run risk models (Drechsler & Yaron 2011) and time-varying disaster risk models (Wachter 2013), which counterfactually predict that forward variance claims should earn massive negative Sharpe ratios ($-1.0$ to $-1.2$).
- Supports myopic power utility / time-varying recovery disaster frameworks (Gabaix 2012).

### 3. Relevance to Option Research

The findings of Dew-Becker et al. provide essential empirical guidance for strategy design in `sophie-option-research`:
1. **Optimal Tenor Selection (30–45 DTE Concentration)**: The variance risk premium is strictly front-loaded (1–2 months). Selling 30–45 DTE options captures maximum risk compensation (Sharpe $-1.4$ to $-1.7$) while completely avoiding the uncompensated duration/vega risk of longer tenors (60–365 DTE).
2. **Superiority of Rolling Short Options**: Explains why systematic rolling of short-tenor options (`08_rolling.py`) dramatically outperforms holding long-tenor options.
3. **Downside Tail Risk Mitigation**: Because the premium is concentrated in downside semivariance ($VIX^D$), short put strategies must implement disciplined stop-losses or delta roll rules (`mgmt04` / `lab/features.py`) to survive 1-month crisis spikes without forfeiting the structural front-month VRP harvest.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Crucial empirical foundation for tenor selection in option writing; demonstrates that the variance risk premium is concentrated entirely at the 1–2 month horizon (Sharpe ratio of -1.7 on 1-month claims) while forward variance beyond 2 months earns zero premium. Strongly justifies trading short-dated tenors (30–45 DTE) to harvest peak theta decay and risk compensation without taking uncompensated long-dated variance duration risk.

## Notable Citations to Follow Up

1. **Aït-Sahalia, Yacine, Mustafa Karaman, and Loriano Mancini (2015)** — *The Term Structure of Variance Swaps, Risk Premia and the Expectations Hypothesis* (Working Paper, Princeton University).
   - Develops continuous-time no-arbitrage term-structure models separating jump risk from diffusive volatility risk across the variance swap curve.
2. **Gabaix, Xavier (2012)** — *Variable Rare Disasters: An Exactly Solved Framework for Ten Puzzles in Macro-Finance* (Quarterly Journal of Economics, 127(2), 645-700).
   - Formulates the time-varying disaster recovery model that explains why short-dated volatility carries extreme premia while long-dated forward volatility news remains unpriced.
3. **Bollerslev, Tim, and Viktor Todorov (2011)** — *Tails, Fears, and Risk Premia* (Journal of Finance, 66(6), 2165-2211).
   - Develops a non-parametric extreme value framework to isolate the jump tail risk premium from high-frequency options data.
