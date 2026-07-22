screen day1_chapter_map():
    modal True

    add "images/map_main.jpg":
        xysize (1920, 1080)

    $ day1_hotspots = [
        (1, 35, 145, 280, 305),
        (2, 300, 145, 290, 305),
        (3, 565, 140, 290, 315),
        (4, 825, 100, 315, 355),
        (5, 1090, 145, 285, 315),
        (6, 1350, 145, 245, 315),
    ]

    for chapter_id, px, py, pw, ph in day1_hotspots:
        $ unlocked = day1_is_unlocked(chapter_id)
        $ completed = chapter_id in day1_completed_chapters

        if unlocked:
            button:
                xpos px
                ypos py
                xsize pw
                ysize ph
                background Solid("#00000000")
                hover_background Solid("#d6a74a44")
                action Return(chapter_id)

                if completed:
                    text "已经完成":
                        xalign 0.5
                        yalign 0.91
                        size 27
                        color "#b7d6ad"
                        outlines [(2, "#172018", 0, 0)]
                elif chapter_id == day1_current_chapter:
                    text "点击进入":
                        xalign 0.5
                        yalign 0.91
                        size 27
                        color "#f1d590"
                        outlines [(2, "#2a2114", 0, 0)]
        else:
            frame:
                xpos px
                ypos py
                xsize pw
                ysize ph
                background Solid("#00000066")

                text "待解锁":
                    xalign 0.5
                    yalign 0.90
                    size 26
                    color "#8f8a80"
                    outlines [(2, "#161616", 0, 0)]

    # 第四章解锁后，直接点击地图中绘制好的六枚地点标志。
    if day1_is_unlocked(4):
        $ meicheng_hotspots = {
            "linchang": (400, 465, 145, 105, "林场"),
            "kongmiao": (670, 465, 150, 105, "孔庙"),
            "minju": (455, 575, 150, 110, "民居"),
            "dock": (485, 690, 165, 110, "梅城码头"),
            "pawnshop": (1100, 575, 165, 110, "当铺"),
            "office": (890, 690, 220, 110, "校务办公处"),
        }
        for location_id, location_data in meicheng_hotspots.items():
            $ lx, ly, lw, lh, location_name = location_data
            $ place_unlocked = day1_meicheng_unlocked(location_id)
            $ place_done = location_id in ch4_places
            button:
                xpos lx ypos ly xsize lw ysize lh
                background (Solid("#d3a44118") if place_unlocked else Solid("#06080888"))
                hover_background (Solid("#e7b94f66") if place_unlocked else Solid("#06080888"))
                action (Return("meicheng:" + location_id) if place_unlocked else NullAction())
                if not place_unlocked:
                    text "尚未解锁" xalign 0.5 yalign 0.98 size 18 color "#827d72" outlines [(2, "#17130d", 0, 0)]
                elif place_done:
                    text "可再次进入" xalign 0.5 yalign 0.98 size 18 color "#b8d395" outlines [(2, "#17130d", 0, 0)]

    frame:
        xpos 1510
        ypos 835
        xsize 365
        ysize 185
        background Solid("#141611e8")
        padding (24, 18)

        vbox:
            spacing 7
            text "章节地图":
                size 28
                color "#dfbd72"
            text "当前章节：[day1_current_chapter] / 6":
                size 22
                color "#eee2c8"
            text "已完成：[len(day1_completed_chapters)] / 6":
                size 22
                color "#eee2c8"
            text "第四章开启后可直接点击梅城地点标志":
                size 18
                color "#cfc2a5"
            text "已经完成的章节可以重新体验":
                size 18
                color "#cfc2a5"

    textbutton "返回主菜单":
        xpos 60
        ypos 990
        text_size 24
        action MainMenu()
