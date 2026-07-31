# ================================================================
# 45日主循环状态与流程
# ================================================================

default mc45_started = False
default mc45_finished = False
default mc45_day = 1
default mc45_time = 0
default mc45_weather = "江雾"
default mc45_event_history = []
default mc45_anchor_seen = []
default mc45_archive = []
default mc45_items = ["蓝布笔记本", "学生证", "家书", "断页"]
default mc45_journal = []

default mc45_knowledge = 2
default mc45_practice = 1
default mc45_reputation = 0
default mc45_will = 2
default mc45_truth = 1

default mc45_stamina = 6
default mc45_health = 92
default mc45_warmth = 1
default mc45_paper = 4
default mc45_money = 3
default mc45_materials = 1

default mc45_school_order = 2
default mc45_material_integrity = 2
default mc45_resident_trust = 1
default mc45_information_credit = 1
default mc45_morale = 2
default mc45_departure_readiness = 0

default mc45_selected_place = "dock"
default mc45_last_result = ""
default mc45_sidebar_open = False


init python:
    def mc45_apply_choice(choice_id):
        store.mc45_stamina = max(0, store.mc45_stamina - 1)
        if choice_id == "practice":
            store.mc45_practice += 1
            store.mc45_school_order += 1
            store.mc45_last_result = "你亲手解决了眼前的问题，校舍秩序有所改善。"
        elif choice_id == "verify":
            store.mc45_knowledge += 1
            store.mc45_truth += 1
            store.mc45_information_credit += 1
            store.mc45_last_result = "你保留了不同记录，并标明仍待核实之处。"
        else:
            store.mc45_reputation += 1
            store.mc45_resident_trust += 1
            store.mc45_last_result = "你先照料了具体的人，这份体谅被记住了。"
        completed_request = campus_try_complete_request(store.mc45_selected_place, choice_id)
        if completed_request:
            store.mc45_last_result += "\n校务请求“%s”已经完成。" % CAMPUS_REQUESTS[completed_request]["title"]

    def mc45_night_settlement():
        cold = store.mc45_weather in ("北风", "寒潮", "霜冻", "雨夹雪", "冻雨")
        if cold and store.mc45_warmth < 2:
            store.mc45_health = max(0, store.mc45_health - 3)
            store.mc45_last_result = "寒气透进铺位，保暖不足使健康下降。"
        elif cold and store.mc45_warmth >= 2:
            store.mc45_health = min(100, store.mc45_health + 2)
            store.mc45_last_result = "热水、干衣与加厚铺盖挡住寒气，今夜恢复得更好。"
        elif store.mc45_health < 100:
            store.mc45_health = min(100, store.mc45_health + 1)
        store.mc45_stamina = 6 if store.mc45_health >= 70 else 5
        if store.mc45_day >= 31:
            store.mc45_departure_readiness += 1
        info = mc45_info(store.mc45_day)
        store.mc45_journal.append((store.mc45_day, info[0], info[2], store.mc45_weather))


