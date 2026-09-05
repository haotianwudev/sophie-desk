---
title: "Recovering Risk Aversion from Option Prices and Realized Returns"
authors: "Jens Carsten Jackwerth"
year: 2000
link: "https://doi.org/10.1093/rfs/13.2.433"
area: option-returns-anomaly
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# Recovering Risk Aversion from Option Prices and Realized Returns

- **Authors:** Jens Carsten Jackwerth
- **Year:** 2000 (Review of Financial Studies 13(2), 433–451; working paper 1997)
- **Link:** [https://doi.org/10.1093/rfs/13.2.433](https://doi.org/10.1093/rfs/13.2.433)
- **PDF:** `jackwerth-2000-recovering-risk-aversion.pdf` (open-access copy, EconWPA / Munich RePEc)

## Testable Hypothesis

The pricing kernel and representative investor risk aversion recovered empirically by contrasting risk-neutral distributions (from S&P 500 option prices) against subjective realized return distributions undergo a structural breakdown post-1987, displaying negative and increasing risk aversion around the money that can be directly exploited via systematic put-selling strategies that dominate buy-and-hold equity even under stress-tested crash simulations.

## Summary

Establishes the seminal "Pricing Kernel Puzzle." In a complete market equilibrium, the ratio of the risk-neutral probability density to the subjective physical probability density defines the representative investor's marginal utility of wealth: $U'(W) \propto P(W) / Q(W)$. Using S&P 500 options data from 1984 through 1995, Jackwerth demonstrates a profound structural regime shift around the October 1987 market crash. Before October 1987, recovered risk aversion functions are uniformly positive and monotonically decreasing in wealth—fully compliant with standard economic theory (concave utility, risk aversion). Post-1987, the recovered risk aversion function becomes partially negative and increasing over the wealth interval $S_T/S_0 \in [0.95, 1.05]$, implying an impossible local risk-seeking representative agent. Jackwerth demonstrates that this anomaly stems from the post-crash structural overpricing of out-of-the-money index puts, and shows that systematic short put strategies yield massive risk-adjusted alphas that persist even after charging full bid-ask spreads, transaction costs, and synthetic 20% crash shocks occurring every 4 to 8 years.

## Detailed Summary

### 1. Theoretical Framework & Deriving Implied Risk Aversion

In a single-period complete market economy with an aggregate representative investor endowed with wealth $W_0 = 1$ and horizon $\tau$, the utility maximization problem is:
$$\max \int Q(W) U(W) dW \quad \text{subject to} \quad \int P(W) W dW = \frac{1}{r^\tau}$$
where $Q(W)$ is the subjective (physical) probability density across terminal wealth states $W$, $P(W)$ is the state-price density (risk-neutral probability density scaled by the risk-free discount factor $r^\tau$), and $U(W)$ is a state-independent Von Neumann-Morgenstern utility function.

Differentiating the Lagrangian with respect to wealth $W$ yields the first-order condition in equilibrium:
$$Q(W) U'(W) = \lambda P(W) r^\tau \implies U'(W) \propto \frac{P(W)}{Q(W)}$$
where $\lambda$ is the constant shadow price of the budget constraint.

The absolute risk aversion function $ARA(W)$ and relative risk aversion function $RRA(W)$ are obtained by logarithmic differentiation:
$$ARA(W) = -\frac{U''(W)}{U'(W)} = \frac{Q'(W)}{Q(W)} - \frac{P'(W)}{P(W)}$$
$$RRA(W) = -W \frac{U''(W)}{U'(W)} = W \cdot ARA(W)$$

Standard microeconomic theory requires:
1. **Positivity:** $U'(W) > 0$ and $ARA(W) > 0$ (investors prefer more wealth to less and are risk-averse).
2. **Monotonicity (Decreasing Absolute Risk Aversion, DARA):** $ARA'(W) \le 0$ (investors become less risk-averse as wealth grows).

### 2. Empirical Data & Probability Density Estimation

- **Data Source & Universe:**
  - CBOE S&P 500 index options (CBOE bid-ask midpoints and closing prices).
  - Pre-crash sample: Mid-1984 to mid-October 1987.
  - Post-crash sample: October 1988 to December 1995 (116 monthly expiration cycles with at least 4 liquid strikes spanning the moneyness range).
  - Subjective distribution $Q(W)$: Estimated using historical daily 4-year rolling return windows of the S&P 500 index, normalized to match the option horizon (31-day and 180-day horizons).
  - Risk-neutral distribution $P(W)$: Extracted from option price smiles using the Jackwerth & Rubinstein (1996) non-parametric implied tree optimization, minimizing the second derivative of implied volatility across strikes subject to fitting option bid-ask bounds.

### 3. Key Quantitative Results

#### The Structural Break: Pre-1987 vs. Post-1987
- **Pre-Crash Period (1984–1987):**
  - Implied risk aversion $RRA(W)$ is positive and smoothly downward-sloping across all wealth states ($RRA \approx 2\text{--}4$ near the money, declining to $\approx 1$ at elevated wealth).
  - Volatility smiles were virtually flat; Black-Scholes assumptions held reasonably well.
- **Post-Crash Period (1988–1995):**
  - Implied risk aversion breaks down completely: in the moneyness range $W/S_0 \in [0.97, 1.03]$, $RRA(W)$ plummets into **negative values** (reaching $-5$ to $-10$) and exhibits an **upward slope** ($\partial RRA / \partial W > 0$).
  - For deep out-of-the-money states ($W/S_0 < 0.92$), recovered risk aversion explodes to extreme values ($RRA > 10\text{--}20$).
  - This shape is robust to:
    1. Alternative bandwidths and smoothing parameters for $P(W)$.
    2. Extending the historical return window for $Q(W)$ up to 10 years.
    3. Allowing for non-lognormal physical return distributions (kernel estimation).

#### The Economic Resolution: OTM Put Overpricing
Jackwerth tests whether peso problems (investors pricing catastrophic disaster risk not realized in the 1988–1995 sample) can reconcile the puzzle. He shows that reconciling the post-crash kernel with positive, declining risk aversion requires investors to price an impending 20% crash with a subjective probability of once every 2 to 3 years—vastly higher than the historical 100-year frequency. The only plausible economic explanation is **the persistent structural overpricing of out-of-the-money put options** driven by institutional demand for downside portfolio protection after the 1987 crash.

#### Quantitative Put-Selling Trading Strategies (Figure 4 & Section III)
Jackwerth backtests systematic short put strategies across 116 one-month horizons (1988–1995):
- **Strategies Tested:** Selling margin-maximized S&P 500 puts with moneyness $K/S_0 = 0.90, 0.925, 0.95,$ and $0.975$.
- **Higher-Moment Risk Adjustments:** Uses Leland's (1996) modified beta and modified alpha to account for the heavy negative skewness and kurtosis of naked put writing:
  $$B = \frac{\text{Cov}(R, -R_m^{-b})}{\text{Cov}(R_m, -R_m^{-b})}$$
- **Simulated Catastrophic Crashes:** Injects artificial synthetic crashes of **$-20\%$ in a single month** occurring at frequencies of once every 4, 8, 16, and 32 years.
- **Results:**
  - Even with a **20% market crash occurring every 8 years**, all four put-writing strategies deliver positive risk-adjusted excess return (annualized Leland alphas of **+3% to +8%**).
  - For 0.975 delta puts and 180-day options, positive alphas persist even with a **20% crash every 4 years**.
  - **Transaction Costs:** Charging full bid prices on entry and a conservative 2% commission reduces annualized alpha by only 3%–4%, leaving substantial net risk-adjusted alpha intact.

### 4. Relevance to Option Research

Jackwerth (2000) provides the empirical cornerstone for option research in `sophie-option-research`:
1. **The Origin of the Put-Writing Edge:** Directly proves that the excess returns of short put strategies (modeled in `01_equity_curve.py`, `04_delta_selection.py`) originate from the post-1987 structural overpricing of downside tail insurance by institutional investors traumatized by Black Monday.
2. **Stress Testing Beyond Sample Data:** Validates the necessity of synthetic crash injection in backtest engines (`lab/report.py`). Because historical sample periods (e.g. 2012–2019) can be devoid of 20% crashes, Jackwerth's stress-testing methodology (evaluating alphas under synthetic 4-year and 8-year crash cycles) is essential for avoiding catastrophic tail-risk overconfidence.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational paper discovering the Pricing Kernel Puzzle and the empirical profitability of post-1987 short put strategies. Proves that selling out-of-the-money index puts mean-variance dominates equity buy-and-hold even under severe synthetic crash stress tests and full transaction costs.

## Notable Citations to Follow Up

1. **Aït-Sahalia, Yacine, and Andrew W. Lo (1998)** — *Nonparametric Estimation of State-Price Densities Implicit in Financial Asset Prices* (Journal of Finance, 53(2), 499–547).
   - Seminal paper using kernel regression to estimate risk-neutral state-price densities directly from option prices.
2. **Jackwerth, Jens Carsten, and Mark Rubinstein (1996)** — *Recovering Probability Distributions from Option Prices* (Journal of Finance, 51(5), 1611–1631).
   - Introduces the non-parametric optimization technique for deriving risk-neutral probability trees from option smiles.
3. **Leland, Hayne E. (1999)** — *Beyond Mean-Variance: Performance Measurement in a Nonsymmetrical World* (Financial Analysts Journal, 55(1), 27–36).
   - Introduces modified betas and alphas that correctly penalize non-normal return distributions and negative option skewness.
