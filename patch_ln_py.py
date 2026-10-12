import re

py_path = r'F:\workspace\sanguo-cards\tools\art_prompts.py'
with open(py_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_cgs = [
    '    "c2_ln_meet": "a frozen dirt road near the Yellow River: the red-armored girl Lu Lingqi falling from her horse in tears, Zhao Yun\'s silver spear at her throat, the hero blocking the spear with his own just in time",',
    '    "c2_ln_sponsor": "outside the Suanzao allied camp: Guo Jia drunkenly writing \'Zhongshan Zhen\' on a huge red banner, the hero standing by proudly; in the background, dozens of carts of sheep and wine covered in red silk",',
    '    "c2_ln_caocao": "outside a military tent in Suanzao: the short-statured Cao Cao slamming a table with red eyes in anger, turning to look at the exasperated hero to borrow grain",',
    '    "c2_ln_bianshui": "the chaos of battle by the Bian river: Cao Cao exhausted and wounded by an arrow, Cao Hong offering him a horse, while the hero appears smiling with two large Changshan warhorses",',
]

if '"c2_ln_meet"' not in text:
    if '"ln_camp":' in text:
        text = text.replace('    "ln_camp":', '\n'.join(new_cgs) + '\n    "ln_camp":')

new_next = [
    '    ("cg", "c2_ln_meet", "北线·夜奔遇险"),',
    '    ("cg", "c2_ln_sponsor", "北线·赞助商大旗"),',
    '    ("cg", "c2_ln_caocao", "北线·曹操借粮"),',
    '    ("cg", "c2_ln_bianshui", "北线·汴水救人"),',
]

if '("cg", "c2_ln_meet",' not in text:
    if '("cg", "ln_camp",' in text:
        text = text.replace('    ("cg", "ln_camp",', '\n'.join(new_next) + '\n    ("cg", "ln_camp",')

with open(py_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched art_prompts.py!')
