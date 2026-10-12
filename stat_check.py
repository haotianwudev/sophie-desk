import json
d = json.load(open(r'F:\workspace\sanguo-cards\godot\data\story.json', encoding='utf-8'))
for q in d['quests']:
    if q['id'] == 'beihai':
        sq = q['squares']
        battles = [s for s in sq.values() if s['type'] == 'battle']
        boss = [s for s in battles if s.get('boss')]
        elite = [s for s in battles if s.get('elite') and not s.get('boss')]
        normal = [s for s in battles if not s.get('elite') and not s.get('boss')]
        print(q['id'], len(sq), 'battles', len(normal), len(elite), len(boss))
