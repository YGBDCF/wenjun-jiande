# ================================================================
# V1.2 固定章节门控与地图翻新（Phase A0-3 / A0-4）
# ================================================================

screen campaign_story_notice(title, body, button_text="进入西迁纪事"):
    modal True
    add "images/world_chapter_map_v2.png":
        xysize (1920, 1080)
    add Solid("#0709079a")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 980
        ysize 410
        background Solid("#11140ff2")
        padding (58, 44)

        vbox:
            xfill True
            spacing 24
            text title:
                xalign 0.5
                size 40
                color "#e8cf91"
            text body:
                xalign 0.5
                text_align 0.5
                size 24
                color "#d8d0bf"
                xmaximum 820
                line_spacing 8
            null height 10
            textbutton button_text:
                xalign 0.5
                xsize 360
                ysize 64
                text_size 23
                text_color "#f0d99c"
                text_hover_color "#fff0c0"
                text_xalign 0.5
                text_yalign 0.5
                background Solid("#352b1de8")
                hover_background Solid("#554225f2")
                action Return()


screen locked_vacant_lot_notice():
    modal True
    add Solid("#0000008c")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 760
        ysize 270
        background Solid("#12150ff2")
        padding (44, 34)
        vbox:
            xfill True
            spacing 18
            text "空地｜尚未启用":
                xalign 0.5
                size 32
                color "#e3cb90"
            text "此处尚未整理，堆着木料、旧桌脚与未拆的绳索。":
                xalign 0.5
                text_align 0.5
                size 22
                color "#d2cbbb"
            textbutton "返回地图":
                xalign 0.5
                text_size 21
                text_color "#e8d39c"
                action Hide("locked_vacant_lot_notice")


screen classroom_opening_card():
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#080a0872")

    frame:
        xpos 180
        ypos 170
        xsize 1080
        ysize 700
        background Solid("#10130eea")
        padding (55, 42)

        vbox:
            spacing 18
            text "临时教室启用":
                size 44
                color "#ead195"
            text "孔庙可借一时，却不能使各班日日相冲。警报一响，桌凳、讲义、点名册皆要重新收拢。":
                size 24
                color "#ded6c6"
                xmaximum 930
                line_spacing 7
            text "空地上的木料已经分好。立柱、遮雨、固定黑板，先搭出一间能上课、能收卷子的讲堂。":
                size 24
                color "#ded6c6"
                xmaximum 930
                line_spacing 7
            text "不是为了有一座体面的房子，是为了下一次铃响时，大家知道应当回到哪里。":
                size 24
                color "#ded6c6"
                xmaximum 930
                line_spacing 7
            text "说明：临时教室为呈现分散办学秩序的游戏化艺术加工。":
                size 17
                color "#9e998d"
            textbutton "回到第7日早晨":
                xsize 330
                ysize 64
                text_size 22
                text_color "#f1d99b"
                text_xalign 0.5
                text_yalign 0.5
                background Solid("#3b301fe8")
                hover_background Solid("#5a4628ee")
                action Return()


label day7_chapter5_gate:
    if campaign_day != 7 or chapter5_completed:
        return
    $ chapter5_unlocked = True
    $ in_forced_story = True
    call screen campaign_story_notice(
        "西迁纪事更新",
        "第五章“黑板挂在我的胸前”已经解锁。\n\n完成本章后，梅城将启用新的临时教室。"
    )
    $ in_forced_story = False
    jump enter_chapter5_episode


label enter_chapter5_episode:
    $ episode_return_day = campaign_day
    $ episode_return_period = campaign_period
    $ episode_return_weather = current_weather
    $ episode_return_event = cached_turn_event_id
    $ in_chapter_episode = True
    $ active_meta_map = "chapter_world_map"
    jump chapter_5


label campaign_complete_chapter5:
    $ chapter5_completed = True
    $ classroom_unlocked = True
    $ map_visual_phase = "post_classroom"
    $ story_flags.add("post_ch5_interactions_unlocked")
    $ story_flags.add("classroom_opening_pending")
    $ campaign_day = episode_return_day
    $ campaign_period = episode_return_period
    $ current_weather = episode_return_weather
    $ cached_turn_event_id = episode_return_event
    $ in_chapter_episode = False
    $ active_meta_map = "jiande_exploration_map"
    $ campaign_sync_legacy_view()
    call classroom_opening_sequence from _call_classroom_opening_sequence
    jump jiande_map_hub


label day20_chapter6_gate:
    if campaign_day != 20 or chapter6_completed:
        return
    $ chapter6_unlocked = True
    $ in_forced_story = True
    call screen campaign_story_notice(
        "公共记录的新任务",
        "第六章《浙大日报》已经解锁。\n\n梅城消息来源零散，广播常被杂音截断。完成本章后，新闻社与日报系统将正式开放。",
        "进入第六章"
    )
    $ in_forced_story = False
    jump enter_chapter6_episode


label enter_chapter6_episode:
    $ episode_return_day = campaign_day
    $ episode_return_period = campaign_period
    $ episode_return_weather = current_weather
    $ episode_return_event = cached_turn_event_id
    $ in_chapter_episode = True
    $ active_meta_map = "chapter_world_map"
    jump chapter_6


label campaign_complete_chapter6:
    $ chapter6_unlocked = True
    $ chapter6_completed = True
    $ newspaper_system_unlocked = True
    $ newspaper_prep_started = True
    $ story_flags.add("newspaper_line_open")
    $ story_flags.add("news_club_open")
    $ campaign_day = episode_return_day
    $ campaign_period = episode_return_period
    $ current_weather = episode_return_weather
    $ cached_turn_event_id = episode_return_event
    $ in_chapter_episode = False
    $ active_meta_map = "jiande_exploration_map"
    $ campaign_sync_legacy_view()
    $ mc45_last_result = "第六章完成：《浙大日报》线与新闻社已经开放。"
    jump jiande_map_hub


label classroom_opening_sequence:
    if classroom_opening_seen:
        return
    call screen classroom_opening_card
    $ classroom_opening_seen = True
    $ story_flags.discard("classroom_opening_pending")
    return
