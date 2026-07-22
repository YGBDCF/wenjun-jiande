# 第二至第六章共用的场景热点系统。
default ch2_spots = []
default ch3_spots = []
default ch5_spots = []
default ch6_spots = []

screen historical_location_map(background_image, title_text, spots, completed_spots):
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
        button:
            xpos sx ypos sy xsize sw ysize sh
            background Solid("#00000000")
            hover_background Solid("#c89a3638")
            action (NullAction() if spot_id in completed_spots else Return(spot_id))
            text (spot_name + ("  已完成" if spot_id in completed_spots else "")):
                xalign 0.5 yalign 0.88
                size 21
                color ("#b9d49e" if spot_id in completed_spots else "#f1d590")
                outlines [(2, "#17130d", 0, 0)]

    textbutton "返回章节地图":
        xpos 48 ypos 1000
        text_size 20
        text_color "#d5be89"
        background Solid("#0b1111cc")
        action Jump("day1_map_hub")

label ch2_explore_hub:
    if len(ch2_spots) >= 3:
        jump ch2_story
    call screen historical_location_map("bg ch2", "江干码头  撤离现场", [("wharf", "登船队伍", 260, 360, 330, 300), ("crates", "待核木箱区", 650, 390, 350, 280), ("boat", "首批船舱", 1110, 330, 330, 330)], ch2_spots)
    if _return == "wharf":
        narrator_day1 "学生按名册排队，老人和孩子被安排在靠里的位置。"
        sy "真正需要先数清的不是箱子，而是人。"
    elif _return == "crates":
        narrator_day1 "教材、仪器与生活物资混在雨中的木箱之间。"
        sy "没有核对的箱子先留在岸上，不能把混乱直接装船。"
    else:
        oldzhou "重箱放中间，怕水的东西垫高。过了潮水就走不了。"
        sy "船舱的每一寸位置，都意味着一次取舍。"
    if _return not in ch2_spots:
        $ ch2_spots.append(_return)
    jump ch2_explore_hub

label ch3_explore_hub:
    if len(ch3_spots) >= 3:
        jump ch3_story
    call screen historical_location_map("bg ch3", "典籍运输船  检查现场", [("table", "封签核对台", 1020, 470, 370, 280), ("crates", "典籍木箱", 380, 300, 520, 390), ("gangplank", "换船跳板", 1120, 120, 360, 300)], ch3_spots)
    if _return == "table":
        sy "目录号、封签和馆藏印必须互相对应，不能只凭箱外的字。"
    elif _return == "crates":
        narrator_day1 "木箱被垫离湿地，油布边缘仍在向下滴水。"
        sy "先吸掉封签上的水，再检查绳结是否被动过。"
    else:
        oldzhou "跳板很滑。换船时每只箱子都必须有人接手。"
        sy "交接的时间和经手人也要写进记录。"
    if _return not in ch3_spots:
        $ ch3_spots.append(_return)
    jump ch3_explore_hub

label ch5_explore_hub:
    if len(ch5_spots) >= 3:
        jump ch5_story
    call screen historical_location_map("bg ch5", "梅城临时课堂  警报前", [("classroom", "课堂与教具", 170, 280, 540, 400), ("alley", "疏散出口", 770, 130, 390, 470), ("shelter", "临时避难处", 1190, 500, 300, 330)], ch5_spots)
    if _return == "classroom":
        sy "粉笔、课程笔记和小黑板都放在伸手可取的位置。"
    elif _return == "alley":
        yq "这条巷子最短，但雨后很滑。行动慢的人必须走在队伍中间。"
    else:
        narrator_day1 "避难处没有桌椅，却有一块能靠住小黑板的石墙。"
    if _return not in ch5_spots:
        $ ch5_spots.append(_return)
    jump ch5_explore_hub

label ch6_explore_hub:
    if len(ch6_spots) >= 4:
        jump ch6_story
    call screen historical_location_map("bg ch6", "浙江大学日报  编辑室", [("radio", "广播收听台", 70, 390, 350, 300), ("desk", "编辑桌", 500, 430, 470, 330), ("press", "印刷处", 980, 300, 310, 330), ("street", "街头分发", 1300, 180, 220, 470)], ch6_spots)
    if _return == "radio":
        sy "每条听到的消息都先记下时间，再标明是否听清。"
    elif _return == "desk":
        az "确认过的消息和传言必须分开放，标题也不能超过证据。"
    elif _return == "press":
        narrator_day1 "油墨、纸张和版面都有限，每一次改动都需要重新安排。"
    else:
        yq "报纸到了街上，就会影响居民今天怎样理解外面的战争。"
    if _return not in ch6_spots:
        $ ch6_spots.append(_return)
    jump ch6_explore_hub
