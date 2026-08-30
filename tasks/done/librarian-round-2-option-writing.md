---
id: librarian-round-2-option-writing
title: Find NEW option-writing papers without duplicating round 1
lane: research
status: done
assignee: claude
gate:
repo: sophie-option-research
blocker:
next: Claim, check existing papers first, then search for genuinely new ones.
probe: bash probes/librarian-round-2-option-writing.sh
progress:
probe_status:
outcome: 4 new papers filed
artifacts: papers/option-writing/carr-wu-2009-variance-risk-premia.md, papers/option-writing/cheng-2019-vix-premium.md, papers/option-writing/augustin-cheng-vandenbergen-2021-volmageddon.md, papers/option-writing/della-corte-ramadorai-sarno-2016-fx-volatility-risk-premia.md
created: 2026-08-30
updated: 2026-08-30
---

## Goal

A second, small test of the claim-and-work loop — this time with **you (a fresh Claude Code
session with no memory of any prior conversation)** as the assignee, to check the same loop
that already worked for agy. Find **3-5 new** open-access papers on option writing / premium
selling and file them into `papers/option-writing/`, the same folder the first round used.

**Before searching, read every existing `.md` note in `papers/option-writing/`** to see
what's already there — titles, authors, and the specific hypothesis or empirical angle each
one covers. Don't just avoid re-adding the exact same paper; avoid papers that would be
substantively redundant with what's already covered (e.g., another generic "covered calls
outperform" survey covers no new ground if `israelov-nielsen-2015-covered-calls-uncovered`
already covers the reversal-decomposition angle in depth). Look for genuinely different
angles: tail risk, roll/management rules, cross-asset premium comparisons, machine-learning
approaches to timing the sell, whatever the existing set is missing.

Same file-pair convention as round 1:
- `<short-slug>.pdf` — only if genuinely open-access (SSRN preprint, arXiv, a journal's own
  free version). Never a paywalled or pirated copy.
- `<short-slug>.md` — title, authors, year, link, one-sentence testable hypothesis.

## Why this folder, why gitignored PDFs

Same as round 1: PDFs are gitignored (`papers/**/*.pdf`, this repo is public); `.md` notes are
committed and are what makes the folder useful without needing the PDFs on hand.

## Not in scope

- Don't touch or re-summarize any existing paper's note.
- Don't touch `sophie-option-research` itself.
- Don't judge whether these papers validate anything — that's a later, gated step.

## Decision log

- 2026-08-30: Read all 9 existing notes in `papers/option-writing/` first. Coverage map: aggregate-index
  VRP existence (Coval-Shumway), embedded-leverage/betting-against-beta (Frazzini-Pedersen), covered-call
  reversal decomposition (Israelov-Nielsen), hedge-fund-replication/tail (Jurek-Stafford), margin/leverage
  constraints (Santa-Clara-Saretto), skew/kurtosis pricing decomposition (Vazquez), and three Wysocki
  papers on sizing, hedging frequency, and ML strike selection for SPX put-writing. Gaps identified: no
  cross-asset comparison (everything is SPX/equity-index), no VIX-futures-based (vs. SPX-option-based)
  harvesting mechanism, and no paper on the systemic/crowding risk of short-vol strategies as opposed to
  the option-implied tail risk already covered by Vazquez/Santa-Clara-Saretto.
- 2026-08-30: Searched for candidates against those specific gaps rather than generic "covered call"
  surveys. Verified each candidate's PDF was a genuine open-access copy (university faculty page,
  institutional repository post-print, or AEA conference archive — not SSRN's paywalled delivery link,
  which 403'd) by downloading and running `pdftotext` on it before filing.
- 2026-08-30: Filed 4 new papers (within the 3-5 target): Carr-Wu 2009 (cross-sectional VRP across index +
  35 single stocks), Cheng 2019 (VIX-futures roll premium, hedging-demand mechanism), Augustin-Cheng-Van
  den Bergen 2021 (Volmageddon — systemic crowding/blowup risk in short-vol ETPs), Della Corte-Ramadorai-
  Sarno 2016 (FX volatility risk premium — first non-equity cross-asset paper in the folder). Stopped at 4
  rather than padding to 5; a fifth candidate (Segonne's SPX variance-dynamics paper) was checked and
  rejected as not substantively about premium selling.

## Result

4 new open-access papers filed in `papers/option-writing/` (`.md` + `.pdf` each, PDFs gitignored):
`carr-wu-2009-variance-risk-premia`, `cheng-2019-vix-premium`,
`augustin-cheng-vandenbergen-2021-volmageddon`, `della-corte-ramadorai-sarno-2016-fx-volatility-risk-premia`.
No existing paper notes were touched.
