# ================================================================
# 《文军长征：建德四十五日》终章
# FINAL_CHAPTER_SCRIPT_AND_ART_TASKBOOK 实施版
# 固定流程：点名→地点回望→离开梅城→竺可桢二问→玩家回答
#          →人物告别→吉安泰和预告→统计→终章菜单
# ================================================================

default finale_profile = {}
default final_answer = ""
default finale_answer = ""
default ending_route = ""
default ending_title = ""
default finale_gallery_index = 0
default finale_route_step = 0


# 竖幅预告图以等比“铺满”方式用于横屏，不拉伸人物。
transform finale_poster_landscape:
    xysize (1920, 1080)
    fit "cover"
    xalign 0.5
    yalign 0.82

init python:
    def finale_number(name, default=0):
        try:
            return float(getattr(store, name, default))
        except (TypeError, ValueError):
            return float(default)

    def finale_collection(name):
        value = getattr(store, name, [])
        if value is None:
            return []
        try:
            return list(value)
        except TypeError:
            return []

    def finale_mapping(name):
        value = getattr(store, name, {})
        if isinstance(value, dict):
            return dict(value)
        return {}

    def finale_relation_average(relationships):
        values = []
        for key in ("xu_nanzhi", "gu_mingchuan", "zhou_shunan"):
            try:
                values.append(float(relationships.get(key, 0)))
            except (TypeError, ValueError):
                values.append(0.0)
        return sum(values) / float(len(values)) if values else 0.0

    def finale_club_stage_count(club_ranks):
        return sum(1 for value in club_ranks.values() if int(value or 0) >= 3)

    def build_finale_profile():
        relationships = finale_mapping("relationship")
        clubs = finale_mapping("club_xp")
        club_ranks = finale_mapping("club_rank")
        archive = set(finale_collection("archive_items"))
        archive.update(finale_collection("mc45_archive"))
        keepsakes = set(finale_collection("mc45_items"))
        exams = finale_collection("exam_history")
        completed_tasks = finale_collection("completed_campus_requests")

        knowledge = max(finale_number("stat_knowledge", 0), finale_number("mc45_knowledge", 0))
        practice = max(finale_number("stat_practical", 0), finale_number("mc45_practice", 0))
        morality = max(finale_number("stat_morality", 0), finale_number("virtue_service", 0))
        reputation = max(finale_number("stat_reputation", 0), finale_number("mc45_reputation", 0))
        will = max(finale_number("stat_will", 0), finale_number("mc45_will", 0))
        truth = max(finale_number("virtue_truth", 0), finale_number("mc45_truth", 0))
        campus_order = max(
            finale_number("campus_score", 0),
            finale_number("world_dorm_order", 0),
            finale_number("mc45_school_order", 0) * 10.0,
        )
        resident_trust = max(
            finale_number("world_resident_trust", 0),
            finale_number("mc45_resident_trust", 0) * 10.0,
        )
        newspaper_credibility = max(
            finale_number("newspaper_accuracy", 0),
            finale_number("world_public_confidence", 0),
            finale_number("mc45_information_credit", 0) * 10.0,
        )
        relation_average = finale_relation_average(relationships)
        academic_progress = float(clubs.get("academic", 0) or 0)
        repair_progress = float(clubs.get("repair", 0) or 0)
        mutual_aid_progress = float(clubs.get("mutual_aid", clubs.get("work_study", 0)) or 0)

        scores = {
            "scholar": knowledge * 3.0 + finale_number("cumulative_gpa", 0) * 10.0 + truth * 4.0 + academic_progress * 0.20,
            "practitioner": practice * 3.0 + campus_order * 0.35 + repair_progress * 0.20 + len(completed_tasks) * 2.0,
            "guardian": morality * 2.5 + truth * 5.0 + len(archive) * 3.0 + newspaper_credibility * 0.25,
            "companion": reputation * 3.0 + relation_average * 0.45 + mutual_aid_progress * 0.20 + resident_trust * 0.25,
        }
        if store.final_answer in scores:
            scores[store.final_answer] += 12.0

        best_key = max(scores, key=scores.get)
        best_titles = {
            "scholar": "求学之灯",
            "practitioner": "落手之处",
            "guardian": "纸上长路",
            "companion": "同舟的人",
        }
        gpa = finale_number("cumulative_gpa", 0)
        best_condition = (
            gpa >= 4.2
            and knowledge >= 17
            and morality >= 17
            and truth >= 8
            and campus_order >= 75
            and relation_average >= 65
            and len(keepsakes) >= 8
            and finale_club_stage_count(club_ranks) >= 2
        )
        title = "弦歌不绝" if best_condition else best_titles.get(best_key, "来日再答")
        if sum(scores.values()) <= 0:
            title = "来日再答"

        return {
            "days": 45,
            "actions": int(finale_number("action_count", len(finale_collection("daily_action_log")))),
            "journals": len(finale_collection("journal_entries")) + len(finale_collection("mc45_journal")),
            "exam_count": len(exams),
            "gpa": gpa,
            "knowledge": int(knowledge),
            "morality": int(morality),
            "practice": int(practice),
            "reputation": int(reputation),
            "will": int(will),
            "truth": int(truth),
            "campus_order": int(campus_order),
            "resident_trust": int(resident_trust),
            "newspaper_credibility": int(newspaper_credibility),
            "relationships": relationships,
            "relation_average": relation_average,
            "clubs": clubs,
            "club_ranks": club_ranks,
            "archive": sorted(archive),
            "keepsakes": sorted(keepsakes),
            "archive_count": len(archive),
            "item_count": len(keepsakes),
            "cg_count": 26,
            "event_count": len(finale_collection("seen_events")) + len(finale_collection("mc45_event_history")),
            "scores": scores,
            "route": best_key,
            "title": title,
        }

    def finale_persist_completion(profile):
        persistent.jiande_completed = True
        persistent.jian_taihe_teaser_unlocked = True
        old_gpa = float(getattr(persistent, "best_jiande_gpa", 0.0) or 0.0)
        persistent.best_jiande_gpa = max(old_gpa, float(profile.get("gpa", 0.0)))
        if getattr(persistent, "final_answer_history", None) is None:
            persistent.final_answer_history = set()
        if getattr(persistent, "ending_routes_unlocked", None) is None:
            persistent.ending_routes_unlocked = set()
        persistent.final_answer_history.add(store.final_answer)
        persistent.ending_routes_unlocked.add(profile.get("route", ""))
        renpy.save_persistent()

    FINALE_GALLERY = [
        ("最后一次点名", "images/finale/roll_call/cg_finale_roll_call_wide.webp"),
        ("蓝布笔记本", "images/finale/roll_call/cg_finale_blue_notebook.webp"),
        ("孔庙回望", "images/finale/retrospective/cg_retrospect_confucian_temple.webp"),
        ("临时教室回望", "images/finale/retrospective/cg_retrospect_classroom.webp"),
        ("林场回望", "images/finale/retrospective/cg_retrospect_forestry.webp"),
        ("校务办公处回望", "images/finale/retrospective/cg_retrospect_office.webp"),
        ("民居回望", "images/finale/retrospective/cg_retrospect_residences.webp"),
        ("当铺回望", "images/finale/retrospective/cg_retrospect_pawnshop.webp"),
        ("梅城码头回望", "images/finale/retrospective/cg_retrospect_port.webp"),
        ("黎明离城", "images/finale/departure/cg_departure_port_wide.webp"),
        ("竺可桢二问", "images/finale/questions/cg_zhu_two_questions.webp"),
        ("船离梅城", "images/finale/departure/cg_boat_leaves_meicheng.webp"),
    ]


