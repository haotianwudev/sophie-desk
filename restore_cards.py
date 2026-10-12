# -*- coding: utf-8 -*-
import json
with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    text = f.read()

scenario_str = '''
    "th_patrol": {"name": "太行巡山兵", "turn_limit": 6, "enemy": "th_patrol"},
    "bh_jiang_trap": {"name": "姜家寨暗哨", "turn_limit": 6, "enemy": "shanzei_bing"},
    "bh_wolf2": {"name": "并州精骑", "turn_limit": 6, "enemy": "ln_langqi"},
    "bh_jz_inf": {"name": "冀州步卒", "turn_limit": 6, "enemy": "hs_jizhou_buzhu"},
    "bh_jz_spear": {"name": "冀州长枪", "turn_limit": 6, "enemy": "hs_jizhou_buzhu"},
    "bh_jz_scout": {"name": "冀州游骑", "turn_limit": 6, "enemy": "hs_jizhou_qibing"},
    "bh_jz_arch": {"name": "冀州强弩", "turn_limit": 6, "enemy": "hs_jizhou_qibing"},
    "bh_hj_duzhan": {"name": "黄巾督战队", "turn_limit": 6, "enemy": "huangjin_vanguard"},
'''

text = text.replace('  "scenarios": {', '  "scenarios": {' + scenario_str)

with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'w', encoding='utf-8') as f:
    f.write(text)

print("Restored missing scenarios to cards.json")
