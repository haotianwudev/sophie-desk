#!/usr/bin/env bash
# Probe: has the deep summary actually been added, not just claimed?
set -u
NOTE="papers/option-writing/israelov-nielsen-2015-covered-calls-uncovered.md"

if [ ! -f "$NOTE" ]; then
  echo "ERROR note file missing"
  exit 0
fi

if grep -q "## Detailed Summary" "$NOTE"; then
  words=$(sed -n '/## Detailed Summary/,$p' "$NOTE" | wc -w)
  if [ "$words" -ge 80 ]; then
    echo "OK Detailed Summary present, ${words} words"
  else
    echo "RUN Detailed Summary section exists but thin (${words} words)"
  fi
else
  echo "RUN no Detailed Summary section yet"
fi
exit 0