screen finale_roll_call_continue():
    modal True
    textbutton "合上笔记本，走出宿舍":
        xalign 0.5
        yalign 0.88
        xsize 520
        ysize 72
        text_size 25
        text_color "#ead9aa"
        text_hover_color "#fff1c7"
        background Solid("#151b18e8")
        hover_background Solid("#493b25f2")
        action Jump("finale_map_retrospective")


screen finale_route_progress(step):
    zorder 20
    text "浙大西迁：文军长征":
        xpos 72
        ypos 54
        font CHAPTER_XINGKAI_FONT
        size 58
        color "#4e3d21"
        outlines [(2, "#ead9aa99", 0, 0)]

    $ nodes = [
        ("建德", 1510, 340),
        ("金华", 1190, 440),
        ("玉山", 900, 535),
        ("樟树", 550, 565),
        ("吉安", 210, 650),
    ]
    for index, data in enumerate(nodes):
        $ active = index < step
        add Solid("#d9b85c" if active else "#544b3a"):
            xpos data[1]
            ypos data[2]
            xsize 20
            ysize 20
        text data[0]:
            xpos data[1] - 24
            ypos data[2] + 28
            size 25
            color ("#f2d47e" if active else "#726a5a")
            outlines [(2, "#17140e", 0, 0)]


screen finale_statistics_page(profile, page):
    modal True
    add "images/finale/statistics/bg_ending_statistics.webp":
        xysize (1920, 1080)
    frame:
        xpos 760
        ypos 90
        xsize 1080
        ysize 890
        padding (68, 58)
        background Solid("#0b1210e8")
        vbox:
            spacing 20
            text "建德四十五日 · 行旅总录" size 42 color "#e1c478"
            add Solid("#8f7848") xsize 930 ysize 2
            if page == 1:
                text "一　概览" size 29 color "#cbb987"
                text "建德生活：45 天" size 25 color "#e5dfcf"
                text "主动行动：[profile['actions']] 次" size 25 color "#e5dfcf"
                text "深夜札记：[profile['journals']] 次" size 25 color "#e5dfcf"
                text "正式周考：6 次" size 25 color "#e5dfcf"
                text "累计 GPA：{:.2f}".format(profile["gpa"]) size 25 color "#f0d98d"
            elif page == 2:
                text "二　属性" size 29 color "#cbb987"
                text "学识 [profile['knowledge']]　学行 [profile['morality']]　实务 [profile['practice']]" size 25 color "#e5dfcf"
                text "人望 [profile['reputation']]　心志 [profile['will']]　求实 [profile['truth']]" size 25 color "#e5dfcf"
                text "校园秩序 [profile['campus_order']]" size 25 color "#f0d98d"
            elif page == 3:
                $ finale_relationships = profile.get("relationships", {})
                $ finale_clubs = profile.get("clubs", {})
                text "三　人物与社团" size 29 color "#cbb987"
                text "许南枝关系：[finale_relationships.get('xu_nanzhi', 0)]" size 24 color "#e5dfcf"
                text "顾明川关系：[finale_relationships.get('gu_mingchuan', 0)]" size 24 color "#e5dfcf"
                text "周顺安关系：[finale_relationships.get('zhou_shunan', 0)]" size 24 color "#e5dfcf"
                null height 8
                text "四社团进度" size 25 color "#cbb987"
                text "学术研讨　[finale_clubs.get('academic', 0)]　　勤工互助　[finale_clubs.get('work_study', 0)]" size 22 color "#d4cdbd"
                text "修缮实务　[finale_clubs.get('repair', 0)]　　校报编辑　[finale_clubs.get('news', 0)]" size 22 color "#d4cdbd"
                text "报纸可信度：[profile['newspaper_credibility']]" size 24 color "#f0d98d"
            elif page == 4:
                text "四　档案" size 29 color "#cbb987"
                text "旧物数量：[profile['item_count']]" size 25 color "#e5dfcf"
                text "终章 CG：26 / 26" size 25 color "#e5dfcf"
                text "关键事件记录：[profile['event_count']]" size 25 color "#e5dfcf"
                text "最终回答：[finale_answer]" size 23 color "#f0d98d" xmaximum 900
            else:
                text "五　结语" size 29 color "#cbb987"
                text "[profile['title']]" size 48 color "#f0d98d"
                if profile["title"] == "来日再答":
                    text "你没有在四十五天里找到一个足以概括未来的答案。可竺可桢在问题之后留下的，本来就不是一张必须当场交回的试卷。蓝布笔记本仍有空页，下一站也仍有新的课程。你将带着尚未完成的回答继续前行。" size 25 color "#e5dfcf" xmaximum 900
                else:
                    text "四十五天没有替你决定一生，却让你的回答有了可以查证的来处。那些课程、木箱、报纸、约定与同行的人，将继续在下一段路上检验它。" size 25 color "#e5dfcf" xmaximum 900
            null height 16
            textbutton ("进入终章菜单" if page == 5 else "继续"):
                xalign 1.0
                xsize 280
                ysize 60
                background Solid("#3b301fe8")
                hover_background Solid("#5a4628ee")
                text_color "#ead39a"
                text_hover_color "#fff3cb"
                action Return()


