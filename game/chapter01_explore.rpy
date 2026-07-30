# ================================================================
# 第一章：西天目山——寺庙里的大学
# 剧本编号：ZJU-1937-01
# 史实边界：1937-09-21 新生迁往禅源寺；09-27 开课；
# 11 月中下旬因局势紧张转赴建德。寺院没有遭到虚构的直接轰炸。
# ================================================================

define ch1_shen = Character("沈砚舟", color="#d7c18a")
define ch1_xu = Character("许南枝", color="#c7d1c0")
define ch1_miaoding = Character("妙定法师", color="#c3b596")
define ch1_tutor = Character("导师", color="#c9b98b")
define ch1_freshman = Character("新生", color="#bdc9d6")
define ch1_messenger = Character("送信人", color="#bdc9d6")

image ch1 gate:
    "images/chapter01/backgrounds/mountain_gate_registration.png"
    xysize (1920, 1080)
image ch1 courtyard:
    "images/chapter01/backgrounds/temple_courtyard_rain.png"
    xysize (1920, 1080)
image ch1 dormitory:
    "images/chapter01/backgrounds/dormitory_rain.png"
    xysize (1920, 1080)
image ch1 classroom:
    "images/chapter01/backgrounds/first_classroom.png"
    xysize (1920, 1080)
image ch1 mentor_room:
    "images/chapter01/backgrounds/mentor_register_room.png"
    xysize (1920, 1080)
image ch1 mail_corridor:
    "images/chapter01/backgrounds/mail_corridor.png"
    xysize (1920, 1080)
image ch1 departure:
    "images/chapter01/backgrounds/departure_classroom.png"
    xysize (1920, 1080)

image ch1 shen_recording = "images/chapter01/characters/shen_recording.png"
image ch1 shen_hesitant = "images/chapter01/characters/shen_hesitant.png"
image ch1 shen_listening = "images/chapter01/characters/shen_listening.png"
image ch1 shen_alert = "images/chapter01/characters/shen_alert.png"
image ch1 shen_sad_letter = "images/chapter01/characters/shen_sad_letter.png"
image ch1 shen_determined = "images/chapter01/characters/shen_determined.png"
image ch1 xu_checking = "images/chapter01/characters/xu_checking.png"
image ch1 xu_repairing = "images/chapter01/characters/xu_repairing.png"
image ch1 xu_worried = "images/chapter01/characters/xu_worried.png"
image ch1 xu_soft = "images/chapter01/characters/xu_soft.png"
image ch1 xu_firm = "images/chapter01/characters/xu_firm.png"
image ch1 xu_departing = "images/chapter01/characters/xu_departing.png"
image ch1 miaoding_explain = "images/chapter01/characters/miaoding_explain.png"
image ch1 miaoding_calm = "images/chapter01/characters/miaoding_calm.png"
image ch1 mentor_explain = "images/chapter01/characters/mentor_explain.png"
image ch1 mentor_recording = "images/chapter01/characters/mentor_recording.png"

default ch1_stage = 1
default ch1_stage_title = "雨中山门"
default ch1_stage_date = "1937年9月21日  午后"
default ch1_task_hint = "完成报到，并协助新生安置行李"
default ch1_sprite = ""
default ch1_allow_return = False
default ch1_items = []
default ch1_archives = []
default ch1_companion_care = 0
default ch1_record_accuracy = 0
default ch1_first_choice = ""
default ch1_mail_choice = ""

default ch1_s1_register = False
default ch1_s1_luggage = False
default ch1_s1_notices = False
default ch1_s2_dorm = False
default ch1_s2_classroom = False
default ch1_s2_study = False
default ch1_s2_passage = False
default ch1_s3_desks = False
default ch1_s3_blackboard = False
default ch1_s3_window = False
default ch1_s3_books = False
default ch1_s4_roll = False
default ch1_s4_health = False
default ch1_s4_supplies = False
default ch1_s5_mail = False
default ch1_s5_table = False
default ch1_s5_lamp = False
default ch1_s6_return = False
default ch1_s6_board = False
default ch1_s6_headcount = False
default ch1_s6_notes = False

