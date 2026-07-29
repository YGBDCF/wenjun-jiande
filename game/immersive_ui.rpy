# ================================================================
# 六章共用沉浸界面
# 后续章节只设置以下变量，不再重复制作 UI。
# ================================================================

default immersive_active = False
default immersive_chapter = ""
default immersive_date = ""
default immersive_objective = ""
default immersive_tasks = []
default immersive_secondary = []
default immersive_items = []
default immersive_archive_count = 0
default immersive_pose = "calm"

init python:
    def immersive_setup(chapter, date, objective, tasks, secondary, items, archives=0, pose="calm"):
        store.immersive_active = True
        store.immersive_chapter = chapter
        store.immersive_date = date
        store.immersive_objective = objective
        store.immersive_tasks = tasks
        store.immersive_secondary = secondary
        store.immersive_items = items
        store.immersive_archive_count = archives
        store.immersive_pose = pose

    def immersive_close():
        store.immersive_active = False

screen immersive_character():
    zorder 5
    if immersive_pose == "thoughtful":
        add "shenyan thoughtful" at ch1_portrait_thoughtful
    elif immersive_pose == "tense":
        add "shenyan tense" at ch1_portrait_tense
    elif immersive_pose == "determined":
        add "shenyan determined" at ch1_portrait_calm
    elif immersive_pose == "worried":
        add "shenyan worried" at ch1_portrait_tense
    elif immersive_pose == "relieved":
        add "shenyan relieved" at ch1_portrait_calm
    else:
        add "shenyan calm" at ch1_portrait_calm

screen immersive_hud():
    zorder 30

    frame:
        xpos 470
        ypos 18
        xsize 780
        ysize 58
        background "images/chapter01/ui/top_button.png"
        padding (28, 11)
        text "[immersive_date]" size 21 color "#dec78f" xalign 0.5 yalign 0.5

    hbox:
        xpos 1540
        ypos 24
        spacing 9
        textbutton "存档" action ShowMenu("save") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "读档" action ShowMenu("load") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "回顾" action ShowMenu("history") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "设置" action ShowMenu("preferences") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"

    frame:
        xpos 1540 ypos 94 xsize 356 ysize 560
        background "images/chapter01/ui/task_panel.png"
        padding (30, 30)
        vbox:
            spacing 11
            text "[immersive_chapter]" size 25 color "#dfc480" xmaximum 300
            text "历史叙事章节" size 17 color "#aeb6b1"
            null height 8
            text "当前目标" size 25 color "#e8d6a7"
            text "[immersive_objective]" size 19 color "#ffffff" xmaximum 300
            null height 10
            text "任务进度" size 22 color "#e8d6a7"
            for task_name, task_done in immersive_tasks:
                text (("完成  " if task_done else "待办  ") + task_name) size 18 color ("#b9d49e" if task_done else "#b9b2a2") xmaximum 300
            null height 10
            text "次要目标" size 22 color "#e8d6a7"
            for secondary_name in immersive_secondary:
                text "[secondary_name]" size 18 color "#b9b2a2" xmaximum 300

    frame:
        xpos 1540 ypos 670 xsize 356 ysize 310
        background "images/chapter01/ui/inventory_panel.png"
        padding (14, 16)
        vbox:
            spacing 12
            hbox:
                spacing 3
                textbutton "返回地图" action Jump("day1_map_hub") xsize 104 ysize 44 background "images/chapter01/ui/tab_idle.png" text_size 17 text_color "#e2c987" text_hover_color "#fff0bd"
                textbutton "档案" action NullAction() xsize 104 ysize 44 background "images/chapter01/ui/tab_idle.png" text_size 20 text_color "#c3ad7c"
                textbutton "物件" action NullAction() xsize 104 ysize 44 background "images/chapter01/ui/tab_active.png" text_size 20 text_color "#f0d799"
            text "随身物件" size 21 color "#dfc480"
            if immersive_items:
                for item_name in immersive_items:
                    frame:
                        xsize 324 ysize 42 background Solid("#171b19cc")
                        text "[item_name]" size 17 color "#d8cfbd" xalign 0.5 yalign 0.5
            else:
                text "尚未获得物件" size 18 color "#898a86"
            text "历史档案  [immersive_archive_count]" size 18 color "#c9b98b"

label immersive_show:
    show screen immersive_character
    show screen immersive_hud
    return

label immersive_hide:
    hide screen immersive_character
    hide screen immersive_hud
    $ immersive_close()
    return