screen finale_menu_screen():
    modal True
    add "images/finale/menu/bg_finale_menu.webp":
        xysize (1920, 1080)
    frame:
        xpos 70
        ypos 55
        xsize 680
        ysize 970
        padding (52, 38)
        background Solid("#07100dcc")
        vbox:
            spacing 10
            text "建德篇 · 完" size 48 color "#e6ca7e"
            text "[ending_title]" size 28 color "#cabd9b"
            add Solid("#8c7344") xsize 570 ysize 2
            for title, value in [
                ("重看终章", "replay"),
                ("查看人物告别", "farewell"),
                ("查看结局统计", "statistics"),
                ("查看旧物档案", "archive"),
                ("查看终章画廊", "gallery"),
                ("查看《吉安—泰和篇》海报", "poster"),
                ("保存通关档案", "save"),
                ("返回标题界面", "title"),
                ("重新开始建德篇", "restart"),
                ("退出游戏", "quit"),
            ]:
                textbutton title:
                    xsize 570
                    ysize 70
                    background Solid("#151b18b8")
                    hover_background Solid("#584526e8")
                    text_color "#ddd4bd"
                    text_hover_color "#ffe5a0"
                    action Return(value)


screen finale_quit_confirm():
    modal True
    add Solid("#030504b8")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        ysize 330
        padding (55, 45)
        background Solid("#101713f5")
        vbox:
            spacing 28
            text "确认退出游戏？" size 38 color "#e6ca7e" xalign 0.5
            text "通关记录已经写入；未手动保存的临时进度仍可能丢失。" size 23 color "#d9d1bf" xalign 0.5
            hbox:
                xalign 0.5
                spacing 34
                textbutton "返回终章菜单" action Return(False)
                textbutton "确认退出" action Return(True)


screen finale_list_card(card_title, entries):
    modal True
    add "images/finale/statistics/bg_ending_statistics.webp":
        xysize (1920, 1080)
    frame:
        xalign 0.70
        yalign 0.50
        xsize 1050
        ysize 850
        padding (60, 46)
        background Solid("#0b1210ee")
        vbox:
            spacing 18
            text card_title size 42 color "#e1c478"
            viewport:
                xsize 900
                ysize 620
                mousewheel True
                scrollbars "vertical"
                vbox:
                    spacing 12
                    if entries:
                        for entry in entries:
                            text "· [entry]" size 23 color "#ded7c6" xmaximum 850
                    else:
                        text "尚未收录。" size 23 color "#9f998d"
            textbutton "返回" xalign 1.0 action Return()


screen finale_gallery_screen(index):
    modal True
    $ title, image_path = FINALE_GALLERY[index]
    add image_path:
        xysize (1920, 1080)
    frame:
        xalign 0.5
        ypos 35
        xsize 660
        ysize 78
        background Solid("#07100dcc")
        text "[title]　[index + 1] / [len(FINALE_GALLERY)]":
            xalign 0.5
            yalign 0.5
            size 27
            color "#ead39a"
    hbox:
        xalign 0.5
        yalign 0.94
        spacing 24
        textbutton "上一张" action Return("prev")
        textbutton "返回菜单" action Return("back")
        textbutton "下一张" action Return("next")


label jiande_finale_entry:
    jump finale_roll_call