init python:
    CH1_STAGE_META = {
        1: ("雨中山门", "1937年9月21日  午后", "ch1 gate"),
        2: ("寺院与学堂", "1937年9月21日  傍晚", "ch1 courtyard"),
        3: ("九月二十七日", "1937年9月27日  清晨", "ch1 classroom"),
        4: ("导师名簿", "1937年9月下旬  午后", "ch1 mentor_room"),
        5: ("迟到的家书", "1937年10月至11月", "ch1 mail_corridor"),
        6: ("把课表折起来", "1937年11月中下旬  夜", "ch1 departure"),
    }

    CH1_STAGE_TASKS = {
        1: [
            ("register", "找到报到处", "ch1_s1_register", (240, 265)),
            ("luggage", "协助清理行李", "ch1_s1_luggage", (680, 390)),
            ("notices", "查看临时告示", "ch1_s1_notices", (1090, 245)),
        ],
        2: [
            ("dorm", "确认僧舍", "ch1_s2_dorm", (180, 285)),
            ("classroom", "安排课堂", "ch1_s2_classroom", (560, 220)),
            ("study", "划出自习处", "ch1_s2_study", (900, 390)),
            ("passage", "保留公共通道", "ch1_s2_passage", (1180, 205)),
        ],
        3: [
            ("desks", "垫稳课桌", "ch1_s3_desks", (185, 245)),
            ("blackboard", "固定黑板", "ch1_s3_blackboard", (570, 190)),
            ("window", "调整窗扇", "ch1_s3_window", (950, 260)),
            ("books", "移开书箱", "ch1_s3_books", (1180, 430)),
        ],
        4: [
            ("roll", "核对生活名簿", "ch1_s4_roll", (275, 270)),
            ("health", "记录夜咳情况", "ch1_s4_health", (720, 360)),
            ("supplies", "整理御寒需求", "ch1_s4_supplies", (1110, 230)),
        ],
        5: [
            ("mail", "领取家书", "ch1_s5_mail", (260, 300)),
            ("table", "协助搬桌", "ch1_s5_table", (710, 395)),
            ("lamp", "整理灯下自习处", "ch1_s5_lamp", (1120, 255)),
        ],
        6: [
            ("return", "归还风灯与桌凳", "ch1_s6_return", (190, 305)),
            ("board", "整理最后一面黑板", "ch1_s6_board", (540, 205)),
            ("headcount", "核对人员与行李", "ch1_s6_headcount", (900, 390)),
            ("notes", "防水封装课程记录", "ch1_s6_notes", (1190, 245)),
        ],
    }

    def ch1_stage_complete(stage):
        return all(getattr(store, entry[2]) for entry in CH1_STAGE_TASKS[stage])

    def ch1_add_unique(target, value):
        if value not in target:
            target.append(value)


transform ch1_portrait:
    xpos 45
    yalign 1.0
    zoom 1.45
    alpha 0.0
    linear 0.22 alpha 1.0
    linear 2.5 yoffset -3
    linear 2.5 yoffset 0
    repeat

transform ch1_portrait_tall:
    xpos 45
    yalign 1.0
    zoom 0.70
    alpha 0.0
    linear 0.22 alpha 1.0
    linear 2.5 yoffset -3
    linear 2.5 yoffset 0
    repeat

screen ch1_character():
    zorder 5
    if ch1_sprite:
        if "miaoding" in ch1_sprite or "mentor" in ch1_sprite:
            add ch1_sprite at ch1_portrait_tall
        else:
            add ch1_sprite at ch1_portrait

screen ch1_status_panel():
    zorder 30

    hbox:
        xpos 1540
        ypos 22
        spacing 8
        textbutton "存档" action ShowMenu("save") xsize 80 ysize 54 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "读档" action ShowMenu("load") xsize 80 ysize 54 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "回顾" action ShowMenu("history") xsize 80 ysize 54 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "设置" action ShowMenu("preferences") xsize 80 ysize 54 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"

    frame:
        xpos 1535
        ypos 92
        xsize 365
        ysize 590
        background "images/chapter01/ui/task_panel.png"
        padding (30, 28)
        vbox:
            spacing 10
            text "第一章  西天目山" size 27 color "#dfc480"
            text "[ch1_stage_date]" size 17 color "#aeb6b1"
            text "[ch1_stage_title]" size 22 color "#e9ddc4"
            null height 6
            text "当前目标" size 24 color "#e8d6a7"
            text "[ch1_task_hint]" size 18 color "#f2eee6" xmaximum 305
            null height 4
            text "待办任务" size 22 color "#e8d6a7"
            for task_id, task_name, flag_name, position in CH1_STAGE_TASKS[ch1_stage]:
                $ task_done = getattr(store, flag_name)
                text (("完成  " if task_done else "待办  ") + task_name) size 17 color ("#b9d49e" if task_done else "#b9b2a2")

    frame:
        xpos 1535
        ypos 696
        xsize 365
        ysize 300
        background "images/chapter01/ui/inventory_panel.png"
        padding (16, 16)
        vbox:
            spacing 10
            hbox:
                spacing 4
                if ch1_allow_return:
                    textbutton "返回任务" action Jump("ch1_stage_hub") xsize 110 ysize 44 background "images/chapter01/ui/tab_active.png" text_size 16 text_color "#f0d799"
                else:
                    textbutton "任务" action NullAction() xsize 110 ysize 44 background "images/chapter01/ui/tab_idle.png" text_size 18 text_color "#8f8064"
                textbutton "档案" action NullAction() xsize 105 ysize 44 background "images/chapter01/ui/tab_idle.png" text_size 18 text_color "#c3ad7c"
                textbutton "物件" action NullAction() xsize 105 ysize 44 background "images/chapter01/ui/tab_active.png" text_size 18 text_color "#f0d799"
            text "随身物件" size 20 color "#dfc480"
            if ch1_items:
                for item in ch1_items[-4:]:
                    text "[item]" size 16 color "#d8cfbd"
            else:
                text "尚未获得物件" size 16 color "#898a86"
            text "历史档案  [len(ch1_archives)] / 4" size 17 color "#c9b98b"

