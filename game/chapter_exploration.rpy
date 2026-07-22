# 第二至第六章共用的场景热点系统。
default ch2_spots = []
default ch3_spots = []
default ch5_spots = []
default ch6_spots = []

screen historical_location_map(background_image, title_text, spots, completed_spots, unlocked_spots=None):
    modal True
    add background_image
    add Solid("#050a0b32")

    frame:
        xpos 48 ypos 38 xsize 610 ysize 116
        background Solid("#091010dd")
        padding (24, 17)
        vbox:
            text "[title_text]" size 31 color "#e4c982"
            text "点击画面中的地点进行调查" size 18 color "#c7c3b7"

    for spot_id, spot_name, sx, sy, sw, sh in spots:
        $ is_done = spot_id in completed_spots
        $ is_unlocked = unlocked_spots is None or spot_id in unlocked_spots
        button:
            xpos sx ypos sy xsize sw ysize sh
            background Solid("#00000000")
            hover_background (Solid("#c89a3638") if is_unlocked and not is_done else Solid("#00000000"))
            action (Return(spot_id) if is_unlocked and not is_done else NullAction())
            frame:
                xalign 0.5 yalign 0.82
                xminimum 190 yminimum 58
                padding (18, 10)
                background ("images/chapter01/ui/choice_hover.png" if is_unlocked and not is_done else "images/chapter01/ui/choice_idle.png")
                vbox:
                    xalign 0.5 yalign 0.5 spacing 2
                    text "[spot_name]":
                        xalign 0.5 size 21
                        color ("#b9d49e" if is_done else ("#777a76" if not is_unlocked else "#f1d590"))
                        outlines [(2, "#17130d", 0, 0)]
                    if is_done:
                        text "已完成" xalign 0.5 size 15 color "#9fbd88"
                    elif not is_unlocked:
                        text "尚未解锁" xalign 0.5 size 15 color "#747772"
                    else:
                        text "点击进入" xalign 0.5 size 15 color "#d3c49d"

    textbutton "返回章节地图":
        xpos 48 ypos 1000
        text_size 20 text_color "#d5be89"
        background Solid("#0b1111cc")
        action Jump("day1_map_hub")

label ch2_explore_hub:
    hide screen immersive_character
    if len(ch2_spots) >= 3:
        scene bg ch2
        show screen immersive_character
        jump ch2_story
    call screen historical_location_map("bg ch2", "江干码头  撤离现场", [("wharf", "登船队伍", 260, 360, 330, 300), ("crates", "待核木箱区", 650, 390, 350, 280), ("boat", "首批船舱", 1110, 330, 330, 330)], ch2_spots)
    if _return == "wharf":
        scene bg ch2 with dissolve
        $ immersive_pose = "tense"
        show screen immersive_character
        narrator_day1 "学生按名册排队，老人和孩子被安排在靠里的位置。"
        sy "真正需要先数清的不是箱子，而是人。"
    elif _return == "crates":
        scene ch2 crates with dissolve
        $ immersive_pose = "thoughtful"
        show screen immersive_character
        narrator_day1 "教材、仪器与生活物资混在雨中的木箱之间。"
        sy "没有核对的箱子先留在岸上，不能把混乱直接装船。"
    else:
        scene ch2 boat with dissolve
        $ immersive_pose = "determined"
        show screen immersive_character
        oldzhou "重箱放中间，怕水的东西垫高。过了潮水就走不了。"
        sy "船舱的每一寸位置，都意味着一次取舍。"
    if _return not in ch2_spots:
        $ ch2_spots.append(_return)
    hide screen immersive_character
    jump ch2_explore_hub

label ch3_explore_hub:
    hide screen immersive_character
    if len(ch3_spots) >= 3:
        scene bg ch3
        show screen immersive_character
        jump ch3_story
    call screen historical_location_map("bg ch3", "典籍运输船  检查现场", [("table", "封签核对台", 1020, 470, 370, 280), ("crates", "典籍木箱", 380, 300, 520, 390), ("gangplank", "换船跳板", 1120, 120, 360, 300)], ch3_spots)
    if _return == "table":
        scene ch3 seals with dissolve
        $ immersive_pose = "thoughtful"
        show screen immersive_character
        sy "目录号、封签和馆藏印必须互相对应，不能只凭箱外的字。"
    elif _return == "crates":
        scene bg ch3 with dissolve
        $ immersive_pose = "worried"
        show screen immersive_character
        narrator_day1 "木箱被垫离湿地，油布边缘仍在向下滴水。"
        sy "先吸掉封签上的水，再检查绳结是否被动过。"
    else:
        scene ch3 gangplank with dissolve
        $ immersive_pose = "determined"
        show screen immersive_character
        oldzhou "跳板很滑。换船时每只箱子都必须有人接手。"
        sy "交接时间和经手人也要写进记录。"
    if _return not in ch3_spots:
        $ ch3_spots.append(_return)
    hide screen immersive_character
    jump ch3_explore_hub

label ch5_explore_hub:
    hide screen immersive_character
    if len(ch5_spots) >= 3:
        scene bg ch5
        show screen immersive_character
        jump ch5_story
    call screen historical_location_map("bg ch5", "梅城临时课堂  警报前", [("classroom", "课堂与教具", 170, 280, 540, 400), ("alley", "疏散出口", 770, 130, 390, 470), ("shelter", "临时避难处", 1190, 500, 300, 330)], ch5_spots)
    if _return == "classroom":
        scene bg ch5 with dissolve
        $ immersive_pose = "calm"
        show screen immersive_character
        sy "粉笔、课程笔记和小黑板都放在伸手可取的位置。"
    elif _return == "alley":
        scene ch5 alley with dissolve
        $ immersive_pose = "tense"
        show screen immersive_character
        yq "这条巷子最短，但雨后很滑。行动慢的人必须走在队伍中间。"
    else:
        scene ch5 shelter with dissolve
        $ immersive_pose = "relieved"
        show screen immersive_character
        narrator_day1 "避难处没有桌椅，却有一面能靠住小黑板的石墙。"
    if _return not in ch5_spots:
        $ ch5_spots.append(_return)
    hide screen immersive_character
    jump ch5_explore_hub

label ch6_explore_hub:
    hide screen immersive_character
    if len(ch6_spots) >= 3:
        scene bg ch6
        show screen immersive_character
        jump ch6_story
    call screen historical_location_map("bg ch6", "《浙大日报》编辑室", [("radio", "广播收听台", 70, 390, 350, 300), ("desk", "编辑核实桌", 500, 430, 470, 330), ("press", "油印与分发", 1080, 260, 390, 420)], ch6_spots)
    if _return == "radio":
        scene ch6 radio with dissolve
        $ immersive_pose = "tense"
        show screen immersive_character
        sy "每条听到的消息都先记下时间，再标明是否听清。"
    elif _return == "desk":
        scene bg ch6 with dissolve
        $ immersive_pose = "thoughtful"
        show screen immersive_character
        az "确认过的消息和传言必须分开，标题也不能超过证据。"
    else:
        scene ch6 press with dissolve
        $ immersive_pose = "determined"
        show screen immersive_character
        narrator_day1 "油墨、纸张和版面都有限，每一次改动都需要重新安排。"
    if _return not in ch6_spots:
        $ ch6_spots.append(_return)
    hide screen immersive_character
    jump ch6_explore_hub
