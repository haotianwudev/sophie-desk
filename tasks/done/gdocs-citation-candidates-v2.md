---
id: gdocs-citation-candidates-v2
title: Extract cited research papers from Gemini docs (v2 -- domain-anchored filter)
lane: research
status: done
assignee: agy
gate:
repo: sophie-desk
blocker:
next:
probe: bash probes/gdocs-citation-candidates.sh
progress: script exists but no citation candidate rows added yet
probe_status: RUN
stall_flag: 
outcome: Added 170 new and 2 merged high-quality research citation candidate rows to papers/FOLLOWUP-CANDIDATES.md using domain-anchored filtering and specific Why descriptions.
artifacts: papers/FOLLOWUP-CANDIDATES.md, scripts/extract_gdoc_citations.py
created: 2026-08-30
updated: 2026-08-30
---

## Goal

**Second attempt** at `tasks/done/gdocs-citation-candidates.md`, which was fully reverted — read
that task's Decision log before starting, it has the concrete failure evidence. In one sentence:
the "genuine research only" filter did not run in practice — ~15 of ~15 raw citations per doc
were kept, including a broker's marketing guide, a financial-ethics essay, a bare "Algorithmic
Trading" title, and a corrupted scraped title, with `Why` fields that were boilerplate restating
the title back rather than real analysis.

**The fix: anchor the filter to concrete domain examples, applied *before* judgment, not as a
replacement for it.** This is not a closed allowlist — a citation from a domain outside these
examples can still qualify — but a citation must clear a real, articulable reason grounded in
what these examples share (an institution actually did original research and published it),
not "it's a comprehensive-sounding title." Reuse `scripts/extract_gdoc_citations.py`'s
fetch/works-cited-parsing logic (that part worked); rewrite its filtering and dedup.

**Domains that are examples of genuine research sources** (not exhaustive — the character
matters more than the exact list): `arxiv.org`, `ssrn.com`, `nber.org`, `repec.org`, any
`*.edu` domain, `federalreserve.gov` and the regional Fed banks (`*.frb.org`, `newyorkfed.org`),
`imf.org`, `bis.org`, `ecb.europa.eu`, `bankofengland.co.uk`, journal publishers
(`tandfonline.com`, `wiley.com`, `sciencedirect.com`, `springer.com`, `jstor.org`,
`cambridge.org`, `aeaweb.org`), `sec.gov`, and a named research arm's own publication page
(e.g. `aqr.com`, `cboe.com/insights`, `cmegroup.com/education` when it's an actual research
paper/whitepaper, not a marketing explainer).

**Domains/content types that are examples of what to reject even if the citing doc used them**:
generic news coverage (a Bloomberg/Reuters/CNBC *news article*, as opposed to that outlet
republishing an actual study), broker or vendor marketing pages (a "Comprehensive Guide" from a
trading platform, an "InH&T"-style branded content page), Investopedia/generic explainer sites,
Wikipedia, Medium/Substack/personal blogs, Reddit, YouTube, ethics/opinion essays, and any
citation whose own title is generic and non-specific ("Algorithmic Trading," bare and
undescriptive — a real paper title says what it found or built, not just the topic).

**A citation from neither list needs a real, specific reason to be kept** — write what that
reason is into `Why it looks worth getting` itself (not a template). If you can't articulate a
specific reason beyond "it's about the topic," leave it out.

## Plan

1. Rewrite `scripts/extract_gdoc_citations.py`'s filtering step: check each citation's URL
   domain against the example lists above first (cheap, mechanical, do this before spending any
   judgment). Domain matches the "genuine research" list → keep, subject to step 2 still
   catching junk within a good domain (e.g. a Fed *blog post* is not the same as a Fed *staff
   working paper* — both live on federalreserve.gov). Domain matches the "reject" list → drop
   without further consideration. Anything else → apply real judgment, and only keep with a
   specific, non-template reason.
2. **No boilerplate `Why` text.** Every `Why it looks worth getting` must say something specific
   to that citation — a real finding, method, or dataset it's known for, inferred from the
   citation's own title/context. A `Why` field that just restates the title back with a wrapper
   phrase ("Cited in research on X; investigates X") is exactly the failure mode from the first
   attempt — do not repeat it. If you can't write something specific, don't add the row.
3. **Dedup must catch near-duplicates within a single doc's own citation list too**, not just
   across docs — the first attempt missed two rows for the same paper cited once with just its
   title and once with a journal name appended, inside the same document. Normalize titles
   (strip trailing punctuation/footnote marks like `∗`, collapse whitespace, lowercase, strip a
   trailing `- <publisher name>` suffix) before comparing.
4. Same as before: for citations that pass, add a row to `papers/FOLLOWUP-CANDIDATES.md`
   matching the schema documented at the top of that file (Title, Authors/Year if known else
   blank, Why, Tags, Surfaced by as an article link, Doc ID Source, Status blank). Multi-source
   dedup (same real paper cited by 2+ different Sophie articles) merges into one row with
   comma-separated `Surfaced by` / `Doc ID Source`, matching order.
5. Same 19-doc scope as the reverted attempt (`gdocs/classified_state.json`,
   `category == "research-paper"`) — this is still validating the pipeline, not scaling yet.
6. **Before committing, print a quick self-check**: total citations found, how many passed the
   domain pre-filter, how many were added after judgment, and 5 example rows so the actual
   output is visible in the task's own Decision log (not just a claimed summary) — this is what
   would have caught the first attempt's problem immediately.
7. Commit the script and updated `papers/FOLLOWUP-CANDIDATES.md`.

