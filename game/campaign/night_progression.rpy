# ================================================================
# 扩展夜归结算：学习节奏、天气、缓存与次日准备
# ================================================================

init python:
    def campaign_forced_return_settlement():
        """晚间行动后的强制返宿：只结算风险，不再给玩家额外行动。"""
        summary = []
        distance_cost = {
            "dock": 1,
            "linchang": 1,
            "pawnshop": 1,
            "office": 0,
            "zhu_residence": 0,
            "minju": 0,
            "kongmiao": 0,
            "classroom": 0,
            "dormitory": -1,
        }.get(store.current_location, 0)
        weather_cost = 0
        if store.current_weather in ("连阴雨", "雨夹雪", "冻雨", "寒潮", "北风"):
            weather_cost = 1
        if store.current_weather in ("冻雨", "雨夹雪") and store.rain_gear_condition <= 0:
            weather_cost += 1

        total_cost = max(0, distance_cost + weather_cost + int(store.night_return_modifier))
        if total_cost:
            store.stat_stamina = campaign_clamp(store.stat_stamina - total_cost, 0, store.stat_stamina_max)
            summary.append("返宿路途：体力-%d" % total_cost)
        else:
            summary.append("返宿路途平安，没有额外损耗")
        if weather_cost:
            summary.append("天气使道路与照明条件变差")
        summary.extend(store.night_return_notes[-2:])
        store.current_location = "dormitory"
        store.night_return_modifier = 0
        store.night_return_notes = []
        return summary

    def campaign_extended_night_settlement():
        summary = []

        if store.daily_knowledge_actions >= 2:
            store.weekly_preparation = campaign_clamp(store.weekly_preparation + 2, 0, 100)
            summary.append("当日学习记录完整，周准备度+2")
        elif store.daily_knowledge_actions == 0 and store.campaign_day not in CAMPAIGN_EXAM_DAYS:
            store.weekly_preparation = campaign_clamp(store.weekly_preparation - 1, 0, 100)
            summary.append("当日未进行学业行动，周准备度-1")

        severe = store.current_weather in ("寒潮", "雨夹雪", "冻雨", "北风")
        wet = store.current_weather in ("小雨", "连阴雨", "雨夹雪", "冻雨", "江雾")
        if severe:
            store.consecutive_severe_weather += 1
            store.weather_hazard_level = min(3, store.weather_hazard_level + 1)
            if store.stat_warmth < 4:
                store.stat_health = max(0, store.stat_health - 1)
                summary.append("保暖不足，健康-1")
        else:
            store.consecutive_severe_weather = 0
            store.weather_hazard_level = max(0, store.weather_hazard_level - 1)

        if wet and store.rain_gear_condition > 0:
            store.rain_gear_condition -= 1

        recovery = 4 if store.stat_health >= 7 else 3
        if store.world_dorm_order < 35:
            recovery -= 1
            summary.append("宿舍秩序偏低，夜间恢复减少")
        store.stat_stamina = campaign_clamp(recovery + 3, 0, store.stat_stamina_max)

        store.previous_weather = store.current_weather
        store.daily_knowledge_actions = 0
        store.virtue_gain_today = 0
        store.cached_turn_event_id = None
        store.cached_turn_context_key = None
        store.current_location = "dormitory"
        store.journal_entries.append({
            "day": store.campaign_day,
            "weather": store.current_weather,
            "campus_score": store.campus_score,
            "preparation": store.weekly_preparation,
            "notes": list(summary),
        })
        store.journal_entries = store.journal_entries[-45:]
        if summary:
            store.campus_last_settlement.extend(summary)
        store.last_night_summary = list(store.campus_last_settlement)
        campaign_normalize_state()