label finale_roll_call:
    window hide
    hide screen immersive_hud
    hide screen immersive_character
    scene expression "images/finale/roll_call/cg_finale_roll_call_wide.webp"
    with fade
    "宿舍里的床比往常显得更宽。不是屋子忽然大了，而是靠墙几张草席已经卷起，床脚边只留下被行李压过的浅痕。先行离开的同学没有来得及逐一告别，他们把木盆、旧报纸和半截蜡烛留在桌上，像是明早还会回来。"
    "油灯的火苗压得很低。窗缝里的风将点名簿吹起一角，值日学生用手掌把它压住，抬头看向屋里。"
    "值日学生" "今晚不记迟到，也不记缺席。只是最后再念一遍。"
    "第一个名字响起。有人应“在”，声音清楚；第二个名字响起，回答有些急，像是刚从外头搬完行李；再往后，有些名字属于已经随先遣队出发的人，值日学生没有说“缺席”，只在页边停一停，便接着往下念。"
    "顾明川靠在门边，肩上还沾着仓房里的木屑。许南枝手里抱着一叠校样，最上面那一张仍留着红笔校改的痕迹。有人在窗边系紧布包，有人在灯下把鞋带重新打了一次结，好像只要把眼前这一件小事做好，就能让心定下来。"
    "终于念到沈砚舟的名字。"
    "沈砚舟" "在。"
    "这一声出口时，他忽然想起四十五天前的第一堂课、孔庙檐下的风、第一次周考时湿冷的桌面、码头上抬过的木箱、临时教室黑板边缘未擦净的粉笔灰。名字还是同一个名字，答应却已经不再只是证明自己住在这里。"
    scene expression "images/finale/roll_call/cg_finale_blue_notebook.webp"
    with dissolve
    "他翻开蓝布笔记本。前几页的字写得很急，后来渐渐整齐起来。书页之间夹着一段麻绳、一张课程表、一封没有寄出的家书，还有从《浙大日报》边角裁下来的日期。四十五天并没有写成一句完整的话，却一页一页地留在这里。"
    "值日学生念完最后一个名字，合上册子，轻轻说了一句：“都点到了。”"
    "没有人纠正他。那些已经走在路上的人，那些明晨将启程的人，那些仍守在码头的人，在这一晚都被算作“在”。"
    centered "{size=38}{color=#e8d29a}建德生活已经走到最后一夜。\n有些地方，还应该再看一眼。{/color}{/size}"
    call screen finale_roll_call_continue


label night_roll_call:
    jump finale_roll_call


label finale_map_retrospective:
    window hide
    scene expression "images/finale/retrospective/cg_retrospect_confucian_temple.webp"
    with fade
    $ renpy.pause(3.0, hard=True)
    "孔庙最初只是一处借来的屋檐。学生抱着书走进来时，没有人知道下一堂课会在哪里继续。后来雨落过庭院，粉笔字写满又擦去，争论声从廊下传到门外。桌椅并不整齐，课程也常被搬运和警报打断，可每一次重新坐下，都像是在回答同一个问题：一所大学究竟依靠什么存在。"
    if finale_number("stat_knowledge", 0) >= 14:
        "你记得自己曾在这里答错，也曾在夜里把错误重新算明白。"
    else:
        "你未必参加过每一次讨论，但仍记得窗外有人朗读时，整座院子都安静下来。"

    scene expression "images/finale/retrospective/cg_retrospect_classroom.webp"
    with dissolve
    $ renpy.pause(3.0, hard=True)
    "这里原本只是一块空地。木料从林场运来，桌椅从各处凑齐，黑板被一次次扶正，终于让课程有了可以固定落脚的地方。第一次周考时，窗外仍有人搬木箱；最后一次周考时，行李已经堆到门边。教室从来没有真正安稳过，却让每个走进来的人暂时相信，明天仍然可以照常上课。"
    if finale_number("classroom_warmth", 0) >= 55:
        "你修过的窗框合得很紧，寒风没有再把试卷吹落。"
    else:
        "窗边仍塞着旧布。它不算完善，却陪大家撑过了建德最后几堂课。"

    scene expression "images/finale/retrospective/cg_retrospect_forestry.webp"
    with dissolve
    $ renpy.pause(3.0, hard=True)
    "林场里的木料有了去处：一部分变成桌腿，一部分补进窗框，还有一些被留给后来的人。你曾以为修缮只是把一块木头钉到另一块木头上，后来才发现，每一寸材料都对应着一间需要挡风的屋子、一块必须立稳的黑板，或一个在夜里仍想看清字迹的人。"
    if finale_mapping("club_xp").get("repair", 0) >= 30:
        "地上那几处熟悉的绳结，是你亲手教别人重新打紧的。"
    else:
        "你没有参与所有修缮，但曾在地图上看见这些木料一点点改变教室和宿舍。"

    scene expression "images/finale/retrospective/cg_retrospect_office.webp"
    with dissolve
    $ renpy.pause(3.0, hard=True)
    "校务办公处的桌面总像来不及清空。课程表压着船运清单，床位名册旁边又添了纸张和煤油的账目。许多决定没有宏大的名字，只是“先把哪一批箱子送走”“今晚哪间教室还能点灯”“谁应当住进不漏雨的房间”。正是这些细小而准确的安排，让一所临时的大学没有在迁徙中散开。"
    if finale_number("virtue_truth", 0) >= 8:
        "你曾在这里纠正过一个编号、一处误记或一条未经核实的消息。"
    if finale_number("campus_score", 0) >= 70:
        "最后一页清单已经盖好，纸角整齐地压在镇纸下面。"

    scene expression "images/finale/retrospective/cg_retrospect_residences.webp"
    with dissolve
    $ renpy.pause(3.0, hard=True)
    "许多学生在建德拥有的并不是“校舍”，而是居民让出的一间屋、半张桌、一只可以烧热水的炉子。借屋的人和住屋的人并非总能立刻明白彼此的习惯，可四十五天过去，门槛边多了一双学生的鞋，墙上也多了一张课程表。离开时，人们才发现，那些临时借来的地方已经装进了彼此的生活。"
    if finale_number("world_resident_trust", 0) >= 65:
        "房主没有催你归还那把旧椅子，只说等船走后，他会亲自送回孔庙。"
    else:
        "屋主在门口点了点头。你们相处不算很深，但每一次借用和归还都被认真记着。"

    scene expression "images/finale/retrospective/cg_retrospect_pawnshop.webp"
    with dissolve
    $ renpy.pause(3.0, hard=True)
    "当铺曾临时容纳过许多无法立刻归类的东西：多出的一床被褥、暂时找不到主人的木箱、学生托人保管的旧物。它像建德生活的一处夹层，收下那些来不及安顿的部分。如今标签大多重新找到主人，仍无人认领的物品也已登记清楚，准备随最后一批行李同行。"
    if len(finale_collection("mc45_items")) >= 8:
        "你认得柜台上几件物品的来历，也知道它们为何值得被带走。"
    else:
        "有些物品对你仍然陌生，但它们属于这段迁徙中的某个人，不应被轻易遗落。"

    scene expression "images/finale/retrospective/cg_retrospect_port.webp"
    with dissolve
    $ renpy.pause(3.0, hard=True)
    "码头是建德生活最先发出声音、也最晚安静下来的地方。书箱、仪器、粮食、家书和消息都从这里抵达，又将从这里离开。你曾在雨里接过湿冷的麻绳，也曾在雾中等待看不清的船影。如今箱号一只只核对完，船头重新指向更远的地方。码头没有说再见，只把离开的路铺到江面上。"
    if finale_mapping("relationship").get("gu_mingchuan", 0) >= 20:
        "顾明川站在最外侧的木板上，正按你们熟悉的顺序检查最后一批箱子。"
    centered "{size=42}{color=#e7d2a0}天将亮了。{/color}{/size}"
    jump finale_depart_meicheng


