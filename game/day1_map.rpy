# Day 1：可点击章节地图

screen day1_chapter_map():
    modal True

    add "images/day1_chapter_map.png":
        xysize (1920, 1080)

    # 与地图中六个章节图标对应的点击区域：
    # (章节编号, xpos, ypos, width, height)
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
                    text "✓ 已完成":
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

    frame:
        xpos 1510
        ypos 845
        xsize 365
        ysize 155
        background Solid("#141611e8")
        padding (24, 18)

        vbox:
            spacing 8

            text "Day 1 功能原型":
                size 28
                color "#dfbd72"

            text "当前章节：[day1_current_chapter] / 6":
                size 23
                color "#eee2c8"

            text "已完成：[len(day1_completed_chapters)] / 6":
                size 23
                color "#eee2c8"

    textbutton "返回主菜单":
        xpos 60
        ypos 990
        text_size 24
        action MainMenu()
