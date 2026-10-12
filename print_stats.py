import json
with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for k in ['chenlan', 'leibo', 'qiaorui', 'jiling']:
    enemy = d['enemies'].get(k)
    if enemy:
        print(f"{k}: hp={enemy.get('hp')} at={enemy.get('at')}")