label map_retrospective:
    jump finale_map_retrospective


label finale_depart_meicheng:
    window hide
    scene expression "images/finale/departure/cg_departure_lane.webp"
    with fade
    "天色从屋脊后面慢慢亮起来。梅城的街巷仍带着夜里的潮气，青石板被来往的脚步磨出一层浅光。学生们并不同时涌向码头，而是按照昨晚重新核过的名单分批出发。有人背着书，有人提着装衣物的布包，还有两个人合抬一只并不沉、却必须保持平稳的仪器箱。"
    "沈砚舟走出宿舍时，下意识回头看了一眼。门没有锁，值日学生还要留下来再查一次床铺。窗内那盏油灯已经熄了，烟气沿灯罩边缘散开，像一条未写完的线。"
    "居民们陆续开门。有人把昨夜烧好的热水递给学生，有人将借出的木凳搬回墙边，也有人只是站在门槛后面，看着这支在城中停留了四十五天的队伍经过。"
    "卖早点的老人将一摞还温热的饼塞进队伍最前面学生的布包，不肯收钱；住在临街屋里的孩子追出几步，又被家人叫回门内。没有锣鼓，也没有整齐的送别词。人们只是尽可能把眼前这段路照顾得稳一些。"
    "巷口贴过课程布告的墙已经被雨洗淡，只剩几处浆糊的痕迹。沈砚舟认出其中一角曾写着周考地点，另一角贴过《浙大日报》的简讯。那些纸张都被揭走了，墙仍在原处，像是一页被翻过去却没有撕掉的纸。"
    scene expression "images/finale/departure/cg_departure_port_wide.webp"
    with dissolve
    "码头比平日更拥挤，却没有等待货船时的嘈杂。木箱按去向排成几列，箱角的编号被重新描过，重要仪器外又包了一层油布。书册、课程记录、实验器材和生活用品彼此挨着，像一所大学被暂时拆成了可以搬动的形状。"
    "船工沿着舷边逐一查看吃水，校务人员在岸上核名，身体不适的学生与带孩子的家属被先安排到避风处。没有人催他们快些；真正的秩序不是所有人同时向前，而是每个人都知道自己应当在什么时候、从哪一块木板踏上船。"
    "许南枝坐在临时搭起的木桌后，将最后几张名单交给不同船只的负责人。她每交出一张，就在自己的抄本上画一条短线。周顺安站在稍远的地方，替不识字的船工辨认箱上的简单符号。他读得不快，却没有读错。"
    scene expression "images/finale/departure/cg_departure_loading.webp"
    with dissolve
    "顾明川从一只木箱后抬起头：“乙组仪器已经装完。丙组还差两箱，别把写着‘向上’的那只倒放。”"
    "一批书箱被抬上船。木板受力后发出低沉的吱呀声。沈砚舟伸手扶住最外侧的一只箱子，手掌触到油布上凝结的水汽。四十五天里，他曾把这些箱子看作“需要搬完的任务”，也曾把里面的东西看作“明日上课要用的材料”。直到离开时，他才明白，箱中装着的不是静止的旧物，而是一所学校仍要继续向前的凭据。"
    "仪器箱被安置在船舱内侧，书箱之间留出防潮的缝隙，生活行李则靠外摆放，方便靠岸后先取用。每一处看似普通的摆放，都来自此前的错误与补救：受潮的纸页、松开的绳结、写错的箱号，已经变成今日不再重复的次序。"
    "沈砚舟将蓝布笔记本放进贴身的布袋，又把周顺安那张还没收到的纸留出位置。他知道有些东西不能只靠记忆携带，也知道再详尽的笔记都无法替代亲手做过的事情。"
    "码头上最后一遍点数开始。数字从岸边传到船上，又从船上被复述回来。有人发现一只登记在乙船的被褥仍放在甲船旁边，便停下重新改写；没有人为了让名单好看而假装它已经到位。"
    "离开一座城，不是把在这里发生过的一切留在身后。真正被带走的东西，往往没有装进木箱。"
    jump finale_zhu_questions


