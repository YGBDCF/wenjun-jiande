# ================================================================
# 建德梅城自由探索模型
# 第四章通关后解锁。首期开放七处地点，竺可桢故居保留为重点扩展位。
# ================================================================

default meicheng_town_day = 1
default meicheng_time_index = 0
default meicheng_visit_log = []
default meicheng_event_log = []
default meicheng_help_count = 0
default meicheng_record_count = 0


init python:
    MEICHENG_TIME_NAMES = ("早晨", "午间", "黄昏", "深夜")
    MEICHENG_TIME_TINTS = (
        "#f2c98012",
        "#fff4ce05",
        "#8f4e2b35",
        "#0714269a",
    )

    # 名称、热点位置与大小。底图本身不含文字，方便后续继续微调。
    MEICHENG_TOWN_SPOTS = (
        ("linchang", "林场", 55, 115, 355, 220),
        ("kongmiao", "孔庙", 45, 345, 370, 245),
        ("dock", "梅城码头", 60, 710, 405, 250),
        ("office", "校务办公处", 665, 105, 420, 220),
        ("zhu_residence", "竺可桢故居", 715, 385, 440, 255),
        ("dormitory", "学生宿舍", 1390, 105, 455, 230),
        ("minju", "民居", 1360, 365, 455, 240),
        ("pawnshop", "当铺", 1370, 690, 455, 255),
    )

    MEICHENG_TOWN_NAMES = {
        place_id: place_name
        for place_id, place_name, px, py, pw, ph in MEICHENG_TOWN_SPOTS
    }

    # 每处先放入两则可替换的随机事件，后续可直接继续追加。
    MEICHENG_RANDOM_EVENTS = {
        "kongmiao": (
            ("课桌还差十二张", "孔庙偏殿已经腾空，学生们正把长凳拼成课桌。雨水从檐角滴下，最靠墙的一排仍需垫高。"),
            ("借来的粉笔", "第一堂课开讲前，粉笔只剩半盒。附近小学送来一包旧粉笔，短的不足一寸，也被仔细收进木匣。"),
        ),
        "linchang": (
            ("灯油见底", "林场办公室今晚仍要誊写名册，但灯油已经不够。管理员提议把两间办公室合在一盏灯下办公。"),
            ("一张临时课表", "新誊写的课表被山风吹落在院里。几名学生逐张拾回，重新核对教师、教室与上课时辰。"),
        ),
        "office": (
            ("第四次改写课表", "新到的一批教师改变了原有安排。校务人员只得再次改写课表，确保第二天每门课都有去处。"),
            ("迟到的学生名册", "一份途中受潮的名册刚送到。纸页已经粘连，需要逐页揭开，确认还有谁尚未报到。"),
        ),
        "minju": (
            ("屋主留下的规矩", "借住的房间只能使用半边灶台，夜间也不可高声交谈。学生们把规矩记在门后，免得打扰主人一家。"),
            ("窗边的旁听生", "屋主家的孩子抱着小凳坐在窗边，听大学生讨论算学。没有人赶他走，只把油灯往外挪了一点。"),
        ),
        "pawnshop": (
            ("铺位与过道", "当铺库房里挤满草席和木箱。若再添两个铺位，夜间通道就会被堵住，必须重新调整。"),
            ("潮气从墙根上来", "库房墙角不断返潮，贴墙的书箱已经留下水印。学生们找来砖块，把箱底一只只垫高。"),
        ),
        "dock": (
            ("迟到的一船仪器", "暮色将近，一艘载着仪器的民船才靠岸。箱体不能淋雨，所有人临时排成一列接力搬运。"),
            ("被雨水冲淡的箱号", "几只木箱的墨字已经模糊。码头登记员拿出旧清单，按重量和封条逐一复核。"),
        ),
        "dormitory": (
            ("共用一盏灯", "宿舍里的灯不够，每四张铺位共用一盏。有人读讲义，有人补衣服，灯芯被调得很低。"),
            ("夜课归来", "晚课结束后，鞋底带回一层泥水。值日生守在门边，提醒大家先擦净鞋底再进屋。"),
        ),
    }

    def meicheng_pick_event(place_id):
        return renpy.random.choice(MEICHENG_RANDOM_EVENTS[place_id])


