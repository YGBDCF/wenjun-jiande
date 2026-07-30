# ================================================================
# PATCH_NEW_GAMEPLAY_SYSTEMS Phase 2
# 临时大学运营：公共物资、校务评分、每日请求与夜间消耗
# ================================================================

define CAMPUS_STOCK_CAPS = {
    "wood": 40,
    "paper": 60,
    "lamp_oil": 30,
    "grain": 60,
    "medicine": 20,
}

define CAMPUS_STOCK_NAMES = {
    "wood": "木料",
    "paper": "纸张",
    "lamp_oil": "灯油",
    "grain": "粮食",
    "medicine": "药品",
}

define CAMPUS_REQUESTS = {
    "repair_desks": {
        "title": "修整课桌",
        "body": "林场送来一批旧木料，需要有人挑出可用部分并修好松动的课桌。",
        "metric": "material",
        "location": "linchang",
        "choice": "practice",
    },
    "check_book_roster": {
        "title": "核对借书名册",
        "body": "临时办公处的借书记录出现重复编号，需要按原始名册逐项核对。",
        "metric": "course",
        "location": "office",
        "choice": "verify",
    },
    "settle_dorm_bedding": {
        "title": "安置新到铺盖",
        "body": "学生宿舍又住进一批同学，需要重新分配床位、草席与防潮位置。",
        "metric": "dorm",
        "location": "dormitory",
        "choice": "care",
    },
    "visit_water_households": {
        "title": "协调居民用水",
        "body": "借住师生增多，几户居民担心井水不够，需要当面商量取水时段。",
        "metric": "resident",
        "location": "minju",
        "choice": "care",
    },
    "verify_public_notice": {
        "title": "校核战讯告示",
        "body": "街上的消息彼此矛盾，需要查明来源，再誊写一份不夸大的公共告示。",
        "metric": "public",
        "location": "office",
        "choice": "verify",
    },
    "count_dock_crates": {
        "title": "复核到岸木箱",
        "body": "码头新到一批图书仪器，船单与箱号对不上，需要重新清点。",
        "metric": "material",
        "location": "dock",
        "choice": "verify",
    },
}

