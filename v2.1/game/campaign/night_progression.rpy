# ================================================================
# 扩展夜归结算：学习节奏、天气、缓存与次日准备
# ================================================================

init python:
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
        campaign_normalize_state()
