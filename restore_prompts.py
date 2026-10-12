# -*- coding: utf-8 -*-
import sys

with open(r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Add missing CGs if they are not there
missing_cgs = '''
    "c4_drink": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。简陋的山寨大堂里，主角与两位年轻的女当家（郑好与姜巧）在火堆旁席地而坐，端起粗瓷大碗豪迈对饮，气氛热烈。",
    "c4_yanliang": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。黄河渡口的芦苇荡边，一员魁梧骁将（颜良）提着大刀列阵，身后是密密麻麻举着强弩的先登死士，压迫感十足。",
    "c4_million_hj": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。从高处俯瞰，北海城外的原野上，连绵不绝、一眼望不到头的黄巾饥民营帐，犹如黄色的汪洋。",
    "c4_taishici_break": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。乱军之中，年轻骁将太史慈单骑突入黑压压的黄巾阵中，双戟如风，将狂热的信徒硬生生撕开一道口子，背影孤绝勇猛。",
    "c4_porridge": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。北海城外的雪地里，架着几十口热气腾腾的大铁锅，原本凶神恶煞的黄巾军扔下了武器，捧着粗糙的陶碗喝着热粥，有人甚至激动得落泪。",
'''

if 'c4_yanliang' not in text:
    text = text.replace('OVERRIDES_ZH = {', 'OVERRIDES_ZH = {' + missing_cgs)
    with open(r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Restored CGs to art_prompts_zh.py")
else:
    print("CGs already in art_prompts_zh.py")
