#!/usr/bin/env bash
# Probe: how many of the current papers have a real relevance rating, and
# whether the progressive index file exists with real content.
set -u
DIR="papers/option-writing"
INDEX="$DIR/REVIEW-INDEX.md"
TOTAL=$(ls "$DIR"/*.md 2>/dev/null | grep -v "REVIEW-INDEX" | wc -l)

rated=0
for f in "$DIR"/*.md; do
  [ "$(basename "$f")" = "REVIEW-INDEX.md" ] && continue
  grep -q "## Relevance to Personal Trading" "$f" 2>/dev/null && rated=$((rated + 1))
done

index_lines=0
[ -f "$INDEX" ] && index_lines=$(wc -l < "$INDEX")

if [ "$rated" -ge "$TOTAL" ]; then
  echo "OK ${rated}/${TOTAL} papers rated, REVIEW-INDEX.md ${index_lines} lines"
else
  echo "RUN ${rated}/${TOTAL} papers rated, REVIEW-INDEX.md ${index_lines} lines"
fi
exit 0
