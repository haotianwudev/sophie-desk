import json
d = json.load(open(r'F:\workspace\sanguo-cards\godot\data\story.json', encoding='utf-8'))
for q in d['quests']:
    if q['id'] == 'beihai':
        print(list(q['squares'].keys()))
