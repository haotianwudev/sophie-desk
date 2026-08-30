---
title: "Demand-Based Option Pricing"
authors: "Nicolae Gârleanu, Lasse Heje Pedersen, Allen M. Poteshman"
year: 2009
link: "https://www.nber.org/papers/w11843"
area: market-microstructure
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Demand-Based Option Pricing

- **Authors:** Nicolae Gârleanu, Lasse Heje Pedersen, Allen M. Poteshman
- **Year:** 2009 (Review of Financial Studies 22(10), 4259-4299; NBER Working Paper 11843, 2005)
- **Link:** [https://www.nber.org/papers/w11843](https://www.nber.org/papers/w11843)
- **PDF:** garleanu-pedersen-poteshman-2009-demand-based-option-pricing.pdf (open-access copy, NBER Working Paper 11843)

## Testable Hypothesis

End-user net demand pressure for unhedgeable option risks increases option prices proportionally to the variance of the unhedgeable component, explaining why net long customer buying of out-of-the-money index puts generates the steep implied volatility smirk and elevated index option prices.

## Summary

Develops an equilibrium model of option pricing where market makers cannot perfectly hedge inventory risk due to jump risk and stochastic volatility. Shows theoretically and empirically—using proprietary CBOE clearing data on non-market-maker positions—that end-user demand pressure directly drives option market prices above Black-Scholes values. In index options, end users are structurally net long index options (especially out-of-the-money puts for portfolio insurance), forcing dealers short and bidding up index implied volatilities and steepening the volatility smirk. In single-stock options, demand imbalances similarly account for cross-sectional option price deviations.

## Detailed Summary

### 1. Theoretical Model & Unhedgeable Inventory Risk

Gârleanu, Pedersen, and Poteshman construct a discrete-time equilibrium model of option market intermediation where competitive, risk-averse dealers (CARA utility, risk aversion $\gamma$) absorb net option order flow from end users. Because markets are incomplete due to discrete rebalancing ($\Delta t$), underlying jumps ($\kappa$), and stochastic volatility ($\Delta \sigma$), dealers cannot perfectly hedge their derivative inventories.

**Demand-Based Pricing Kernel & Price Sensitivity (Theorems 1 & 2):**
The equilibrium option price vector $p_t$ satisfies $p_t = \frac{1}{R_f} E_t^d[p_{t+1}]$ under a demand-shifted pricing kernel $m_{t+1}^d$. The marginal price impact of end-user demand $d_t^j$ on option contract $i$ is:
$$\frac{\partial p_t^i}{\partial d_t^j} = \gamma (R_f - 1) \text{Cov}_t^d(\bar{p}_{t+1}^i, \bar{p}_{t+1}^j)$$
where $\bar{p}_{t+1}^k = R_f^{-1}(p_{t+1}^k - R_f p_t^k - \frac{\text{Cov}_t^d(p_{t+1}^k, R_{t+1}^e)}{\text{Var}_t^d(R_{t+1}^e)} R_{t+1}^e)$ represents the unhedgeable component of the price change.

**Core Theoretical Predictions:**
1. **Unhedgeable Variance Markup**: Total premium paid by end users over frictionless price is proportional to dealer aggregate risk aversion and the total variance of their unhedgeable portfolio:
   $$d_t' p_t = d_t' p_t(0) + \gamma (R_f - 1) \text{Var}_t^d(d_t' \bar{p}_{t+1})$$
2. **Cross-Option Spillover**: Buying pressure in contract $j$ drives up prices of all correlated options $i$ on the same underlying through $\text{Cov}(\bar{p}^i, \bar{p}^j)$.
3. **Smirk Formation via Jumps**: While discrete trading and stochastic volatility primarily shift the **level** of implied volatility, unhedgeable jump risk $\kappa$ generates a first-order steepening of the **implied volatility smirk** (Propositions 4 & 6).

### 2. Data & Empirical Setup

- **Sample Period**: January 1996 through December 2001 ($N = 1,511$ trading days).
- **Unique Positioning Data**: Daily CBOE open interest records for all S&P 500 (SPX) index options and 303 liquid single-stock options, categorizing positions into: Public Customers, Firm Proprietary Traders, and Market Makers.
- **Option Metrics**: Daily implied volatilities from OptionMetrics Ivy DB.
- **Reference Volatility Benchmarks**: Filtered physical volatility from Bates (2005) jump-diffusion model for SPX; 5-year rolling GARCH(1,1) for individual equities.

### 3. Key Quantitative Results

#### End-User Demand Imbalances & Dealer Inventories (Table 1 & Figures 1–4)
- **SPX Index Options**: End users maintain a massive, persistent net long position averaging **$+103,254$ contracts/day** (public customers $+136,239$ contracts).
- **Concentration in OTM Puts**: Net demand is overwhelmingly concentrated in out-of-the-money puts: **$+124,345$ put contracts/day** vs. **$-21,091$ call contracts/day** (end users are net short index calls). 39% of net demand is concentrated in short tenors (<30 calendar days).
- **Dealers are Structurally Short Volatility**: Market makers are forced into aggregate short index option positions ($-103,254$ contracts/day).
- **Single-Stock Contrast**: In equity options, end users are **net sellers** ($-2,717$ contracts/day per stock), explaining why single-stock options are not systematically overpriced.

#### Excess Implied Volatility & Market Maker Profitability (Figures 1 & 5)
- **SPX Overpricing**: SPX options exhibit an average excess implied volatility of **$+8.7\%$** above Bates (2005) fundamental volatility.
- **Market Maker P&L**: Delta-hedged SPX market makers earned cumulative profits of **$\approx \$800\text{M}$** over 1996–2001 (Figure 5), translating to **$\approx \$1\text{M}$ per year per market maker** across ~100 CBOE market makers. Daily unhedgeable P&L swings fluctuated between $-\$100\text{M}$ and $+\$100\text{M}$, confirming large economic compensation for bearing unhedgeable inventory risk.

#### Econometric Demand Regressions (Tables 2–5)
- **Time-Series Expensiveness (Table 2)**: Regressing SPX excess implied volatility on jump-risk-weighted net demand yields $t\text{-stat} = 3.68, \text{Adj. } R^2 = 26\%$. A 1-standard-deviation increase in net demand elevates excess IV by $0.5$ standard deviations ($+5.6$ percentage points). Net demand directly explains $1.7\%$ out of the $4.9\%$ average excess IV level.
- **Dealer Capital Constraints**: Following 20-day market maker losses, price sensitivity $b$ doubles ($2.6 \times 10^{-5}, t = 3.7$) relative to profitable periods ($1.1 \times 10^{-5}, t = 6.1$), confirming that dealer balance-sheet stress magnifies option premiums.
- **Implied Volatility Smirk (Table 4)**: Net demand skew (OTM puts minus ATM) explains SPX smirk steepness with $t = 3.0\text{--}3.4, \text{Adj. } R^2 = 28\%$.
- **Single-Stock Cross Section (Table 3 & Fama-MacBeth)**: Net demand positively predicts single-stock option expensiveness with $t = 6.44$ ($p < 0.0001$).

### 4. Relevance to Option Research

Gârleanu, Pedersen, and Poteshman provides the foundational market microstructure rationale for systematic option selling in `sophie-option-research`:
1. **Microstructure Source of Option Alpha**: Confirms that the high returns of systematic short put strategies (`01_equity_curve.py`, `04_delta_selection.py`) originate from structural institutional buying pressure for OTM index put protection, which forces dealers to demand a large unhedgeable variance premium ($\approx \$1\text{M}$/dealer/yr).
2. **Index vs. Single-Stock Divergence**: Explains why selling SPX index options is structurally profitable (end users long $+103\text{k}$ contracts), whereas selling individual stock options lacks structural edge (end users net short $-2.7\text{k}$ contracts).
3. **Dealer Distress & Execution Modeling**: When market makers suffer losses, price impact doubles ($2.6 \times 10^{-5}$). In backtesting and execution pipelines (`lab/report.py`, `08_rolling.py`), slippage and spread models must account for widening bid-ask spreads and surging demand elasticity during market drawdowns.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational market microstructure theory explaining why option selling strategies earn structural excess returns: end-user net buying of OTM index puts for portfolio insurance forces market makers into unhedgeable short positions, bidding up implied volatility and steepening the smirk. Proves that option sellers are compensated in proportion to the unhedgeable variance of dealer inventories.

## Notable Citations to Follow Up

1. **Amin, Kaushik, Joshua D. Coval, and H. Nejat Seyhun (2004)** — *Index Option Prices and Stock Market Momentum* (Journal of Business, 77(4), 835-874).
   - Examines how market momentum interactively shifts customer option demand and the relative expensiveness of index options across strikes.
2. **Bates, David S. (2003)** — *Empirical Option Pricing: A Retrospection* (Journal of Econometrics, 116(1-2), 387-404).
   - Authoritative survey detailing the limits of affine representative-agent models and the necessity of modeling dealer financial intermediation constraints.
3. **Shleifer, Andrei, and Robert W. Vishny (1997)** — *The Limits of Arbitrage* (Journal of Finance, 52(1), 35-55).
   - Foundational behavioral finance framework explaining how specialized arbitrageur capital constraints allow persistent derivative premia to persist.
