import json
with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['quests']:
    if q['id'] == 'dongui':
        for k, v in q['squares'].items():
            print(f"{k}: next={v.get('next')}")
