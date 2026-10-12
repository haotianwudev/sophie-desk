# -*- coding: utf-8 -*-
import re

new_prompts_zh = '''
    "c4_drink": "化敌为友：简陋的太行山寨大堂里，主角端着酒碗，左右坐着两位女土匪头子（郑好、姜巧），三人豪迈对饮，充满短暂的温馨与安宁",
    "c4_yanliang": "渡口截杀：冰冷的冀州河滩上，面容阴鸷、威风凛凛的颜良长刀下劈，身后是无数举着重型大弩的先登死士，地上插满箭矢，给主角极强的压迫感",
    "c4_million_hj": "百万黄巾：从北海城头俯瞰，城外漫山遍野全都是头裹黄巾的流民与乱军，连绵不绝的火把一直烧到天际线，令人绝望",
    "c4_taishici_break": "单骑破阵：夕阳下，太史慈一骑白马一杆长枪，如同利刃般切开黑压压的黄巾军阵，英姿勃发",
    "c4_porridge": "阵前熬粥：在两军阵前，主角支起几十口大锅熬粥，热气腾腾；无数饿得脱相的黄巾军丢下武器，捧着粥碗痛哭失声",
'''

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # insert before the end of the dictionary (assuming the last one ends before "}")
    # Actually just search for "c4_lvbu": "雪中宣平门·吕布（结局二前的最后一战）", and append after it in RELICS.
    # Wait, art_prompts_zh.py is a dict PROMPTS_ZH. 
    # Let's just insert before the closing brace of PROMPTS_ZH.
    match = re.search(r'\}\s*$', text)
    if match:
        text = text[:match.start()] + new_prompts_zh + text[match.start():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Updated {filepath}")
    else:
        print(f"Failed to update {filepath}")

update_file(r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py')
