import json

new_battles = {
  "bh_zhenghao": {"name": "郑家寨", "turn_limit": 10, "enemy": "zhenghao"},
  "bh_jiangqiao": {"name": "姜家寨", "turn_limit": 10, "enemy": "jiangqiao"},
  "bh_lubu": {"name": "太行山口·吕布", "turn_limit": 8, "enemy": "lvbu_hulao"},
  "bh_guanhai": {"name": "北海解围", "turn_limit": 15, "enemy": "guanhai"}
}

new_enemies = {
  "zhenghao": {
    "name": "郑好", "portrait": "zhenghao", "hp": 14000, "at": 320, "actions": 2,
    "moves": [{"name": "厚背大刀", "power": 1.2, "weight": 4}, {"name": "压寨劈砍", "power": 1.5, "weight": 2, "pierce": True}]
  },
  "jiangqiao": {
    "name": "姜巧", "portrait": "jiangqiao", "hp": 12000, "at": 280, "actions": 3,
    "moves": [{"name": "连弩", "power": 0.8, "weight": 4}, {"name": "毒蒺藜", "power": 0.5, "weight": 2, "poison": 0.3}]
  },
  "guanhai": {
    "name": "管亥", "portrait": "guanhai", "hp": 20000, "at": 400, "actions": 2,
    "moves": [{"name": "狂沙斩", "power": 1.2, "weight": 4}, {"name": "黄天当立", "power": 1.8, "weight": 1}]
  }
}

new_cards = {
  "zhenghao": {"name": "郑好", "type": "hero", "hp": 400, "at": 180, "desc": "原郑家寨大当家，刀法泼辣狂放。", "tags": ["北线", "近战"]},
  "jiangqiao": {"name": "姜巧", "type": "hero", "hp": 350, "at": 140, "desc": "原姜家寨大当家，精通暗器与陷阱。", "tags": ["北线", "远程"]},
  "zheng_daoshou": {"name": "郑家刀手", "type": "soldier", "cost": 2, "hp": 200, "at": 120, "desc": "郑好的亲卫，作战不要命。"},
  "jiang_jiguanshou": {"name": "姜家机关手", "type": "soldier", "cost": 2, "hp": 150, "at": 100, "desc": "姜巧的手下，擅长远程暗器。"},
  "beihai_tuntian": {"name": "北海屯田兵", "type": "soldier", "cost": 1, "hp": 250, "at": 60, "desc": "青州降卒编成的屯田兵，耐力极好。"}
}

with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'r', encoding='utf-8') as f:
    text = f.read()

# Helper to inject safely
def inject(target, block):
    global text
    for k, v in block.items():
        if f'"{k}":' not in text:
            # find start of block
            marker = f'"{target}": {{'
            if marker in text:
                v_str = json.dumps(v, ensure_ascii=False)
                new_entry = f'\n    "{k}": {v_str},'
                text = text.replace(marker, marker + new_entry)

inject("scenarios", new_battles)
inject("enemies", new_enemies)
inject("cards", new_cards)

with open(r'F:\workspace\sanguo-cards\godot\data\cards.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated cards.json!')
