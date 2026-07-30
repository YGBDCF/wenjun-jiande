# ================================================================
# 六章全局路线图
# 仅负责章节选择；梅城地点探索由第四章内部地图负责。
# ================================================================

screen day1_chapter_map():
    modal True

    add "images/world_chapter_map_v2.png":
        xysize (1920, 1080)

    # 顶部题签。背景图中不焊死任何文字。
    frame:
        xpos 0
        ypos 0
        xsize 1920
        ysize 145
        background Solid("#090b09dc")

        text "负笈西行  六章纪程":
            xpos 55
            yalign 0.5
            size 42
            color "#e4cb8d"

        text "从山寺课堂到战时校报":
            xpos 475
            yalign 0.54
            size 22
            color "#b9b09b"

        text "当前章节  [day1_current_chapter] / 6    已完成  [len(day1_completed_chapters)] / 6":
            xalign 0.96
            yalign 0.5
            size 22
            color "#d6c49b"

    # 六个地标依照背景中的金色路线排列。
    $ world_hotspots = [
        (1, 55, 190, 360, 255),
        (2, 545, 185, 390, 270),
        (3, 1260, 180, 390, 280),
        (4, 1295, 620, 390, 275),
        (5, 600, 620, 400, 275),
        (6, 45, 615, 400, 285),
    ]

    for chapter_id, px, py, pw, ph in world_hotspots:
        $ unlocked = day1_is_unlocked(chapter_id)
        $ completed = chapter_id in day1_completed_chapters
        $ chapter_name, chapter_subtitle = DAY1_CHAPTER_INFO[chapter_id]

        button:
            xpos px
            ypos py
            xsize pw
            ysize ph
            background Solid("#00000000")
            hover_background (Solid("#c79b4524") if unlocked else Solid("#00000000"))
            action (Return(chapter_id) if unlocked else NullAction())

            vbox:
                xalign 0.5
                yalign 1.0
                spacing 2

                text "第[chapter_id]章  [chapter_name]":
                    xalign 0.5
                    size 25
                    color ("#e5cb8a" if unlocked else "#8b887f")
                    outlines [(3, "#17130f", 0, 0)]

                if completed:
                    text "已完成  可再次进入":
                        xalign 0.5
                        size 17
                        color "#b7d59f"
                        outlines [(2, "#17130f", 0, 0)]
                elif unlocked:
                    text "[chapter_subtitle]":
                        xalign 0.5
                        size 17
                        color "#ded4be"
                        outlines [(2, "#17130f", 0, 0)]
                else:
                    text "尚未解锁":
                        xalign 0.5
                        size 17
                        color "#97938a"
                        outlines [(2, "#17130f", 0, 0)]

    # 第四章通关后，梅城成为独立的长期探索区域。
    if 4 in day1_completed_chapters:
        frame:
            xpos 1635
            ypos 570
            xsize 245
            ysize 74
            background Solid("#10140fe8")
            padding (8, 6)

            textbutton "进入梅城镇":
                xfill True
                yfill True
                text_size 22
                text_color "#ead091"
                text_hover_color "#ffe4a0"
                text_xalign 0.5
                text_yalign 0.5
                action Return("meicheng_town")

    frame:
        xpos 715
        ypos 965
        xsize 490
        ysize 72
        background Solid("#0c100fe8")
        padding (22, 12)

        hbox:
            xalign 0.5
            spacing 28

            textbutton "返回主菜单":
                text_size 22
                text_color "#d8c8a1"
                text_hover_color "#ffe2a0"
                action MainMenu()

            text "已完成章节仍可重温":
                size 18
                color "#9f9a8f"
                yalign 0.5
