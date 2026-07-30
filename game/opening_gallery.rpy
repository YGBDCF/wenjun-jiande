# ================================================================
# 开场随机历史画页
# 从六章正式场景图中随机抽取一张，并显示对应的历史知识。
# ================================================================

init python:
    import os

    CHAPTER_XINGKAI_FONT = (
        "C:/Windows/Fonts/STXINGKA.TTF"
        if os.path.exists("C:/Windows/Fonts/STXINGKA.TTF")
        else "SourceHanSansLite.ttf"
    )

    OPENING_HISTORY_CARDS = [
        # 第一章：西天目山
        ("images/chapter01/backgrounds/mountain_gate_registration.png", "西天目山禅源寺", "1937年9月21日前后，浙江大学一年级学生迁往西天目山禅源寺，在寺院中开始新的大学生活。"),
        ("images/chapter01/backgrounds/temple_courtyard_rain.png", "寺庙里的大学", "寺院的殿堂、僧舍与廊庑被临时改作教室和住处。校园可以迁移，教学仍要继续。"),
        ("images/chapter01/backgrounds/dormitory_rain.png", "临时僧舍", "初到西天目山时，学生需要自己安置行李、书册和铺位，潮湿与拥挤成为日常困难。"),
        ("images/chapter01/backgrounds/first_classroom.png", "山中的课堂", "浙大在西天目山维持授课，并在此推行导师制，让教师对新生的学习和生活给予具体指导。"),
        ("images/chapter01/backgrounds/mentor_register_room.png", "导师制", "导师制不只是安排课程，也帮助初入大学的学生在动荡环境中找到可以依靠的学习秩序。"),
        ("images/chapter01/backgrounds/mentor_radio_room.png", "来自杭州的消息", "师生通过广播、书信和来人不断了解杭州局势，并为可能再次迁移预作准备。"),
        ("images/chapter01/backgrounds/mail_corridor.png", "战时书信", "在交通和通信不稳定的年代，一封家书既是亲人的消息，也可能带来城市局势的变化。"),
        ("images/chapter01/backgrounds/departure_classroom.png", "再次启程", "1937年11月下旬，浙西形势趋紧，西天目山的一年级学生奉命前往建德与学校会合。"),

        # 第二章：江干码头
        ("images/chapter02/jianggan_wharf.png", "江干码头", "1937年11月，浙大师生和家属分批从杭州江干一带乘船西行，沿钱塘江和富春江前往建德。"),
        ("images/chapter02/crate_inspection.png", "把大学装进木箱", "随校迁移的不只有师生，还有图书、实验仪器、讲义、名册和维持教学所需的各种校产。"),
        ("images/chapter02/boat_cabin.png", "拥挤的船舱", "有限的船位要同时容纳人员与物资，装载次序、箱号记录和重量核对都关系到后续办学。"),
        ("images/chapter02/scenes/jianggan_loading.png", "离开杭州", "装船工作需要在紧张局势中进行。人员安全、精密仪器和教学资料必须同时得到照顾。"),
        ("images/chapter02/scenes/lost_manifest.png", "不能遗失的清单", "战时转运中，清单是确认人员、书箱与仪器去向的重要依据，少一页就可能失去一段线索。"),
        ("images/chapter02/scenes/water_damaged_list.png", "雨水与纸张", "沿江运输最怕雨水侵入。名册与目录一旦受潮，木箱中的物品就更难重新辨认。"),
        ("images/chapter02/scenes/boat_six_cabin.png", "船舱里的取舍", "船舱空间有限，师生必须反复调整人员和物资的位置，在安全与教学需求之间寻找平衡。"),
        ("images/chapter02/scenes/tonglu_transfer.png", "沿江转运", "船只、车辆和人力常常需要接力，学校就是在一次次核对与搬运中继续向西。"),
        ("images/chapter02/scenes/jiande_arrival.png", "抵达建德", "到达并不等于安定。师生下船后还要立即寻找住处、教室和能够存放图书仪器的地点。"),

        # 第三章：护送《四库全书》
        ("images/chapter03/siku_cargo_hold.png", "文化记忆的木箱", "战火中，文澜阁《四库全书》面临转移。浙大协助有关人员保护并转运这批珍贵典籍。"),
        ("images/chapter03/seal_desk.png", "封签与箱号", "护送古籍不能只靠搬运。箱号、封签、目录和交接记录共同证明每一箱书的身份。"),
        ("images/chapter03/gangplank_transfer.png", "换船与跳板", "转运途中一次换船就可能造成箱号混乱，因此每次移动都需要重新点验与记录。"),
        ("images/chapter03/scenes/broken_seal.png", "破损封签", "封签破损并不等于书籍丢失，但必须立即记录、复核并重新封存，避免后续责任不清。"),
        ("images/chapter03/scenes/blurred_crate.png", "模糊的箱号", "雨水会让墨迹变淡。目录、重量、旧印记和相邻箱号都可以成为辨认书箱的旁证。"),
        ("images/chapter03/scenes/rain_tarp_warehouse.png", "防水与通风", "古籍既怕水，也怕长时间密闭受潮。油布遮盖、垫高木箱和保持通风缺一不可。"),
        ("images/chapter03/scenes/two_numbers.png", "重复号码", "战时登记难免出现重号或漏号，可靠的处理方法是留下疑点并继续寻找其他证据。"),
        ("images/chapter03/scenes/route_records.png", "交接路线", "一份完整的运输记录要说明时间、地点、经手人和箱数，才能让典籍在多次转运后仍可追溯。"),
        ("images/chapter03/scenes/warehouse_closed.png", "仓门落锁", "结束一日工作前，最后一次点验和封仓同样重要。守护典籍依靠的是连续而克制的细节。"),

        # 第四章：建德梅城
        ("images/chapter04/meicheng_campus.png", "建德梅城", "浙大在建德停留约四十五天。短暂并没有成为停课的理由，师生迅速重建教学秩序。"),
        ("images/chapter04/meicheng_dock.png", "梅城码头", "码头承担接收人员、图书和仪器的任务，也是学校与沿江运输线保持联系的关键地点。"),
        ("images/chapter04/kongmiao_classroom.png", "孔庙课堂", "孔庙等既有建筑被借作临时课堂。旧空间在短时间内获得了新的教育用途。"),
        ("images/chapter04/linchang_office.png", "林场办公点", "学校办公室分散设置在城中多处，行政人员依靠名册、通知和往来记录维持运转。"),
        ("images/chapter04/minju_lodging.png", "借居民宅", "部分师生住进当地民居。借住不仅需要安排铺位，也需要尊重原有住户的生活。"),
        ("images/chapter04/pawnshop_dormitory.png", "当铺宿舍", "万源当等建筑曾被用作临时住处。能遮风避雨的空间都可能成为大学的一部分。"),
        ("images/chapter04/school_affairs_office.png", "校务办公处", "一所迁移中的大学仍需要处理课程、住宿、物资和人员登记，校务工作从未真正停止。"),

        # 第五章：警报中的课堂
        ("images/chapter05/scenes/class_alarm.png", "警报中的课堂", "防空警报响起时，安全疏散必须先于授课。坚持教学并不等于忽视危险。"),
        ("images/chapter05/scenes/shelter_rollcall.png", "避难与点名", "进入安全地点后，教师和学生需要核对人数，确认每一名缺席者的去向。"),
        ("images/chapter05/scenes/return_class.png", "方才讲到这里", "警报解除后，师生整理桌椅、讲义和粉笔，课堂从中断处继续。"),
        ("images/chapter05/scenes/emergency_pack.png", "应急背包", "讲义、名册、急救用品和防水油布都可能进入应急背包，有限容量要求明确取舍。"),
        ("images/chapter05/scenes/mobile_lessons.png", "移动课堂", "数学、地理和工程知识可以直接帮助计算载重、判断路线与解决迁移中的实际问题。"),
        ("images/chapter05/scenes/verification_night_v2.png", "未经核实，不宜遽书", "课堂训练的不只是记忆答案，也包括核对来源、标明疑点和在证据不足时保持克制。"),

        # 第六章：《浙大日报》
        ("images/chapter06/scenes/radio_noise_v2.png", "从杂音中辨认消息", "广播信号时断时续，记录者必须反复收听关键词，并把已确认内容和听不清的部分分开。"),
        ("images/chapter06/radio_room.png", "情报委员会", "建德时期，学校组织人员收听广播、整理消息，努力弥补当地新闻来源不足。"),
        ("images/chapter06/scenes/proofreading.png", "新闻核验", "战时报纸不能把传闻当作事实。人名、地点、时间和消息来源都需要交叉核对。"),
        ("images/chapter06/scenes/wall_newspaper.png", "从壁报到日报", "零散的广播记录先被整理成壁报，随后逐渐形成更稳定的新闻编辑与传播工作。"),
        ("images/chapter06/scenes/first_issue.png", "《浙大日报》", "《浙大日报》向师生和当地居民传播时事，也让学生在编辑、油印和发行中承担公共责任。"),
        ("images/chapter06/scenes/street_sale.png", "走向街头", "工读学生将报纸带到街头，新闻由校园走向居民，也为部分学生提供生活补助。"),
        ("images/chapter06/scenes/departure.png", "把记录带上路", "当学校再次启程，保存下来的报纸、名册和记录成为这段短暂办学经历的见证。"),
    ]


