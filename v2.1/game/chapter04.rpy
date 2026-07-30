# ================================================================
# 第四章：建德梅城——一城皆为讲舍
# 正式剧本编号：ZJU-1937-04
# ================================================================

define zhou = Character("周顺安", color="#c7ad79")
define householder = Character("房主", color="#bda98a")
define administrator = Character("行政人员", color="#c3baa5")

default ch4_task_progress = {}
default ch4_current_place = ""
default ch4_location_tasks = []
default ch4_lamp_choice = ""
default ch4_literacy_choice = ""

init python:
    CH4_LOCATION_META = {
        "dock": (
            "梅城码头外",
            "1937年11月中旬 · 黄昏",
            "ch4 dock",
            "理解梅城没有统一校园边界",
            [
                ("dock_manifest", "核对到埠名册", 160, 300, 350, 350),
                ("dock_route", "询问入城路线", 600, 370, 370, 300),
                ("dock_crates", "疏通木箱通道", 1040, 270, 390, 370),
            ],
        ),
        "kongmiao": (
            "孔庙临时课堂",
            "1937年11月中旬 · 次日清晨",
            "ch4 kongmiao",
            "送达讲义并让第一堂课准时开始",
            [
                ("kong_sign", "修正时间木牌", 160, 290, 350, 360),
                ("kong_lectures", "追回错送讲义", 600, 365, 370, 300),
                ("kong_seats", "借凳重排座位", 1040, 260, 390, 380),
            ],
        ),
        "minju": (
            "东门街民居",
            "1937年11月中旬 · 傍晚",
            "ch4 minju",
            "与居民共同制定借屋规则",
            [
                ("home_furniture", "确认家具边界", 160, 300, 350, 350),
                ("home_water", "约定用水时段", 600, 370, 370, 300),
                ("home_rules", "写下安静与防火规则", 1040, 270, 390, 370),
            ],
        ),
        "linchang": (
            "林场办公与自习点",
            "1937年11月中旬 · 午后",
            "ch4 linchang",
            "处理四件同时紧急的校务",
            [
                ("forest_water", "协调饮水", 160, 300, 350, 350),
                ("forest_leak", "遮住漏雨处", 600, 370, 370, 300),
                ("forest_lamp", "分配最后灯油", 1040, 270, 390, 370),
            ],
        ),
        "pawnshop": (
            "东城当铺宿舍",
            "1937年11月中旬 · 入夜前",
            "ch4 pawnshop",
            "让宿舍、物资与疏散通道同时可用",
            [
                ("pawn_beds", "安排草席铺位", 160, 300, 350, 350),
                ("pawn_storage", "划分物资区", 600, 370, 370, 300),
                ("pawn_passage", "保留中央通道", 1040, 270, 390, 370),
            ],
        ),
        "office": (
            "方宅校务办公处",
            "1937年11月中下旬 · 深夜",
            "ch4 office",
            "把分散房屋接入同一张课表",
            [
                ("office_lodging", "核实今晚可住", 160, 300, 350, 350),
                ("office_schedule", "发布第四版课表", 600, 370, 370, 300),
                ("office_report", "向孙宅准确汇报", 1040, 270, 390, 370),
            ],
        ),
    }


label chapter_4:
    $ ch4_places = []
    $ ch4_task_progress = {}
    $ ch4_lamp_choice = ""
    $ ch4_literacy_choice = ""
    $ immersive_items = ["梅城校舍简图", "房屋登记册"]
    $ immersive_archive_count = 3
    $ ch4_return_to_world_map = False
    call screen chapter_title_card(
        "images/chapter04/meicheng_campus.png",
        "第四章",
        "建德梅城",
        "一城皆为讲舍",
        "1937年11月中旬至12月下旬"
    )
    scene bg ch4
    show screen immersive_hud
    narrator_day1 "梅城不是一片等待学校改造的空地。这里已有居民、店铺、庙宇、街巷和自己的生活秩序。"
    gu "二年级住东城当铺。天目山来的一年级，先去严州中学第二部登记。"
    sy "教室、宿舍、办公厅全不在一处。浙江大学究竟在何处？"
    zhou "此处不是，前街也不是。可这些日子，城里处处都是你们的人。"
    menu:
        "我怎样进入梅城？"
        "请周顺安带路，并教他认课表":
            $ ch4_literacy_choice = "课表识字"
            $ day1_trust += 1
        "按校舍图寻找登记处":
            $ ch4_literacy_choice = "自绘街巷"
            $ day1_records += 1
        "留下协助卸书箱":
            $ ch4_literacy_choice = "码头协作"
            $ day1_trust += 1
    jump chapter_4_hub


