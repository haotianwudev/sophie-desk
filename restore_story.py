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

# We are rebuilding ALL my missing nodes.
# 1. Taihang Mountains
# Current order: bh_m1/m2 -> bh_bandit -> bh_zheng_pre
# I wanted: bh_bandit -> bh_patrol -> bh_zheng_pre
# Let's insert bh_patrol after bh_bandit
bandit_node = sq['bh_bandit']
start_x = bandit_node['x'] + 1
shift_x(start_x, 1)
sq['bh_patrol'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "太行巡山", "next": ["bh_zheng_pre"],
    "battle": "th_patrol", "text": ["太行山外围，遇到了一波巡山贼。"]
}
bandit_node['next'] = ['bh_patrol']

# 2. Before Jiang Qiao (bh_jiang_pre is at x=...)
# Insert bh_jiang_trap
jiang_pre_node = sq['bh_jiang_pre']
start_x = jiang_pre_node['x']
shift_x(start_x, 1)
sq['bh_jiang_trap'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "姜家外围", "next": ["bh_jiang_pre"],
    "battle": "bh_jiang_trap", "text": ["去姜家寨的路上，布满了各种陷阱暗哨。"]
}
sq['bh_zheng']['next'] = ['bh_jiang_trap']

# 3. Toasting CG (bh_zj_peace)
# I added a CG to bh_zj_peace: cg: "c4_drink"
# Wait, let's just add it to bh_zj_join (the user added card rewards here, I'll add the CG here)
sq['bh_zj_join']['cg'] = "c4_drink"
sq['bh_zj_join']['text'][0] = "随后在简陋的山寨大堂里，三人豪迈对饮。你收编了两寨人马做近卫，给她们赐名：郑家的叫郑好（「正好」），姜家的叫姜巧（「将巧」）。"

# 4. Before Gao Shun
gaoshun_node = sq['bh_gaoshun']
start_x = gaoshun_node['x']
shift_x(start_x, 1)
sq['bh_wolf2'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "并州精骑", "next": ["bh_gaoshun"],
    "battle": "bh_wolf2", "text": ["陷阵营之前，还有一队精锐的并州骑兵掩护。"]
}
sq['bh_wolf']['next'] = ['bh_wolf2']

# 5. Before Yan Liang (Branch)
# bh_river is currently what bh_m5 and bh_m6 point to.
river_node = sq['bh_river']
start_x = river_node['x']
m5 = sq['bh_m5']
m6 = sq['bh_m6']
yanliang_x = start_x + 3

# Delete bh_river
del sq['bh_river']

# Shift for branch
shift_x(start_x + 1, 3)

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

sq['bh_yanliang'] = {
    "x": start_x + 3, "y": 1, "type": "battle", "label": "渡口·颜良", "next": ["bh_cross"],
    "battle": "bh_yanliang", "elite": True, "cg": "c4_yanliang",
    "text": ["黄河渡口，一员大将提着大刀列阵，身后满是举着强弩的先登死士。", "@yanliang 袁公有令，黑山余党，一个不留！颜良在此！"]
}

# 6. Million Yellow Turbans CG
sq['bh_beihai_start']['cg'] = "c4_million_hj"

# 7. Taishi Ci break CG
sq['bh_taishici_meet']['cg'] = "c4_taishici_break"

# 8. Before Guan Hai
rest2_node = sq['bh_rest2']
start_x = rest2_node['x']
shift_x(start_x, 2)

sq['bh_hj_qushuai'] = {
    "x": start_x, "y": 1, "type": "battle", "label": "黄巾渠帅", "next": ["bh_hj_duzhan"],
    "battle": "bh_hj_qushuai", "elite": True,
    "text": ["冲破狂信徒后，一个穿着道袍的黄巾渠帅拦住去路，狂热念咒。"]
}
sq['bh_hj_gate']['next'] = ['bh_hj_qushuai']

sq['bh_hj_duzhan'] = {
    "x": start_x + 1, "y": 1, "type": "battle", "label": "黄巾督战", "next": ["bh_rest2"],
    "battle": "bh_hj_duzhan", "text": ["击败渠帅后，黄巾军的精锐督战队拦住了去路。"]
}

# 9. Porridge CG
sq['bh_porridge']['cg'] = "c4_porridge"

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

print("Restored agent changes to story.json successfully.")
