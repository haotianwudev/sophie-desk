---
title: "Non-Spanning Identification of Scheduled Event Risk in Option Pricing"
authors: "Tenghan Zhong"
year: 2026
link: "https://arxiv.org/abs/2606.12872"
area: event-risk
relevance: Medium
has_pdf: true
has_detailed_summary: false
citations_surfaced: 3
---

# Non-Spanning Identification of Scheduled Event Risk in Option Pricing

- **Authors:** Tenghan Zhong
- **Year:** 2026 (arXiv:2606.12872, June 2026)
- **Link:** [https://arxiv.org/abs/2606.12872](https://arxiv.org/abs/2606.12872)
- **PDF:** zhong-2026-non-spanning-identification-scheduled-event-risk.pdf (open-access copy, arXiv)

## Testable Hypothesis

Separating the continuous no-event implied volatility surface from scheduled event jumps via a non-spanning expiry identification protocol isolates macroeconomic announcement variance markups (FOMC, CPI, NFP) in short-dated SPX options and improves out-of-sample pricing of event-volatility option combinations.

## Summary

Examines short-dated S&P 500 index options (SPXW) from May 2022 to August 2025 around major scheduled macroeconomic announcements (FOMC, CPI, Non-Farm Payrolls). Formulates a non-spanning identification protocol where non-spanning expiries identify the baseline continuous volatility surface while event-spanning quotes calibrate the scheduled deterministic event jump. Demonstrates that explicit scheduled event-jump specifications consistently improve held-out event-spanning option pricing and event-volatility straddle/strangle pricing over standard surface smoothing, preventing continuous volatility models from misattributing event markups to baseline diffusion variance.

## Relevance to Personal Trading & Research

- **Rating:** Medium
- **Rationale:** Econometric identification framework that isolates scheduled macroeconomic event risk (FOMC, CPI, NFP) from continuous baseline diffusion variance. Demonstrates that CPI and FOMC carry substantial priced event jump variance concentrated in direction-agnostic volatility combinations (straddles/strangles) rather than directional skew, directly supporting macro calendar event-gating in `sophie-option-research`.

## Notable Citations to Follow Up

1. **Londono, Juan M., and Mehrdad Samadi (2023)** — *The Price of Macroeconomic Uncertainty: Evidence from Daily Options* (Federal Reserve Board IFDP 1376).
   - Uses same-day and 1-day SPX expirations to estimate release-specific volatility premia across major macroeconomic announcements.
2. **Wright, Jonathan H. (2020)** — *Event-Day Options* (NBER Working Paper 28306).
   - Formulates option-implied variance risk premium dynamics and jump risk compensation specifically spanning FOMC and employment report release days.
3. **Alexiou, Lykourgos, Amit Goyal, Alexandros Kostakis, and Leonidas Rompolis (2025)** — *Pricing Event Risk: Evidence from Concave Implied Volatility Curves* (Review of Finance, 29(4), 963-1007).
   - Demonstrates that scheduled event announcements induce distinct concavity, bimodality, and elevated crash premia in short-term risk-neutral state-price densities.
