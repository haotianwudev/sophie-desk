#!/usr/bin/env bash
# Probe: round-3 paper count. Baseline going in was 13 notes / 13 PDFs.
set -u
DIR="papers/option-writing"

notes=$(ls "$DIR"/*.md 2>/dev/null | wc -l)
pdfs=$(ls "$DIR"/*.pdf 2>/dev/null | wc -l)
BASELINE=13

new_notes=$(( notes - BASELINE ))

if [ "$new_notes" -le 0 ]; then
  echo "RUN ${notes} notes total (baseline ${BASELINE}), 0 new yet"
elif [ "$new_notes" -ge 3 ]; then
  echo "OK ${notes} notes total, ${new_notes} new, ${pdfs} local PDFs"
else
  echo "RUN ${notes} notes total, only ${new_notes} new so far (aiming for 3-5)"
fi
exit 0
