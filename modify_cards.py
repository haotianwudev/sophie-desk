# -*- coding: utf-8 -*-
with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    text = f.read()

enemy_str = '''
    "yanliang": {"name": "颜良", "portrait": "yanliang", "hp": 18500, "at": 400, "actions": 2, "moves": [{"name": "大刀", "power": 1.0, "weight": 3}, {"name": "狂劈", "power": 1.6, "weight": 1}, {"name": "震慑", "power": 0.5, "weight": 1, "confuse": 0.5}, {"name": "蓄力", "power": 0, "weight": 1, "charge": "泰山压顶"}, {"name": "泰山压顶", "power": 3.0, "weight": 0}]},
    "th_patrol": {"name": "太行巡山兵", "portrait": "bandit", "hp": 4000, "at": 150, "actions": 1, "moves": [{"name": "小刀", "power": 1.0, "weight": 3}, {"name": "设陷阱", "power": 0.5, "weight": 1, "ap_drain": 1}], "card": "taihang_yiyong"},
    "hj_qushuai": {"name": "黄巾渠帅", "portrait": "huangjin", "hp": 11000, "at": 280, "actions": 2, "moves": [{"name": "大刀", "power": 1.0, "weight": 3}, {"name": "狂热念咒", "power": 0.5, "weight": 1, "heal": 0.1, "rage": 0.2}, {"name": "蓄力", "power": 0, "weight": 1, "charge": "太平妖术"}, {"name": "太平妖术", "power": 2.5, "weight": 0, "ap_drain": 1}]},
'''

scenario_str = '''
    "bh_patrol": {"name": "太行伏兵", "turn_limit": 6, "enemy": "th_patrol"},
    "bh_yanliang": {"name": "渡口·颜良", "turn_limit": 10, "enemy": "yanliang"},
    "bh_hj_qushuai": {"name": "青州渠帅", "turn_limit": 8, "enemy": "hj_qushuai"},
'''

text = text.replace('  "enemies": {', '  "enemies": {' + enemy_str)
text = text.replace('  "scenarios": {', '  "scenarios": {' + scenario_str)

with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated cards.json")
