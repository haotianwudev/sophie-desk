# -*- coding: utf-8 -*-
import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# Find beihai quest
q = next(q for q in d['quests'] if q['id'] == 'beihai')
sq = q['squares']

# Helper to shift x of all nodes starting from a specific x
def shift_x(start_x, shift=1):
    for k, v in sq.items():
        if v.get('x') >= start_x:
            v['x'] += shift

# 1. Insert bh_patrol after bh_bandit
# bh_bandit is at x=2, next is bh_zheng_pre (x=3)
shift_x(3, 1)
sq['bh_patrol'] = {
    "x": 3, "y": 1, "type": "battle", "label": "太行巡山", "next": ["bh_zheng_pre"],
    "battle": "bh_patrol", "text": ["太行山林里，突然杀出一群拦路的贼寇。", "「交出买路财！」"]
}
sq['bh_bandit']['next'] = ['bh_patrol']

# 2. Insert bh_drink after bh_zj_join
# bh_zj_join is at x=9 (wait, we shifted +1, so it's 10). next is bh_rest1 (x=11)
join_node = sq['bh_zj_join']
shift_x(join_node['x'] + 1, 1)
sq['bh_drink'] = {
    "x": join_node['x'] + 1, "y": 1, "type": "event", "label": "山寨敬酒", "next": join_node['next'],
    "cg": "c4_drink", "text": ["简陋的山寨大堂里，你端起酒碗。", "郑好和姜巧左右坐着，端起酒碗一饮而尽。", "在这短暂的安宁里，你们化敌为友。"]
}
join_node['next'] = ['bh_drink']

# 3. Insert bh_yanliang after bh_river
# bh_river next is bh_cross
river_node = sq['bh_river']
shift_x(river_node['x'] + 1, 1)
sq['bh_yanliang'] = {
    "x": river_node['x'] + 1, "y": 1, "type": "battle", "label": "渡口·颜良", "next": river_node['next'],
    "battle": "bh_yanliang", "elite": True, "cg": "c4_yanliang",
    "text": ["你们逃脱了吕布的追杀，一路狂奔至冀州渡口。", "岸边，一员威风凛凛的大将提着大刀列阵。", "「袁公有令，黑山余党，一个不留！颜良在此！」", "身后，无数先登死士举起了强弩。"]
}
river_node['next'] = ['bh_yanliang']

# 4. Add CG to bh_beihai_start
sq['bh_beihai_start']['cg'] = "c4_million_hj"

# 5. Add CG to bh_taishici_meet
sq['bh_taishici_meet']['cg'] = "c4_taishici_break"

# 6. Insert bh_hj_qushuai after bh_hj_gate
# bh_hj_gate next is bh_rest2
gate_node = sq['bh_hj_gate']
shift_x(gate_node['x'] + 1, 1)
sq['bh_hj_qushuai'] = {
    "x": gate_node['x'] + 1, "y": 1, "type": "battle", "label": "黄巾渠帅", "next": gate_node['next'],
    "battle": "bh_hj_qushuai", "elite": True,
    "text": ["冲破狂信徒后，一个穿着道袍的渠帅拦住了去路。", "「苍天已死，黄天当立！」他挥舞着大刀，身后的黄巾军像潮水般涌来。"]
}
gate_node['next'] = ['bh_hj_qushuai']

# 7. Add CG to bh_porridge
sq['bh_porridge']['cg'] = "c4_porridge"
sq['bh_porridge']['text'].insert(0, "你下令不杀降兵，而是在两军阵前支起几十口大锅熬粥。")
sq['bh_porridge']['text'].insert(1, "无数饿得脱相的黄巾军丢下武器，捧着粥碗痛哭失声。")

# Now we need to save story.json. 
# Because json.dump will ruin the formatting, we will do what we did before:
# Write the modified quest back by converting the whole dict back to string, but that ruins other quests.
# Better to just use a custom dumper for this quest!
import json
def dump_compact(obj):
    if isinstance(obj, dict):
        items = []
        for k, v in obj.items():
            items.append(f'"{k}": {dump_compact(v)}')
        return "{" + ", ".join(items) + "}"
    elif isinstance(obj, list):
        items = []
        for v in obj:
            items.append(dump_compact(v))
        return "[" + ", ".join(items) + "]"
    elif isinstance(obj, str):
        return json.dumps(obj, ensure_ascii=False)
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif obj is None:
        return "null"
    else:
        return str(obj)

# Dump the squares object
squares_json = "        \"squares\": {\n"
for k, v in sq.items():
    squares_json += f"          \"{k}\": {dump_compact(v)},\n"
# remove last comma
squares_json = squares_json.rstrip(",\n") + "\n        }"

# Read original
with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# Replace the squares block of beihai
pattern = r'("id": "beihai",.*?)"squares": \{.*?\n        \}(.*?\})'
match = re.search(pattern, text, re.DOTALL)
if match:
    new_text = text[:match.start()] + match.group(1) + squares_json + match.group(2) + text[match.end():]
    with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated story.json")
else:
    print("Could not find beihai squares block!")
