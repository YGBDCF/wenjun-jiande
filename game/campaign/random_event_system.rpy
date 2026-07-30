# ================================================================
# 83条地点随机事件：JSON数据驱动、缓存、冷却与统一结算
# ================================================================

init python:
    import json
    import re

    _event_file = renpy.open_file("data/random_event_catalog.json")
    RANDOM_EVENT_CATALOG = json.loads(_event_file.read().decode("utf-8"))
    _event_file.close()
    RANDOM_EVENT_BY_ID = dict((event["id"], event) for event in RANDOM_EVENT_CATALOG)

    RANDOM_PERIOD_NAME = {0: "早晨", 1: "中午", 2: "晚间", 3: "深夜结算"}

    def campaign_event_weather_matches(event_weather):
        if "任意" in event_weather:
            return True
        current = str(store.current_weather)
        if current in event_weather:
            return True
        wet = ("江雾", "小雨", "连阴雨", "雨夹雪", "冻雨")
        if current in wet and any(value in wet for value in event_weather):
            return True
        calm = ("晴", "晴冷", "阴")
        if current in calm and any(value in calm for value in event_weather):
            return True
        return False

    def campaign_days_until_next_exam():
        future = [day for day in CAMPAIGN_EXAM_DAYS if day >= store.campaign_day]
        return (future[0] - store.campaign_day) if future else 99

    def campaign_event_prereq_ok(text):
        text = str(text or "无")
        if text in ("无", "固定执行"):
            return True
        if "chapter5_completed == True" in text and not store.chapter5_completed:
            return False
        if "classroom_unlocked == True" in text and not store.classroom_unlocked:
            return False
        if "《浙大日报》线已开启" in text and not store.chapter6_completed:
            return False
        if "四库支线开启" in text and 3 not in store.day1_completed_chapters:
            return False
        if "前两日有雨" in text or "前日为小雨或连阴雨" in text:
            if store.previous_weather not in ("小雨", "连阴雨", "雨夹雪", "冻雨", "江雾"):
                return False
        if "days_until_next_exam <= 2" in text and campaign_days_until_next_exam() > 2:
            return False
        if "official_exam_count > 0" in text and not store.exam_history:
            return False
        if "official_exam_active == True" in text:
            return False
        if "campaign_day == 43" in text and store.campaign_day != 43:
            return False

        value_sources = {
            "学识": store.stat_knowledge,
            "人望": store.stat_reputation,
            "心志": store.stat_will,
            "保暖": store.stat_warmth,
            "求实": store.virtue_truth,
            "居民信任": store.world_resident_trust,
            "迁移准备": store.world_migration_readiness,
            "木料": store.campus_stock["wood"],
            "灯油": store.campus_stock["lamp_oil"],
            "许南枝关系": store.relationship.get("xu_nanzhi", 0),
            "顾明川关系": store.relationship.get("gu_mingchuan", 0),
            "周顺安关系": store.relationship.get("zhou_shunan", 0),
            "陈同学关系": 0,
            "导师关系": store.relationship.get("mentor", 0),
            "船工信任": store.world_resident_trust,
            "宿舍容量": store.world_dorm_order,
            "道路通行度": store.world_migration_readiness,
        }
        for label, current in value_sources.items():
            match = re.search(re.escape(label) + r"\s*(>=|<=|>|<|=)\s*(-?\d+)", text)
            if not match:
                continue
            operator, wanted_text = match.groups()
            wanted = int(wanted_text)
            checks = {
                ">=": current >= wanted, "<=": current <= wanted,
                ">": current > wanted, "<": current < wanted, "=": current == wanted,
            }
            if not checks[operator]:
                return False
        # 无法安全解析的叙事前置条件保持宽容，避免目录内容永久不可见。
        return True

    def campaign_event_unlock_ok(event):
        group = event.get("unlock_group", "base")
        if group == "post_ch5":
            return store.chapter5_completed
        if group == "classroom":
            return store.classroom_unlocked
        if group in ("classroom_exam_conduct", "classroom_exam_weather"):
            return False
        return True

    def campaign_random_event_candidates(location_id):
        period_name = RANDOM_PERIOD_NAME[store.campaign_period]
        candidates = []
        for event in RANDOM_EVENT_CATALOG:
            if event["location_id"] not in (location_id, "global"):
                continue
            if not (int(event["days"][0]) <= store.campaign_day <= int(event["days"][1])):
                continue
            if period_name not in event["periods"]:
                continue
            if not campaign_event_weather_matches(event["weather"]):
                continue
            if not campaign_event_unlock_ok(event) or not campaign_event_prereq_ok(event.get("prereq")):
                continue
            if int(store.event_cooldowns.get(event["id"], 0)) > store.campaign_day:
                continue
            candidates.append(event)
        return candidates

    def campaign_pick_random_event(location_id):
        context = (store.campaign_day, store.campaign_period, location_id, store.current_weather)
        if store.cached_turn_context_key == context and store.cached_turn_event_id in RANDOM_EVENT_BY_ID:
            return RANDOM_EVENT_BY_ID[store.cached_turn_event_id]
        candidates = campaign_random_event_candidates(location_id)
        if not candidates:
            store.cached_turn_context_key = context
            store.cached_turn_event_id = None
            return None
        unseen_local = [event for event in candidates if event["id"] not in store.seen_events and event["location_id"] == location_id]
        unseen_any = [event for event in candidates if event["id"] not in store.seen_events]
        non_recent = [event for event in candidates if event["id"] not in store.recent_events]
        pool = unseen_local or unseen_any or non_recent or candidates
        chosen = renpy.random.choice(pool)
        store.cached_turn_context_key = context
        store.cached_turn_event_id = chosen["id"]
        return chosen

    def campaign_apply_catalog_effects(effects):
        canonical = {}
        direct = {
            "学识": "knowledge", "道德": "morality", "实务": "practical",
            "人望": "reputation", "心志": "will", "健康": "health",
            "体力": "stamina", "保暖": "warmth", "周准备": "prep",
            "求实": "truth", "课程连续度": "course",
            "物资完整度": "material", "居民信任": "resident",
            "宿舍秩序": "dorm_order", "校务公信": "public",
            "迁移准备": "migration", "恐慌": "panic",
            "木料": "stock_wood", "纸张": "stock_paper",
            "灯油": "stock_lamp_oil", "导师关系": "rel_mentor",
            "许南枝关系": "rel_xu_nanzhi", "顾明川关系": "rel_gu_mingchuan",
            "周顺安关系": "rel_zhou_shunan", "诚信次数": "integrity",
        }
        for key, amount in effects.items():
            if key in direct:
                canonical[direct[key]] = canonical.get(direct[key], 0) + int(amount)
            elif key in ("钱", "饭票", "铅笔"):
                inventory_key = {"钱": "money", "饭票": "meal_ticket", "铅笔": "pencil"}[key]
                store.inventory[inventory_key] = max(0, int(store.inventory.get(inventory_key, 0)) + int(amount))
            elif key in ("孔庙修缮度", "教室修缮", "课桌", "林场秩序", "校务秩序", "安全度"):
                canonical["backlog"] = canonical.get("backlog", 0) - int(round(int(amount) / 5.0))
            elif key in ("文化保护", "地图", "记忆碎片"):
                if int(amount) > 0:
                    store.archive_items.add("%s_%s" % (key, store.campaign_day))
            elif key in ("疲劳惩罚", "宿舍疲劳"):
                canonical["stamina"] = canonical.get("stamina", 0) - max(0, int(amount))
            elif key in ("迁移风险", "归档风险", "火灾风险", "校务压力"):
                canonical["panic"] = canonical.get("panic", 0) + int(amount)
            else:
                store.story_flags.add("catalog_effect_%s_%s" % (key, int(amount)))
        campaign_apply_canonical_effects(canonical)

    def campaign_location_base_progress(location_id):
        if location_id in ("kongmiao", "classroom"):
            store.weekly_preparation = campaign_clamp(store.weekly_preparation + 2, 0, 100)
            store.daily_knowledge_actions += 1
            store.weekly_attendance_possible += 1
            store.weekly_attendance_present += 1
        elif location_id in ("linchang", "dock", "pawnshop"):
            store.stat_practical = campaign_clamp(store.stat_practical + 1, 0, 20)
        elif location_id in ("minju", "dormitory"):
            store.stat_morality = campaign_clamp(store.stat_morality + 1, 0, 20)
        elif location_id in ("office", "zhu_residence"):
            store.stat_reputation = campaign_clamp(store.stat_reputation + 1, 0, 20)

    def campaign_complete_random_event(event, choice_index):
        choice = event["choices"][choice_index]
        campaign_apply_catalog_effects(choice.get("effects", {}))
        campaign_location_base_progress(event["location_id"] if event["location_id"] != "global" else store.current_location)
        store.stat_stamina = max(0, store.stat_stamina - 1)
        store.seen_events.add(event["id"])
        store.recent_events.append(event["id"])
        store.recent_events = store.recent_events[-8:]
        store.event_cooldowns[event["id"]] = store.campaign_day + int(event.get("cooldown", 1))
        if choice.get("follow"):
            store.story_flags.add("follow_%s" % event["id"])
        approach = "verify" if any(key in choice.get("effects", {}) for key in ("求实", "学识")) else ("practice" if "实务" in choice.get("effects", {}) else "care")
        campus_try_complete_request(store.current_location, approach)
        store.mc45_event_history.append((store.campaign_day, store.campaign_period, store.current_location, event["title"], choice_index))
        store.action_count = min(135, store.action_count + 1)
        store.mc45_time = min(3, store.mc45_time + 1)
        store.campaign_period = store.mc45_time
        store.cached_turn_event_id = None
        store.cached_turn_context_key = None
        campaign_sync_legacy_view()


