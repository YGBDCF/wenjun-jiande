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

    def campaign_event_pages(event):
        pages = []
        for paragraph in event.get("narrative_segments", event.get("opening", [])):
            pages.append({"kind": "narrative", "text": paragraph})
        dialogue = event.get("dialogue_nodes", [])
        if dialogue:
            pages.append({"kind": "dialogue", "lines": dialogue})
        if not pages:
            pages.append({"kind": "narrative", "text": "现场记录暂缺。"})
        return pages

    def campaign_event_scene_image(event, reader_page=0):
        illustration = event.get("illustration_path")
        if illustration and int(reader_page) >= 1 and renpy.loadable(illustration):
            return illustration
        if event.get("location_id") == "classroom" and renpy.loadable(campaign_classroom_background()):
            return campaign_classroom_background()
        return campaign_location_background(store.current_location)

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

    def campaign_location_base_progress(location_id, event=None):
        """每次地点行动的稳定收益；随机事件本身的代价仍由事件JSON决定。"""
        location_id = {
            "residence": "minju",
            "student_dormitory": "dormitory",
        }.get(location_id, location_id)
        effects = {}
        if location_id in ("kongmiao", "classroom"):
            effects = {"prep": 4, "course": 1}
            store.daily_knowledge_actions += 1
        elif location_id == "linchang":
            effects = {"practical": 1, "material": 1}
        elif location_id == "office":
            effects = {"reputation": 1, "public": 1}
        elif location_id == "minju":
            effects = {"morality": 1, "resident": 1}
        elif location_id == "pawnshop":
            effects = {"practical": 1, "material": 1}
        elif location_id == "dock":
            effects = {"practical": 1, "migration": 1}
        elif location_id == "dormitory":
            effects = {"will": 1, "dorm_order": 1}
        elif location_id == "zhu_residence":
            effects = {"will": 1, "reputation": 1}
            store.hidden_zhu_impression = campaign_clamp(store.hidden_zhu_impression + 1, -10, 10)
        campaign_apply_canonical_effects(effects)

        title = event.get("title", "地点活动") if event else "地点活动"
        store.daily_action_log.append({
            "day": store.campaign_day,
            "period": store.campaign_period,
            "location": location_id,
            "title": title,
            "effects": dict(effects),
        })
        store.daily_action_log = store.daily_action_log[-135:]
        campaign_update_newspaper_preparation(location_id)

    def campaign_update_newspaper_preparation(location_id):
        """Day10—19把日常地点工作接入创刊筹备，不改变史实中的创刊结果。"""
        if not (10 <= store.campaign_day <= 19):
            return
        store.newspaper_prep_started = True
        flag_by_location = {
            "office": "sources",
            "dock": "delivery",
            "kongmiao": "proofreading",
            "classroom": "proofreading",
            "minju": "distribution",
            "dormitory": "volunteers",
        }
        prep_flag = flag_by_location.get(location_id)
        if prep_flag and prep_flag not in store.newspaper_prep_flags:
            store.newspaper_prep_flags.add(prep_flag)
            store.newspaper_prep_score = min(7, store.newspaper_prep_score + 1)
            store.story_flags.add("newspaper_prep_%s" % prep_flag)

    def campaign_complete_random_event(event, choice_index):
        choice = event["choices"][choice_index]
        campaign_apply_catalog_effects(choice.get("effects", {}))
        campaign_location_base_progress(
            event["location_id"] if event["location_id"] != "global" else store.current_location,
            event,
        )
        store.stat_stamina = max(0, store.stat_stamina - 1)
        store.seen_events.add(event["id"])
        store.recent_events.append(event["id"])
        store.recent_events = store.recent_events[-8:]
        store.event_cooldowns[event["id"]] = store.campaign_day + int(event.get("cooldown", 1))
        follow_text = str(choice.get("follow") or "")
        if follow_text and follow_text != "无":
            store.story_flags.add("follow_%s" % event["id"])
            if "夜归损耗+1" in follow_text or "夜归迟到" in follow_text or "夜归风险上升" in follow_text:
                store.night_return_modifier += 1
                store.night_return_notes.append("白日的决定增加了返宿难度")
            if "夜归损耗-1" in follow_text or "夜归全员安全" in follow_text:
                store.night_return_modifier -= 1
                store.night_return_notes.append("白日的准备降低了返宿风险")
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
    default reader_page = 0
    $ reader_pages = campaign_event_pages(event)
    $ reader_last_page = len(reader_pages) - 1
    $ reader_content = reader_pages[reader_page]
    $ reader_background = campaign_event_scene_image(event, reader_page)

    add reader_background:
        xysize (1920, 1080)
    add Solid("#090b09"):
        alpha 0.18
    frame:
        xpos 55
        ypos 55
        xsize 760
        ysize 140
        background Solid("#11150edc")
        padding (30, 20)
        vbox:
            text event["title"] size 38 color "#ead296"
            text "[event['location']]　[RANDOM_PERIOD_NAME[campaign_period]]　记录 [reader_page + 1] / [len(reader_pages)]" size 19 color "#aaa598"
    frame:
        xpos 170
        ypos 570
        xsize 1580
        ysize 455
        background Solid("#d8c9aaf4")
        padding (52, 34)
        vbox:
            spacing 18
            if reader_content["kind"] == "dialogue":
                text "现场对白" size 22 color "#75613b"
                for line in reader_content["lines"]:
                    text line size 25 color "#28241d" xmaximum 1450 line_spacing 8
            else:
                text reader_content["text"] size 25 color "#28241d" xmaximum 1450 line_spacing 9

            null height 6
            if reader_page < reader_last_page:
                hbox:
                    xalign 1.0
                    spacing 18
                    if reader_page > 0:
                        textbutton "上一页":
                            xsize 160
                            ysize 55
                            text_size 19
                            text_color "#e9d39a"
                            text_hover_color "#fff0bd"
                            text_xalign 0.5
                            text_yalign 0.5
                            background Solid("#171a16f2")
                            hover_background Solid("#4c3b22f2")
                            action SetScreenVariable("reader_page", reader_page - 1)
                    textbutton "继续阅读":
                        xsize 190
                        ysize 55
                        text_size 19
                        text_color "#e9d39a"
                        text_hover_color "#fff0bd"
                        text_xalign 0.5
                        text_yalign 0.5
                        background Solid("#171a16f2")
                        hover_background Solid("#4c3b22f2")
                        action SetScreenVariable("reader_page", reader_page + 1)
            else:
                if len(event["choices"]) <= 3:
                    hbox:
                        xalign 0.5
                        spacing 18
                        for index, choice in enumerate(event["choices"]):
                            textbutton choice["text"]:
                                xsize 470
                                ysize 82
                                text_size 18
                                text_color "#e9d39a"
                                text_hover_color "#fff0bd"
                                text_xalign 0.5
                                text_yalign 0.5
                                background Solid("#171a16f2")
                                hover_background Solid("#4c3b22f2")
                                action Return(index)
                else:
                    grid 2 2:
                        xalign 0.5
                        spacing 16
                        for index, choice in enumerate(event["choices"]):
                            textbutton choice["text"]:
                                xsize 690
                                ysize 68
                                text_size 18
                                text_color "#e9d39a"
                                text_hover_color "#fff0bd"
                                text_xalign 0.5
                                text_yalign 0.5
                                background Solid("#171a16f2")
                                hover_background Solid("#4c3b22f2")
                                action Return(index)
                if reader_page > 0:
                    textbutton "返回上一页":
                        xalign 0.0
                        text_size 17
                        text_color "#6e5b38"
                        text_hover_color "#372b18"
                        background None
                        action SetScreenVariable("reader_page", reader_page - 1)


screen campaign_event_outcome(event, choice_index):
    modal True
    $ outcome_background = campaign_event_scene_image(event, 99)
    add outcome_background:
        xysize (1920, 1080)
    add Solid("#090b09"):
        alpha 0.16
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