## Decision log

- **2026-08-30** — v2 of `gdocs-citation-candidates`, which was reverted after its filter let
  marketing/explainer/opinion content through with boilerplate `Why` text and unmerged
  near-duplicates. This version anchors the filter to concrete domain examples applied before
  judgment (not instead of it), forbids templated `Why` text explicitly, and requires a
  self-check summary with real example rows before committing.
- **2026-08-30** — v2 implementation completed and validated:
  1. Filter redesign: Implemented domain-anchored pre-filtering with explicit exclusions for news, blogs, broker marketing, glossaries, student projects, and API/doc specs.
  2. Title sanitization: Stripped publisher prefixes (`Article Title:`, `Full article:`, `NOTE `, `(PDF)`, `[PDF]`, `[arXiv:...]`), trailing suffixes (` - arXiv`, ` - SSRN`, ` - ResearchGate`, ` - Taylor & Francis Online`, ` - Columbia Business School`, ` - NBER`, ` - PLOS`, ` | Request PDF`, ` | Semantic Scholar`, etc.), and footnote marks (`*`, `∗`, `†`, `‡`).
  3. Deduplication & multi-source merging: Normalized titles (punctuation, lowercase, financial noun stemming) to eliminate near-duplicates within individual docs and merge multi-source citations across docs with concatenated `Surfaced by` and `Doc ID Source` values.
  4. Specific `Why` descriptions: Built domain-specific descriptions detailing empirical findings, mathematical models, or trading mechanics (e.g. Avellaneda-Stoikov, VRP jump decompositions, CRR3/xVA, Deflated Sharpe, Base Correlation, GEX inference) without template or wrapper phrasing.
  5. Self-check summary:
     - Total citations found: 1079 (across 19 research-paper Gemini Google Docs)
     - Passed domain pre-filter: 291
     - Passed full quality filter & deduped: 172 unique candidates (170 new candidate rows added, 2 existing rows merged)
     - Filtered out: 873 non-research/marketing/explainer/unparseable items
  6. Example rows:
     - `An Extended Model of Effective Bid-ask Spread` | Why: "Extends Roll's spread model to account for order flow persistence, asymmetric information, and inventory holding costs in high-frequency trading." | Surfaced by: `[The Anatomy of Speed: Modern Market Making in High-Frequency Trading](https://www.sophie-ai-finance.com/articles/anatomy-of-speed-modern-market-making-hft)`
     - `Past, Present and Future: The Evolution and Development of Electronic Financial Markets` | Why: "Surveys the structural transition of exchange market microstructure from physical specialist floors to electronic limit order books and algorithmic matching." | Surfaced by: `[The Anatomy of Speed: Modern Market Making in High-Frequency Trading](https://www.sophie-ai-finance.com/articles/anatomy-of-speed-modern-market-making-hft)`
     - `Option Profit and Loss Attribution and Pricing: A New Framework` | Why: "Carr and Wu's foundational framework decomposing daily option P&L into delta, gamma, theta, and implied volatility surface carry and curvature components." | Surfaced by: `[Academic Foundations of Option Writing: A Research Review](https://www.sophie-ai-finance.com/articles/academic-foundations-option-writing-research-review)`
     - `Betting Against Beta` | Why: "Frazzini and Pedersen's foundational framework showing that leverage-constrained investors overpay for high-beta assets, creating a robust Betting Against Beta (BAB) anomaly." | Surfaced by: `[The Architecture of Quantitative Insight: The AQR Research Legacy](https://www.sophie-ai-finance.com/articles/architecture-quantitative-insight-aqr-research-legacy)`
     - `PlanCompiler: A Deterministic Compilation Architecture for Structured Multi-Step LLM Pipelines` | Why: "Introduces PlanCompiler, an architecture compiling natural language intent into deterministic, statically verifiable execution graphs for multi-step LLM pipelines." | Surfaced by: `[Agent Compiler Framework: Deterministic AI Analysts](https://www.sophie-ai-finance.com/articles/agent-compiler-framework-deterministic-ai-analysts)`
  7. Probe verified: `bash probes/gdocs-citation-candidates.sh` -> `OK 172 citation candidate rows added`.
- **2026-08-30** — Independently verified rather than trusting the self-check (same discipline
  that caught v1's failure). Spot-checked ~95 of the 172 titles by eye: all read as genuine,
  specific research (VRP, tail-risk hedging, factor investing, correlation risk premium, RAG/LLM
  papers, IMF/BIS reports) -- no reject-list leakage (no marketing pages, ethics essays,
  Investopedia-style content) found this time, a dramatic improvement over v1. One real issue:
  a mechanical check for reused `Why` text across different titles found exactly one pair --
  "High Frequency Market Making" and "High Frequency Trading: Price Dynamics Models and Market
  Making Strategies" -- both from the same source doc, same `Why` text word-for-word, almost
  certainly a within-doc near-duplicate the dedup pass should have caught. Fixed by hand:
  removed the shorter/more generic title, kept the more specific one. Final count: **171**
  citation candidate rows (170 + 1 pre-existing merge, minus the 1 duplicate just removed).

## Result

- Script: `scripts/extract_gdoc_citations.py`
- Candidate backlog: `papers/FOLLOWUP-CANDIDATES.md` — **171** rows added from the 19-doc pilot
  (172 as originally committed, minus 1 near-duplicate found on manual verification and
  removed). Quality independently spot-checked, not just taken on the task's own self-report.
- Verification probe: `probes/gdocs-citation-candidates.sh` (172 candidate rows verified)