screen ch1_hud():
    use ch1_status_panel

screen ch1_task_board():
    modal True
    add CH1_STAGE_META[ch1_stage][2]

    vbox:
        xpos 48
        ypos 42
        spacing 4
        text "[ch1_stage_title]":
            size 36
            color "#ead49e"
            outlines [(3, "#11130f", 0, 0)]
        text "点击场景标记完成待办；探索界面不会显示人物。":
            size 18
            color "#e1ddd1"
            outlines [(2, "#11130f", 0, 0)]

    for task_id, task_name, flag_name, position in CH1_STAGE_TASKS[ch1_stage]:
        $ task_done = getattr(store, flag_name)
        button:
            xpos position[0]
            ypos position[1]
            xsize 250
            ysize 88
            background Solid("#694820df")
            hover_background Solid("#8a642ce8")
            action Return(task_id)
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 2
                text task_name size 21 color "#f0e6cf" xalign 0.5
                text ("已完成" if task_done else "点击调查") size 15 color ("#b9d49e" if task_done else "#ead095") xalign 0.5

    if ch1_stage_complete(ch1_stage):
        textbutton "继续本幕":
            xpos 1130
            ypos 825
            xsize 350
            ysize 82
            action Return("continue")
            background Solid("#2a2115e8")
            hover_background Solid("#76582ee8")
            text_size 25
            text_color "#f2d797"

    use ch1_status_panel


label ch1_set_stage(stage, hint):
    $ ch1_stage = stage
    $ ch1_stage_title = CH1_STAGE_META[stage][0]
    $ ch1_stage_date = CH1_STAGE_META[stage][1]
    $ ch1_task_hint = hint
    return


label ch1_start:
    $ ch1_stage = 1
    $ ch1_items = []
    $ ch1_archives = []
    $ ch1_companion_care = 0
    $ ch1_record_accuracy = 0
    $ ch1_first_choice = ""
    $ ch1_mail_choice = ""
    $ ch1_s1_register = False
    $ ch1_s1_luggage = False
    $ ch1_s1_notices = False
    $ ch1_s2_dorm = False
    $ ch1_s2_classroom = False
    $ ch1_s2_study = False
    $ ch1_s2_passage = False
    $ ch1_s3_desks = False
    $ ch1_s3_blackboard = False
    $ ch1_s3_window = False
    $ ch1_s3_books = False
    $ ch1_s4_roll = False
    $ ch1_s4_health = False
    $ ch1_s4_supplies = False
    $ ch1_s5_mail = False
    $ ch1_s5_table = False
    $ ch1_s5_lamp = False
    $ ch1_s6_return = False
    $ ch1_s6_board = False
    $ ch1_s6_headcount = False
    $ ch1_s6_notes = False

    call ch1_set_stage(1, "完成报到，并协助新生安置行李") from _call_ch1_set_stage
    call screen chapter_title_card(
        "images/chapter01/backgrounds/temple_courtyard_rain.png",
        "第一章",
        "西天目山",
        "寺庙里的大学",
        "1937年9月21日  禅源寺"
    )

    scene ch1 gate
    with dissolve
    show screen ch1_hud
    $ ch1_sprite = "ch1 shen_alert"
    show screen ch1_character
    narrator_day1 "雨从山雾里落下来。石阶被新生们的鞋底踩得发亮，木箱与铺盖沿着山门一侧排开。"
    narrator_day1 "九月十四日，学校与寺方商定借用房舍。九月二十一日，一年级学生陆续迁入西天目山禅源寺。"
    ch1_shen "入学通知写着浙江大学。可我真正抵达的地方，是一座藏在山雨里的寺院。"
    $ ch1_sprite = "ch1 xu_worried"
    ch1_xu "劳驾，替我扶一下箱盖。山路一颠，铜扣松了。"
    $ ch1_sprite = "ch1 shen_recording"
    ch1_shen "箱扣已经松了。到了寺里，我替你找一截细绳。"
    $ ch1_sprite = "ch1 xu_soft"
    ch1_xu "多谢。箱中没有贵重之物，只有几册书。只是书若散了，反倒比旁的东西更难收拾。"
    narrator_day1 "她叫许南枝，也是一年级新生。我们在报到前先认识了彼此的书箱。"

    menu:
        "山门前越来越拥挤，我先做什么？"
        "替许南枝修好箱扣":
            $ ch1_first_choice = "repair"
            $ ch1_companion_care += 2
            $ day1_trust += 1
            $ ch1_sprite = "ch1 xu_repairing"
            ch1_xu "绳结别打死。往后若再迁，还要重新拆开。"
        "先清理湿滑的石阶":
            $ ch1_first_choice = "steps"
            $ ch1_companion_care += 1
            $ day1_morale += 1
            $ ch1_sprite = "ch1 shen_alert"
            ch1_shen "先让后面的人安全上来。箱子可以晚一点搬。"
        "先查看课表与住宿名册":
            $ ch1_first_choice = "notice"
            $ ch1_record_accuracy += 2
            $ day1_records += 1
            $ ch1_sprite = "ch1 shen_recording"
            ch1_shen "先弄清每个人该到哪里，才不会把山门堵得更乱。"

    narrator_day1 "寺门内传来木鱼声。我们压低说话声，把行李移到廊下。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_stage_hub