screen campaign_random_event(event):
    modal True
    add MC45_LOCATION_META[current_location][1]:
        xysize (1920, 1080)
    frame:
        xpos 55
        ypos 55
        xsize 760
        ysize 140
        background Solid("#11150edc")
        padding (30, 20)
        vbox:
            text event["title"] size 38 color "#ead296"
            text "[event['location']]　[RANDOM_PERIOD_NAME[campaign_period]]" size 19 color "#aaa598"
    frame:
        xpos 245
        ypos 625
        xsize 1430
        ysize 390
        background Solid("#d8c9aaed")
        padding (42, 30)
        vbox:
            spacing 14
            for line in event["opening"]:
                text line size 23 color "#28241d" xmaximum 1320 line_spacing 6
            null height 8
            hbox:
                spacing 16
                for index, choice in enumerate(event["choices"]):
                    textbutton choice["text"]:
                        xsize 430
                        ysize 92
                        text_size 19
                        text_color "#e9d39a"
                        text_hover_color "#fff0bd"
                        text_xalign 0.5
                        text_yalign 0.5
                        background Solid("#171a16f2")
                        hover_background Solid("#4c3b22f2")
                        action Return(index)


screen campaign_event_outcome(event, choice_index):
    modal True
    add MC45_LOCATION_META[current_location][1]:
        xysize (1920, 1080)
    frame:
        xpos 280
        ypos 670
        xsize 1360
        ysize 300
        background Solid("#d8c9aaee")
        padding (45, 32)
        vbox:
            spacing 16
            for line in event["choices"][choice_index]["lines"]:
                text line size 24 color "#28241d" xmaximum 1250 line_spacing 7
            if event["choices"][choice_index].get("follow"):
                text "后续：[event['choices'][choice_index]['follow']]" size 18 color "#6e5b38"
            textbutton "记入行动记录":
                xalign 1.0
                text_size 20
                text_color "#f1dba0"
                background Solid("#1a1d18ef")
                hover_background Solid("#504025ef")
                action Return()


label campaign_random_event_label(event):
    call screen campaign_random_event(event)
    $ catalog_choice_index = _return
    call screen campaign_event_outcome(event, catalog_choice_index)
    $ campaign_complete_random_event(event, catalog_choice_index)
    $ mc45_last_result = "完成随机事件“%s”。已阅事件 %d / 83。" % (event["title"], len(seen_events))
    return
