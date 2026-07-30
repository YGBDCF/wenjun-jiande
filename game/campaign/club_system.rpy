# ================================================================
# 社团系统：主社团、经验、等级、固定活动时段
# ================================================================

define CLUB_NAMES = {
    "academic": "学术互助会",
    "work_study": "工读互助组",
    "repair": "校舍修缮队",
    "news": "新闻社",
}

define CLUB_RANK_NAMES = ("旁听者", "成员", "骨干", "负责人")

init python:
    CLUB_RULES = {
        "academic": {
            "locations": ("classroom", "kongmiao"),
            "days": (9, 16, 23, 30, 37, 44),
            "period": 2,
            "events": (
                ("CLUB_001", "三个人的补课表", "三份课表互相冲突。有人缺课，有人值夜，还有人要去码头搬书。"),
                ("CLUB_002", "答案还是方法", "一名同学只想抄下答案，另一名同学坚持把推导过程重新讲一遍。"),
                ("CLUB_003", "最后一次讨论班", "离开建德前，大家决定把没有讲完的问题列在同一张纸上。"),
            ),
        },
        "work_study": {
            "locations": ("office", "dock", "newspaper"),
            "days": (10, 17, 24, 31, 38, 44),
            "period": 1,
            "events": (
                ("CLUB_004", "印刷机旁的位置", "印刷机旁只剩一个能避雨的位置，待装订的纸张却越堆越高。"),
                ("CLUB_005", "一分钱怎样分", "卖报所得不多，几名工读生商量怎样补贴最困难的同学。"),
                ("CLUB_006", "先搬哪一箱", "码头同时到了粮食和讲义，两边都在催人。"),
            ),
        },
        "repair": {
            "locations": ("linchang", "classroom", "dormitory"),
            "days": (11, 18, 25, 32, 39),
            "period": 1,
            "events": (
                ("CLUB_007", "旧桌板的新用途", "一块旧桌板还能做成讲台踏板，也能补上宿舍漏风的窗。"),
                ("CLUB_008", "漏雨点不止一个", "屋顶新添了三处漏点，现有木料只能先修其中两处。"),
                ("CLUB_009", "离开前的门窗", "迁校准备已经开始，但门窗若不修，留下的人仍要挨过寒夜。"),
            ),
        },
        "news": {
            "locations": ("office", "classroom", "minju"),
            "days": (21, 27, 34, 41),
            "period": 2,
            "events": (
                ("CLUB_010", "一个“不”字", "排字盘里漏了一个“不”字，整条消息的意思因此完全相反。"),
                ("CLUB_011", "消息没有第二来源", "一条街谈巷议只有一个来源，却已经传遍半座城。"),
                ("CLUB_012", "最后一期的版面", "版面只剩半栏，离校通知和民生消息都等着刊登。"),
            ),
        },
    }

    def campaign_club_rank_from_xp(value):
        value = int(value)
        if value >= 120:
            return 3
        if value >= 70:
            return 2
        if value >= 30:
            return 1
        return 0

    def campaign_club_can_join(club_id):
        if store.campaign_day < 8:
            return False
        if club_id == "news" and not store.chapter6_completed:
            return False
        return club_id in CLUB_RULES

    def campaign_join_club(club_id):
        if not campaign_club_can_join(club_id):
            return False
        if store.primary_club is None:
            store.primary_club = club_id
            return True
        if store.primary_club == club_id:
            return True
        if store.club_switch_used:
            return False
        old_id = store.primary_club
        store.club_xp[old_id] = max(0, int(store.club_xp.get(old_id, 0)) - 10)
        store.club_rank[old_id] = campaign_club_rank_from_xp(store.club_xp[old_id])
        store.stat_reputation = campaign_clamp(store.stat_reputation - 1, 0, 20)
        store.primary_club = club_id
        store.club_switch_used = True
        return True

    def campaign_club_activity_for_turn(location_id):
        if store.campaign_day < 8 or store.campaign_period == 3:
            return None
        for club_id, rule in CLUB_RULES.items():
            if location_id not in rule["locations"]:
                continue
            if store.campaign_day not in rule["days"] or store.campaign_period != rule["period"]:
                continue
            turn_key = (club_id, store.campaign_day)
            if turn_key in store.club_weekly_done:
                continue
            available = [event for event in rule["events"] if event[0] not in store.club_events_seen]
            if not available:
                available = list(rule["events"])
            return (club_id,) + available[0]
        return None

    def campaign_apply_club_activity(club_id, event_id, approach):
        # 参加其他社团公开任务可获得行动效果，但不获得正式经验与等级。
        if club_id == "academic":
            store.stat_knowledge = campaign_clamp(store.stat_knowledge + 1, 0, 20)
            store.weekly_preparation = campaign_clamp(store.weekly_preparation + 8, 0, 100)
        elif club_id == "work_study":
            store.stat_morality = campaign_clamp(store.stat_morality + 1, 0, 20)
            store.stat_reputation = campaign_clamp(store.stat_reputation + 1, 0, 20)
            stock_id = "grain" if store.campus_stock["grain"] <= store.campus_stock["paper"] else "paper"
            store.campus_stock[stock_id] += 2
        elif club_id == "repair":
            store.stat_practical = campaign_clamp(store.stat_practical + 1, 0, 20)
            if approach == "improvise":
                campaign_gain_virtue("innovation", 1)
            store.campus_repair_backlog = max(0, store.campus_repair_backlog - 1)
            store.campus_stock["wood"] = max(0, store.campus_stock["wood"] - 1)
        else:
            campaign_gain_virtue("truth", 1)
            store.newspaper_accuracy = campaign_clamp(store.newspaper_accuracy + 4, 0, 100)
            store.campus_stock["paper"] = max(0, store.campus_stock["paper"] - 1)

        store.stat_stamina = max(0, store.stat_stamina - 1)
        if store.primary_club == club_id:
            gain = {"careful": 18, "cooperate": 14, "improvise": 10}.get(approach, 10)
            store.club_xp[club_id] = int(store.club_xp.get(club_id, 0)) + gain
            store.club_rank[club_id] = campaign_club_rank_from_xp(store.club_xp[club_id])
        store.club_events_seen.add(event_id)
        store.club_weekly_done.add((club_id, store.campaign_day))
        store.action_count = min(135, store.action_count + 1)
        store.mc45_time = min(3, store.mc45_time + 1)
        store.campaign_period = store.mc45_time
        campaign_sync_legacy_view()