label ch1_stage_hub:
    $ ch1_allow_return = False
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    call screen ch1_task_board
    $ ch1_selected_task = _return
    if ch1_selected_task == "continue":
        if ch1_stage == 1:
            jump ch1_scene2_open
        elif ch1_stage == 2:
            jump ch1_scene3_open
        elif ch1_stage == 3:
            jump ch1_scene3_class
        elif ch1_stage == 4:
            jump ch1_scene4_review
        elif ch1_stage == 5:
            jump ch1_scene5_choice
        else:
            jump ch1_scene6_end
    jump expression "ch1_task_{}_{}".format(ch1_stage, ch1_selected_task)


label ch1_event_begin(background, sprite):
    scene expression background
    with dissolve
    show screen ch1_hud
    $ ch1_allow_return = True
    $ ch1_sprite = sprite
    show screen ch1_character
    return

label ch1_event_end:
    $ ch1_allow_return = False
    $ ch1_sprite = ""
    hide screen ch1_character
    hide screen ch1_hud
    jump ch1_stage_hub


# 第一幕：雨中山门
label ch1_task_1_register:
    call ch1_event_begin("ch1 gate", "ch1 shen_recording") from _call_ch1_event_begin
    if ch1_s1_register:
        ch1_shen "姓名、籍贯与住宿位置都已核过。我的名字旁有一枚新落下的墨点。"
        jump ch1_event_end
    narrator_day1 "报到桌设在山门内侧。纸页被风吹得起伏，负责登记的同学用镇纸压住名册。"
    ch1_freshman "沈砚舟，工学院一年级。这里签名，再去西侧厢房领住宿号。"
    ch1_shen "许南枝的名字也在下一页。她的箱子先放在二号廊柱边。"
    narrator_day1 "我把自己的去处与同伴的行李位置一并记进蓝布笔记本。"
    $ ch1_s1_register = True
    $ ch1_record_accuracy += 1
    $ ch1_add_unique(ch1_archives, "西天目山办学")
    narrator_day1 "历史档案已收录：西天目山办学。"
    jump ch1_event_end

label ch1_task_1_luggage:
    call ch1_event_begin("ch1 gate", "ch1 xu_repairing") from _call_ch1_event_begin_1
    if ch1_s1_luggage:
        ch1_xu "三位同学的行李都已离开石阶。下雨时，这条路必须一直能走。"
        jump ch1_event_end
    narrator_day1 "三名后来抵达的新生把铺盖搁在石阶中央。雨水正从高处往下淌。"
    ch1_xu "我扶箱子，你把铺盖先送到檐下。不要堵住寺中原有的路。"
    ch1_shen "先搬最下面那件。上面的两捆若滑落，会把人带下台阶。"
    narrator_day1 "我们来回三趟，终于把行李按住宿号分在廊下。"
    $ ch1_s1_luggage = True
    $ ch1_companion_care += 1
    jump ch1_event_end

label ch1_task_1_notices:
    call ch1_event_begin("ch1 gate", "ch1 xu_checking") from _call_ch1_event_begin_2
    if ch1_s1_notices:
        ch1_xu "课表、住宿名册与临时校牌的位置都已记下。"
        jump ch1_event_end
    narrator_day1 "一块临时校牌倚在墙边。旁边贴着课程预告、住宿名册与寺院通行说明。"
    ch1_xu "二十七日开课。教室地点尚未全部确定。"
    ch1_shen "先把时间抄下。地点可以再改，开课的日期不能含糊。"
    $ ch1_s1_notices = True
    $ ch1_record_accuracy += 1
    $ ch1_add_unique(ch1_items, "临时课表")
    narrator_day1 "获得物件：临时课表。"
    jump ch1_event_end


# 第二幕：寺院与学堂
label ch1_scene2_open:
    call ch1_set_stage(2, "在不扰乱寺院秩序的前提下划分临时校园") from _call_ch1_set_stage_1
    scene ch1 courtyard
    with fade
    show screen ch1_hud
    $ ch1_sprite = "ch1 miaoding_explain"
    show screen ch1_character
    ch1_miaoding "寺中有寺中的功课，诸位也有诸位的功课。同在一处，彼此都应留一条可行之路。"
    $ ch1_sprite = "ch1 xu_firm"
    ch1_xu "我们把桌凳移到西廊，诵经前不经过正殿。宿舍用水也按时段分开。"
    $ ch1_sprite = "ch1 shen_recording"
    ch1_shen "还要留出夜间通道。若灯灭了，也不能让人被木箱绊住。"
    narrator_day1 "寺院不是一块空地。临时校园必须嵌进原有的生活，而不是把它挤走。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_stage_hub

