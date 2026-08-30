---
title: "The Market for Crash Risk"
authors: "David S. Bates"
year: 2008
link: "https://www.nber.org/papers/w8557"
area: tail-risk
relevance: High
has_pdf: true
has_detailed_summary: true
citations_surfaced: 3
---

# The Market for Crash Risk

- **Authors:** David S. Bates
- **Year:** 2008 (Journal of Economic Dynamics and Control 32(7), 2291-2321; NBER Working Paper 8557, 2001)
- **Link:** [https://www.nber.org/papers/w8557](https://www.nber.org/papers/w8557)
- **PDF:** ates-2008-market-for-crash-risk.pdf (open-access copy, NBER Working Paper 8557)

## Testable Hypothesis

Heterogeneous crash aversion across market participants creates an equilibrium option market where less crash-averse investors sell out-of-the-money index put options to insure more crash-averse investors, systematically driving index option implied volatilities above objective jump probabilities and explaining the empirical pricing kernel puzzle.

## Summary

Models an economy where market participants have heterogeneous risk preferences regarding market crashes, and options markets dynamically complete the market. The less crash-averse investors sell out-of-the-money index put options, serving as insurers for highly crash-averse investors. In equilibrium, out-of-the-money put option prices substantially exceed the actuarial value of physical crash probabilities, generating persistent excess returns for systematic put writers while resolving several classic option pricing anomalies, including the overprediction of volatility and jump risk and the Jackwerth (2000) non-monotonic pricing kernel puzzle.

## Detailed Summary

### 1. Theoretical Framework & Heterogeneous Equilibrium

Bates develops a continuous-time general equilibrium endowment economy over $[0, T]$ that resolves why post-1987 stock index options persistently overpredict volatility and crash risk. 

News regarding terminal dividend fundamentals $D_T$ follows a Markov jump-diffusion:
$$d\ln D_t = \mu_d dt + \sigma_d dZ_t + \gamma_d dN_t$$
where $Z_t$ is a standard Wiener process, $N_t$ is a Poisson counter with constant intensity $\lambda$, and $\gamma_d < 0$ is a deterministic negative jump size.

Three non-redundant traded assets dynamically span the economy:
1. A riskless numeraire bond.
2. An equity claim paying terminal dividend $D_T$.
3. A jump insurance contract in zero net supply costing $\lambda_t^* dt$ instantaneously and paying 1 unit of consumption conditional on a jump (dynamically synthesized via exchange-traded options).

**Heterogeneous Crash-Averse Preferences:**
Investors possess state-dependent utility over terminal wealth $W_T$ and the cumulative number of realized jumps $N_T$:
$$U(W_T, N_T, t) = E_t \left[ e^{Y N_T} \frac{W_T^{1-R} - 1}{1-R} \right] \quad (R > 0)$$
where $R$ is constant relative risk aversion and $Y \ge 0$ captures idiosyncratic crash aversion. 
- **Crash-tolerant agents ($Y = 0$)**: Act as option market makers and natural option writers.
- **Crash-averse agents ($Y > 0$)**: Act as natural option buyers seeking downside portfolio insurance.

Solving the central planner Pareto problem with social weights $\omega_Y$ yields the state-dependent pricing kernel $\eta_t = D_t^{-R} e^{Y N_t} e^{\kappa_\eta(T-t)}$ and the risk-neutral jump intensity:
$$\lambda_t^*(N_t, t) = \lambda e^{-R \gamma_d} \frac{g(N_t + 1, t; \lambda e^{-R \gamma_d})}{g(N_t, t; \lambda e^{-R \gamma_d})}$$

### 2. Empirical Anomalies & Calibration Baseline

- **Sample Context**: 1988–1998 S&P 500 futures options (CBOE/CME).
- **Unconditional Volatility Puzzle**: 30-day at-the-money implied standard deviations (ISD) average **2% higher** than subsequent realized volatility ($1988\text{--}1998$), generating option-writing Sharpe ratios **2 to 6 times higher** than equity buy-and-hold (Fleming 1998; Jackwerth 2000).
- **Conditional Volatility Puzzle**: Regressing annualized realized volatility on 30-day ISD yields:
  $$\text{RV}_t = 0.0160 + 0.756 \cdot \text{ISD}_t \quad (R^2 = 0.45)$$
  $$\text{RV}_t^2 = 0.0027 + 0.681 \cdot \text{ISD}_t^2 \quad (R^2 = 0.33)$$
  Slopes significantly below 1.0 prove that ISDs are especially upward-biased during elevated volatility regimes.
- **Calibration Parameters**: Annual diffusive equity volatility $\sigma_d = 15\%$, jump size $\gamma_d = -10\%$, objective jump arrival rate $\lambda = 0.25$ (one crash per 4 years).

### 3. Key Quantitative Results

#### Equity and Crash Insurance Risk Premia (Section 2.2)
- **Jump Intensity Markup**:
  $$\ln(\lambda^* / \lambda) = -R \gamma_d + Y = 0.10 R + Y$$
  Equity risk premium: $\mu \approx 0.025 R + 0.025 Y$.
  For $R = 1$ and $Y = 1$, the equity premium is 5%/year, while the risk-neutral jump intensity $\lambda^*$ is **3.0 times the true physical jump intensity** ($\lambda^* / \lambda = e^{1.10} \approx 3.0$). Crash aversion $Y$ accounts for the massive wedge between implied and realized crash risk without requiring unpalatably high risk aversion $R$.
- **Sharpe Ratio of Writing Crash Insurance (Equation 21)**:
  $$\text{SR}_{\text{crash}} = \frac{(\lambda^* - \lambda)dt}{\sqrt{\text{Var}_t[1_{dN=1}]}} = \sqrt{\lambda}\left(\frac{\lambda^*}{\lambda} - 1\right)\sqrt{dt}$$
  Because $\lambda^* / \lambda \approx 3.0$, selling crash insurance generates an instantaneous Sharpe ratio substantially larger than holding equity ($\mu / \sqrt{\sigma^2 + \lambda k^2}$), matching the empirical profitability of short put strategies.

#### Crash Amplification under Heterogeneity (Table 2 & Figure 4)
- **Endogenous Feedback on Stock Prices**: When crash-tolerant ($Y = 0$) and crash-averse ($Y = 1$) agents interact, adverse news triggers severe portfolio reallocations.
- For a small **3% fundamental dividend shock** ($\gamma_d = -0.03$), the instantaneous stock price drop $\ln(1 + k_t)$ is magnified to **between $-3.0\%$ and $-18.9\%$**:
  - Balanced wealth ($w_1 = 0.3, R = 1$): price drop expands from $-3.0\%$ to **$-18.9\%$** (a 6.3x crash multiplier).
  - Risk aversion $R = 2, w_1 = 0.5$: price drop reaches **$-17.8\%$**.
- **Market Maker Capital Exposure (Table 3 & Figure 5)**:
  - When crash-averse investors hold most wealth ($w_1 \to 1.0$), crash-tolerant option writers sell massive insurance positions ($q_0^* = -0.382$ to $-0.839$), exposing **38% to 84% of their total net worth** to a single market crash in exchange for high premium capture.

#### Dynamic Volatility Cycles (Figure 7 & Figure 8)
- Following market crashes, wealth transfers from option sellers to option buyers, concentrating market wealth in crash-averse hands ($w_1 \uparrow$) and spiking implied volatility and $\lambda_t^*$ sharply.
- During prolonged bull markets (e.g., 1992–1996), steady insurance premium decay transfers wealth back to option sellers ($w_1 \downarrow$), driving implied crash risk down to fundamental levels.

### 4. Relevance to Option Research

Bates' equilibrium framework provides the foundational economic theory for option selling strategies evaluated in `sophie-option-research`:
1. **Source of Put-Writing Alpha**: The supernormal Sharpe ratios documented in short put backtests (`01_equity_curve.py`, `04_delta_selection.py`) are not market inefficiencies or statistical artifacts; they represent the structural equilibrium price of crash insurance ($(\lambda^* - \lambda) / \sqrt{\lambda}$) demanded by capital-constrained market makers.
2. **Crash Amplification & Tail Risk Clustering**: Explains why short option drawdowns are non-linearly amplified during crises (the 6.3x fundamental shock multiplier). In backtest risk engines (`lab/features.py`, `lab/report.py`), accounts for why fixed delta positions suffer sudden delta expansion and margin contraction as implied jump intensity $\lambda_t^*$ surges following market dips.

## Relevance to Personal Trading & Research

- **Rating:** High
- **Rationale:** Foundational theoretical and empirical justification for systematic put writing, proving that index put options are priced in equilibrium above actuarial crash probabilities because market makers demand large premia to absorb tail risk. Directly explains why short OTM put strategies generate persistent risk-adjusted excess return (Sharpe ratios 2–6x the underlying equity market).

## Notable Citations to Follow Up

1. **Jackwerth, Jens Carsten (2000)** — *Recovering Risk Aversion from Option Prices and Realized Returns* (Review of Financial Studies, 13, 433-451).
   - Empirically documents the pricing kernel anomaly and details the exceptional risk-adjusted profitability of systematic put- and straddle-writing strategies.
2. **Christensen, B. J., and N. R. Prabhala (1998)** — *The Relation Between Implied and Realized Volatility* (Journal of Financial Economics, 50, 125-150).
   - Investigates the econometric relationship between implied and realized volatility, establishing the persistence of the volatility risk premium in index options.
3. **Grossman, Sanford J., and Zhongquan Zhou (1996)** — *Equilibrium Analysis of Portfolio Insurance* (Journal of Finance, 51, 1379-1403).
   - Models the equilibrium market impact and volatility effects generated by institutional investors purchasing downside crash protection and portfolio insurance.
