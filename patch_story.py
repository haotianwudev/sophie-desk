import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for q in d['quests']:
    if q['id'] == 'shouluoyang':
        # Modify farewell
        farewell = q['squares']['farewell']
        farewell['next'] = ['lijue_test']
        record = farewell.pop('record', None)
        
        # Add lijue_test node
        q['squares']['lijue_test'] = {
            'x': 18,
            'y': 1,
            'type': 'battle',
            'label': '拦路迎亲',
            'next': [],
            'elite': True,
            'battle': 'c4_lijue_test',
            'record_win': '击退了试探的李傕',
            'text': [
                '去长安的路上，过函谷关时，一支重甲西凉铁骑拦住了去路。带头的正是董卓麾下大将李傕。',
                '@lijue 李傕提着大刀大笑：「孙女婿，太师说了，去长安的路不太平。让某家试试，你护不护得住白小姐！」',
                '@dongbai 董白掀开车帘就骂：「李傕！你敢拦我的车？！」',
                '@lijue 李傕笑得更大声了：「大小姐，这是太师的军令！孙女婿，拔刀吧！」',
                '{lord}（内心）：……好家伙，丈老爷派人半路劫道试功夫？这算是哪门子的迎亲风俗？'
            ]
        }
        if record:
            q['squares']['lijue_test']['record'] = record

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('Patched story.json!')