screen mc45_world_map():
    modal True
    $ day_info = mc45_info(mc45_day)
    $ time_name = MC45_TIME_NAMES[mc45_time]
    $ campaign_post_classroom = classroom_unlocked and map_visual_phase == "post_classroom"
    $ campaign_map_image = mc45_weather_map_image(mc45_weather, campaign_post_classroom)
    $ campaign_pre_rects = {
        "linchang": (240, 155, 150, 58),
        "office": (925, 165, 190, 58),
        "dormitory": (1450, 155, 190, 58),
        "kongmiao": (180, 365, 150, 58),
        "zhu_residence": (925, 415, 180, 58),
        "minju": (1430, 405, 150, 58),
        "pawnshop": (1480, 700, 150, 58),
        "dock": (340, 700, 170, 58),
    }
    $ campaign_post_rects = {
        "linchang": (650, 170, 150, 58),
        "office": (1080, 175, 190, 58),
        "dormitory": (1510, 170, 190, 58),
        "kongmiao": (485, 350, 150, 58),
        "zhu_residence": (1080, 400, 180, 58),
        "minju": (1490, 390, 150, 58),
        "pawnshop": (1510, 620, 150, 58),
        "dock": (800, 650, 170, 58),
    }
    $ campaign_map_rects = campaign_post_rects if campaign_post_classroom else campaign_pre_rects
    $ classroom_rect = (145, 560, 180, 58)

    add campaign_map_image:
        xysize (1920, 1080)
    add Solid(MC45_TIME_TINTS[mc45_time])
    use mc45_weather_overlay(mc45_weather)

    frame:
        xpos 30
        ypos 24
        xsize 690
        ysize 86
        background Solid("#10140ec7")
        padding (20, 9)
        vbox:
            spacing 2
            text "建德梅城  第[mc45_day]日  [day_info[0]]  [time_name]":
                size 25
                color "#ead39a"
            text "[day_info[1]]阶段 · [mc45_weather] · 今日：[day_info[2]]":
                size 16
                color "#c7c1b2"

    frame:
        xpos 735
        ypos 24
        xsize 925
        ysize 58
        background Solid("#10140eb8")
        padding (18, 9)
        hbox:
            spacing 18
            text "体力 [mc45_stamina]/6" size 16 color "#d7c894"
            text "健康 [mc45_health]" size 16 color "#d7c894"
            text "保暖 [mc45_warmth]" size 16 color "#d7c894"
            text "纸墨 [mc45_paper]" size 16 color "#d7c894"
            text "学识 [mc45_knowledge]" size 16 color "#bfc5b5"
            text "实务 [mc45_practice]" size 16 color "#bfc5b5"
            text "人望 [mc45_reputation]" size 16 color "#bfc5b5"

    textbutton ("收起今日信息" if mc45_sidebar_open else "今日信息"):
        xpos 1680
        ypos 24
        xsize 205
        ysize 58
        text_size 17
        text_color "#e5ca8c"
        text_hover_color "#fff0bd"
        text_xalign 0.5
        text_yalign 0.5
        background Solid("#10140ed0")
        hover_background Solid("#352b1de8")
        action ToggleVariable("mc45_sidebar_open")

    $ campaign_place_ids = ("kongmiao", "linchang", "office", "minju", "pawnshop", "dock", "dormitory", "zhu_residence")
    for place_id in campaign_place_ids:
        $ meta = MC45_LOCATION_META[place_id]
        $ place_name, place_bg, old_rect = meta
        $ rect = campaign_map_rects[place_id]
        $ px, py, pw, ph = rect
        $ residence_open = (place_id != "zhu_residence" or mc45_day >= 3)
        $ weather_open, weather_reason = mc45_weather_location_access(place_id, mc45_weather)
        $ can_enter = mc45_time < 3 and mc45_stamina > 0 and residence_open and weather_open
        button:
            xpos px
            ypos py
            xsize pw
            ysize ph
            background Solid("#00000000")
            hover_background (Solid("#d3a64b38") if can_enter else Solid("#00000000"))
            action (Return(place_id) if can_enter else (Notify(weather_reason) if not weather_open else NullAction()))
            frame:
                xalign 0.5
                yalign 0.5
                xsize pw
                ysize ph
                background Solid("#11140ec4")
                padding (6, 3)
                vbox:
                    xalign 0.5
                    text place_name:
                        xalign 0.5
                        size 18
                        color ("#ead39a" if can_enter else "#99958a")
                    if not residence_open:
                        text "第3日后开放" xalign 0.5 size 11 color "#9a9281"
                    elif not weather_open:
                        text "天气暂停通行" xalign 0.5 size 11 color "#c09a72"
                    elif mc45_time == 3:
                        text "深夜不可行动" xalign 0.5 size 11 color "#9a9281"
                    elif mc45_stamina <= 0:
                        text "体力不足" xalign 0.5 size 11 color "#9a9281"
                    else:
                        text "进入" xalign 0.5 size 11 color "#c1b89f"

    # 第五章完成后，镜头拉远并在左侧扩出临时教室；此前不显示虚假建筑。
    if classroom_unlocked:
        button:
            xpos classroom_rect[0]
            ypos classroom_rect[1]
            xsize classroom_rect[2]
            ysize classroom_rect[3]
            background Solid("#11140ec4")
            hover_background Solid("#d3a64b38")
            action Return("classroom")
            vbox:
                xalign 0.5
                yalign 0.5
                text "临时教室" xalign 0.5 size 18 color "#ead39a"
                text "进入" xalign 0.5 size 11 color "#c1b89f"

    if mc45_sidebar_open:
        frame:
            xpos 1510
            ypos 98
            xsize 375
            ysize 440
            background Solid("#11140ef2")
            padding (22, 17)
            vbox:
                spacing 7
                text "今日主题" size 21 color "#e5ca8c"
                text day_info[2] size 25 color "#eee3c9"
                text day_info[3] size 16 color "#c9c4b7" xmaximum 325 line_spacing 4
                null height 4
                text "今日标志物" size 18 color "#e5ca8c"
                text day_info[4] size 20 color "#d9d3c5"
                null height 4
                text "行动规则" size 18 color "#e5ca8c"
                text "早晨、午间、傍晚各行动一次；深夜返回学生宿舍结算。" size 15 color "#aaa79e" xmaximum 325 line_spacing 3
                text "天气提示" size 18 color "#e5ca8c"
                text mc45_weather_notice(mc45_weather) size 14 color "#c9c4b7" xmaximum 325 line_spacing 3
                null height 4
                text "公共物资" size 18 color "#e5ca8c"
                text "木料 [campus_stock['wood']]  纸张 [campus_stock['paper']]  灯油 [campus_stock['lamp_oil']]" size 14 color "#c9c4b7"
                text "粮食 [campus_stock['grain']]  药品 [campus_stock['medicine']]  校务 [campus_score]" size 14 color "#c9c4b7"

    if mc45_time == 3:
        frame:
            xpos 560
            ypos 720
            xsize 800
            ysize 180
            background Solid("#11151aeb")
            padding (30, 18)
            vbox:
                xalign 0.5
                spacing 12
                text "夜色已深，地图停止行动。":
                    xalign 0.5
                    size 28
                    color "#e6d6ad"
                text "回到学生宿舍，整理记录并结算今日状态。":
                    xalign 0.5
                    size 19
                    color "#bbb7ad"
                textbutton "夜归宿舍":
                    xalign 0.5
                    xsize 300
                    ysize 56
                    text_size 22
                    text_color "#ead39a"
                    text_hover_color "#fff0bd"
                    background Solid("#3b301fe8")
                    hover_background Solid("#5a4628ee")
                    action Return("night")

    frame:
        xpos 30
        ypos 1000
        xsize 650
        ysize 55
        background Solid("#11140edc")
        hbox:
            xalign 0.5
            yalign 0.5
            spacing 28
            textbutton "返回六章地图":
                text_size 18
                text_color "#d6c69c"
                text_hover_color "#ffe5a5"
                action Return("world")
            text "档案 [len(mc45_archive)]" size 17 color "#aaa598" yalign 0.5
            text "行动记录 [len(mc45_event_history)]" size 17 color "#aaa598" yalign 0.5


