---
title: "Option Prices, Implied Price Processes, and Stochastic Volatility"
authors: "Mark Britten-Jones, Anthony Neuberger"
year: 2000
link: "https://doi.org/10.1111/0022-1082.00228"
area: vrp-measurement
relevance: High
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# Option Prices, Implied Price Processes, and Stochastic Volatility

**STATUS: PDF NOT DOWNLOADED — Journal of Finance paywall (Wiley)**

- **Authors:** Mark Britten-Jones, Anthony Neuberger
- **Year:** 2000 (Journal of Finance 55(2), 839–866)
- **Link:** [https://doi.org/10.1111/0022-1082.00228](https://doi.org/10.1111/0022-1082.00228)
- **PDF:** Not downloaded (publisher paywall)

## Testable Hypothesis

If the underlying asset price follows any continuous diffusion process, the risk-neutral expectation of integrated return variance over a future interval $[t, T]$ is completely and uniquely determined by the cross-section of European option prices maturing at $T$, without requiring parametric specification of the drift, volatility process, or investor preferences.

## Summary

Establishes the continuous-time mathematical foundation for "model-free implied volatility" (MFIV). Prior literature (Dupire 1994, Derman & Kani 1994) showed that European option prices uniquely determine a deterministic local volatility function $\sigma(S, t)$, but left open what option prices imply when volatility is stochastic. Britten-Jones and Neuberger resolve this by proving that while stochastic volatility dynamics cannot be fully disentangled without path-dependent or multi-maturity derivatives, the risk-neutral expectation of total integrated variance $\mathbb{E}_t^{\mathbb{Q}}[\int_t^T \sigma_s^2 ds]$ is model-free and strictly equal to a weighted integral of European call and put prices across all strikes from 0 to $\infty$, scaled inversely by the strike squared ($1/K^2$). This mathematical identity became the theoretical foundation for variance swaps and the CBOE VIX index methodology.

## Detailed Summary

### 1. Mathematical Derivation of Model-Free Implied Volatility

Consider an asset price $S_t$ following a continuous semi-martingale on a filtered probability space $(\Omega, \mathcal{F}, \{\mathcal{F}_t\}, \mathbb{P})$:
$$dS_t = \mu_t dt + \sigma_t dW_t$$
where $W_t$ is a standard Brownian motion under the risk-neutral measure $\mathbb{Q}$, and $\sigma_t$ is an arbitrary stochastic volatility process adapted to $\mathcal{F}_t$, with paths almost surely continuous. The risk-free interest rate $r$ and dividend yield $q$ are assumed constant for exposition.

Applying Itô's Lemma to the logarithmic price process $\ln S_T$:
$$d\ln S_t = \left( r - q - \frac{1}{2}\sigma_t^2 \right) dt + \sigma_t dW_t$$
Integrating from $t$ to $T$:
$$\ln S_T - \ln S_t = (r - q)(T - t) - \frac{1}{2} \int_t^T \sigma_s^2 ds + \int_t^T \sigma_s dW_s$$
Taking conditional risk-neutral expectations $\mathbb{E}_t^{\mathbb{Q}}[\cdot]$ (under which the Itô stochastic integral is a martingale with expectation zero):
$$\mathbb{E}_t^{\mathbb{Q}}\left[ \int_t^T \sigma_s^2 ds \right] = 2 \left( (r - q)(T - t) - \mathbb{E}_t^{\mathbb{Q}}\left[ \ln\left( \frac{S_T}{S_t} \right) \right] \right)$$

Britten-Jones and Neuberger exploit the fundamental static spanning identity (Carr & Madan 1998, 2001) that any smooth contract payoff $f(S_T)$ can be synthesized using a position in bonds, forward contracts, and a continuum of out-of-the-money European options:
$$f(S_T) = f(F_t) + f'(F_t)(S_T - F_t) + \int_0^{F_t} f''(K)(K - S_T)^+ dK + \int_{F_t}^\infty f''(K)(S_T - K)^+ dK$$
Setting $f(S_T) = -\ln(S_T / F_t)$, with $f'(K) = -1/K$ and $f''(K) = 1/K^2$:
$$-\ln\left(\frac{S_T}{F_t}\right) = -\frac{S_T - F_t}{F_t} + \int_0^{F_t} \frac{1}{K^2} (K - S_T)^+ dK + \int_{F_t}^\infty \frac{1}{K^2} (S_T - K)^+ dK$$
Taking expectations under $\mathbb{Q}$ and multiplying by 2 yields the celebrated **Britten-Jones & Neuberger Model-Free Variance Formula**:
$$\mathbb{E}_t^{\mathbb{Q}}\left[ \int_t^T \sigma_s^2 ds \right] = 2 e^{r(T-t)} \left[ \int_0^{F_t} \frac{P(T, K)}{K^2} dK + \int_{F_t}^\infty \frac{C(T, K)}{K^2} dK \right]$$
where $F_t = S_t e^{(r-q)(T-t)}$ is the forward price, $P(T, K)$ is the European put price with strike $K$ and expiration $T$, and $C(T, K)$ is the European call price.

### 2. Generalization vs. Local Volatility

- **Dupire (1994) vs. Britten-Jones & Neuberger (2000):**
  - Dupire proved that if volatility is a deterministic function $\sigma(S, t)$, the entire local volatility surface is uniquely recovered by differentiating option prices with respect to maturity $T$ and strike $K$: $\sigma_{\text{local}}^2(K, T) = \frac{2 \partial C / \partial T}{K^2 \partial^2 C / \partial K^2}$.
  - Britten-Jones & Neuberger demonstrate that if volatility is stochastic, the local volatility surface $\sigma_{\text{local}}(K, T)$ merely reflects the expected instantaneous variance conditional on $S_T = K$, but cannot identify the volatility-of-volatility or correlation parameters.
  - However, the integrated return variance $\int_t^T \sigma_s^2 ds$ is invariant to the degree of stochasticity in $\sigma_s$, as long as the asset price process does not exhibit discontinuous jumps.

### 3. Key Quantitative & Implementation Insights

#### Discrete Strike Discretization & Truncation Errors
In practice, market options trade on a discrete strike grid $\{K_1, K_2, \dots, K_N\}$ rather than a continuum:
- Numerical approximation requires numerical integration (trapezoidal rule or Simpson's rule):
  $$\Delta K_i = \frac{K_{i+1} - K_{i-1}}{2}, \quad \int \frac{Q(K)}{K^2} dK \approx \sum_{i=1}^N \frac{\Delta K_i}{K_i^2} Q(K_i)$$
- **Strike Truncation Error:** The theoretical integral spans $K \in (0, \infty)$, whereas available market strikes are truncated at $K_1 > 0$ and $K_N < \infty$.
  - Truncation of deep OTM puts ($K < K_1$) causes underestimation of implied variance, especially in volatile regimes where downside crash risk is priced.
  - Truncation of deep OTM calls ($K > K_N$) has negligible impact due to the $1/K^2$ weighting rapidly diminishing call premium contributions.
- **Interpolation Schemes:** Testing cubic spline smoothing across implied volatilities versus direct price interpolation demonstrates that interpolating implied volatilities and converting back to Black-Scholes prices ensures no-arbitrage conditions (monotonic call prices, convex implied distributions).

#### Foundation for CBOE VIX (2003 Revision)
- The original VIX index (created by Whaley in 1993, now $VXO$) used Black-Scholes inversion of 8 at-the-money S&P 100 ($OEX$) options.
- In September 2003, CBOE redesigned VIX to implement the Britten-Jones & Neuberger formula on S&P 500 ($SPX$) options, defining:
  $$\text{VIX}^2 = \frac{2 e^{rT}}{T} \sum_{i} \frac{\Delta K_i}{K_i^2} Q(K_i) - \frac{1}{T}\left( \frac{F_t}{K_0} - 1 \right)^2$$
  directly operationalizing the Britten-Jones & Neuberger continuous-strike integral.

### 4. Relevance to Option Research

In `sophie-option-research`:
1. **Model-Free Implied Variance Benchmark:** The Britten-Jones & Neuberger integration formula provides the exact mathematical benchmark for computing model-free implied variance ($MFIV$) from raw SPX option chains in `lab/data.py` and comparing it against Black-Scholes at-the-money IV.
2. **Variance Swap Pricing & Replicating Portfolios:** The $1/K^2$ weighting profile defines the exact static option portfolio needed to hedge the quadratic variation of equity index returns. Understanding this weighting explains why deep OTM puts (which receive large $1/K^2$ weights) dominate the level and dynamics of the VIX, and why option sellers capture substantial edge from short OTM put premium.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational mathematical proof enabling model-free implied volatility calculation and variance swap replication. Establishes the exact continuous-strike integration framework used to define the VIX and extract the market's risk-neutral expected variance without model bias.

## Notable Citations to Follow Up

1. **Dupire, Bruno (1994)** — *Pricing with a Smile* (Risk, 7(1), 18–20).
   - The pioneering paper on local volatility, deriving how option price surfaces uniquely determine deterministic volatility functions.
2. **Carr, Peter, and Dilip Madan (2001)** — *Towards a Theory of Volatility Trading* (Option Pricing, Interest Rates and Risk Management, Cambridge University Press, 417–432).
   - Formalizes the static spanning identity of contingent claims with European options and log-contract synthesis.
3. **Demeterfi, Kresimir, Emanuel Derman, Michael Kamal, and Joseph Zou (1999)** — *A Guide to Variance Swaps* (Goldman Sachs Quantitative Strategies Research Notes).
   - Bridges the Britten-Jones & Neuberger theoretical integration into practical institutional variance swap pricing and replication.
