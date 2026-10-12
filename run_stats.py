import json
d = json.load(open('godot/data/story.json', encoding='utf-8'))
art = json.load(open('pics/art.json', encoding='utf-8'))
cgs_delivered = set(art.get('cgs', {}).keys())
for q in d['quests']:
    sq = q['squares']
    battles = [s for s in sq.values() if s['type'] == 'battle']
    boss = [s for s in battles if s.get('boss')]
    elite = [s for s in battles if s.get('elite') and not s.get('boss')]
    normal = [s for s in battles if not s.get('elite') and not s.get('boss')]
    cgs = [s['cg'] for s in sq.values() if s.get('cg')]
    recruited = {c for s in sq.values() for c in s.get('cards', [])} | \
                {o['card'] for s in sq.values() for o in s.get('options', []) if o.get('card')}
    print(q['id'], len(sq), 'battles', len(normal), len(elite), len(boss),
          'cg', len(cgs), sum(c in cgs_delivered for c in cgs),
          'recruits', sorted(recruited))
