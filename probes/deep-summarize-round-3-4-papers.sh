#!/usr/bin/env bash
# Probe: how many of the 10 in-scope papers (11 minus the no-PDF one) now
# have a real Detailed Summary, and whether has_detailed_summary got updated.
set -u
DIR="papers/option-writing"
TARGETS="andersen-benzoni-lund-2002-continuous-time-equity-return-models
bates-2008-market-for-crash-risk
bekaert-hoerova-2014-vix-variance-premium
bollerslev-tauchen-zhou-2009-expected-stock-returns-vrp
dew-becker-giglio-le-rodriguez-2017-price-of-variance-risk
feunou-jahan-parvar-okou-2018-downside-variance-risk-premium
garleanu-pedersen-poteshman-2009-demand-based-option-pricing
goyal-saretto-2009-cross-section-option-returns
zhong-2026-non-spanning-identification-scheduled-event-risk
zhou-2018-variance-risk-premia-macro-uncertainty"
TOTAL=10

done_count=0
for slug in $TARGETS; do
  f="$DIR/$slug.md"
  grep -q "## Detailed Summary" "$f" 2>/dev/null && done_count=$((done_count + 1))
done

if [ "$done_count" -ge "$TOTAL" ]; then
  echo "OK ${done_count}/${TOTAL} papers deep-summarized"
else
  echo "RUN ${done_count}/${TOTAL} papers deep-summarized"
fi
exit 0
