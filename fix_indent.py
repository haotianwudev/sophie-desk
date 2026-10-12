# -*- coding: utf-8 -*-
filepath = r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the indent for the lines we added
lines = text.split('\n')
for i, line in enumerate(lines):
    if '"c4_drink":' in line or '"c4_yanliang":' in line or '"c4_million_hj":' in line or '"c4_taishici_break":' in line or '"c4_porridge":' in line:
        lines[i] = 'OVERRIDES_ZH[' + line.strip().split(':')[0] + '] = ' + ':'.join(line.split(':')[1:]).strip()

with open(filepath, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
