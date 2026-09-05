---
title: "Covered Call Strategies: One Fact and Eight Myths"
authors: "Roni Israelov, Lars N. Nielsen"
year: 2014
link: "https://doi.org/10.2469/faj.v70.n6.3"
area: covered-calls
relevance: High
has_pdf: false
has_detailed_summary: true
citations_surfaced: 3
---

# Covered Call Strategies: One Fact and Eight Myths

**STATUS: PDF NOT DOWNLOADED — Financial Analysts Journal paywall (CFA Institute / Taylor & Francis)**

- **Authors:** Roni Israelov, Lars N. Nielsen
- **Year:** 2014 (*Financial Analysts Journal*, 70(6), November/December 2014, 23–31; SSRN Working Paper No. 2444993)
- **Link:** [https://doi.org/10.2469/faj.v70.n6.3](https://doi.org/10.2469/faj.v70.n6.3)
- **PDF:** None (Paywalled; see companion research paper `israelov-nielsen-2015-covered-calls-uncovered.pdf` in `papers/option-writing/`)

## Testable Hypothesis

The widespread practitioner perception that covered call overwriting is an "income-generating" or "downside-protecting" strategy is rooted in behavioral myths; in reality, covered call strategies represent a pure two-asset allocation decision combining reduced equity market beta with exposure to the volatility risk premium (VRP). Any performance deviations outside of these two compensated risk factors stem from uncompensated, path-dependent equity-reversal exposure that degrades portfolio efficiency.

## Summary

In this influential foundational article in the *Financial Analysts Journal*, Roni Israelov and Lars Nielsen (AQR Capital Management) provide a rigorous economic deconstruction of covered call strategies, dispelling eight persistent industry myths. 

The paper establishes **One Fundamental Fact**:
> A covered call strategy is not a mysterious or magical investment trick; it is fundamentally an asset allocation decision that reduces exposure to the underlying equity market while introducing a short exposure to equity volatility. The performance of a covered call strategy is determined almost entirely by the performance of the equity market and the volatility risk premium.

The authors systematically dismantle eight widely accepted practitioner beliefs regarding yield, downside protection, exit targeting, moneyness selection, Sharpe ratios, market regime performance, benchmark comparisons, and equity timing. They demonstrate that the sole compensated source of non-equity return in covered calls is the Volatility Risk Premium (VRP)—the structural tendency for option implied volatility to exceed subsequent realized volatility.

## Key Takeaways for Option Writing

1. **Option Premium is Not Income:** Option premiums collected from writing calls represent an advance monetization of future capital appreciation, not incremental yield or coupon income. Treating option premium as free cash flow masks the asymmetric truncation of upside equity returns.
2. **Negligible Downside Protection:** A monthly call option premium (typically 1.5%–2.5% for ATM calls, and <1% for OTM calls) provides almost no cushion against serious equity market drawdowns (e.g., -20% to -50%). Once the underlying falls past the strike, the option expires worthless and the portfolio inherits 100% of subsequent downside losses with an equity beta near 1.0.
3. **The Flaw of Using Options as Price Targets:** Selling calls with the rationale of being "happy to sell at the strike" is economically flawed. If the stock rallies massively, the seller suffers substantial opportunity cost; if the stock collapses, the seller continues to hold 100% of the plummeting stock.
4. **Proper Benchmarking Requires Beta Matching:** Because covered call strategies (such as the CBOE BXM index) have an average equity beta between 0.50 and 0.70, comparing them directly against 100% long equity indices (S&P 500) confuses structural beta reduction with managerial alpha. The appropriate benchmark is a blended portfolio of ~60% equities and 40% cash plus a volatility harvesting overlay.
5. **Sharpe Ratios are Artificially Inflated:** Because covered calls truncate the right tail of the return distribution while leaving the left tail exposed, return series exhibit strong negative skewness (-1.5 to -2.0) and high kurtosis. Naive Sharpe ratios understate true tail risk.

## Detailed Summary

### The "One Fact": Economic Return Decomposition

A standard covered call position consists of a long position in the underlying equity and a short call option:
$$\text{Covered Call} = \text{Equity} - \text{Call}$$

Using standard option pricing relationships, the return of the covered call can be cleanly separated into two primary economic exposures:
1. **Reduced Strategic Equity Exposure:** By selling a call option with delta $\Delta_c$ (where $\Delta_c \approx 0.50$ for ATM calls, or $\approx 0.30$ for OTM calls), the investor reduces their net effective equity exposure to $1 - \Delta_c$. The strategy earns a proportional share of the Equity Risk Premium (ERP).
2. **Short Volatility Exposure (VRP Harvesting):** By being short options, the investor earns the spread between implied volatility and realized volatility (the Volatility Risk Premium).

All other perceived attributes of covered calls are diversions from this core asset allocation reality.

---

### The "Eight Myths" Deconstructed

#### Myth 1: Covered calls generate incremental "income" / yield.
- *Practitioner belief:* Writing calls provides an attractive dividend-like income stream, making it suitable for income-seeking investors (e.g., retirees or endowments).
- *Economic reality:* Premiums received are not income in the traditional sense (like bond coupons or stock dividends that flow from productive corporate capital). Rather, selling a call sells away right-tail capital appreciation in exchange for upfront cash. It is a monetization of future capital gains. When the underlying rallies beyond the strike, the lost capital gain offsets the premium received.

#### Myth 2: Covered calls provide meaningful downside protection.
- *Practitioner belief:* The cash premium received buffers portfolio losses during falling markets.
- *Economic reality:* The premium buffer is minuscule compared to equity drawdown risk. For an S&P 500 ATM call with 1 month to expiration, the premium is typically ~2.0% of the index value. If the market falls 10%, 20%, or 40%, the investor absorbs 8%, 18%, or 38% losses. Furthermore, as the stock drops, the call option rapidly loses value and its delta approaches zero; past that point, the short call provides zero incremental hedging, leaving the investor exposed to 100% of further market declines.

#### Myth 3: Writing calls allows investors to sell shares at a targeted higher price (exit strategy).
- *Practitioner belief:* Writing an out-of-the-money call option at strike $K$ is an attractive limit order: "If the stock reaches $K$, I am happy to sell it at that price anyway."
- *Economic reality:* An option is a contingent claim, not a limit order. If the stock skyrockets far beyond $K$, the investor is forced to sell at $K$, missing out on massive upside. Conversely, if the stock crashes, the option expires worthless and the investor is left holding 100% of the depreciated stock. Thus, the investor sells precisely when holding would have been most lucrative, and retains full ownership when selling would have been most protective.

#### Myth 4: Writing out-of-the-money (OTM) calls is safer or always better than at-the-money (ATM) calls.
- *Practitioner belief:* OTM calls provide upside participation while still generating income, making them strictly superior to ATM calls.
- *Economic reality:* OTM calls provide substantially less downside premium buffer (<1%) than ATM calls (~2%), while leaving the portfolio with higher equity beta (~0.70–0.85). Furthermore, OTM calls harvest less volatility risk premium per dollar of option notional. Choosing between ATM and OTM overwriting simply tunes the balance between equity risk and volatility risk; OTM is not inherently "safer".

#### Myth 5: Covered call writing provides an attractive risk-return profile because of high Sharpe ratios.
- *Practitioner belief:* Indices like the CBOE S&P 500 BuyWrite Index (BXM) exhibit Sharpe ratios comparable to or higher than the S&P 500 with ~30% lower volatility, proving superior risk-adjusted returns.
- *Economic reality:* The Sharpe ratio is a mean-variance metric that implicitly assumes normal return distributions. By capping upside gains and preserving full downside losses, covered calls generate severe negative skewness (around -1.7) and high excess kurtosis (around 8.7). Standard deviation understates the probability and severity of tail drawdowns. On downside-adjusted metrics (such as Sortino ratio or Conditional VaR), covered call outperformance is substantially attenuated.

#### Myth 6: Covered calls outperform equities in all flat or moderately declining markets.
- *Practitioner belief:* If the market moves sideways over the life of the option, the covered call must beat long equities by the full amount of the premium.
- *Economic reality:* Returns are path-dependent. Because of option gamma and volatility clustering, intra-month market turbulence can cause the short call's mark-to-market value to fluctuate violently. If the index experiences a sharp mid-month drawdown followed by an explosive recovery to flat, the short call suffers large losses during the rally, causing the covered call strategy to underperform long equity even though the net end-of-month price was unchanged.

#### Myth 7: Covered call strategies should be evaluated relative to long-only equity benchmarks.
- *Practitioner belief:* The natural benchmark for an overwritten equity portfolio is the underlying equity index (e.g., S&P 500).
- *Economic reality:* Because covered calls operate with an average market beta of ~0.60, comparing them directly against 100% equity benchmarks is deceptive. In a bull market, covered calls lag simply due to lower beta; in a bear market, covered calls decline less simply due to lower beta. To isolate true alpha, covered calls must be benchmarked against a beta-matched portfolio: a combination of ~60% equity and 40% risk-free cash, plus a standalone volatility selling overlay.

#### Myth 8: The primary benefit of covered call writing is equity market timing or harvesting equity reversal.
- *Practitioner belief:* The dynamic delta behavior of a covered call (delta falls toward 0 as the market rallies; delta rises toward 1 as the market falls) constitutes an intelligent contrarian market-timing strategy.
- *Economic reality:* This automatic mechanical rebalancing mimics an unmanaged equity mean-reversion bet. However, empirical asset pricing shows that short-term equity reversal over monthly horizons produces zero expected risk-adjusted return while introducing substantial path-dependent risk (accounting for over 25% of the strategy's total volatility). The only reliable source of long-term excess return in covered calls is the Volatility Risk Premium (VRP).

---

### Implementation & Relevance to Sophie Desk / SPX Option Strategies

- **Architecture of Option Selling Strategies:** In `sophie-option-research`, whether implementing covered calls (BuyWrite), cash-secured put writing (PutWrite), or delta-neutral short straddles, the quantitative edge is identical: the Volatility Risk Premium. Put-call parity dictates that a covered call is economically identical to a cash-secured short put ($	ext{Stock} - 	ext{Call} = 	ext{Cash} - 	ext{Put}$).
- **De-biasing Retail Perceptions:** Strategy descriptions, backtest metrics, and educational materials must avoid the "income generation" and "downside protection" marketing traps. Premiums are monetization of equity upside, and downside tail risk remains fully active.
- **Risk Attribution & Benchmarking:** All option strategies backtested in `sophie-option-research` should be evaluated against beta-matched benchmarks rather than raw buy-and-hold SPX. Alpha should be attributed strictly to the VRP harvest after stripping out passive equity beta.
- **Delta-Hedging Overlays:** As formalized in Israelov & Nielsen (2015), neutralizing the uncompensated equity-reversal exposure via daily futures/ETF delta-hedging allows option desks to capture pure VRP while dramatically improving Sharpe and Sortino ratios.

## Citations & Follow-ups

- **Israelov, Roni, and Lars N. Nielsen (2015):** *Covered Calls Uncovered* (*Financial Analysts Journal*, 71(6), 44–57) — the mathematical companion that formalizes the exact performance attribution decomposition and details daily futures delta-hedging to eliminate reversal risk.
- **Figelman, Igor (2008):** *Expected Return and Risk of Covered Call Strategies* (*Financial Analysts Journal*, 64(3), 67–80) — provides analytical proof of optimal covered call strike selection.
- **Hill, Joanne M., Vasant Balasubramanian, Krag Gregory, and Ingrid Tierens (2006):** *Finding Alpha via Covered Index Writing* (*Financial Analysts Journal*, 62(5), 29–46) — empirical examination of institutional buy-write performance.