label meicheng_departure:
    jump finale_depart_meicheng


label finale_zhu_questions:
    scene expression "images/finale/questions/cg_zhu_arrives_at_port.webp"
    with dissolve
    "竺可桢没有立刻走到队伍正前方。他先向负责装运的人问了几句，确认书箱与仪器是否分开安置，又看了看靠近船舱的位置是否留给身体不适的学生。校务人员答复时，他没有催促，只把其中一处尚未核清的数字重新问了一遍。"
    "竺可桢" "没有核清的，就写明没有核清。不要为了表面齐整，把疑问擦掉。"
    "说完，他抬头看见沈砚舟怀里的蓝布笔记本。"
    "竺可桢" "这一路都在记？"
    "沈砚舟" "起初记课程，后来什么都记一点。箱号、天气、谁借过哪张桌子……有些事情怕忘。"
    "竺可桢" "记得多未必就是明白。可若连事实都不肯留下，后来的人便只能凭想象替我们回答。"
    "江风从水面吹来，船舷轻轻撞在木桩上。竺可桢没有示意所有人停下，也没有把这段谈话变成正式训辞。他只是站在即将离开的学生面前，将声音放得足够清楚。"
    scene expression "images/finale/questions/cg_zhu_two_questions.webp"
    with dissolve
    "竺可桢" "诸位在校，有两个问题应该自己问问：第一，到浙大来做什么？第二，将来毕业后要做什么样的人？"
    "风声短暂静了一瞬。沈砚舟想起孔庙、教室、码头和夜里的宿舍，想起自己曾把许多事情看作“先做完再说”，如今才发觉，四十五天的每一次选择其实都已经在替自己回答。"
    "这两个问题并不要求学生在码头上交卷。它们会跟随一个人离开课堂，进入工作、判断与责任之中。今日说出的答案也许仍不完整，却必须有事实支撑，必须经得住下一段路的检验。"
    "竺可桢看着正在装船的人群，没有替任何人规定词句。他只提醒学生：答案不能借来，也不能只在危急时说得响亮；往后每一次如何求证、如何做事、如何对待同行者，都会把答案重新写一遍。"
    centered "{size=32}{color=#ead39a}这不是一道只有标准答案的问题。\n你过去四十五天的选择，将与这一次回答共同决定终章主题。{/color}{/size}"
    jump finale_player_answer


label zhu_two_questions:
    jump finale_zhu_questions


label finale_player_answer:
    menu:
        "为求知明理，也为让学问真正有用":
            $ final_answer = "scholar"
            $ finale_answer = "为求知明理，也为让学问真正有用"
            scene expression "images/finale/answers/cg_answer_scholar.webp"
            with dissolve
            "沈砚舟" "我到浙大来，是想知道世界为什么如此运转。起初我以为学问只在书页和课堂里，后来才发现，一张船单上的数字、一道受潮后看不清的题、一个还没有证据的判断，也都要求人认真。将来无论身在何处，我都愿意把不知道的事情问清，把已经知道的事情说明白，也把学问用在真正需要它的地方。"
            "竺可桢" "学问不怕从不知道开始，只怕把不知道装成已经知道。求知不是为了让自己显得高明，而是为了使判断更可靠，使工作更有益于人。你若愿意一直问下去，也愿意一直核实下去，离开哪一间教室，都不会真正离开大学。"
        "学会在混乱中找到能够落手的一步":
            $ final_answer = "practitioner"
            $ finale_answer = "学会在混乱中找到能够落手的一步"
            scene expression "images/finale/answers/cg_answer_practitioner.webp"
            with dissolve
            "沈砚舟" "我到浙大来，是想学会在事情混乱的时候，仍能找到可以落手的一步。四十五天里，许多问题没有等我们准备好才出现：船晚了，纸不够，窗漏风，课程却仍要继续。我现在明白，实干不是只求快，也不是一个人把所有事情扛下来，而是先看清条件，再和别人把眼前的一步做稳。将来我愿意解决真实的问题，不让知识只停在纸上。"
            "竺可桢" "一所学校能够继续，并不只靠讲台上的声音。核清一张表，修好一扇窗，把一只箱子平安送到下一站，这些事看似细小，却都在决定学问能否继续。愿你以后仍肯亲手去做，也仍肯在动手以前把事情想明白。"
        "守住书册、事实与仍不能中断的记忆":
            $ final_answer = "guardian"
            $ finale_answer = "守住书册、事实与仍不能中断的记忆"
            scene expression "images/finale/answers/cg_answer_guardian.webp"
            with dissolve
            "沈砚舟" "我到浙大来，是因为有些书、有些事实、有些人的记忆不能断。过去我以为保存只是不把东西丢掉，后来才知道，若不记清它从哪里来、为何重要、由谁交到下一人手里，即使物件还在，意义也可能散失。将来我愿意做那个在风雨里仍替它们留一盏灯的人，让后来的人知道，我们曾怎样把课程、书册和彼此的责任带过这一段路。"
            "竺可桢" "保存不是把旧物锁起来，而是使它们仍能服务今日，也能到达明日。记忆若离开事实，容易成为传说；事实若没有人承担，又会很快散失。你愿意守住它们，也应当记得，守护的最终目的仍是让更多人能够学习、判断和前行。"
        "成为一个能与他人同行、值得信任的人":
            $ final_answer = "companion"
            $ finale_answer = "成为一个能与他人同行、值得信任的人"
            scene expression "images/finale/answers/cg_answer_companion.webp"
            with dissolve
            "沈砚舟" "我起初只想着自己的课程，以为只要把题做会、把日子安排好，就算没有辜负来到大学的机会。到了今日才明白，一个人能走多远，也在于是否愿意与别人同行。有人替我留过一份讲义，有人和我一起搬过木箱，也有人在我失约时仍给我重新说明的机会。将来我想做一个让身边的人可以信任的人，在自己能够前进的时候，也替别人留出可以同行的位置。"
            "竺可桢" "人与人之间的信任，也是一所学校的根基。没有谁能独自把书、仪器、课程和责任带过这样长的路。你愿意看见同行的人，也要记得，真正的信任不是一句好听的话，而是一次次守约、承担和如实相告。日后无论身在何处，莫把别人只当作帮助自己前进的工具。"
    "竺可桢没有评价哪一种回答更正确。他只让沈砚舟把这句话写进自己的笔记本，并在答案后面留出一片空白。"
    "竺可桢" "往后的日子，还会替你继续回答。"
    jump finale_companion_farewells