transform opening_gallery_motion:
    xalign 0.5
    yalign 0.5
    subpixel True
    zoom 1.0
    linear 6.2 zoom 1.018


screen opening_history_card(background_image, location_name, history_fact):
    modal True

    add background_image at opening_gallery_motion:
        xysize (1920, 1080)

    add Solid("#03060738")

    frame:
        xpos 52
        ypos 765
        xsize 1180
        ysize 245
        background Solid("#09100fdf")
        padding (34, 26)

        vbox:
            spacing 10

            text "历史画页":
                size 20
                color "#a98a4f"

            text "[location_name]":
                size 35
                color "#ecd69d"

            frame:
                xsize 820
                ysize 2
                background Solid("#94713a99")

            text "[history_fact]":
                size 24
                color "#e5e0d4"
                xmaximum 1080
                line_spacing 8

    frame:
        xpos 1570
        ypos 900
        xsize 290
        ysize 78
        background Solid("#101713e8")

        textbutton "进入六章地图":
            xfill True
            yfill True
            text_size 24
            text_color "#dfc98f"
            text_hover_color "#ffe6a1"
            text_xalign 0.5
            text_yalign 0.5
            action Return()

    text "画面将在数秒后自动进入地图":
        xpos 1580
        ypos 990
        size 17
        color "#c5c0b3"
        outlines [(2, "#080a09", 0, 0)]

    timer 6.5 action Return()
    key "dismiss" action Return()