screen mc45_event_scene(place_id, event_title, event_text, is_anchor=False):
    modal True
    $ place_name, place_bg, rect = MC45_LOCATION_META[place_id]
    $ pose_path = renpy.random.choice((
        "images/chapter01/characters/shenyan_calm.png",
        "images/chapter01/characters/shenyan_thoughtful.png",
        "images/chapter01/characters/shenyan_determined.png",
        "images/chapter01/characters/shenyan_worried.png",
    ))

    add place_bg:
        xysize (1920, 1080)
    add Solid(MC45_TIME_TINTS[mc45_time])

    add Transform(pose_path, xysize=(510, 880), fit="contain"):
        xpos 28
        yalign 1.0

    frame:
        xpos 32
        ypos 28
        xsize 830
        ysize 98
        background Solid("#10140ed0")
        padding (23, 11)
        vbox:
            text "[place_name] · [MC45_TIME_NAMES[mc45_time]] · [mc45_weather]" size 26 color "#e9d39a"
            text ("今日固定事件" if is_anchor else "地点事件") size 16 color "#aaa79c"

    frame:
        xpos 405
        ypos 655
        xsize 1215
        ysize 350
        background Solid("#151710ef")
        padding (38, 25)
        vbox:
            spacing 8
            text event_title size 35 color "#edd69d"
            frame:
                xsize 1110
                ysize 2
                background Solid("#98743eaa")
            text event_text:
                size 24
                color "#e7e2d6"
                xmaximum 1120
                line_spacing 7
            null height 4
            hbox:
                spacing 18
                textbutton "动手解决":
                    xsize 340
                    ysize 63
                    text_size 21
                    text_color "#ead39a"
                    text_hover_color "#fff0bd"
                    background Solid("#283026e8")
                    hover_background Solid("#4d3c22ef")
                    action Return("practice")
                textbutton "核对记录":
                    xsize 340
                    ysize 63
                    text_size 21
                    text_color "#ead39a"
                    text_hover_color "#fff0bd"
                    background Solid("#283026e8")
                    hover_background Solid("#4d3c22ef")
                    action Return("verify")
                textbutton "先照料人":
                    xsize 340
                    ysize 63
                    text_size 21
                    text_color "#ead39a"
                    text_hover_color "#fff0bd"
                    background Solid("#283026e8")
                    hover_background Solid("#4d3c22ef")
                    action Return("care")

    frame:
        xpos 1645
        ypos 145
        xsize 240
        ysize 420
        background Solid("#11140ee5")
        padding (17, 15)
        vbox:
            spacing 7
            text "当前状态" size 22 color "#e3ca8c"
            text "体力 [mc45_stamina]/6" size 18 color "#d6d0bf"
            text "学识 [mc45_knowledge]" size 18 color "#d6d0bf"
            text "实务 [mc45_practice]" size 18 color "#d6d0bf"
            text "人望 [mc45_reputation]" size 18 color "#d6d0bf"
            text "心志 [mc45_will]" size 18 color "#d6d0bf"
            null height 8
            text "世界状态" size 22 color "#e3ca8c"
            text "校舍秩序 [mc45_school_order]" size 17 color "#aaa79d"
            text "居民信任 [mc45_resident_trust]" size 17 color "#aaa79d"
            text "信息公信 [mc45_information_credit]" size 17 color "#aaa79d"