label ch1_task_2_dorm:
    call ch1_event_begin("ch1 dormitory", "ch1 xu_checking") from _call_ch1_event_begin_3
    if ch1_s2_dorm:
        ch1_xu "铺位、用水时段与夜间出口都已写在门边。"
        jump ch1_event_end
    narrator_day1 "东侧厢房被借作僧舍。床位不够，一部分人只能铺草席。"
    ch1_shen "靠窗处漏雨，书箱要垫高；中间留一人宽，夜里不能堵死。"
    ch1_xu "我去把用水时段补在住宿名册后面。"
    $ ch1_s2_dorm = True
    jump ch1_event_end

label ch1_task_2_classroom:
    call ch1_event_begin("ch1 courtyard", "ch1 miaoding_calm") from _call_ch1_event_begin_4
    if ch1_s2_classroom:
        ch1_miaoding "西廊的桌凳不会影响早晚课，安排妥当。"
        jump ch1_event_end
    narrator_day1 "西廊采光较好，离正殿也有一段距离。几名学生正在试摆桌凳。"
    ch1_miaoding "晨昏诵念之时，诸位从侧门出入即可。"
    ch1_shen "讲课声也尽量压低。这里先是一座寺院，才又成为我们的教室。"
    $ ch1_s2_classroom = True
    jump ch1_event_end

label ch1_task_2_study:
    call ch1_event_begin("ch1 courtyard", "ch1 xu_firm") from _call_ch1_event_begin_5
    if ch1_s2_study:
        ch1_xu "自习处已移到西厢，避开正殿早晚功课。"
        jump ch1_event_end
    narrator_day1 "原定的自习角离正殿太近，夜里灯火与脚步都会经过僧众的功课处。"
    ch1_xu "西厢虽小，却能关窗挡风。桌子排成两列，仍坐得下。"
    ch1_shen "油灯集中保管。最后离开的人负责熄灯和检查火星。"
    $ ch1_s2_study = True
    $ ch1_record_accuracy += 1
    jump ch1_event_end

label ch1_task_2_passage:
    call ch1_event_begin("ch1 courtyard", "ch1 shen_alert") from _call_ch1_event_begin_6
    if ch1_s2_passage:
        ch1_shen "木箱已贴墙放稳，山门到厢房的公共通道保持畅通。"
        jump ch1_event_end
    narrator_day1 "两排书箱横在廊下。白天尚能绕开，一旦熄灯便十分危险。"
    ch1_shen "把箱号朝外，沿墙单排。风灯挂在转角处，遇事谁都能取到。"
    ch1_miaoding "留路，是为自己，也是为旁人。"
    $ ch1_s2_passage = True
    $ ch1_companion_care += 1
    $ ch1_add_unique(ch1_items, "寺院风灯")
    narrator_day1 "获得物件：寺院风灯。"
    jump ch1_event_end


# 第三幕：九月二十七日
label ch1_scene3_open:
    call ch1_set_stage(3, "在第一堂课开始前完成临时教室准备") from _call_ch1_set_stage_2
    scene ch1 classroom
    with fade
    show screen ch1_hud
    $ ch1_sprite = "ch1 shen_alert"
    show screen ch1_character
    narrator_day1 "九月二十七日清晨。晨钟之后，第一堂课将在西廊侧厅开始。"
    ch1_shen "课桌会晃，黑板还没固定，迎风的窗扇一直作响。"
    $ ch1_sprite = "ch1 xu_firm"
    ch1_xu "还有一箱教材堵在后门。先生来之前，我们分头处理。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_stage_hub

label ch1_task_3_desks:
    call ch1_event_begin("ch1 classroom", "ch1 xu_repairing") from _call_ch1_event_begin_7
    if ch1_s3_desks:
        ch1_xu "两张桌子都已垫稳，写字时不会再晃。"
        jump ch1_event_end
    narrator_day1 "两张旧桌短了一角。许南枝把废纸折成厚垫，我扶住桌面。"
    ch1_xu "别用课程预告。拿写坏的登记纸，折四层正好。"
    $ ch1_s3_desks = True
    jump ch1_event_end

label ch1_task_3_blackboard:
    call ch1_event_begin("ch1 classroom", "ch1 shen_alert") from _call_ch1_event_begin_8
    if ch1_s3_blackboard:
        ch1_shen "黑板已用绳索固定在木架上，没有钉伤寺院墙面。"
        jump ch1_event_end
    narrator_day1 "黑板斜靠墙边，一写就会滑。墙面不能钉钉，我们只能另想办法。"
    ch1_shen "用两根竹竿搭架，再以绳索绑紧。底部压石，不碰原墙。"
    $ ch1_s3_blackboard = True
    $ ch1_record_accuracy += 1
    jump ch1_event_end

label ch1_task_3_window:
    call ch1_event_begin("ch1 classroom", "ch1 xu_checking") from _call_ch1_event_begin_9
    if ch1_s3_window:
        ch1_xu "迎风窗已合到一半，雨进不来，桌面仍有足够光线。"
        jump ch1_event_end
    narrator_day1 "完全关窗会使室内昏暗，全开又会让雨丝落在讲义上。"
    ch1_xu "合上迎风那扇，背风处留一道缝。这样不用白天点灯。"
    $ ch1_s3_window = True
    jump ch1_event_end

