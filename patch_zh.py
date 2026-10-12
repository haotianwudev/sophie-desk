import re

zh_path = r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py'
with open(zh_path, 'r', encoding='utf-8') as f:
    text = f.read()

new_cgs = [
    '    "c3_recruit_board": "北线·真定发榜（剧情 CG）",',
    '    "c3_bribe_villager": "北线·和稀泥（剧情 CG）",',
    '    "c3_encounter_ning": "北线·深山绝壁（剧情 CG）",',
    '    "c3_leave_ning": "北线·明哲保身（剧情 CG）",',
    '    "c3_zhangyan_meet": "北线·黑山大寨（剧情 CG）",',
    '    "c3_guotu_raid": "北线·郭图寻仇（剧情 CG）",',
    '    "c3_secret_path": "北线·黑山秘道（剧情 CG）",',
    '    "c3_guojia_map": "北线·界桥前夜（剧情 CG）",',
    '    "c3_breakout": "北线·府门突围（剧情 CG）",',
]

# Insert into DICT
if '"c3_xiahoulan_law":' in text:
    text = text.replace('    "c3_xiahoulan_law":', '\n'.join(new_cgs) + '\n    "c3_xiahoulan_law":')

new_overrides = [
    'OVERRIDES_ZH["c3_recruit_board"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。常山真定城门口：主角在一块写着招贤榜的木板前拍着胸脯，赵云在旁边扛着银枪，一群朴实的乡亲围在旁边看热闹。地面为开阔坚硬平整的夯土城道。"',
    'OVERRIDES_ZH["c3_bribe_villager"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。常山村头：主角一脸尴尬地把几串铜钱塞给被抢了鸡的老乡，旁边那个抢鸡的兵痞还在得意地笑，夏侯兰在远处冷眼旁观。地面为开阔坚硬平整的土路。"',
    'OVERRIDES_ZH["c3_encounter_ning"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。太行绝壁前：素白布衣的少女张宁背着药箱，手持金针冷冷对峙一群黄巾狂信徒。领头的黄巾渠帅张白骑正指着她大笑。地面为开阔坚硬平整的山道石台。"',
    'OVERRIDES_ZH["c3_leave_ning"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。太行山谷外：主角带着队伍悄悄撤离，主角回头看了一眼山谷深处被围困的白衣少女，神情复杂。地面为开阔坚硬平整的黄土山路。"',
    'OVERRIDES_ZH["c3_zhangyan_meet"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。太行绝顶黑山大寨：黑山首领张燕如灵猫般从高崖上跃下，稳稳落在主角面前。四周悬崖上站满了举着火把的十几万黑山军。地面为开阔坚硬平整的山顶平地。"',
    'OVERRIDES_ZH["c3_guotu_raid"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。无极甄府大门外：郭图骑在马上，摇着扇子阴冷地笑着，一队冀州重甲兵撞开了甄府的大门。地面为开阔坚硬平整的青石板街道。"',
    'OVERRIDES_ZH["c3_secret_path"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。太行秘道前夜景：张夫人牵着年幼的甄宓，在黑山军举着火把的掩护下撤入漆黑的山洞，甄宓回头看向无极方向远处的火光。地面为开阔坚硬平整的山地石径。"',
    'OVERRIDES_ZH["c3_guojia_map"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。夜间的军帐里：郭嘉端着酒杯，用一根马鞭指着铺在矮榻上的行军地图，主角、赵云和张燕等人在一旁围观。地面为开阔坚硬平整的木板营地。"',
    'OVERRIDES_ZH["c3_breakout"] = "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。燃烧的无极甄府门前：主角带着一百铁骑在大火中向外突围，长枪挑飞拦路的冀州强弩手。地面为开阔坚硬平整的石板街道。"',
]

if 'OVERRIDES_ZH["c3_xiahoulan_law"] =' in text:
    text = text.replace('OVERRIDES_ZH["c3_xiahoulan_law"] =', '\n'.join(new_overrides) + '\nOVERRIDES_ZH["c3_xiahoulan_law"] =')

with open(zh_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Patched art_prompts_zh.py!')