label chapter_4_hub:
    hide screen immersive_character
    $ immersive_chapter = "第四章  建德梅城"
    $ immersive_date = "1937年11月至12月 · 梅城"
    $ immersive_objective = "让六处分散地点依同一张课表运转"
    $ immersive_tasks = [
        ("接收梅城码头物资", "dock" in ch4_places),
        ("布置孔庙课堂", "kongmiao" in ch4_places),
        ("协商民居宿舍", "minju" in ch4_places),
        ("建立林场办公点", "linchang" in ch4_places),
        ("整理当铺住宿区", "pawnshop" in ch4_places),
        ("接通校务办公处", "office" in ch4_places),
    ]
    $ immersive_secondary = ["不扰乱居民原有生活", "课程迁移期间不停"]
    $ ch4_unlocked = ["dock"]
    if "dock" in ch4_places:
        $ ch4_unlocked += ["kongmiao", "minju"]
    if "kongmiao" in ch4_places and "minju" in ch4_places:
        $ ch4_unlocked += ["linchang", "pawnshop"]
    if "linchang" in ch4_places and "pawnshop" in ch4_places:
        $ ch4_unlocked += ["office"]
    if len(ch4_places) >= 6:
        jump chapter_4_morning_check
    show screen immersive_hud
    call screen historical_location_map(
        "bg ch4",
        "建德梅城  分散的临时校园",
        [
            ("kongmiao", "孔庙", 100, 210, 420, 300),
            ("minju", "民居", 530, 420, 300, 270),
            ("linchang", "林场", 650, 100, 350, 270),
            ("pawnshop", "当铺", 920, 430, 300, 270),
            ("office", "校务办公处", 1110, 120, 350, 270),
            ("dock", "梅城码头", 1280, 430, 280, 300),
        ],
        ch4_places,
        ch4_unlocked,
    )
    $ ch4_map_choice = _return
    if ch4_map_choice == "dock":
        jump chapter_4_dock
    elif ch4_map_choice == "kongmiao":
        jump chapter_4_kongmiao
    elif ch4_map_choice == "minju":
        jump chapter_4_minju
    elif ch4_map_choice == "linchang":
        jump chapter_4_linchang
    elif ch4_map_choice == "pawnshop":
        jump chapter_4_pawnshop
    elif ch4_map_choice == "office":
        jump chapter_4_office
    jump chapter_4_hub


label ch4_run_location(place):
    $ ch4_current_place = place
    $ ch4_meta = CH4_LOCATION_META[place]
    $ ch4_location_tasks = list(ch4_task_progress.get(place, []))
    $ immersive_chapter = "第四章  建德梅城"
    $ immersive_date = ch4_meta[1]
    $ immersive_objective = ch4_meta[3]
    $ immersive_tasks = [(task[1], task[0] in ch4_location_tasks) for task in ch4_meta[4]]
    $ immersive_secondary = ["借用不等于占有", "完成后恢复原状"]
    show screen immersive_hud

label ch4_location_loop:
    $ ch4_meta = CH4_LOCATION_META[ch4_current_place]
    scene expression ch4_meta[2]
    hide screen immersive_character
    call screen chapter_task_scene(
        ch4_meta[2],
        ch4_meta[0],
        "地点完成后会解锁下一批校舍",
        ch4_meta[4],
        ch4_location_tasks,
    )
    $ ch4_selected = _return
    if ch4_selected == "continue":
        if ch4_current_place not in ch4_places:
            $ ch4_places.append(ch4_current_place)
        $ ch4_task_progress[ch4_current_place] = list(ch4_location_tasks)
        return
    call expression "ch4_task_" + ch4_selected from _call_expression_2
    if ch4_selected not in ch4_location_tasks:
        $ ch4_location_tasks.append(ch4_selected)
    $ ch4_task_progress[ch4_current_place] = list(ch4_location_tasks)
    jump ch4_location_loop


