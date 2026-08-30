# Harvesting the Volatility Risk Premium: A Learning-to-Rank Approach

- **Authors:** Maciej Wysocki
- **Year:** 2026
- **Link:** [https://arxiv.org/abs/2608.24786](https://arxiv.org/abs/2608.24786)
- **PDF:** `wysocki-2026-harvesting-vrp-ltr.pdf` (open-access copy)

## Testable Hypothesis

A learning-to-rank machine learning framework with uncertainty-based abstention gates outperforms passive put-writing benchmarks by dynamically selecting optimal strike deltas and sitting out unfavorable volatility regimes in 0DTE SPXW options.

## Summary

Implements a LightGBM LambdaRank model on 1-minute intraday data to rank candidate short-put strikes (0.05 to 0.45 delta) against a cash 'SKIP' option for 0DTE SPXW trading. Demonstrates robust out-of-sample Sharpe ratios and sharp drawdown suppression compared to mechanical CBOE PUT index benchmarks.