label ch1_task_3_books:
    call ch1_event_begin("ch1 classroom", "ch1 shen_recording") from _call_ch1_event_begin_10
    if ch1_s3_books:
        ch1_shen "教材箱已移到侧墙，后门与通道都空出来了。"
        jump ch1_event_end
    narrator_day1 "最后一箱教材横在后门。我们按班级拆分，先把当天要用的讲义摆上桌。"
    ch1_shen "箱号和领取数量一并记下，散课后再逐本核对。"
    $ ch1_s3_books = True
    jump ch1_event_end

label ch1_scene3_class:
    scene ch1 classroom
    with dissolve
    show screen ch1_hud
    $ ch1_allow_return = False
    $ ch1_sprite = "ch1 mentor_explain"
    show screen ch1_character
    narrator_day1 "先生进门时，教室里没有一件东西还在摇晃。"
    ch1_tutor "诸位今日坐在寺院里，并不表示你们少上了一天大学。"
    ch1_tutor "恰恰相反，从今日起，你们要比寻常时候更明白：上课为何不能轻易中断。"
    narrator_day1 "粉笔在黑板上写下日期：九月二十七日。"
    $ ch1_sprite = "ch1 xu_soft"
    ch1_xu "外面的钟声与先生的讲课声，竟不相扰。"
    $ ch1_sprite = "ch1 shen_listening"
    ch1_shen "也许因为它们都在提醒人，时辰已经到了。"
    $ ch1_add_unique(ch1_archives, "禅源寺开课")
    narrator_day1 "历史档案已收录：九月二十七日开课。"
    $ ch1_sprite = ""
    hide screen ch1_character
    hide screen ch1_hud
    jump ch1_scene4_open


# 第四幕：导师名簿
label ch1_scene4_open:
    call ch1_set_stage(4, "协助导师把学生的生活困难记录清楚") from _call_ch1_set_stage_3
    scene ch1 mentor_room
    with fade
    show screen ch1_hud
    $ ch1_sprite = "ch1 mentor_recording"
    show screen ch1_character
    narrator_day1 "开课后，导师制在西天目山推行。导师不仅过问功课，也查看新生能否安稳生活。"
    ch1_tutor "先把名簿中的情况分清：立即处理、继续观察、可由同伴协助。"
    $ ch1_sprite = "ch1 shen_recording"
    ch1_shen "三人缺厚被，一人没有家书，两人夜间咳嗽，还有一人没有合脚的鞋袜。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_stage_hub

label ch1_task_4_roll:
    call ch1_event_begin("ch1 mentor_room", "ch1 shen_recording") from _call_ch1_event_begin_11
    if ch1_s4_roll:
        ch1_shen "住宿、家信与鞋袜情况已逐项核对，没有只写一个模糊的‘困难’。"
        jump ch1_event_end
    narrator_day1 "我按住宿号重新核对名簿，把‘无家书’与‘缺少御寒物’分成不同栏。"
    ch1_tutor "记录越具体，处理时越不会遗漏。"
    $ ch1_s4_roll = True
    $ ch1_record_accuracy += 1
    jump ch1_event_end

label ch1_task_4_health:
    call ch1_event_begin("ch1 mentor_room", "ch1 mentor_recording") from _call_ch1_event_begin_12
    if ch1_s4_health:
        ch1_tutor "夜咳的两名学生已安排复查，暂不与普通缺被混在一栏。"
        jump ch1_event_end
    narrator_day1 "两名学生只在夜里咳嗽。我们补记发作时间、铺位和是否发热。"
    ch1_shen "先观察一夜，若加重便立即送医；同时把铺位移离漏雨窗边。"
    $ ch1_s4_health = True
    $ ch1_companion_care += 1
    jump ch1_event_end

label ch1_task_4_supplies:
    call ch1_event_begin("ch1 mentor_room", "ch1 xu_checking") from _call_ch1_event_begin_13
    if ch1_s4_supplies:
        ch1_xu "厚被、鞋袜与修锁用具已经分开登记，能借的先借，需购的再报。"
        jump ch1_event_end
    ch1_xu "这些琐事，也在导师职责之内么？"
    $ ch1_sprite = "ch1 mentor_explain"
    ch1_tutor "人若久不得安眠，再好的文章也读不进去。治学不能只问案头之书，也要顾念读书之人。"
    $ ch1_s4_supplies = True
    jump ch1_event_end

