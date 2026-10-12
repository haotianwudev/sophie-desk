import re

with open(r'F:\workspace\sanguo-cards\tools\art_prompts.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_prompts = '''
    "zhenghao": "Character portrait, half-body, Zheng Hao (郑好), female bandit boss. Wild and aggressive, holding a thick-backed broadsword. Anime cel-shaded style, Rance 10 style, thick coloring, solid light gray background.",
    "jiangqiao": "Character portrait, half-body, Jiang Qiao (姜巧), female bandit boss. Cunning and agile, with hidden weapons and traps on her belt. Anime cel-shaded style, Rance 10 style, thick coloring, solid light gray background.",
    "c4_escape": "16:9 Story CG. Two female bandit bosses (one with a broadsword, one with hidden weapons) fighting side by side in a snowy mountain pass, holding off an unseen enemy army. Action pose. Anime cel-shaded style, thick coloring.",
    "end_juefa": "16:9 Story CG. Tragic ending. A young female warrior (Lu Lingqi) falls, mortally wounded, taking a blow meant for the protagonist in a snowy mountain pass. The protagonist catches her. Anime cel-shaded style, thick coloring, dramatic lighting.",
    "c4_taishici": "16:9 Story CG. A young heroic general (Taishi Ci) with a spear, fighting his way through a chaotic crowd of yellow-turbaned rebels outside a city wall. Anime cel-shaded style, thick coloring.",
    "c4_kongrong": "16:9 Story CG. An older, dignified scholar (Kong Rong) sitting at a low wooden table indoors, smiling as he pushes a golden official seal across the table towards the viewer. Anime cel-shaded style, thick coloring.",
'''

# Find the end of PROMPTS = { ... }
if '"zhenghao"' not in text:
    text = re.sub(r'(    "end_fuchao": ".*?",\n)', r'\1' + new_prompts, text)
    with open(r'F:\workspace\sanguo-cards\tools\art_prompts.py', 'w', encoding='utf-8') as f:
        f.write(text)

with open(r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py', 'r', encoding='utf-8') as f:
    text_zh = f.read()

new_prompts_zh = '''
    "zhenghao": "角色立绘半身像，三国历史战棋视觉小说立绘，兰斯10赛璐珞厚涂风格，精致清晰的黑色墨线勾勒，华丽沉稳的厚重色彩。郑好，女土匪大当家。气质泼辣狂放，手持厚背大刀，服饰带有山寨野性风格。纯浅灰纯色干净背景。",
    "jiangqiao": "角色立绘半身像，三国历史战棋视觉小说立绘，兰斯10赛璐珞厚涂风格，精致清晰的黑色墨线勾勒，华丽沉稳的厚重色彩。姜巧，女土匪大当家。气质机灵狡黠，身上挂着暗器和连弩，服饰轻盈干练。纯浅灰纯色干净背景。",
    "c4_escape": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。太行雪山隘口，两位女当家（郑好持大刀，姜巧持暗器）并肩作战，默契配合，阻挡前方看不见的重甲步兵阵列，动作充满张力。下方35%留白为雪地。",
    "end_juefa": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。悲壮结局。太行雪山隘口，吕玲绮为了保护主角，被画戟重创倒在主角怀里。漫天风雪，气氛绝望悲凉。下方35%留白为染血的雪地。",
    "c4_taishici": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。北海城外，年轻骁将太史慈手持长枪，单人突阵，在黄巾军的人海中如入无人之境。下方35%留白为开阔的黄土地。",
    "c4_kongrong": "16:9 横版故事剧情事件插画，视觉小说剧情 CG，兰斯10赛璐珞厚涂风格，精致清晰黑色墨线勾勒，华丽沉稳色彩。郡府室内，长须儒雅的老者（孔融）微笑着，将一枚金色的北海相大印顺着矮榻桌面推向画面前方。下方35%留白为木质地板。",
'''

if '"zhenghao"' not in text_zh:
    text_zh = re.sub(r'(    "end_fuchao": ".*?",\n)', r'\1' + new_prompts_zh, text_zh)
    with open(r'F:\workspace\sanguo-cards\tools\art_prompts_zh.py', 'w', encoding='utf-8') as f:
        f.write(text_zh)

print('Updated art prompts properly!')