screen mc45_result_card():
    modal True
    add MC45_LOCATION_META[mc45_selected_place][1]:
        xysize (1920, 1080)
    add Solid("#07100c62")
    frame:
        xalign 0.5
        yalign 0.78
        xsize 1050
        ysize 205
        background Solid("#151710ee")
        padding (35, 24)
        vbox:
            xalign 0.5
            spacing 15
            text mc45_last_result:
                xalign 0.5
                text_align 0.5
                size 25
                color "#e7ddc7"
                xmaximum 940
            textbutton "返回梅城地图":
                xalign 0.5
                xsize 300
                ysize 55
                text_size 21
                text_color "#e8d19a"
                text_hover_color "#fff0bd"
                background Solid("#3b301fe8")
                hover_background Solid("#5a4628ee")
                action Return()


screen mc45_deep_night():
    modal True
    $ info = mc45_info(mc45_day)
    add "images/chapter01/backgrounds/dormitory_rain.png":
        xysize (1920, 1080)
    add Solid("#07142682")
    frame:
        xpos 170
        ypos 135
        xsize 1580
        ysize 760
        background Solid("#11140eea")
        padding (48, 35)
        hbox:
            spacing 45
            vbox:
                xsize 920
                spacing 12
                text "深夜札记  第[mc45_day]日" size 34 color "#ead39a"
                text "[info[0]] · [mc45_weather]" size 20 color "#aaa79c"
                frame:
                    xsize 880
                    ysize 2
                    background Solid("#98743eaa")
                text "今日：[info[2]]" size 27 color "#e7e0d0"
                text "沈砚舟把事实、猜测和仍待核实的部分分开写下。窗外的风雨没有停，隔壁铺位已经熄灯。" size 22 color "#c9c5ba" xmaximum 860 line_spacing 7
                if mc45_last_result:
                    text "最后一笔：[mc45_last_result]" size 19 color "#aaa79d" xmaximum 860 line_spacing 5
            vbox:
                xsize 500
                spacing 10
                text "夜间结算" size 28 color "#ead39a"
                text "健康 [mc45_health]" size 21 color "#d7d0bf"
                text "保暖 [mc45_warmth]" size 21 color "#d7d0bf"
                text "师生士气 [mc45_morale]" size 21 color "#d7d0bf"
                text "迁移准备 [mc45_departure_readiness]" size 21 color "#d7d0bf"
                null height 4
                text "今日回流" size 20 color "#e3ca8c"
                for settlement_line in last_night_summary[-6:]:
                    text "· [settlement_line]" size 15 color "#bdb8aa" xmaximum 470
                null height 20
                if mc45_day < 45:
                    textbutton "进入下一日":
                        xsize 380
                        ysize 65
                        text_size 23
                        text_color "#ead39a"
                        text_hover_color "#fff0bd"
                        background Solid("#3b301fe8")
                        hover_background Solid("#5a4628ee")
                        action Return()
                else:
                    textbutton "结束建德生活":
                        xsize 380
                        ysize 65
                        text_size 23
                        text_color "#ead39a"
                        text_hover_color "#fff0bd"
                        background Solid("#3b301fe8")
                        hover_background Solid("#5a4628ee")
                        action Jump("finale_roll_call")


