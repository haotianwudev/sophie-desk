import json
with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d['enemies']['guanhai'] = {
    "name": "管亥", "portrait": "guanhai", "hp": 20000, "at": 400, "actions": 2,
    "moves": [{"name": "狂沙斩", "power": 1.2, "weight": 4}, {"name": "黄天当立", "power": 1.8, "weight": 1}]
}

d['cards']['zhenghao'] = {"name": "郑好", "type": "hero", "hp": 400, "at": 180, "desc": "原郑家寨大当家，刀法泼辣狂放。", "tags": ["北线", "近战"]}
d['cards']['jiangqiao'] = {"name": "姜巧", "type": "hero", "hp": 350, "at": 140, "desc": "原姜家寨大当家，精通暗器与陷阱。", "tags": ["北线", "远程"]}

# To write back without destroying order and format:
text = ""
with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    text = f.read()

# guanhai enemy
if '    "guanhai": {"name": "管亥", "portrait": "guanhai"' not in text:
    target = '"enemies": {'
    v_str = json.dumps(d['enemies']['guanhai'], ensure_ascii=False)
    text = text.replace(target, target + f'\n    "guanhai": {v_str},')

# zhenghao card
if '    "zhenghao": {"name": "郑好", "type": "hero"' not in text:
    target = '"cards": {'
    v_str = json.dumps(d['cards']['zhenghao'], ensure_ascii=False)
    text = text.replace(target, target + f'\n    "zhenghao": {v_str},')

# jiangqiao card
if '    "jiangqiao": {"name": "姜巧", "type": "hero"' not in text:
    target = '"cards": {'
    v_str = json.dumps(d['cards']['jiangqiao'], ensure_ascii=False)
    text = text.replace(target, target + f'\n    "jiangqiao": {v_str},')

with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated missing cards and enemies!')
