#!/usr/bin/env bash
# Probe: how many of the 13 total papers now have a real Detailed Summary.
set -u
DIR="papers/option-writing"
TOTAL=13

done_count=0
for f in "$DIR"/*.md; do
  grep -q "## Detailed Summary" "$f" 2>/dev/null && done_count=$((done_count + 1))
done

if [ "$done_count" -ge "$TOTAL" ]; then
  echo "OK ${done_count}/${TOTAL} papers have a Detailed Summary"
else
  echo "RUN ${done_count}/${TOTAL} papers have a Detailed Summary"
fi
exit 0
