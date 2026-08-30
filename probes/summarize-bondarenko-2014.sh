#!/usr/bin/env bash
set -u
NOTE="papers/option-writing/bondarenko-2014-why-are-puts-expensive.md"

if grep -q "## Detailed Summary" "$NOTE"; then
  words=$(sed -n '/## Detailed Summary/,$p' "$NOTE" | wc -w)
  [ "$words" -ge 80 ] && echo "OK Detailed Summary present, ${words} words" \
                      || echo "RUN Detailed Summary section exists but thin (${words} words)"
else
  echo "RUN no Detailed Summary section yet"
fi
exit 0
