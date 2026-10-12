import re

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Patch heishan CGs
text = text.replace('\"hs_start\": {\"type\"', '\"hs_start\": {\"cg\": \"c3_recruit_board\", \"type\"')
text = text.replace('\"hs_peiqian\": {\"type\"', '\"hs_peiqian\": {\"cg\": \"c3_bribe_villager\", \"type\"')
text = text.replace('\"hs_encounter\": {\"type\"', '\"hs_encounter\": {\"cg\": \"c3_encounter_ning\", \"type\"')
text = text.replace('\"hs_ignore\": {\"type\"', '\"hs_ignore\": {\"cg\": \"c3_leave_ning\", \"type\"')

text = text.replace('\"hs_zhangyan\": {\"type\"', '\"hs_zhangyan\": {\"cg\": \"c3_zhangyan_meet\", \"type\"')
text = text.replace('\"hs_save_fight\": {\"type\"', '\"hs_save_fight\": {\"cg\": \"c3_save_ning\", \"type\"')
text = text.replace('\"hs_junfa\": {\"type\"', '\"hs_junfa\": {\"cg\": \"c3_xiahoulan_law\", \"type\"')

text = text.replace('\"hs_timeskip\": {\"type\"', '\"hs_timeskip\": {\"cg\": \"c3_guotu_raid\", \"type\"')
text = text.replace('\"hs_escape\": {\"type\"', '\"hs_escape\": {\"cg\": \"c3_secret_path\", \"type\"')
text = text.replace('\"hs_jieqiao_eve\": {\"type\"', '\"hs_jieqiao_eve\": {\"cg\": \"c3_guojia_map\", \"type\"')
text = text.replace('\"hs_breakout\": {\"type\"', '\"hs_breakout\": {\"cg\": \"c3_breakout\", \"type\"')
text = text.replace('\"hs_alliance\": {\"type\"', '\"hs_alliance\": {\"cg\": \"c3_alliance\", \"type\"')
text = text.replace('\"hs_quyi\": {\"type\"', '\"hs_quyi\": {\"cg\": \"c3_quyi_camp\", \"type\"')
text = text.replace('\"hs_wenchou\": {\"type\"', '\"hs_wenchou\": {\"cg\": \"c3_save_zan\", \"type\"')
text = text.replace('\"hs_end\": {\"type\"', '\"hs_end\": {\"cg\": \"c3_banma_flag\", \"type\"')

# 2. Patch luoyang_n CGs
text = text.replace('\"ln_charge\": {\"x\"', '\"ln_charge\": {\"cg\": \"c2_ln_meet\", \"x\"')
text = text.replace('\"ln_banner\": {\"x\"', '\"ln_banner\": {\"cg\": \"c2_ln_sponsor\", \"x\"')
text = text.replace('\"ln_caocao\": {\"x\"', '\"ln_caocao\": {\"cg\": \"c2_ln_caocao\", \"x\"')
text = text.replace('\"ln_rescue\": {\"x\"', '\"ln_rescue\": {\"cg\": \"c2_ln_bianshui\", \"x\"')

# 3. Patch shouluoyang lijue_test
old_farewell = '\"farewell\": {\"x\": 17, \"y\": 1, \"type\": \"event\", \"label\": \"去长安\", \"next\": [],'
new_farewell = '\"farewell\": {\"x\": 17, \"y\": 1, \"type\": \"event\", \"label\": \"去长安\", \"next\": [\"lijue_test\"],'
text = text.replace(old_farewell, new_farewell)

farewell_record = '\"prompt\": \"你带着董白和蔡文姬，出发去长安。\", \"record\": \"路线：长安\"}'
farewell_no_record = '\"prompt\": \"你带着董白和蔡文姬，出发去长安。\"}'

# Remove the record from farewell only inside shouluoyang.
# Wait, let's just find the exact farewell text and replace it.
exact_farewell = '\"farewell\": {\"x\": 17, \"y\": 1, \"type\": \"event\", \"label\": \"去长安\", \"next\": [\"lijue_test\"], \"text\": [\"出发去长安的前一夜，你把孙策和周瑜叫到城头。\", \"{lord}：「我去长安，一是成亲，二是替主公看着董卓，三是找王允。」\", \"周瑜：「大哥，那是龙潭虎穴。」孙策：「谁敢动大哥，我带兵打进长安！」\", \"{lord}：「虎子，你乖乖在洛阳帮你爹。三弟，账本给我留一页——大哥的份子钱，记着。」\", \"董白在城下喊你：「喂！走了！爷爷在等我们！」她今天穿了一身新衣裳，笑得比哪天都亮。\", \"{lord}（内心）：她是真心高兴。高兴要嫁人，高兴能和爷爷和好。……可我这一趟去长安，到底是为了什么？\", \"吴夫人把一只包袱塞进你怀里：「喜服娘给你改好了。……活着回来。」\", \"蔡文姬抱着琴，跟在车后：「我也去。家父在长安。」\"], \"portraits\": [\"dongbai\", \"wuguotai\"], \"prompt\": \"你带着董白和蔡文姬，出发去长安。\", \"record\": \"路线：长安\"}'

exact_farewell_new = exact_farewell.replace('\"record\": \"路线：长安\"}', '\"record\": \"路线：长安\"}') # wait, I need to remove record from farewell, and add lijue_test after it.
exact_farewell_new = exact_farewell.replace('\"prompt\": \"你带着董白和蔡文姬，出发去长安。\", \"record\": \"路线：长安\"}', '\"prompt\": \"你带着董白和蔡文姬，出发去长安。\"}')

lijue_test = ',\n        \"lijue_test\": {\"x\": 18, \"y\": 1, \"type\": \"battle\", \"label\": \"拦路迎亲\", \"next\": [], \"elite\": true, \"battle\": \"c4_lijue_test\", \"record_win\": \"击退了试探的李傕\", \"record\": \"路线：长安\", \"text\": [\"去长安的路上，过函谷关时，一支重甲西凉铁骑拦住了去路。带头的正是董卓麾下大将李傕。\", \"@lijue 李傕提着大刀大笑：「孙女婿，太师说了，去长安的路不太平。让某家试试，你护不护得住白小姐！」\", \"@dongbai 董白掀开车帘就骂：「李傕！你敢拦我的车？！」\", \"@lijue 李傕笑得更大声了：「大小姐，这是太师的军令！孙女婿，拔刀吧！」\", \"{lord}（内心）：……好家伙，丈老爷派人半路劫道试功夫？这算是哪门子的迎亲风俗？\"]}'

text = text.replace(exact_farewell, exact_farewell_new + lijue_test)

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'w', encoding='utf-8') as f:
    f.write(text)

print('Patched story.json cleanly!')
