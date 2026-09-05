#!/usr/bin/env bash
# Probe: round-5 (core VRP/option-writing) paper count, and how many are recorded-but-not-downloaded.
set -u
DIR="papers/option-writing"

notes=$(ls "$DIR"/*.md 2>/dev/null | grep -v REVIEW-INDEX | wc -l)
pdfs=$(ls "$DIR"/*.pdf 2>/dev/null | wc -l)
unavailable=$(grep -l "STATUS: PDF NOT DOWNLOADED" "$DIR"/*.md 2>/dev/null | wc -l)
deep=$(grep -l "## Detailed Summary" "$DIR"/*.md 2>/dev/null | wc -l)
BASELINE=24
TARGET=8

new_notes=$(( notes - BASELINE ))

if [ "$new_notes" -le 0 ]; then
  echo "RUN ${notes} notes total (baseline ${BASELINE}), 0 new yet"
elif [ "$new_notes" -ge "$TARGET" ]; then
  echo "OK ${notes} notes total, ${new_notes} new (${unavailable} recorded-unavailable, ${deep} with Detailed Summary), ${pdfs} local PDFs"
else
  echo "RUN ${notes} notes total, only ${new_notes} new so far (aiming for ${TARGET})"
fi
exit 0
