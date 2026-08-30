#!/usr/bin/env bash
# Probe: round-4 paper count, and how many are recorded-but-not-downloaded.
set -u
DIR="papers/option-writing"

notes=$(ls "$DIR"/*.md 2>/dev/null | wc -l)
pdfs=$(ls "$DIR"/*.pdf 2>/dev/null | wc -l)
unavailable=$(grep -l "STATUS: PDF NOT DOWNLOADED" "$DIR"/*.md 2>/dev/null | wc -l)
BASELINE=18

new_notes=$(( notes - BASELINE ))

if [ "$new_notes" -le 0 ]; then
  echo "RUN ${notes} notes total (baseline ${BASELINE}), 0 new yet"
elif [ "$new_notes" -ge 3 ]; then
  echo "OK ${notes} notes total, ${new_notes} new (${unavailable} recorded-unavailable), ${pdfs} local PDFs"
else
  echo "RUN ${notes} notes total, only ${new_notes} new so far (aiming for 3-5)"
fi
exit 0