label chapter_4_dock:
    call ch4_run_location("dock") from _call_ch4_run_location
    jump chapter_4_location_return

label chapter_4_kongmiao:
    call ch4_run_location("kongmiao") from _call_ch4_run_location_1
    jump chapter_4_location_return

label chapter_4_minju:
    call ch4_run_location("minju") from _call_ch4_run_location_2
    jump chapter_4_location_return

label chapter_4_linchang:
    call ch4_run_location("linchang") from _call_ch4_run_location_3
    jump chapter_4_location_return

label chapter_4_pawnshop:
    call ch4_run_location("pawnshop") from _call_ch4_run_location_4
    jump chapter_4_location_return

label chapter_4_office:
    call ch4_run_location("office") from _call_ch4_run_location_5
    jump chapter_4_location_return


label ch4_task_dock_manifest:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    gu "一年级先登记住处。写清楚今晚可住，还是明早可住。"
    sy "一个‘正在整理’，不能给人当床铺。"
    hide screen immersive_character
    return

label ch4_task_dock_route:
    $ immersive_pose = "calm"
    show screen immersive_character
    zhou "城里没有一扇门能通向所有教室。先记街，再认木牌。"
    sy "那便从今日最用得上的字认起：上午八时，临时教室。"
    hide screen immersive_character
    return

label ch4_task_dock_crates:
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "师生把图书、仪器与铺盖分开，先清出人员通道。"
    sy "不能让一只箱子堵住一堂课，也不能堵住一条回家的路。"
    hide screen immersive_character
    return

label ch4_task_kong_sign:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    zhou "我只是不认得那几个字。若真按我指的路走错，岂不是更耽误？"
    sy "木牌改成：上午八时，孔庙临时教室。一个字也不能含糊。"
    hide screen immersive_character
    return

label ch4_task_kong_lectures:
    $ immersive_pose = "determined"
    show screen immersive_character
    gu "我去追回错送讲义。许南枝核下一堂地点，你补座位。半个时辰后报结果。"
    narrator_day1 "讲义在开课前送回，课表上的地点也被重新核过。"
    hide screen immersive_character
    return

label ch4_task_kong_seats:
    $ immersive_pose = "calm"
    show screen immersive_character
    xu "祭器、匾额和居民平日使用之处不能随意搬。只使用两侧，长凳排紧一些。"
    sy "课堂建立了，借用空间原有的秩序也要保留。"
    $ day1_trust += 1
    hide screen immersive_character
    return

label ch4_task_home_furniture:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    householder "家具不能乱搬。房屋只是暂借，不是赠予。"
    xu "移动前记录位置，离开前恢复原状。我们写进借屋约定。"
    hide screen immersive_character
    return

label ch4_task_home_water:
    $ immersive_pose = "calm"
    show screen immersive_character
    householder "用水不能挤了老人和孩子。"
    sy "学生分时取水，早晚各留一段给原住户。"
    $ day1_trust += 1
    hide screen immersive_character
    return

label ch4_task_home_rules:
    $ immersive_pose = "determined"
    show screen immersive_character
    xu "清扫轮值、用水时段、夜间安静、禁止明火，离开前恢复原状。"
    householder "既住了读书人，便算半间讲舍。莫使它失了体面。"
    hide screen immersive_character
    return

label ch4_task_forest_water:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    administrator "宿舍灯油不足，饮水点太远，屋顶漏水，码头通道被木箱堵住。都急。"
    sy "先把饮水时段与附近住户协调清楚，避免所有人同时拥到井边。"
    hide screen immersive_character
    return

label ch4_task_forest_leak:
    $ immersive_pose = "determined"
    show screen immersive_character
    gu "先用油布遮漏，再把课桌移开。彻底修屋顶来不及，但下午课不能中断。"
    hide screen immersive_character
    return