# 六章共用的章回题签。字体优先使用本机华文行楷，
# 若字体不可用则自动回退到工程内置中文字体。
screen chapter_title_card(background_image, chapter_number, chapter_title, chapter_subtitle, chapter_date):
    modal True

    add background_image at opening_gallery_motion:
        xysize (1920, 1080)

    add Solid("#05070662")

    vbox:
        xalign 0.5
        yalign 0.47
        spacing 13

        text "[chapter_number]":
            xalign 0.5
            font CHAPTER_XINGKAI_FONT
            size 42
            color "#d5bb7d"
            outlines [(3, "#17130e", 0, 0)]

        text "[chapter_title]":
            xalign 0.5
            font CHAPTER_XINGKAI_FONT
            size 76
            color "#f0dda8"
            outlines [(4, "#17130e", 0, 0)]

        frame:
            xalign 0.5
            xsize 620
            ysize 2
            background Solid("#bd9652bb")

        text "[chapter_subtitle]":
            xalign 0.5
            font CHAPTER_XINGKAI_FONT
            size 36
            color "#e3d4b1"
            outlines [(3, "#17130e", 0, 0)]

        null height 10

        text "[chapter_date]":
            xalign 0.5
            size 21
            color "#ddd8cb"
            outlines [(2, "#11130f", 0, 0)]

    text "点击继续":
        xalign 0.5
        ypos 950
        size 19
        color "#d0c3a1"
        outlines [(2, "#11130f", 0, 0)]

    timer 4.5 action Return()
    key "dismiss" action Return()