label ch1_scene4_review:
    scene ch1 mentor_room
    with dissolve
    show screen ch1_hud
    $ ch1_sprite = "ch1 xu_worried"
    show screen ch1_character
    narrator_day1 "最后剩下许南枝坏掉的箱锁。它不影响今晚休息，却会在下一次搬运行李时留下隐患。"
    menu:
        "这件事应归入哪一类？"
        "立即处理：今晚就找人修锁":
            $ ch1_companion_care += 2
            $ day1_trust += 1
            ch1_xu "并非最急，却谢谢你没有把它忘在名簿末尾。"
        "继续观察：等锁彻底坏掉再处理":
            $ ch1_record_accuracy -= 1
            ch1_tutor "若已经看见风险，便不该用‘观察’代替处理。重新分类。"
        "同伴协助：先用细绳固定并登记修理":
            $ ch1_record_accuracy += 2
            $ ch1_companion_care += 1
            $ day1_records += 1
            ch1_xu "这最合适。今天能用，也留下之后修理的记录。"

    $ ch1_sprite = "ch1 shen_recording"
    ch1_shen "我从前只在这本笔记里记公式。"
    $ ch1_sprite = "ch1 mentor_explain"
    ch1_tutor "公式若只替自己保存，仍嫌太窄。把人的处境也记清楚，它才真正成为一册大学笔记。"
    $ ch1_add_unique(ch1_items, "导师名簿摘记")
    $ ch1_add_unique(ch1_archives, "西天目山导师制")
    narrator_day1 "获得物件：导师名簿摘记。历史档案已收录：西天目山导师制。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_scene5_open


# 第五幕：迟到的家书
label ch1_scene5_open:
    call ch1_set_stage(5, "领取邮件，并维持灯下自习的日常") from _call_ch1_set_stage_4
    scene ch1 mail_corridor
    with fade
    show screen ch1_hud
    $ ch1_sprite = "ch1 shen_sad_letter"
    show screen ch1_character
    narrator_day1 "十月以后，山路上的邮件常常迟到。我的信封上只有八个字：家中暂安，汝在山中安心求学。"
    $ ch1_sprite = "ch1 xu_worried"
    narrator_day1 "许南枝的格子仍是空的。她只看了一眼，便转身去扶自习桌。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_stage_hub

label ch1_task_5_mail:
    call ch1_event_begin("ch1 mail_corridor", "ch1 shen_sad_letter") from _call_ch1_event_begin_14
    if ch1_s5_mail:
        ch1_shen "已领取的信件均按姓名登记，未到的没有擅自写成坏消息。"
        jump ch1_event_end
    ch1_messenger "这批信只到十二封。下一趟何时上山，还没有准信。"
    ch1_shen "请把未领取名单留一份。消息不确定，也要把不确定写清楚。"
    $ ch1_s5_mail = True
    $ ch1_record_accuracy += 1
    jump ch1_event_end

label ch1_task_5_table:
    call ch1_event_begin("ch1 mail_corridor", "ch1 xu_soft") from _call_ch1_event_begin_15
    if ch1_s5_table:
        ch1_xu "桌子已经抬到灯下。今晚仍可按原定时间自习。"
        jump ch1_event_end
    narrator_day1 "一张自习桌被雨水浸湿，需要换到廊内。许南枝抬住一端。"
    ch1_xu "不必先问信的事。替我抬住这一端便好。"
    ch1_shen "好。先把桌腿绕过柱子，别碰到灯。"
    $ ch1_s5_table = True
    $ ch1_companion_care += 1
    jump ch1_event_end

label ch1_task_5_lamp:
    call ch1_event_begin("ch1 mail_corridor", "ch1 shen_recording") from _call_ch1_event_begin_16
    if ch1_s5_lamp:
        ch1_shen "风灯、灭火砂与最后离开者的名字都已安排。"
        jump ch1_event_end
    narrator_day1 "风从廊口灌进来，灯焰不断偏向信纸。"
    ch1_shen "把灯移到柱后，旁边放一盆灭火砂。最后离开的人负责归还风灯。"
    $ ch1_s5_lamp = True
    jump ch1_event_end

label ch1_scene5_choice:
    scene ch1 mail_corridor
    with dissolve
    show screen ch1_hud
    $ ch1_sprite = "ch1 xu_worried"
    show screen ch1_character
    ch1_xu "没有信，未必便是坏消息。山路遥远，迟误也是常事。不必宽慰我，替我抬住这一端便好。"
    menu:
        "我怎样回应？"
        "不追问，只帮她把桌子抬稳":
            $ ch1_mail_choice = "restraint"
            $ ch1_companion_care += 2
            $ day1_trust += 1
            $ ch1_sprite = "ch1 xu_soft"
            ch1_xu "谢谢。等信来时，我自然会告诉你。"
        "把自己的家书递给她看":
            $ ch1_mail_choice = "share"
            $ ch1_companion_care += 1
            ch1_shen "只有一句平安。至少说明路虽然慢，信仍能进山。"
        "去问送信人下一趟邮件时间":
            $ ch1_mail_choice = "action"
            $ ch1_record_accuracy += 1
            $ day1_records += 1
            ch1_shen "我不替消息下结论，只去问下一趟邮件何时可能到。"

    narrator_day1 "雨敲着瓦面。没有新的消息，晚自习仍按课表开始。"
    $ ch1_add_unique(ch1_items, "迟到的家书")
    narrator_day1 "获得物件：迟到的家书。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_scene6_open


