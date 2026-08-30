#!/usr/bin/env bash
# Probe: round-2 paper count. Baseline from round 1 was 9 notes / 9 PDFs.
set -u
DIR="papers/option-writing"

notes=$(ls "$DIR"/*.md 2>/dev/null | wc -l)
pdfs=$(ls "$DIR"/*.pdf 2>/dev/null | wc -l)
BASELINE=9

new_notes=$(( notes - BASELINE ))

if [ "$new_notes" -le 0 ]; then
  echo "RUN ${notes} notes total (baseline ${BASELINE}), 0 new yet"
elif [ "$new_notes" -ge 3 ]; then
  echo "OK ${notes} notes total, ${new_notes} new, ${pdfs} local PDFs"
else
  echo "RUN ${notes} notes total, only ${new_notes} new so far (aiming for 3-5)"
fi
exit 0