label player_final_answer:
    jump finale_player_answer


label finale_companion_farewells:
    scene expression "images/finale/farewells/cg_farewell_xu_nanzhi.webp"
    with fade
    "许南枝把最后一张名单交给船上的负责人，确认对方在页角签下姓名，才将自己的笔收回笔袋。"
    "许南枝" "你那本蓝布册子，还剩多少空页？"
    "沈砚舟" "大概还有三分之一。"
    "许南枝" "那就别急着在今天写完。"
    "她从纸袋中抽出一张没有印刷的纸，纸边还留着裁切后的毛边。她把纸对折，夹进蓝布笔记本最后几页。"
    "许南枝" "到下一站以后，再写。不要把建德当成已经总结清楚的故事。我们现在知道的，只是自己站过的这一段。"
    if finale_mapping("club_xp").get("news", 0) >= 20:
        "她又递来一枚排字用过的小铅块：“这不是纪念品。下次排版还要用。先放在你这里，到了吉安记得还我。”"
    "她没有把离别说得很重。那些名单、校样与核实过的日期已经替她说明了许多事。她只看了一眼蓝布笔记本，确认那张空纸没有滑落。"
    "许南枝" "别只记别人说过什么，也记得自己答应过什么。"

    scene expression "images/finale/farewells/cg_farewell_gu_mingchuan.webp"
    with dissolve
    "顾明川蹲在船边，把最后一个绳结重新收紧。绳子已经勒进油布，他仍用手掌推了推箱角，确认它不会随着船身晃动。"
    "顾明川" "这只箱子记得么？"
    "沈砚舟" "迟到的那批仪器。"
    "顾明川笑了一下：“当时差一点把不能倒放的那只横着抬上岸。”"
    if "check_manifest" in finale_collection("story_flags"):
        "顾明川" "幸亏你先把船单翻出来。那天我只想着天快黑了，没想到快一步也可能错一步。"
    "他把一小段多余的麻绳递给沈砚舟。沈砚舟说以后还会有绳子，顾明川却让他当场把那个结重新打一遍。"
    "第一次太松，他没替沈砚舟接手，只让他拆开重来。第二次收紧后，绳结稳稳贴住箱角。"
    "顾明川" "这就行。到了下一站，未必还有时间等人教。"
    if finale_mapping("relationship").get("gu_mingchuan", 0) >= 30:
        "顾明川" "下一站若还分组，我会把你的名字写在我这一组。不是因为你力气大，是因为出问题时你肯留下来把事情说清。"
    "他转身继续检查下一只箱子，没有停下来等一句郑重的答复。沈砚舟把那段麻绳收进本子夹层，知道真正的约定还要在下一次搬运中完成。"

    scene expression "images/finale/farewells/cg_farewell_zhou_shunan.webp"
    with dissolve
    "周顺安没有随船离开。他站在码头边，手里攥着一张折了几次的纸，等沈砚舟从装运队伍里腾出手。"
    "周顺安" "这个给你。"
    "纸上只有一行字，笔画有些僵硬，几个字之间的距离也不均匀，却每一个都认得出来："
    centered "{size=42}{color=#ead39a}路远，书声不断。{/color}{/size}"
    "沈砚舟" "是你自己写的？"
    "周顺安" "先在沙地上写了很多次。许同学说，纸不够，想清楚再落笔。"
    if "literacy_complete" in finale_collection("story_flags"):
        "周顺安" "这个“声”字我以前总少写一横。今天没有少。"
    "周顺安看着一只船离岸，问：“你们到了江西，还会教人认字么？”"
    "沈砚舟" "会。也许先教自己还不认识的。"
    "周顺安笑了，往后退了两步，抬手用力挥了挥。"
    "周顺安" "到了以后，给这里写封信。字别写太小。"
    "那张纸没有印章，也不在任何正式清单上。可它写明了建德与下一站之间还有一条由人维系的路。沈砚舟将纸夹进空白页，和课程表、剪报与麻绳放在一起。"
    centered "{size=30}{color=#e8d29a}获得终章旧物：周顺安的第一句话{/color}{/size}"
    if "周顺安的第一句话" not in mc45_items:
        $ mc45_items.append("周顺安的第一句话")
    jump finale_jian_taihe_teaser