label meicheng_town_hub:
    hide screen immersive_character
    hide screen immersive_hud
    hide screen ch1_character
    hide screen ch1_hud
    $ immersive_active = False

    if 4 not in day1_completed_chapters:
        jump day1_map_hub

    if not mc45_started:
        $ mc45_started = True
        $ mc45_day = 1
        $ mc45_time = 0
        $ mc45_weather = "江雾"

    $ mc45_sync_weather_ambience(mc45_weather)
    $ campaign_import_legacy_turn()
    if campaign_exam_is_due():
        if campaign_day >= 8 and not classroom_unlocked:
            $ chapter5_unlocked = True
            $ chapter5_completed = True
            $ classroom_unlocked = True
            $ map_visual_phase = "post_classroom"
            call classroom_opening_sequence
        jump campaign_forced_exam
    if campaign_day == 7 and not chapter5_completed:
        jump day7_chapter5_gate
    if campaign_day >= 20 and not chapter6_completed:
        jump day20_chapter6_gate

    call screen mc45_world_map
    $ mc45_selection = _return

    if mc45_selection == "world":
        $ campaign_import_legacy_turn()
        if can_switch_meta_map():
            $ campaign_prepare_map_switch("chapter_world_map")
            jump chapter_world_map_hub
        jump meicheng_town_hub
    if mc45_selection == "night":
        jump mc45_night_return
    if mc45_selection == "classroom":
        jump campaign_classroom_hub

    $ mc45_selected_place = mc45_selection
    $ current_location = mc45_selected_place
    jump mc45_run_interaction


label mc45_run_interaction:
    if mc45_selected_place == "office":
        call campus_office_request_board

    $ bond_candidate = campaign_bond_candidate(mc45_selected_place)
    if bond_candidate:
        call campaign_bond_event_label(bond_candidate)
        if _return:
            call screen mc45_result_card
            jump meicheng_town_hub

    $ club_candidate = campaign_club_activity_for_turn(mc45_selected_place)
    if club_candidate:
        call campaign_club_activity_label(club_candidate)
        if _return:
            call screen mc45_result_card
            jump meicheng_town_hub

    $ info = mc45_info(mc45_day)
    $ is_anchor = mc45_day not in mc45_anchor_seen
    if is_anchor:
        $ event_title = info[2]
        $ event_text = info[3]
    else:
        $ catalog_event = campaign_pick_random_event(mc45_selected_place)
        if catalog_event:
            call campaign_random_event_label(catalog_event)
            call screen mc45_result_card
            jump meicheng_town_hub
        $ event_title, event_text = mc45_pick_location_event(mc45_selected_place, mc45_day, mc45_event_history)

    call screen mc45_event_scene(mc45_selected_place, event_title, event_text, is_anchor)
    $ event_choice = _return
    $ mc45_apply_choice(event_choice)

    if is_anchor:
        $ mc45_anchor_seen.append(mc45_day)
        if info[4] not in mc45_items:
            $ mc45_items.append(info[4])
        if mc45_day in MC45_ARCHIVE_FACTS and MC45_ARCHIVE_FACTS[mc45_day] not in mc45_archive:
            $ mc45_archive.append(MC45_ARCHIVE_FACTS[mc45_day])

    $ mc45_event_history.append((mc45_day, mc45_time, mc45_selected_place, event_title, event_choice))
    $ mc45_time = min(3, mc45_time + 1)
    $ campaign_import_legacy_turn()
    call screen mc45_result_card
    jump meicheng_town_hub


label mc45_night_return:
    $ return_summary = campaign_forced_return_settlement()
    $ current_location = "dormitory"
    $ campaign_period = 3
    $ mc45_night_settlement()
    $ campus_night_settlement()
    $ campus_last_settlement = return_summary + campus_last_settlement
    $ campaign_extended_night_settlement()
    call screen mc45_deep_night
    $ night_settlement_count += 1
    if mc45_day >= 45:
        jump finale_roll_call
    $ mc45_day += 1
    $ mc45_time = 0
    $ mc45_weather = mc45_weather_next(mc45_day, mc45_weather)
    $ mc45_last_result = ""
    $ campaign_import_legacy_turn()
    $ days_completed = min(45, night_settlement_count)
    jump meicheng_town_hub