label ch4_task_forest_lamp:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    menu:
        "最后一桶灯油应该怎样分配？"
        "留给方宅校务登记":
            $ ch4_lamp_choice = "方宅"
            $ day1_records += 2
        "留给学生晚间自习":
            $ ch4_lamp_choice = "学生"
            $ day1_morale += 2
        "两处分半夜，并亲自往返补救":
            $ ch4_lamp_choice = "分半夜"
            $ day1_trust += 1
    xu "没有绝对无损的选择。被推迟的工作，明日要由我们亲手补上。"
    hide screen immersive_character
    return

label ch4_task_pawn_beds:
    $ immersive_pose = "calm"
    show screen immersive_character
    narrator_day1 "草席沿墙铺开，二年级学生的行李按名册排列。"
    sy "铺位不只要够数，也要让夜间点名能找到每个人。"
    hide screen immersive_character
    return

label ch4_task_pawn_storage:
    $ immersive_pose = "determined"
    show screen immersive_character
    gu "柜台后存物资，外间住学生。寝铺与清点路线分开。"
    hide screen immersive_character
    return

label ch4_task_pawn_passage:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    zhou "中间留得这么宽，会少铺好几个人。"
    sy "拥挤免不了，但不能让拥挤成为警报时的危险。"
    hide screen immersive_character
    return

label ch4_task_office_lodging:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    administrator "尚有数人没有正式铺位，今晚暂住教室；两人发热，已送医查看。"
    sy "把暂住、正式入住和送医分开写，不能用‘均已安顿’掩过去。"
    hide screen immersive_character
    return

label ch4_task_office_schedule:
    $ immersive_pose = "determined"
    show screen immersive_character
    xu "这是第四版课表。地点、时刻、教师、讲义送达情况都已重核。"
    sy "一张课表若写得含糊，整座城都要替它付出脚程。"
    $ day1_records += 1
    hide screen immersive_character
    return

label ch4_task_office_report:
    $ immersive_pose = "calm"
    show screen immersive_character
    zc "学校不能只问学生白日读什么，也要问他们夜里睡在何处。"
    sy "房屋是散的，真的还能算一所大学吗？"
    zc "房屋是散的，课表不能散。少接上一处，明日便有人无课可上。"
    hide screen immersive_character
    return


label chapter_4_location_return:
    if len(ch4_places) >= 6:
        jump chapter_4_morning_check
    if ch4_return_to_world_map:
        $ ch4_return_to_world_map = False
        jump day1_map_hub
    jump chapter_4_hub


label chapter_4_morning_check:
    scene bg ch4
    show screen immersive_hud
    narrator_day1 "数日后清晨，我们沿课表完成四节点核验。"
    narrator_day1 "07:40，孔庙：教师、黑板与讲义齐备。07:50，东门街：学生按正确木牌出发。"
    narrator_day1 "08:00，严州中学第二部完成点名。08:10，方宅收到缺席与延误报告，最后断点被补上。"
    zhou "上午八时，临时教室。我一个字也没认错吧？"
    sy "一个字也没错。"
    xu "不是‘总算’。是每个人把自己那一段接上了。"
    sy "我曾以为大学必有一道校门。到了梅城才明白，它有时是许多人共同遵守的一张课表。"
    jump chapter_4_finish


label chapter_4_finish:
    narrator_day1 "十二月中下旬，课表背面开始出现新的地名。"
    xu "这张表才用了几日。"
    gu "那便让它用到最后一日。教室照常开，船也照常装。"
    narrator_day1 "白日维持课程，夜间清点图书仪器；借屋钥匙被归还，家具、房间与通道恢复原状。"
    zhou "你们才把路认熟，为什么又要走？"
    sy "因为路还没有走完。但在走之前，今日的课仍要准时开始。"
    $ day1_finish_chapter(4)
    hide screen immersive_hud
    centered "{size=46}第四章完成{/size}\n\n第五章　“黑板挂在我的胸前”已解锁"
    jump day1_map_hub