screen campaign_club_board():
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#090b0877")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1220
        ysize 780
        background Solid("#11150ff2")
        padding (52, 42)
        vbox:
            spacing 18
            text "学生社团公告板" size 40 color "#e8cf91"
            if primary_club:
                text "主社团：[CLUB_NAMES[primary_club]]　[CLUB_RANK_NAMES[club_rank[primary_club]]]　经验 [club_xp[primary_club]]" size 22 color "#d8d0bf"
            else:
                text "摸底考试后，学生开始自发组织互助社团。你尚未选择主社团。" size 22 color "#d8d0bf"
            text "主社团活动可获得经验与等级；其他社团的公开任务仍可协助，但不计正式经验。" size 18 color "#aaa598"
            null height 8
            for club_id in ("academic", "work_study", "repair", "news"):
                $ locked = not campaign_club_can_join(club_id)
                $ status = "第六章完成后开放" if club_id == "news" and locked else ("当前主社团" if primary_club == club_id else "选择为主社团")
                textbutton "[CLUB_NAMES[club_id]]　—　[status]":
                    xsize 1050
                    ysize 66
                    sensitive not locked
                    text_size 23
                    text_color ("#77736a" if locked else "#e7d097")
                    text_hover_color "#fff0bd"
                    background Solid("#24271fdd")
                    hover_background Solid("#4b3b23ee")
                    action Return(club_id)
            textbutton "返回临时教室":
                xalign 0.5
                text_size 21
                text_color "#d9c58f"
                action Return(None)


screen campaign_club_activity(event_data):
    modal True
    $ club_id, event_id, title, body = event_data
    add MC45_LOCATION_META[current_location][1]:
        xysize (1920, 1080)
    frame:
        xpos 105
        ypos 105
        xsize 1110
        ysize 730
        background Solid("#11140eea")
        padding (48, 38)
        vbox:
            spacing 20
            text "[CLUB_NAMES[club_id]]" size 25 color "#ba9b5c"
            text title size 42 color "#ead296"
            text body size 25 color "#ded6c6" xmaximum 980 line_spacing 8
            null height 18
            textbutton "逐项核对，留下可复查的记录":
                xsize 980
                ysize 70
                text_size 22
                text_color "#ead39a"
                background Solid("#25271fef")
                hover_background Solid("#524124ef")
                action Return("careful")
            textbutton "与同伴分工，先解决共同困难":
                xsize 980
                ysize 70
                text_size 22
                text_color "#ead39a"
                background Solid("#25271fef")
                hover_background Solid("#524124ef")
                action Return("cooperate")
            textbutton "利用手边材料，尝试新的办法":
                xsize 980
                ysize 70
                text_size 22
                text_color "#ead39a"
                background Solid("#25271fef")
                hover_background Solid("#524124ef")
                action Return("improvise")
            textbutton "暂不参加":
                text_size 19
                text_color "#aaa598"
                action Return(None)


label campaign_club_board_label:
    call screen campaign_club_board
    $ selected_club = _return
    if selected_club:
        $ joined = campaign_join_club(selected_club)
        if joined:
            $ mc45_last_result = "你已将%s登记为主社团。" % CLUB_NAMES[selected_club]
        else:
            $ mc45_last_result = "主社团只能更换一次；当前登记没有改变。"
    return


label campaign_club_activity_label(event_data):
    call screen campaign_club_activity(event_data)
    $ club_approach = _return
    if club_approach:
        $ campaign_apply_club_activity(event_data[0], event_data[1], club_approach)
        $ mc45_last_result = "完成“%s”。%s经验：%d。" % (event_data[2], CLUB_NAMES[event_data[0]], club_xp[event_data[0]])
        return True
    return False
