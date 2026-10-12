import re

py_path = r'F:\workspace\sanguo-cards\tools\art_prompts.py'
with open(py_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_cgs = [
    '    "c3_recruit_board": "a recruitment board at the gate of Zhending: the hero slapping his chest proudly before a wooden notice board, Zhao Yun standing by with his silver spear, a crowd of simple villagers watching with amusement",',
    '    "c3_bribe_villager": "a village road in Changshan: the hero awkwardly pressing copper coins into a villager\'s hands, a rogue soldier smirking nearby, Xiahou Lan watching coldly from a distance",',
    '    "c3_encounter_ning": "a cliffside in the Taihang mountains: Zhang Ning (a young woman in white with a medicine box) holding a gold needle coldly defying a mob of Yellow Turban zealots; the bandit leader Zhang Baiqi laughing and pointing at her",',
    '    "c3_leave_ning": "the entrance of a mountain valley: the hero leading his troops quietly away, looking back with a conflicted expression at the trapped girl in white deep in the valley",',
    '    "c3_zhangyan_meet": "the Black Mountain stronghold at the peak of Taihang: the bandit king Zhang Yan landing lightly from a high cliff before the hero; surrounding cliffs filled with thousands of bandits holding torches",',
    '    "c3_guotu_raid": "outside the gates of the Zhen manor in Wuji: the sinister Guo Tu laughing on horseback with a fan, as heavy Jizhou infantry smash open the manor\'s great doors",',
    '    "c3_secret_path": "the entrance of a secret mountain tunnel at night: Lady Zhang leading the young girl Zhen Mi into the dark cave guided by Black Mountain bandits with torches; Zhen Mi looking back at distant fires in Wuji",',
    '    "c3_guojia_map": "inside a military tent at night: Guo Jia holding a wine cup and pointing at a campaign map with a riding crop; the hero, Zhao Yun, and Zhang Yan watching closely around the low table",',
    '    "c3_breakout": "the burning gates of the Zhen manor: the hero leading a cavalry charge out of the fire, his spear knocking aside a Jizhou crossbowman blocking the way",',
]

if '"c3_xiahoulan_law":' in text:
    text = text.replace('    "c3_xiahoulan_law":', '\n'.join(new_cgs) + '\n    "c3_xiahoulan_law":')

new_next = [
    '    ("cg", "c3_recruit_board", "北线·真定发榜"),',
    '    ("cg", "c3_bribe_villager", "北线·和稀泥"),',
    '    ("cg", "c3_encounter_ning", "北线·深山绝壁"),',
    '    ("cg", "c3_leave_ning", "北线·明哲保身"),',
    '    ("cg", "c3_zhangyan_meet", "北线·黑山大寨"),',
    '    ("cg", "c3_guotu_raid", "北线·郭图寻仇"),',
    '    ("cg", "c3_secret_path", "北线·黑山秘道"),',
    '    ("cg", "c3_guojia_map", "北线·界桥前夜"),',
    '    ("cg", "c3_breakout", "北线·府门突围"),',
]

if '("cg", "c3_xiahoulan_law",' in text:
    text = text.replace('    ("cg", "c3_xiahoulan_law",', '\n'.join(new_next) + '\n    ("cg", "c3_xiahoulan_law",')

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched art_prompts.py!')
