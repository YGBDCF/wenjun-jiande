# ================================================================
# V1.2 开发断言。仅供开发验证，不进入正式剧情。
# ================================================================

init python:
    def campaign_assert_a0_state():
        assert 1 <= store.campaign_day <= 45
        assert 0 <= store.campaign_period <= 3
        assert 0 <= store.stat_knowledge <= 20
        assert 0 <= store.stat_morality <= 20
        assert 0 <= store.stat_practical <= 20
        assert 0 <= store.stat_reputation <= 20
        assert 0 <= store.stat_will <= 20
        assert 0 <= store.stat_health <= 10
        assert 0 <= store.stat_stamina <= 10
        assert -10 <= store.hidden_truthfulness <= 10
        if store.campaign_period == 3:
            assert store.current_location == "dormitory"
        assert store.active_meta_map in ("chapter_world_map", "jiande_exploration_map")
        return True

    def campaign_assert_switch_cost(before, after):
        assert before == after
        return True

    def campaign_assert_exam_schedule():
        assert CAMPAIGN_EXAM_DAYS == (1, 8, 15, 22, 29, 36, 43)
        assert CAMPAIGN_EXAM_CONFIG[1]["credit"] == 0.0
        assert all(CAMPAIGN_EXAM_CONFIG[day]["credit"] > 0 for day in CAMPAIGN_EXAM_DAYS[1:])
        assert all(len(CAMPAIGN_EXAM_QUESTIONS[day]) == 3 for day in CAMPAIGN_EXAM_DAYS)
        assert campaign_score_to_gpa(97, False) == 4.8
        assert campaign_score_to_gpa(97, True) == 5.0
        return True

    def campaign_assert_gameplay_patch_state():
        assert set(store.campus_stock.keys()) == set(CAMPUS_STOCK_CAPS.keys())
        assert all(0 <= store.campus_stock[key] <= cap for key, cap in CAMPUS_STOCK_CAPS.items())
        assert 0 <= store.campus_score <= 100
        assert 0 <= store.virtue_truth <= 20
        assert 0 <= store.virtue_service <= 20
        assert 0 <= store.virtue_innovation <= 20
        assert 0 <= store.virtue_gain_today <= 2
        assert set(store.club_xp.keys()) == {"academic", "work_study", "repair", "news"}
        assert set(store.relationship.keys()) >= {"xu_nanzhi", "gu_mingchuan", "zhou_shunan", "mentor"}
        assert all(0 <= value <= 100 for value in store.relationship.values())
        assert campus_recalculate_score() == store.campus_score
        assert len(RANDOM_EVENT_CATALOG) == 83
        assert all(len(event.get("choices", [])) >= 2 for event in RANDOM_EVENT_CATALOG)
        assert all(
            any(bool(choice.get("effects")) or bool(choice.get("follow")) for choice in event["choices"])
            for event in RANDOM_EVENT_CATALOG
        )
        assert isinstance(store.daily_action_log, list)
        assert isinstance(store.last_night_summary, list)
        assert isinstance(store.night_return_modifier, int)
        return True

    def campaign_assert_campus_stock_caps():
        old_wood = store.campus_stock["wood"]
        store.campus_stock["wood"] = CAMPUS_STOCK_CAPS["wood"]
        assert campus_stock_adjust("wood", 99) == 0
        assert store.campus_stock["wood"] == CAMPUS_STOCK_CAPS["wood"]
        store.campus_stock["wood"] = 0
        assert campus_stock_adjust("wood", -99) == 0
        assert store.campus_stock["wood"] == 0
        store.campus_stock["wood"] = old_wood
        return True


label campaign_dev_a0_check:
    $ campaign_begin()
    $ campaign_assert_a0_state()
    $ campaign_assert_exam_schedule()
    $ campaign_assert_gameplay_patch_state()
    $ campaign_assert_campus_stock_caps()
    $ before_switch = campaign_snapshot()
    $ active_meta_map = "chapter_world_map"
    $ active_meta_map = "jiande_exploration_map"
    $ campaign_assert_switch_cost(before_switch, campaign_snapshot())
    return