label companion_farewells:
    jump finale_companion_farewells


label character_epilogues:
    jump finale_companion_farewells


label finale_jian_taihe_teaser:
    scene expression "images/finale/departure/cg_boat_leaves_meicheng.webp"
    with fade
    "木板被收回岸上，麻绳从系船桩上解开。船工用篙抵住码头，船身先是轻轻一晃，随后离开了岸边。"
    "没有人高声宣布建德生活已经结束。岸上的人仍在挥手，船上的人仍在确认行李。许南枝低头护住纸袋，顾明川蹲在箱子旁听木板是否有异响，竺可桢站在靠前的位置继续与校务人员核对下一段行程。"
    "梅城的屋顶在晨雾里渐渐连成一条深色的线，孔庙、临时教室和宿舍都看不清了。可当它们真正看不清时，沈砚舟反而能够想起每一个地方的细节。"
    "四十五天并没有把一所大学安置下来。它只是证明，在不得不离开的地方，课程仍可以开始；在必须继续上路的时候，人仍可以把学问和责任带走。"

    scene expression "images/finale/route/cg_route_jiande_to_jian.webp"
    with dissolve
    $ finale_route_step = 0
    show screen finale_route_progress(finale_route_step)
    "船向西行。"
    $ finale_route_step = 1
    $ renpy.pause(0.8, hard=True)
    $ finale_route_step = 2
    $ renpy.pause(0.8, hard=True)
    $ finale_route_step = 3
    $ renpy.pause(0.8, hard=True)
    $ finale_route_step = 4
    $ renpy.pause(0.8, hard=True)
    $ finale_route_step = 5
    $ renpy.pause(1.2, hard=True)
    "1937年12月起，师生从建德出发，经金华、玉山、樟树，转抵江西吉安。"
    "但吉安仍不是终点。"
    hide screen finale_route_progress
    "地图边缘又展开一角，纸上慢慢露出“泰和”二字。新的校舍仍需要寻找，新的课程仍需要安排。书箱会再次开合，名单会再次誊写，学生会在陌生的屋檐下重新辨认上课铃声的方向。"
    "蓝布笔记本自动翻开新的一页。页面上写着：吉安—泰和。下一行仍然空白。"
    "沈砚舟" "建德篇写完了。下一页，从一条更远的江开始。"

    scene expression "images/finale/teaser/poster_jian_taihe.webp" at finale_poster_landscape
    with fade
    centered "{size=64}{color=#f0ddb0}负笈西行 · 吉安—泰和篇{/color}{/size}\n\n{size=31}{color=#e3d8c1}新校舍、新课程，仍从一张空白名单开始。{/color}{/size}"
    $ renpy.pause(6.0, hard=True)
    jump finale_statistics


label jian_taihe_teaser:
    jump finale_jian_taihe_teaser


label finale_statistics:
    $ finale_profile = build_finale_profile()
    $ ending_route = finale_profile["route"]
    $ ending_title = finale_profile["title"]
    call screen finale_statistics_page(finale_profile, 1)
    call screen finale_statistics_page(finale_profile, 2)
    call screen finale_statistics_page(finale_profile, 3)
    call screen finale_statistics_page(finale_profile, 4)
    call screen finale_statistics_page(finale_profile, 5)
    $ finale_persist_completion(finale_profile)
    $ renpy.save("finale_autosave_complete")
    jump finale_menu


label ending_statistics:
    jump finale_statistics


label finale_menu:
    $ finale_choice = renpy.call_screen("finale_menu_screen")
    if finale_choice == "replay":
        jump finale_roll_call
    elif finale_choice == "farewell":
        jump finale_companion_farewells
    elif finale_choice == "statistics":
        jump finale_statistics
    elif finale_choice == "archive":
        $ finale_entries = finale_profile.get("keepsakes", []) + finale_profile.get("archive", [])
        call screen finale_list_card("四十五日旧物与档案", finale_entries)
        jump finale_menu
    elif finale_choice == "gallery":
        jump finale_gallery
    elif finale_choice == "poster":
        scene expression "images/finale/teaser/poster_jian_taihe.webp" at finale_poster_landscape
        with fade
        centered "{size=64}{color=#f0ddb0}负笈西行 · 吉安—泰和篇{/color}{/size}"
        pause
        jump finale_menu
    elif finale_choice == "save":
        $ renpy.save("finale_manual_complete")
        centered "{size=30}{color=#ead39a}通关档案已保存。{/color}{/size}"
        jump finale_menu
    elif finale_choice == "title":
        $ renpy.full_restart(transition=fade)
    elif finale_choice == "restart":
        jump chapter_4
    elif finale_choice == "quit":
        call screen finale_quit_confirm
        if _return:
            $ renpy.quit()
        jump finale_menu
    jump finale_menu


label post_ending_menu:
    jump finale_menu


label finale_gallery:
    $ finale_gallery_choice = renpy.call_screen("finale_gallery_screen", finale_gallery_index)
    if finale_gallery_choice == "prev":
        $ finale_gallery_index = (finale_gallery_index - 1) % len(FINALE_GALLERY)
        jump finale_gallery
    elif finale_gallery_choice == "next":
        $ finale_gallery_index = (finale_gallery_index + 1) % len(FINALE_GALLERY)
        jump finale_gallery
    jump finale_menu


label finale_calculation:
    jump finale_statistics
