import json

new_quest = {
  "id": "beihai",
  "title": "第四章 · 双凤乱太行",
  "requires": "界桥：救下公孙瓒",
  "event_scope": "north",
  "soldier_scope": "north",
  "squares": {
    "bh_start": {
      "x": 0, "y": 1, "type": "event", "label": "太行外围", "next": ["bh_m1", "bh_m2"],
      "text": [
        "【初平三年 · 夏】界桥之战后，斑马军退回太行山扎稳了脚跟。可山外围还有两股谁也不服谁的女匪：郑家寨的大当家一口厚背大刀，姜家寨的大当家一身暗器机关。两寨仇杀多年，把商路搅得没法走。",
        "{lord}（内心）：女土匪？没听过。……三国演义我不熟，可这两位肯定不在里面。"
      ]
    },
    "bh_m1": {"x": 1, "y": 1, "type": "mystery", "next": ["bh_bandit"]},
    "bh_m2": {"x": 1, "y": 2, "type": "treasure", "next": ["bh_bandit"]},
    "bh_bandit": {
      "x": 2, "y": 1, "type": "battle", "label": "外围山贼", "battle": "shanzei_band", "next": ["bh_zheng_pre"],
      "text": ["刚进山道，一伙喽啰就拦住了去路。这是郑姜两寨的外围人马。"]
    },
    "bh_zheng_pre": {
      "x": 3, "y": 1, "type": "event", "label": "郑家寨", "next": ["bh_zheng"],
      "text": ["打散了喽啰，前面就是郑家寨。大当家郑好提着厚背大刀，带着一群刀斧手冲了出来。"]
    },
    "bh_zheng": {
      "x": 4, "y": 1, "type": "battle", "label": "郑好", "elite": True, "battle": "bh_zhenghao", "next": ["bh_jiang_pre"],
      "text": ["郑好刀法泼辣，招招都是不要命的强攻！"]
    },
    "bh_jiang_pre": {
      "x": 5, "y": 1, "type": "event", "label": "供出死敌", "next": ["bh_jiang"],
      "text": ["郑好被五花大绑押上来。她呸了一声：「有本事把隔壁姜家那个狐狸精也揍了！我就服你！」", "{lord}：「好说，带路。」"]
    },
    "bh_jiang": {
      "x": 6, "y": 1, "type": "battle", "label": "姜巧", "elite": True, "battle": "bh_jiangqiao", "next": ["bh_zj_choose"],
      "text": ["姜家寨前，大当家姜巧布下了满地的机关暗器。"]
    },
    "bh_zj_choose": {
      "x": 7, "y": 1, "type": "choose", "label": "调解双凤",
      "text": ["两个女大当家都被绑在柱子上，还不忘互相吐口水对骂。你要怎么处置她们？"],
      "choose": [
        {"label": "把两人关一屋，调解到和好为止", "goto": "bh_zj_peace", "record": "郑姜：和好"},
        {"label": "随她们去，各管各的", "goto": "bh_zj_fight", "record": "郑姜：内讧"}
      ]
    },
    "bh_zj_peace": {
      "x": 8, "y": 1, "type": "event", "next": ["bh_zj_join"],
      "text": ["你搬了把椅子坐在门口，听两人从吵架吵到对骂、从对骂吵到一起骂你。天亮时，两人勾着肩出来了。"]
    },
    "bh_zj_fight": {
      "x": 8, "y": 2, "type": "event", "next": ["bh_zj_join"],
      "text": ["你给两人松了绑。两人各自冷哼一声，带着自己的人守在不同的山头，谁也不肯替谁补位。"]
    },
    "bh_zj_join": {
      "x": 9, "y": 1, "type": "event", "label": "收服双凤", "next": ["bh_rest1"],
      "text": ["你收编了两寨人马做近卫，给她们赐名：郑家的叫郑好（「正好」），姜家的叫姜巧（「将巧」）。", "两人异口同声：「凭什么她的名字比我的好听？」", "（获得兵卡：郑家刀手、姜家机关手）"]
    },
    "bh_rest1": {"x": 10, "y": 1, "type": "recover", "label": "太行休整", "next": ["bh_m3", "bh_m4"]},
    "bh_m3": {"x": 11, "y": 1, "type": "mystery", "next": ["bh_lubu_start"]},
    "bh_m4": {"x": 11, "y": 2, "type": "treasure", "next": ["bh_lubu_start"]},
    "bh_lubu_start": {
      "x": 12, "y": 1, "type": "event", "label": "吕布北来", "next": ["bh_wolf"],
      "text": ["【初平三年 · 冬】袁绍为了剿灭太行山的黑山军，派来了刚投奔他的猛虎——吕布。", "吕布根本不在乎山里是谁，黑山的粮和马，够他的并州兵吃一冬了。"]
    },
    "bh_wolf": {
      "x": 13, "y": 1, "type": "battle", "label": "并州狼骑", "battle": "bingzhou_langqi", "next": ["bh_gaoshun"],
      "text": ["冰天雪地里，并州狼骑的冲锋撕开了外围防线。"]
    },
    "bh_gaoshun": {
      "x": 14, "y": 1, "type": "battle", "label": "陷阵营", "elite": True, "battle": "gaoshun_camp", "next": ["bh_lubu_face"],
      "text": ["紧接着，高顺的陷阵营一步一步压上山口。他们一声不吭，盾墙连成一片，比喊得响的可怕多了。"]
    },
    "bh_lubu_face": {
      "x": 15, "y": 1, "type": "event", "label": "故人相见", "next": ["bh_lubu"],
      "text": ["吕布亲自杀到，赤兔马在山口一停，盯着你的脸看了半天：「……你？江东那个短毛？头发怎么长出来了？」", "{lord}一头雾水：「什么江东？我河北的！」", "他又看见了你身后的吕玲绮，脸色一下子铁青：「逃了婚，还钻进土匪窝里当贼？我吕奉先的脸，都让你丢尽了！」", "画戟一抬，指的不是你，是她：「今天我亲手清理门户。」"]
    },
    "bh_lubu": {
      "x": 16, "y": 1, "type": "battle", "label": "暴怒吕布", "boss": True, "battle": "bh_lubu", "lose_goto": "bh_lubu_check", "next": ["bh_lubu_check"],
      "text": ["吕布狂怒之下，攻势如同排山倒海！这一战根本打不赢，只能边打边退！"]
    },
    "bh_lubu_check": {
      "x": 17, "y": 1, "type": "choose", "label": "阵线崩溃",
      "text": ["太行山口的防线即将被吕布彻底击穿！"],
      "choose": [
        {"label": "（郑姜：和好）金蝉脱壳", "requires": "郑姜：和好", "goto": "bh_escape"},
        {"label": "（郑姜：内讧）防线溃散", "unless": "郑姜：和好", "goto": "bh_bad_end"}
      ]
    },
    "bh_bad_end": {
      "x": 18, "y": 2, "type": "event", "cg": "end_juefa", "label": "结局七", "next": [], "ending": "结局七 · 绝罚",
      "text": ["因为郑姜两家各守各的山头，互不支援，防线一冲就散。吕玲绮挡在你身前，倒在父亲的戟下。", "你抱着她战死在山口，斑马军就此散了。"]
    },
    "bh_escape": {
      "x": 18, "y": 1, "type": "event", "cg": "c4_escape", "label": "金蝉脱壳", "next": ["bh_flee"],
      "text": ["郑姜两寨亲如一家，机关与刀阵配合得天衣无缝，硬生生拖住了陷阵营的脚步！", "{lord}：「太行守不住了，往东撤！过黄河去青州！」"]
    },
    "bh_flee": {
      "x": 19, "y": 1, "type": "event", "label": "千里突围", "next": ["bh_m5", "bh_m6"],
      "text": ["斑马军放弃了太行基业，顶着暴风雪一路向东，千里突围直奔黄河渡口。"]
    },
    "bh_m5": {"x": 20, "y": 1, "type": "mystery", "next": ["bh_river"]},
    "bh_m6": {"x": 20, "y": 2, "type": "treasure", "next": ["bh_river"]},
    "bh_river": {
      "x": 21, "y": 1, "type": "battle", "label": "冀州追兵", "battle": "hs_jizhou_cavalry", "next": ["bh_cross"],
      "text": ["眼看就要到黄河边，袁绍的冀州骑兵还是咬了上来。"]
    },
    "bh_cross": {
      "x": 22, "y": 1, "type": "recover", "label": "渡河", "next": ["bh_beihai_start"],
      "text": ["打退追兵，全军登船渡过黄河，终于把袁绍的大军甩在了对岸。青州，到了。"]
    },
    "bh_beihai_start": {
      "x": 23, "y": 1, "type": "event", "label": "北海之围", "next": ["bh_m7", "bh_m8"],
      "text": ["一进青州，就听说黄巾军的大首领管亥正率领几万大军围攻北海相孔融。"]
    },
    "bh_m7": {"x": 24, "y": 1, "type": "mystery", "next": ["bh_hj_out"]},
    "bh_m8": {"x": 24, "y": 2, "type": "treasure", "next": ["bh_hj_out"]},
    "bh_hj_out": {
      "x": 25, "y": 1, "type": "battle", "label": "黄巾饥兵", "battle": "huangjin_remnant", "next": ["bh_taishici_meet"],
      "text": ["北海城外，遍地都是黄巾军的营帐。外围全是骨瘦如柴的饥兵。"]
    },
    "bh_taishici_meet": {
      "x": 26, "y": 1, "type": "event", "cg": "c4_taishici", "label": "太史慈", "next": ["bh_hj_gate"],
      "text": ["乱军之中，一员年轻骁将提枪连挑数人，正往城里冲。", "{lord}：「好汉子！来搭把手，一起杀进去！」", "太史慈大笑：「正愁没人破阵！」（太史慈入队）"]
    },
    "bh_hj_gate": {
      "x": 27, "y": 1, "type": "battle", "label": "狂信徒", "battle": "huangjin_fanatic", "next": ["bh_rest2"],
      "text": ["城门下，一群头裹黄巾的狂信徒死死堵住退路，悍不畏死。"]
    },
    "bh_rest2": {"x": 28, "y": 1, "type": "recover", "label": "城门休整", "next": ["bh_guanhai_pre"]},
    "bh_guanhai_pre": {
      "x": 29, "y": 1, "type": "event", "label": "管亥搦战", "next": ["bh_guanhai"],
      "text": ["城下黄巾大阵裂开，大首领管亥倒拖长刀而出，威风凛凛。"]
    },
    "bh_guanhai": {
      "x": 30, "y": 1, "type": "battle", "label": "管亥", "boss": True, "battle": "bh_guanhai", "record_win": "北海：斩管亥", "next": ["bh_kongrong"],
      "text": ["管亥势大力沉，太史慈与赵云双枪并举，迎战贼首！"]
    },
    "bh_kongrong": {
      "x": 31, "y": 1, "type": "event", "cg": "c4_kongrong", "label": "让北海", "next": ["bh_seal"],
      "text": ["北海解围，孔融将你请进郡府。他捋着胡子，把北海相的印推了过来：「老夫要去洛阳朝廷述职。北海的百姓认你，这印，让给你。」", "{lord}（内心）：孔融！这个我知道——孔融让梨！课本上的！……让梨让到让北海，这位是真的会让。"]
    },
    "bh_seal": {
      "x": 32, "y": 1, "type": "event", "label": "朝廷使节", "next": ["bh_seal_cross", "bh_seal_normal"],
      "text": ["孔融上表朝廷，力荐你为北海相。没过多久，洛阳的使节就带着诏书到了。"]
    },
    "bh_seal_cross": {
      "x": 33, "y": 1, "type": "event", "requires": "南阳：袁术东逃", "next": ["bh_end"],
      "text": ["传诏的宦官宣完旨，抬起头盯着你看了半天：「……将军前些日子不是还在南阳打袁术吗？头发怎么长出来了？」", "{lord}干笑：「水土好，长得快。」"]
    },
    "bh_seal_normal": {
      "x": 33, "y": 2, "type": "event", "unless": "南阳：袁术东逃", "next": ["bh_end"],
      "text": ["传诏的宦官宣读了任命你为北海相的诏书。"]
    },
    "bh_end": {
      "x": 34, "y": 1, "type": "event", "label": "北海相", "record": "北线：北海相", "next": [],
      "text": ["有了北海做根基，斑马军终于在青州真正立足。青州的黄巾遗兵，也尽数编入了屯田营。", "（获得兵卡：北海屯田兵）"]
    }
  }
}

with open(r'F:\workspace\sanguo-cards\godot\data\story.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# Replace if exists, else append
found = False
for i, q in enumerate(d['quests']):
    if q['id'] == 'beihai':
        d['quests'][i] = new_quest
        found = True
        break
if not found:
    # insert before ch4 dongui if we want to keep order, or just append
    d['quests'].append(new_quest)

# Wait, I cannot use json.dump directly because it breaks story.json formatting!
# I will use a custom formatter for just this quest.
