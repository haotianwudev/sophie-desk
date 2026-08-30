#!/usr/bin/env bash
# Probe: option-writing paper library test.
# Real evidence only: count actual files in the folder, not a claim about them.
set -u
DIR="papers/option-writing"

notes=$(ls "$DIR"/*.md 2>/dev/null | wc -l)
pdfs=$(ls "$DIR"/*.pdf 2>/dev/null | wc -l)

if [ "$notes" -eq 0 ] && [ "$pdfs" -eq 0 ]; then
  echo "RUN 0 papers filed yet"
elif [ "$notes" -ge 5 ]; then
  echo "OK ${notes} notes, ${pdfs} local PDFs"
else
  echo "RUN ${notes} notes, ${pdfs} local PDFs -- aiming for 5-10"
fi
exit 0
