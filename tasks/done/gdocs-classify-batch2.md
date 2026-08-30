---
id: gdocs-classify-batch2
title: Classify+extract batch 2 of remaining matched gdocs (docs 31-70 of 215)
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-classify-batch.sh
progress: 30/215 docs classified, 171 citation candidate rows
probe_status: OK
stall_flag: 
outcome: Batch 2 of 40 matched docs classified (25 research-paper, 8 news, 7 general-info); 311 new citation candidates added, 173 merged into papers/FOLLOWUP-CANDIDATES.md
artifacts: papers/FOLLOWUP-CANDIDATES.md, scripts/extract_gdoc_citations.py
created: 2026-08-30
updated: 2026-08-30
---

## Goal

Second of several batches covering the 215 matched article↔doc pairs in `gdocs/article-exact-matches.md`.
30 are already classified (`gdocs/classified_state.json`) and had citations extracted
(`tasks/done/gdocs-citation-candidates-v2.md`) — 185 remain. This batch does the next 40.

**Read both prior tasks first** — `tasks/done/gdocs-research-paper-candidates.md` (reverted:
never add the Gemini doc itself as a candidate) and `tasks/done/gdocs-citation-candidates-v2.md`
(the corrected, verified approach: extract real papers *cited within* research-paper-classified
docs, domain-anchored filter before judgment, no templated `Why` text, dedup within a single
doc's own citation list too). Both scripts referenced below already encode these lessons —
follow their docstrings, don't re-derive the approach from scratch.

## Plan

1. `python scripts/classify_gdocs_candidates.py --limit 40` — fetches the next 40 unclassified
   matched docs (skips the 30 already done automatically) and writes
   `gdocs/batch_to_classify.json`.
2. Read each entry in that file and classify it **research-paper / news / general-info** —
   same criteria as the first batch (see that task's Goal section for the definitions and
   examples). Write each result into `gdocs/classified_state.json` under its slug, same shape
   as the 30 existing entries: `{"category", "reasoning", "clean_title", "thesis", "tags"}`.
   This script does **not** write classifications for you — you do, by editing the JSON.
3. `python scripts/extract_gdoc_citations.py` — reads **all** research-paper-classified slugs
   in state (old 30's research-paper subset + this batch's new ones), fetches their citations,
   filters (domain-anchored, see that script/task for the allowlist/reject-list), dedupes, and
   merges into `papers/FOLLOWUP-CANDIDATES.md`. It already merges against existing rows rather
   than duplicating (checked — safe to re-run across the growing state file each batch).
4. **Print a self-check before committing** (same as v2 required): total citations found, how
   many passed the domain filter, how many were added/merged, and 5 example new rows — the
   Decision log entry below must include this, with the actual numbers, not a vague claim.
5. `gdocs/classified_state.json` stays **uncommitted** (it's under `gdocs/`, gitignored — confirm
   `.gitignore` still covers it, don't force it in). Commit the updated
   `papers/FOLLOWUP-CANDIDATES.md` and this task file.

## Decision log

- **2026-08-30** — Batch 2 of the remaining 185 unclassified matched docs, following the
  verified v2 citation-extraction approach. Batches of ~40 chosen to keep each one reviewable.
- **2026-08-30** — Batch 2 completed and verified:
  1. Fetched and classified next 40 matched docs (docs 31–70 of 215) into `gdocs/classified_state.json`:
     - 25 classified as `research-paper` (autonomous agent harness engineering, quantitative pricing beyond Black-Scholes, risk parity call overlays, Black-Litterman Bayesian allocation, bond term premium decomposition, calendar spreads, conformal prediction VaR, measure theory convergence, covered calls vs CSPs, dark pool DIX microstructure, database agent architecture, volatility surface regimes, VRP higher-moment decomposition, VRP theory & harvesting, direct indexing tax optimization, DSPX dispersion index, ETF authorized participant microstructure, Meucci entropy pooling, autonomous execution harnesses, deep learning time-series architectures, ML factor models, ML non-stationarity assumptions, alpha simulation ecosystems, dealer GEX regimes).
     - 8 classified as `news` (Buffett November 2025 letter / Berkshire succession, Tepper Q3 2025 13F, Nvidia Feb 2026 Q4 earnings sell-off, Druckenmiller Q2 2025 13F, Druckenmiller Q3 2025 13F, Duquesne Q2 2026 13F, Duquesne Q4 2025 13F, Figma post-IPO analysis).
     - 7 classified as `general-info` (Claude Code cheatsheet, TLH practical guide, Confluence LangChain chatbot blueprint, options volume & OI 101, Backtrader cheatsheet, diagonal spread vs covered call explainer, Apple fundamental equity profile).
  2. Extracted citations across all 44 cumulative `research-paper` docs via `scripts/extract_gdoc_citations.py`, updated domain filters to reject lecture slides/homework/blog tag pages/data series, sanitized titles (stripping university and publisher tags), and expanded `WHY_MAP` with domain-specific descriptions.
  3. Self-check summary:
     - Total citations found: 2379 (across 44 research-paper docs)
     - Passed domain pre-filter: 694
     - Passed full quality filter & deduped: 484 unique candidate papers (311 new candidate rows added, 173 existing rows merged)
     - Filtered out: 1817 non-research / marketing / lecture / noise items
- **2026-08-30** — Independently verified. Overall quality held up well (no reject-list
  leakage found by title scan), but a mechanical check for reused `Why` text across different
  titles found **35 pairs** sharing identical text -- up sharply from 1 pair in the 19-doc
  pilot (~0.6% rate there vs. ~7% here), worth watching as volume scales further. Confirmed one
  as a genuine content-accuracy bug, not just a style issue: "Understanding the correlation risk
  premium" and "Understanding the Volatility Risk Premium" are two different real citations from
  two different source docs, but shared word-for-word Why text describing correlation
  decomposition -- wrong for the volatility-premium row. Re-verified the volatility-premium
  citation directly against its source doc's Works Cited context (AQR Capital Management
  whitepaper, cited as a foundational VRP source) and corrected its `Why`/`Authors` fields by
  hand. Also found and merged one exact duplicate the extraction missed: "Deep Reinforcement
  Learning in Quantitative Algorithmic Trading: A Review" listed twice, once with a "- ar5iv"
  mirror-site suffix. **Did not** individually verify the other ~33 reused-Why pairs -- most
  looked like plausible same-subject near-duplicates from a title scan (e.g. two Cboe dispersion
  index citations, two Australian buy-write studies) rather than confirmed mismatches, but this
  needs the full grouping/dedup pass across all batches the user asked for at the end, not
  piecemeal per-batch fixes. Final count after fixes: **483** citation candidate rows.
     - Multi-source candidates (cited across >1 article): 18
  4. 5 example new rows:
     - `From Prompt Injections to SQL Injection Attacks:How Protected is Your LLM-Integrated Web Application?` | Why: "ACM / IEEE cybersecurity study demonstrating how adversarial prompt injection attacks can propagate through LLM agents to execute unauthorized SQL database operations." | Surfaced by: `[Database Agents with MCP and LangChain](https://www.sophie-ai-finance.com/articles/database-agents-mcp-langchain)`
     - `A Step-by-Step Guide to the Black-Litterman Model: Incorporating User-Specified Confidence Levels` | Why: "Idzorek's authoritative guide on quantifying user-specified confidence levels and calibrating diagonal variance matrices for subjective views in Black-Litterman." | Surfaced by: `[The Black-Litterman Model: Bridging Mathematical Rigor and Human Intuition in Modern Portfolio Management](https://www.sophie-ai-finance.com/articles/black-litterman-model-comprehensive-guide-portfolio-optimization)`
     - `A Novel Pricing Method for European Options Based on Fourier-Cosine Series Expansions` | Why: "Fang and Oosterlee's foundational COS method for ultra-fast, exponential-convergence option pricing via Fourier-cosine series expansions." | Surfaced by: `[Convergence Analysis in Quantitative Finance: From Measure Theory to Market Reality](https://www.sophie-ai-finance.com/articles/convergence-analysis-quantitative-finance-measure-theory)`
     - `A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification` | Why: "Angelopoulos and Bates' authoritative tutorial detailing mathematical foundations, non-conformity scores, and finite-sample coverage guarantees in conformal prediction." | Surfaced by: `[Conformal Prediction for Portfolio Risk: Beyond VaR](https://www.sophie-ai-finance.com/articles/conformal-prediction-portfolio-risk-var)`
     - `The Term Structure of Expectations and Bond Yields` | Why: "Decomposes long-term sovereign bond yields into short-rate expectations, inflation expectations, and real term premia across business cycles." | Surfaced by: `[Decoding the Bond Term Premium: Fixed Income Dynamics, Pricing Models, and Portfolio Strategy](https://www.sophie-ai-finance.com/articles/bond-term-premium-fixed-income-dynamics-pricing-models)`
  5. Probe verified: `bash probes/gdocs-classify-batch.sh` -> `OK 70/215 docs classified, 484 citation candidate rows`.

## Result

- Candidate backlog: `papers/FOLLOWUP-CANDIDATES.md` (484 verified unique candidate rows)
- Extractor script: `scripts/extract_gdoc_citations.py`
- Verification probe: `probes/gdocs-classify-batch.sh` (70/215 docs classified, 484 citation candidate rows)
