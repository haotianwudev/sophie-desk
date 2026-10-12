# -*- coding: utf-8 -*-
import json
import re

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

match = re.search(r'("id":\s*"beihai".*?"squares":\s*)(\{.*?\n\s*\})(?=\s*\}\s*,\s*\{\s*"id":\s*"dongui")', text, re.DOTALL)
if not match:
    print("Match failed")
    exit(1)

sq = json.loads(match.group(2))

# Helper to shift nodes
def shift_x(start_x, shift):
    for k, v in sq.items():
        if v.get('x', 0) >= start_x:
            v['x'] += shift

# 1. Before Jiang Qiao (bh_jiang_pre is at x=7)
# Insert bh_jiang_trap
jiang_pre_node = sq['bh_jiang_pre']
start_x = jiang_pre_node['x']
shift_x(start_x, 1)
sq['bh_jiang_trap'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "姜家外围", "next": ["bh_jiang_pre"],
    "battle": "bh_jiang_trap", "text": ["去姜家寨的路上，布满了各种陷阱暗哨。"]
}
sq['bh_zheng']['next'] = ['bh_jiang_trap']

# 2. Before Gao Shun (bh_gaoshun is at x=... wait, it shifted)
gaoshun_node = sq['bh_gaoshun']
start_x = gaoshun_node['x']
shift_x(start_x, 1)
sq['bh_wolf2'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "并州精骑", "next": ["bh_gaoshun"],
    "battle": "bh_wolf2", "text": ["陷阵营之前，还有一队精锐的并州骑兵掩护。"]
}
sq['bh_wolf']['next'] = ['bh_wolf2']

# 3. Before Yan Liang (Branch)
# bh_river is currently what bh_m5 and bh_m6 point to.
# Let's replace bh_river with bh_route_choose.
river_node = sq['bh_river'] # We will delete this and add new nodes.
start_x = river_node['x']
m5 = sq['bh_m5']
m6 = sq['bh_m6']
yanliang = sq['bh_yanliang']

# Delete bh_river
del sq['bh_river']

# We need to insert a choose node, and 2 paths of 2 nodes each.
# Total width needed: choose (x), path1_1 (x+1, y=0), path1_2 (x+2, y=0), path2_1 (x+1, y=2), path2_2 (x+2, y=2).
# This takes 3 columns. bh_river took 1. So shift by 2.
shift_x(start_x + 1, 2)

sq['bh_route_choose'] = {
    "x": start_x, "y": 1, "type": "choose", "label": "突围路线",
    "prompt": "前往冀州渡口，有两条路可走。",
    "options": [
        {"label": "走平原官道", "effects": [{"say": "官道宽阔，但守军森严。"}, {"goto": "bh_jz_inf"}]},
        {"label": "钻芦苇小路", "effects": [{"say": "小路崎岖，且容易遇伏。"}, {"goto": "bh_jz_scout"}]}
    ]
}
m5['next'] = ['bh_route_choose']
m6['next'] = ['bh_route_choose']

sq['bh_jz_inf'] = {
    "x": start_x + 1, "y": 0, "type": "battle", "label": "冀州步卒", "next": ["bh_jz_spear"],
    "battle": "bh_jz_inf", "text": ["官道上，遇到了袁绍的正规步卒。"]
}
sq['bh_jz_spear'] = {
    "x": start_x + 2, "y": 0, "type": "battle", "label": "冀州长枪", "next": ["bh_yanliang"],
    "battle": "bh_jz_spear", "text": ["前方是密集的冀州长枪阵。"]
}

sq['bh_jz_scout'] = {
    "x": start_x + 1, "y": 2, "type": "battle", "label": "冀州游骑", "next": ["bh_jz_arch"],
    "battle": "bh_jz_scout", "text": ["芦苇荡里，遇到了巡逻的游骑兵。"]
}
sq['bh_jz_arch'] = {
    "x": start_x + 2, "y": 2, "type": "battle", "label": "冀州强弩", "next": ["bh_yanliang"],
    "battle": "bh_jz_arch", "text": ["芦苇深处射出漫天弩箭！"]
}

# 4. Before Guan Hai (bh_guanhai_pre is at x=...)
# Insert bh_hj_duzhan after bh_hj_qushuai (before bh_rest2)
rest2_node = sq['bh_rest2']
start_x = rest2_node['x']
shift_x(start_x, 1)
sq['bh_hj_duzhan'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "黄巾督战", "next": ["bh_rest2"],
    "battle": "bh_hj_duzhan", "text": ["击败渠帅后，黄巾军的精锐督战队拦住了去路。"]
}
sq['bh_hj_qushuai']['next'] = ['bh_hj_duzhan']


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

squares_json = "{\n"
items = list(sq.items())
for i, (k, v) in enumerate(items):
    squares_json += f'          "{k}": {dump_compact(v)}'
    if i < len(items) - 1:
        squares_json += ",\n"
    else:
        squares_json += "\n        }"

new_text = text[:match.start()] + match.group(1) + squares_json + text[match.end():]

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated story.json")
