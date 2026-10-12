import json
import re

zh_path = r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py'
with open(zh_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_cgs = [
    '    "c2_ln_meet": "北线·夜奔遇险（剧情 CG）",',
    '    "c2_ln_sponsor": "北线·赞助商大旗（剧情 CG）",',
    '    "c2_ln_caocao": "北线·曹操借粮（剧情 CG）",',
    '    "c2_ln_bianshui": "北线·汴水救人（剧情 CG）",',
]

if '"c2_ln_meet"' not in text:
    if '"ln_camp":' in text:
        text = text.replace('    "ln_camp":', '\n'.join(new_cgs) + '\n    "ln_camp":')

new_overrides = [
    'OVERRIDES_ZH["c2_ln_meet"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。黄河古道冰冻的土路上：红甲的少女吕玲绮满脸泪痕地跌落下马，赵云的白马银枪直指她的咽喉，主角挺枪在千钧一发之际架住了赵云的枪。地面为开阔坚硬平整的冰冻土路。"',
    'OVERRIDES_ZH["c2_ln_sponsor"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。酸枣诸侯大营前：郭嘉借着酒劲在一面红锦大旗上挥毫写下『中山甄记』，主角满脸得意地站在一旁。背景是几十车用大红绸缎盖着的肥羊和美酒。地面为开阔坚硬平整的黄土营地。"',
    'OVERRIDES_ZH["c2_ln_caocao"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。酸枣大营外：个子不高的曹操按着剑柄、红着眼睛拍桌子怒骂，转头看向满脸无奈的主角，似乎正在厚着脸皮借粮。地面为开阔坚硬平整的夯土营地。"',
    'OVERRIDES_ZH["c2_ln_bianshui"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。汴水河畔的乱军中：曹操身中流矢狼狈不堪，曹洪正要把自己的战马让给他。主角牵着两匹高大的常山战马微笑着出现在旁边。地面为开阔坚硬平整的河滩碎石地。"',
]

if 'OVERRIDES_ZH["c2_ln_meet"]' not in text:
    if 'OVERRIDES_ZH["ln_camp"] =' in text:
        text = text.replace('OVERRIDES_ZH["ln_camp"] =', '\n'.join(new_overrides) + '\nOVERRIDES_ZH["ln_camp"] =')

with open(zh_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched art_prompts_zh.py!')