# 第六幕：把课表折起来
label ch1_scene6_open:
    call ch1_set_stage(6, "恢复寺院原貌，清点师生并封装课程记录") from _call_ch1_set_stage_5
    scene ch1 departure
    with fade
    show screen ch1_hud
    $ ch1_sprite = "ch1 shen_alert"
    show screen ch1_character
    narrator_day1 "十一月中下旬，浙西形势转急。学校通知一年级学生离开西天目山，前往建德与本部会合。"
    $ ch1_sprite = "ch1 xu_departing"
    ch1_xu "我们才将这里安顿下来。"
    $ ch1_sprite = "ch1 mentor_explain"
    ch1_tutor "正因已经安顿过一次，下一次便不会全然无措。"
    narrator_day1 "这一次，我们不仅要收拾自己的行李，还要把借来的寺院完整归还。"
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""
    jump ch1_stage_hub

label ch1_task_6_return:
    call ch1_event_begin("ch1 departure", "ch1 xu_firm") from _call_ch1_event_begin_17
    if ch1_s6_return:
        ch1_xu "风灯、桌凳与铺板都已按寺方清单归还。"
        jump ch1_event_end
    narrator_day1 "我们把西廊桌凳叠好，将寺院风灯交回妙定法师，并清扫铺位。"
    ch1_miaoding "来时留路，走时复原。诸位做得周全。"
    $ ch1_s6_return = True
    jump ch1_event_end

label ch1_task_6_board:
    call ch1_event_begin("ch1 departure", "ch1 shen_recording") from _call_ch1_event_begin_18
    if ch1_s6_board:
        ch1_shen "黑板已擦净，最后一道题另抄进笔记，没有损坏寺院墙面。"
        jump ch1_event_end
    narrator_day1 "黑板上还留着下午的最后一道习题。有人举起湿布，又迟迟没有落下。"
    ch1_shen "把题目抄进笔记，再擦干净。课堂不能留在借来的墙上，却可以继续留在我们手里。"
    $ ch1_s6_board = True
    $ ch1_record_accuracy += 1
    jump ch1_event_end

label ch1_task_6_headcount:
    call ch1_event_begin("ch1 departure", "ch1 shen_alert") from _call_ch1_event_begin_19
    if ch1_s6_headcount:
        ch1_shen "约二百五十名新生按组核点，人员、书箱与铺盖都已对应。"
        jump ch1_event_end
    narrator_day1 "班级、住宿组与行李号逐项核对。名字必须由本人或同组同学回应。"
    ch1_shen "箱子可以晚到，人不能被名册上的一个勾替代。再念一遍最后一组。"
    $ ch1_s6_headcount = True
    $ ch1_companion_care += 1
    jump ch1_event_end

label ch1_task_6_notes:
    call ch1_event_begin("ch1 departure", "ch1 xu_departing") from _call_ch1_event_begin_20
    if ch1_s6_notes:
        ch1_xu "课表、导师名簿摘记与个人笔记均已包好，箱外标明防水。"
        jump ch1_event_end
    narrator_day1 "油布不够覆盖所有行李。课程记录、衣物与日用品必须重新排出次序。"
    menu:
        "最后一块油布应当包住什么？"
        "课表、导师名簿与个人笔记":
            $ ch1_record_accuracy += 2
            $ day1_records += 1
            ch1_xu "这些记录能让下一处课堂不必从零开始。"
        "所有人的衣物，各取最上面一件":
            $ ch1_companion_care += 1
            ch1_shen "衣物仍需照顾，但可以分进已有铺盖；记录无法重抄。"
        "把油布留作路上临时避雨":
            $ day1_morale += 1
            ch1_xu "留一角作应急，其余仍包课程记录。两件事都不能全放弃。"
    $ ch1_s6_notes = True
    $ ch1_add_unique(ch1_items, "油布封装的蓝布笔记")
    jump ch1_event_end

label ch1_scene6_end:
    scene ch1 departure
    with dissolve
    show screen ch1_hud
    $ ch1_allow_return = False
    $ ch1_sprite = "ch1 xu_departing"
    show screen ch1_character
    ch1_xu "若到了建德，还要再迁呢？"
    $ ch1_sprite = "ch1 mentor_explain"
    ch1_tutor "那么，便再将课表挂起来。"
    $ ch1_sprite = "ch1 shen_determined"
    narrator_day1 "教室恢复了原样。最后一盏灯熄灭前，一片银杏叶从窗外落进我的蓝布笔记。"
    ch1_shen "山门会留在身后，第一堂课不会。"
    narrator_day1 "1937年11月中下旬，约二百五十名一年级学生由西天目山转赴建德。"
    narrator_day1 "与此同时，杭州本部正在设法把一所大学装上船。"
    $ ch1_add_unique(ch1_items, "西天目山银杏叶")
    $ ch1_add_unique(ch1_archives, "西天目山迁往建德")
    hide screen ch1_character
    hide screen ch1_hud
    $ ch1_sprite = ""

    $ day1_finish_chapter(1)
    scene black
    with fade
    centered "{size=54}第一章完成{/size}\n\n{size=30}第二章  江干码头  已解锁{/size}\n\n{size=21}临时校园完整归还  师生名册无遗漏  课程记录连续{/size}"
    pause 2.2
    jump day1_map_hub
