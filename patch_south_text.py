import json

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# 1. Modify isk to be south
if 'risk' in d['events']:
    d['events']['risk']['scope'] = 'south'
    
    # Create isk_n for north
    d['events']['risk_n'] = {
        'scope': 'north',
        'text': [
            '风雪迷了眼。向导缩着脖子指着悬崖：「从这道险沟穿过去能抄近路，就是容易遇见伏兵。」',
            '{lord}（内心）：兰斯十里这叫「难度UP」。选了，后面的敌人更强，奖励也更好。'
        ],
        'choose': [
            {'label': '走险沟（敌人变强，但必掉宝箱）', 'danger': 1},
            {'label': '绕大路'}
        ]
    }

# 2. Modify ln_feast text
for q in d['quests']:
    if q['id'] == 'luoyang_n':
        if 'ln_feast' in q['squares']:
            q['squares']['ln_feast']['text'] = [
                '十几路诸侯天天开会、开完就喝酒，一谈出兵就顾左右而言他。',
                '{lord}（内心）：袁绍——爱开会、从不拍板的那种老板。',
                '郭嘉吃了一顿饭就出来了：「袁本初只学了周公礼贤下士的样子，不懂用人。」'
            ]
        break

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print('Fixed risk event and ln_feast text!')
