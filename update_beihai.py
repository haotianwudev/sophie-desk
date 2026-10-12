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

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

q = next(q for q in d['quests'] if q['id'] == 'beihai')
sq = q['squares']

def shift_x(start_x, shift=1):
    for k, v in sq.items():
        if v.get('x', 0) >= start_x:
            v['x'] += shift

shift_x(3, 1)
sq['bh_patrol'] = {
    "x": 3, "y": 1, "type": "battle", "label": "太行巡山", "next": ["bh_zheng_pre"],
    "battle": "bh_patrol", "text": ["太行山林里，突然杀出一群拦路的贼寇。", "「交出买路财！」"]
}
sq['bh_bandit']['next'] = ['bh_patrol']

join_node = sq['bh_zj_join']
shift_x(join_node['x'] + 1, 1)
sq['bh_drink'] = {
    "x": join_node['x'] + 1, "y": 1, "type": "event", "label": "山寨敬酒", "next": join_node['next'],
    "cg": "c4_drink", "text": ["简陋的山寨大堂里，你端起酒碗。", "郑好和姜巧左右坐着，端起酒碗一饮而尽。", "在这短暂的安宁里，你们化敌为友。"]
}
join_node['next'] = ['bh_drink']

river_node = sq['bh_river']
shift_x(river_node['x'] + 1, 1)
sq['bh_yanliang'] = {
    "x": river_node['x'] + 1, "y": 1, "type": "battle", "label": "渡口·颜良", "next": river_node['next'],
    "battle": "bh_yanliang", "elite": True, "cg": "c4_yanliang",
    "text": ["你们逃脱了吕布的追杀，一路狂奔至冀州渡口。", "岸边，一员威风凛凛的大将提着大刀列阵。", "「袁公有令，黑山余党，一个不留！颜良在此！」", "身后，无数先登死士举起了强弩。"]
}
river_node['next'] = ['bh_yanliang']

sq['bh_beihai_start']['cg'] = "c4_million_hj"
sq['bh_taishici_meet']['cg'] = "c4_taishici_break"

gate_node = sq['bh_hj_gate']
shift_x(gate_node['x'] + 1, 1)
sq['bh_hj_qushuai'] = {
    "x": gate_node['x'] + 1, "y": 1, "type": "battle", "label": "黄巾渠帅", "next": gate_node['next'],
    "battle": "bh_hj_qushuai", "elite": True,
    "text": ["冲破狂信徒后，一个穿着道袍的渠帅拦住了去路。", "「苍天已死，黄天当立！」他挥舞着大刀，身后的黄巾军像潮水般涌来。"]
}
gate_node['next'] = ['bh_hj_qushuai']

sq['bh_porridge']['cg'] = "c4_porridge"
sq['bh_porridge']['text'].insert(0, "你下令不杀降兵，而是在两军阵前支起几十口大锅熬粥。")
sq['bh_porridge']['text'].insert(1, "无数饿得脱相的黄巾军丢下武器，捧着粥碗痛哭失声。")

squares_json = "{\n"
items = list(sq.items())
for i, (k, v) in enumerate(items):
    squares_json += f'          "{k}": {dump_compact(v)}'
    if i < len(items) - 1:
        squares_json += ",\n"
    else:
        squares_json += "\n        }"

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

import re
# strictly replace the squares block of beihai
pattern = re.compile(r'("id":\s*"beihai",.*?)"squares":\s*\{.*?\n        \}(?=\s*\})', re.DOTALL)

def repl(m):
    return m.group(1) + '"squares": ' + squares_json

new_text = pattern.sub(repl, text)

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Updated story.json successfully.")
