# ================================================================
# 临时教室基础入口。正式课程与考试将在 A0-5 接入。
# ================================================================

screen campaign_classroom_stub():
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#080a0844")

    frame:
        xpos 55
        ypos 45
        xsize 720
        ysize 150
        background Solid("#10140ee8")
        padding (28, 18)
        vbox:
            text "临时教室" size 38 color "#ead296"
            text "Day 8 起，正式课程、周考、阅卷与复盘均在此进行。" size 20 color "#c9c2b3"

    frame:
        xalign 0.5
        yalign 0.78
        xsize 850
        ysize 310
        background Solid("#11140ef0")
        padding (42, 30)
        vbox:
            xalign 0.5
            spacing 20
            text "黑板、点名册和收卷处已经归位。":
                xalign 0.5
                size 25
                color "#ded6c5"
            text "这里可准备周考、查看学生社团公告，也可返回梅城继续行动。":
                xalign 0.5
                size 18
                color "#aaa395"
            hbox:
                xalign 0.5
                spacing 28
                textbutton "准备课程":
                    text_size 22
                    text_color "#efd89d"
                    action Return("study")
                if campaign_day >= 8:
                    textbutton "社团公告":
                        text_size 22
                        text_color "#efd89d"
                        action Return("club")
            textbutton "返回梅城地图":
                xalign 0.5
                text_size 22
                text_color "#efd89d"
                action Return("back")


label campaign_classroom_hub:
    if not classroom_unlocked:
        call screen locked_vacant_lot_notice
        jump jiande_map_hub
    call screen campaign_classroom_stub
    $ classroom_action = _return
    if classroom_action == "club":
        call campaign_club_board_label from _call_campaign_club_board_label
        jump campaign_classroom_hub
    if classroom_action == "study":
        $ current_location = "classroom"
        $ club_candidate = campaign_club_activity_for_turn("classroom")
        if club_candidate:
            call campaign_club_activity_label(club_candidate) from _call_campaign_club_activity_label
            if _return:
                jump jiande_map_hub
        $ stat_knowledge = campaign_clamp(stat_knowledge + 1, 0, 20)
        $ weekly_preparation = campaign_clamp(weekly_preparation + 6, 0, 100)
        $ weekly_attendance_possible += 1
        $ weekly_attendance_present += 1
        $ daily_knowledge_actions += 1
        $ stat_stamina = max(0, stat_stamina - 1)
        $ mc45_time = min(3, mc45_time + 1)
        $ campaign_period = mc45_time
        $ action_count = min(135, action_count + 1)
        $ mc45_last_result = "你完成了一次课程整理，周准备度有所提高。"
        $ campaign_sync_legacy_view()
    jump jiande_map_hub