screen meicheng_town_map():
    modal True
    $ current_time_name = MEICHENG_TIME_NAMES[meicheng_time_index]

    add "images/meicheng_town/meicheng_town_base_v1.png":
        xysize (1920, 1080)

    add Solid(MEICHENG_TIME_TINTS[meicheng_time_index])

    # 顶部只保留一条窄信息栏，不遮挡城镇全景。
    frame:
        xpos 34
        ypos 24
        xsize 760
        ysize 96
        background Solid("#11140fcf")
        padding (26, 13)

        vbox:
            spacing 2
            text "建德梅城自由探索":
                size 32
                color "#ead39a"
            text "第 [meicheng_town_day] 日  [current_time_name]":
                size 20
                color "#c8c1ae"

    frame:
        xpos 1280
        ypos 24
        xsize 606
        ysize 96
        background Solid("#11140fcf")
        padding (22, 12)

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 20
            for time_number, time_name in enumerate(MEICHENG_TIME_NAMES):
                text time_name:
                    size 20
                    color ("#f0d18a" if time_number == meicheng_time_index else "#847f73")
                    outlines [(2, "#11120f", 0, 0)]

    for place_id, place_name, px, py, pw, ph in MEICHENG_TOWN_SPOTS:
        $ is_key_place = place_id == "zhu_residence"
        $ can_move = meicheng_time_index < 3 and not is_key_place

        button:
            xpos px
            ypos py
            xsize pw
            ysize ph
            background Solid("#00000000")
            hover_background (Solid("#d7a64a18") if can_move else Solid("#00000000"))
            action (Return(place_id) if can_move else NullAction())

            frame:
                xalign 0.5
                yalign 1.0
                xsize min(pw - 24, 300)
                ysize 66
                background Solid("#11140fe2")
                padding (10, 7)

                vbox:
                    xalign 0.5
                    spacing 0
                    text place_name:
                        xalign 0.5
                        size 24
                        color ("#ead091" if can_move else "#aaa398")
                        outlines [(2, "#11120f", 0, 0)]
                    if is_key_place:
                        text "重点地点  后续开放":
                            xalign 0.5
                            size 15
                            color "#c09b58"
                    elif meicheng_time_index == 3:
                        text "深夜不可行动":
                            xalign 0.5
                            size 15
                            color "#8f969c"
                    else:
                        text "点击进入":
                            xalign 0.5
                            size 15
                            color "#c5c0b1"

    if meicheng_time_index == 3:
        frame:
            xalign 0.5
            ypos 800
            xsize 520
            ysize 150
            background Solid("#10151aea")
            padding (28, 18)

            vbox:
                xalign 0.5
                spacing 10
                text "夜深了，今日不可继续行动。":
                    xalign 0.5
                    size 25
                    color "#e5d8b7"
                textbutton "结束今日，返回早晨":
                    xalign 0.5
                    text_size 22
                    text_color "#ddc68e"
                    text_hover_color "#ffe3a0"
                    action Return("sleep")

    frame:
        xpos 34
        ypos 994
        xsize 420
        ysize 58
        background Solid("#11140fdc")

        hbox:
            xalign 0.5
            yalign 0.5
            spacing 28
            textbutton "返回六章地图":
                text_size 19
                text_color "#d8c79f"
                text_hover_color "#ffe1a0"
                action Return("world")
            text "已记录事件 [len(meicheng_event_log)]":
                size 17
                color "#aaa598"
                yalign 0.5


screen meicheng_random_event_card(place_name, event_title, event_text):
    modal True

    add "images/meicheng_town/meicheng_town_base_v1.png":
        xysize (1920, 1080)

    add Solid(MEICHENG_TIME_TINTS[meicheng_time_index])
    add Solid("#080b0a38")

    frame:
        xpos 205
        ypos 650
        xsize 1510
        ysize 330
        background Solid("#11140ff2")
        padding (44, 30)

        vbox:
            spacing 10
            text place_name:
                size 20
                color "#a98b52"
            text event_title:
                size 36
                color "#ecd69d"
            frame:
                xsize 1060
                ysize 2
                background Solid("#98743eaa")
            text event_text:
                size 25
                color "#e4dfd2"
                xmaximum 1370
                line_spacing 8

            null height 8

            hbox:
                spacing 24
                textbutton "上前帮忙":
                    xsize 310
                    ysize 58
                    text_size 21
                    text_color "#e1cd99"
                    text_hover_color "#ffe4a0"
                    background Solid("#263027dd")
                    hover_background Solid("#4b3a20ee")
                    action Return("help")
                textbutton "先记下情况":
                    xsize 310
                    ysize 58
                    text_size 21
                    text_color "#e1cd99"
                    text_hover_color "#ffe4a0"
                    background Solid("#263027dd")
                    hover_background Solid("#4b3a20ee")
                    action Return("record")


label legacy_meicheng_town_hub:
    hide screen immersive_character
    hide screen immersive_hud
    hide screen ch1_character
    hide screen ch1_hud
    $ immersive_active = False

    if 4 not in day1_completed_chapters:
        jump day1_map_hub

    call screen meicheng_town_map
    $ meicheng_selection = _return

    if meicheng_selection == "world":
        jump day1_map_hub

    if meicheng_selection == "sleep":
        $ meicheng_town_day += 1
        $ meicheng_time_index = 0
        jump meicheng_town_hub

    call legacy_meicheng_town_random_event(meicheng_selection) from _call_legacy_meicheng_town_random_event
    jump meicheng_town_hub


label legacy_meicheng_town_random_event(place_id):
    $ place_name = MEICHENG_TOWN_NAMES[place_id]
    $ event_title, event_text = meicheng_pick_event(place_id)

    call screen meicheng_random_event_card(place_name, event_title, event_text)
    $ event_response = _return

    if event_response == "help":
        $ meicheng_help_count += 1
    else:
        $ meicheng_record_count += 1

    $ meicheng_visit_log.append(place_id)
    $ meicheng_event_log.append((meicheng_town_day, meicheng_time_index, place_id, event_title, event_response))
    $ meicheng_time_index = min(meicheng_time_index + 1, 3)
    return