init python:
    def campus_stock_adjust(stock_id, amount):
        cap = CAMPUS_STOCK_CAPS[stock_id]
        before = int(store.campus_stock.get(stock_id, 0))
        after = campaign_clamp(before + int(amount), 0, cap)
        store.campus_stock[stock_id] = after
        return after - before

    def campus_metric_value(metric):
        return {
            "course": store.world_course_continuity,
            "dorm": store.world_dorm_order,
            "material": store.world_material_integrity,
            "resident": store.world_resident_trust,
            "public": store.world_public_confidence,
            "migration": store.world_migration_readiness,
        }[metric]

    def campus_metric_adjust(metric, amount):
        field_name = {
            "course": "world_course_continuity",
            "dorm": "world_dorm_order",
            "material": "world_material_integrity",
            "resident": "world_resident_trust",
            "public": "world_public_confidence",
            "migration": "world_migration_readiness",
        }[metric]
        current = int(getattr(store, field_name))
        setattr(store, field_name, campaign_clamp(current + int(amount), 0, 100))

    def campus_recalculate_score():
        if store.campaign_day <= 34:
            score = (
                store.world_course_continuity * 0.30
                + store.world_dorm_order * 0.20
                + store.world_material_integrity * 0.20
                + store.world_resident_trust * 0.15
                + store.world_public_confidence * 0.15
            )
        else:
            score = (
                store.world_course_continuity * 0.25
                + store.world_dorm_order * 0.15
                + store.world_material_integrity * 0.15
                + store.world_resident_trust * 0.10
                + store.world_public_confidence * 0.10
                + store.world_migration_readiness * 0.25
            )
        store.campus_score = campaign_clamp(int(round(score)), 0, 100)
        return store.campus_score

    def campus_score_tier():
        score = campus_recalculate_score()
        if score >= 85:
            return "秩序井然"
        if score >= 70:
            return "运转稳定"
        if score >= 50:
            return "勉力维持"
        if score >= 30:
            return "多处告急"
        return "濒临失序"

    def campus_current_week():
        return int((store.campaign_day - 1) // 7) + 1

    def campus_generate_requests():
        if store.campaign_day < 3 or store.campaign_day > 42:
            store.campus_request_choices = []
            store.campus_request_day = store.campaign_day
            return []
        if store.campus_request_day == store.campaign_day and store.campus_request_choices:
            return list(store.campus_request_choices)

        metric_order = sorted(
            ("course", "dorm", "material", "resident", "public"),
            key=lambda metric: (campus_metric_value(metric), metric),
        )
        ordered = []
        start = store.campaign_day % len(CAMPUS_REQUESTS)
        request_ids = sorted(CAMPUS_REQUESTS.keys())
        for offset in range(len(request_ids)):
            request_id = request_ids[(start + offset) % len(request_ids)]
            request_metric = CAMPUS_REQUESTS[request_id]["metric"]
            if request_metric == metric_order[0] and request_id not in ordered:
                ordered.append(request_id)
        for metric in metric_order:
            for request_id in request_ids:
                if CAMPUS_REQUESTS[request_id]["metric"] == metric and request_id not in ordered:
                    ordered.append(request_id)
        store.campus_request_choices = ordered[:2]
        store.campus_request_day = store.campaign_day
        return list(store.campus_request_choices)

    def campus_accept_request(request_id):
        if request_id not in CAMPUS_REQUESTS:
            return False
        if store.accepted_campus_request_day == store.campaign_day:
            return False
        store.accepted_campus_request = request_id
        store.accepted_campus_request_day = store.campaign_day
        return True

    def campus_emergency_supply():
        week = campus_current_week()
        if store.emergency_supply_used_week == week:
            return None
        shortage_order = sorted(
            CAMPUS_STOCK_CAPS.keys(),
            key=lambda stock_id: (
                float(store.campus_stock.get(stock_id, 0)) / CAMPUS_STOCK_CAPS[stock_id],
                stock_id,
            ),
        )
        stock_id = shortage_order[0]
        campus_stock_adjust(stock_id, 4)
        store.stat_reputation = campaign_clamp(store.stat_reputation - 1, 0, 20)
        store.emergency_supply_used_week = week
        return stock_id

    def campus_try_complete_request(place_id, choice_id):
        request_id = store.accepted_campus_request
        if request_id is None or store.accepted_campus_request_day != store.campaign_day:
            return None
        request = CAMPUS_REQUESTS[request_id]
        if request["location"] != place_id or request["choice"] != choice_id:
            return None

        campus_metric_adjust(request["metric"], 5)
        if request_id == "repair_desks":
            campus_stock_adjust("wood", -2)
            store.campus_repair_backlog = max(0, store.campus_repair_backlog - 1)
        elif request_id == "check_book_roster":
            campus_stock_adjust("paper", 2)
        elif request_id == "settle_dorm_bedding":
            store.dormitory_warmth = campaign_clamp(store.dormitory_warmth + 5, 0, 100)
        elif request_id == "visit_water_households":
            store.virtue_service = campaign_clamp(store.virtue_service + 1, 0, 20)
        elif request_id == "verify_public_notice":
            store.virtue_truth = campaign_clamp(store.virtue_truth + 1, 0, 20)
        elif request_id == "count_dock_crates":
            campus_stock_adjust("paper", 1)

        store.completed_campus_requests.add("%d:%s" % (store.campaign_day, request_id))
        store.accepted_campus_request = None
        campus_recalculate_score()
        return request_id

    def campus_night_settlement():
        results = []
        campus_stock_adjust("grain", -2)
        results.append("全校口粮 -2")

        studied_today = store.daily_knowledge_actions > 0
        examined_today = any(entry.get("day") == store.campaign_day for entry in store.exam_history)
        if studied_today or examined_today:
            campus_stock_adjust("paper", -1)
            results.append("课程用纸 -1")

        wet_or_cold = store.current_weather in ("小雨", "连阴雨", "寒潮", "雨夹雪", "冻雨", "北风")
        if wet_or_cold:
            campus_stock_adjust("lamp_oil", -1)
            results.append("夜间灯油 -1")

        shortages = set()
        for stock_id, amount in store.campus_stock.items():
            if int(amount) <= 0:
                shortages.add(stock_id)
        store.campus_shortages = shortages

        if "grain" in shortages:
            campus_metric_adjust("dorm", -3)
            store.stat_health = campaign_clamp(store.stat_health - 1, 0, 10)
            results.append("口粮见底：宿舍秩序与健康下降")
        if "paper" in shortages:
            campus_metric_adjust("course", -3)
            results.append("纸张见底：课程连续性下降")
        if "lamp_oil" in shortages:
            campus_metric_adjust("course", -2)
            store.classroom_warmth = campaign_clamp(store.classroom_warmth - 2, 0, 100)
            results.append("灯油见底：夜课受阻")
        if store.campus_repair_backlog > 0:
            campus_metric_adjust("material", -2)
            results.append("积压修缮：校产完整度下降")

        if (
            store.accepted_campus_request is not None
            and store.accepted_campus_request_day == store.campaign_day
        ):
            results.append("今日校务请求未完成")
            store.accepted_campus_request = None

        store.virtue_gain_today = 0
        store.campus_last_settlement = results
        campus_recalculate_score()
        return results


screen campus_request_board():
    modal True
    $ request_ids = campus_generate_requests()
    $ accepted_id = accepted_campus_request if accepted_campus_request_day == campaign_day else None
    $ emergency_available = emergency_supply_used_week != campus_current_week()

    add Solid("#0508058a")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        ysize 680
        background Solid("#11140ff4")
        padding (46, 35)
        vbox:
            xfill True
            spacing 16
            text "校务请求｜第[campaign_day]日":
                xalign 0.5
                size 36
                color "#e8cf91"
            text "接受请求不消耗行动；必须在今日前往指定地点，用对应方式完成。":
                xalign 0.5
                size 18
                color "#aaa598"
            if accepted_id:
                $ accepted = CAMPUS_REQUESTS[accepted_id]
                frame:
                    xfill True
                    ysize 250
                    background Solid("#20251cd8")
                    padding (28, 20)
                    vbox:
                        spacing 10
                        text "已接受：[accepted['title']]" size 28 color "#ead39a"
                        text accepted["body"] size 21 color "#d8d2c3" xmaximum 950 line_spacing 5
                        text "前往：[MC45_LOCATION_META[accepted['location']][0]]" size 19 color "#b8b2a5"
            elif request_ids:
                hbox:
                    xalign 0.5
                    spacing 20
                    for request_id in request_ids:
                        $ request = CAMPUS_REQUESTS[request_id]
                        button:
                            xsize 485
                            ysize 300
                            background Solid("#20251cd8")
                            hover_background Solid("#3b301fe8")
                            action Return(("accept", request_id))
                            vbox:
                                xalign 0.5
                                yalign 0.5
                                spacing 12
                                text request["title"] xalign 0.5 size 27 color "#ead39a"
                                text request["body"] text_align 0.5 xalign 0.5 size 19 color "#d8d2c3" xmaximum 420 line_spacing 4
                                text "地点：[MC45_LOCATION_META[request['location']][0]]" xalign 0.5 size 17 color "#aaa598"
            else:
                text "今日不再派发新的校务请求。" xalign 0.5 size 25 color "#d8d2c3"

            hbox:
                xalign 0.5
                spacing 24
                if emergency_available:
                    textbutton "申请一次应急物资":
                        xsize 330
                        ysize 58
                        text_size 20
                        text_color "#e8d19a"
                        text_hover_color "#fff0bd"
                        background Solid("#31291ce8")
                        hover_background Solid("#554225f2")
                        action Return(("emergency", None))
                textbutton "离开请求栏":
                    xsize 280
                    ysize 58
                    text_size 20
                    text_color "#d5c8a6"
                    text_hover_color "#fff0bd"
                    background Solid("#252820e8")
                    hover_background Solid("#45483cef")
                    action Return(("close", None))


label campus_office_request_board:
    if campaign_day < 3 or campaign_day > 42:
        return
    call screen campus_request_board
    $ campus_board_action, campus_board_value = _return
    if campus_board_action == "accept":
        $ campus_accept_request(campus_board_value)
    elif campus_board_action == "emergency":
        $ emergency_stock_id = campus_emergency_supply()
        if emergency_stock_id:
            $ mc45_last_result = "临时调拨了4份%s；但校务处记下了这次额外求援。" % CAMPUS_STOCK_NAMES[emergency_stock_id]
    return
