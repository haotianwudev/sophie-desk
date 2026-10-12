import json
with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['quests']:
    if q['id'] in ['shouluoyang', 'changan', 'dongui']:
        print(f"Quest: {q['id']}, requires: {q.get('requires')}, unless: {q.get('unless')}")
