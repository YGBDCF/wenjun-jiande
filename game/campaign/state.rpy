# ================================================================
# V1.2 建德四十五日：共享战役状态（Phase A0-1）
# 权威规格：docs/CODEX_IMPLEMENTATION_GUIDE.md
# ================================================================

define CAMPAIGN_PERIODS = ("morning", "noon", "evening", "night")
define CAMPAIGN_PERIOD_NAMES = ("早晨", "中午", "晚间", "深夜")
define CAMPAIGN_EXAM_DAYS = (1, 8, 15, 22, 29, 36, 43)
define ZHU_TWO_QUESTIONS = "诸位在校，有两个问题应该自己问问：第一，到浙大来做什么？第二，将来毕业后要做什么样的人？"

# 时间、地点与双地图
default campaign_started = False
default campaign_finished = False
default campaign_day = 1
default campaign_period = 0
default current_location = "dormitory"
default current_weather = "cloudy"
default previous_weather = "cloudy"
default weather_forecast = "cloudy"
default weather_forecast_accuracy = 0.80
default action_count = 0
default days_completed = 0
default night_settlement_count = 0

default active_meta_map = "chapter_world_map"
default map_return_context = None
default cached_turn_event_id = None
default cached_turn_context_key = None
default in_chapter_episode = False
default in_forced_story = False

# 固定章节、地图翻新与报纸系统
default chapter5_unlocked = False
default chapter5_completed = False
default chapter6_unlocked = False
default chapter6_completed = False
default classroom_unlocked = False
default map_visual_phase = "pre_classroom"
default classroom_opening_seen = False

default newspaper_prep_started = False
default newspaper_prep_flags = set()
default newspaper_prep_score = 0
default newspaper_fallback_used = False
default newspaper_system_unlocked = False
default world_newspaper_published = False
default day20_gate_applied = False

default episode_return_day = None
default episode_return_period = None
default episode_return_weather = None
default episode_return_event = None

# 沈砚舟：核心能力 0-20，生存状态 0-10
default stat_knowledge = 3
default stat_morality = 12
default stat_practical = 5
default stat_reputation = 8
default stat_will = 10
default stat_health = 8
default stat_stamina = 8
default stat_stamina_max = 10
default stat_warmth = 3
default hidden_truthfulness = 0
default hidden_zhu_impression = 0

# 学业与考试
default current_week = 1
default weekly_preparation = 20
default weekly_attendance_present = 0
default weekly_attendance_possible = 0
default daily_knowledge_actions = 0
default consecutive_activity_id = None
default consecutive_activity_days = 0
default diagnostic_score = None
default exam_history = []
default cumulative_gpa = 0.0
default academic_misconduct_count = 0
default exam_pending = False

# 世界、关系、物资与事件
default world_course_continuity = 50
default world_material_integrity = 50
default world_resident_trust = 50
default world_dorm_order = 50
default world_public_confidence = 50
default world_migration_readiness = 0
default world_panic = 0

default seen_events = set()
default recent_events = []
default event_cooldowns = {}
default story_flags = set()
default relationship = {"xu_nanzhi": 10, "gu_mingchuan": 5, "zhou_shunan": 0, "mentor": 10}
default inventory = {"paper": 3, "pencil": 2, "lamp_oil": 3, "wood": 0, "meal_ticket": 3, "money": 2}

# PATCH_NEW_GAMEPLAY_SYSTEMS：临时大学运营、社团、羁绊与终局评价。
# 这些字段独立于旧 inventory，避免破坏现有章节和旧存档。
default campus_stock = {"wood": 8, "paper": 16, "lamp_oil": 10, "grain": 20, "medicine": 4}
default campus_repair_backlog = 0
default campus_score = 50
default accepted_campus_request = None
default accepted_campus_request_day = None
default completed_campus_requests = set()
default campus_request_day = None
default campus_request_choices = []
default campus_last_settlement = []
default campus_shortages = set()
default emergency_supply_used_week = -1

default primary_club = None
default club_xp = {"academic": 0, "work_study": 0, "repair": 0, "news": 0}
default club_rank = {"academic": 0, "work_study": 0, "repair": 0, "news": 0}
default club_switch_used = False
default club_weekly_done = set()
default club_events_seen = set()

default bond_flags = set()
default bond_pending_tasks = {}
default bond_events_seen = set()
default virtue_truth = 5
default virtue_service = 4
default virtue_innovation = 3
default virtue_gain_today = 0
default journal_entries = []
default journal_focus_counts = {"study": 0, "people": 0, "service": 0, "truth": 0, "memory": 0}
default archive_items = set()
default archive_memories_seen = set()

default weather_hazard_level = 0
default consecutive_severe_weather = 0
default rain_gear_condition = 2
default classroom_warmth = 40
default dormitory_warmth = 45
default integrity_violations = 0
default newspaper_accuracy = 50
default newspaper_tasks_completed = 0
default minigame_results = {}
default weekly_reflections = []
default final_evaluation = {}
default daily_action_log = []
default last_night_summary = []
default night_return_modifier = 0
default night_return_notes = []

init python:
    import copy
    import datetime

    CAMPAIGN_START_DATE = datetime.date(1937, 11, 12)

    def campaign_clamp(value, low, high):
        return max(low, min(high, value))

    def campaign_date(day=None):
        value = store.campaign_day if day is None else day
        value = campaign_clamp(int(value), 1, 45)
        return CAMPAIGN_START_DATE + datetime.timedelta(days=value - 1)

    def campaign_date_text(day=None):
        value = campaign_date(day)
        return "%d年%d月%d日" % (value.year, value.month, value.day)

    def campaign_turn_key():
        return (store.campaign_day, store.campaign_period, store.current_location)

    def campaign_snapshot():
        """地图往返前后用于验证状态未变化的轻量快照。"""
        return (
            store.campaign_day,
            store.campaign_period,
            store.current_weather,
            store.stat_stamina,
            store.cached_turn_event_id,
            store.action_count,
        )

    def campaign_normalize_state():
        store.campaign_day = campaign_clamp(int(store.campaign_day), 1, 45)
        store.campaign_period = campaign_clamp(int(store.campaign_period), 0, 3)
        store.stat_knowledge = campaign_clamp(int(store.stat_knowledge), 0, 20)
        store.stat_morality = campaign_clamp(int(store.stat_morality), 0, 20)
        store.stat_practical = campaign_clamp(int(store.stat_practical), 0, 20)
        store.stat_reputation = campaign_clamp(int(store.stat_reputation), 0, 20)
        store.stat_will = campaign_clamp(int(store.stat_will), 0, 20)
        store.stat_health = campaign_clamp(int(store.stat_health), 0, 10)
        store.stat_stamina = campaign_clamp(int(store.stat_stamina), 0, 10)
        store.stat_warmth = campaign_clamp(int(store.stat_warmth), 0, 10)
        store.hidden_truthfulness = campaign_clamp(int(store.hidden_truthfulness), -10, 10)
        store.days_completed = campaign_clamp(int(store.days_completed), 0, 45)
        store.virtue_truth = campaign_clamp(int(store.virtue_truth), 0, 20)
        store.virtue_service = campaign_clamp(int(store.virtue_service), 0, 20)
        store.virtue_innovation = campaign_clamp(int(store.virtue_innovation), 0, 20)
        store.virtue_gain_today = campaign_clamp(int(store.virtue_gain_today), 0, 2)
        store.campus_repair_backlog = max(0, int(store.campus_repair_backlog))
        store.campus_score = campaign_clamp(int(store.campus_score), 0, 100)
        store.weather_hazard_level = campaign_clamp(int(store.weather_hazard_level), 0, 3)
        store.consecutive_severe_weather = max(0, int(store.consecutive_severe_weather))
        store.rain_gear_condition = campaign_clamp(int(store.rain_gear_condition), 0, 2)
        store.classroom_warmth = campaign_clamp(int(store.classroom_warmth), 0, 100)
        store.dormitory_warmth = campaign_clamp(int(store.dormitory_warmth), 0, 100)
        store.newspaper_accuracy = campaign_clamp(int(store.newspaper_accuracy), 0, 100)
        for person_id in ("xu_nanzhi", "gu_mingchuan", "zhou_shunan", "mentor"):
            store.relationship[person_id] = campaign_clamp(int(store.relationship.get(person_id, 0)), 0, 100)
        if store.campaign_period == 3:
            store.current_location = "dormitory"

    def _campaign_add_missing(name, value):
        """只补缺失字段；绝不覆盖旧存档中已有的玩家进度。"""
        if not hasattr(store, name):
            setattr(store, name, copy.deepcopy(value))

    def _campaign_convert_core_scale(name):
        """补丁规定核心能力统一为 0–20；旧 0–100 存档按五等分迁移。"""
        value = int(getattr(store, name))
        if value > 20:
            value = int(round(value / 5.0))
        setattr(store, name, campaign_clamp(value, 0, 20))

    def migrate_gameplay_patch_save():
        """将补丁新增系统安全地接入新游戏和任意版本的旧存档。"""
        defaults = {
            "campus_stock": {"wood": 8, "paper": 16, "lamp_oil": 10, "grain": 20, "medicine": 4},
            "campus_repair_backlog": 0,
            "campus_score": 50,
            "accepted_campus_request": None,
            "accepted_campus_request_day": None,
            "completed_campus_requests": set(),
            "campus_request_day": None,
            "campus_request_choices": [],
            "campus_last_settlement": [],
            "campus_shortages": set(),
            "emergency_supply_used_week": -1,
            "primary_club": None,
            "club_xp": {"academic": 0, "work_study": 0, "repair": 0, "news": 0},
            "club_rank": {"academic": 0, "work_study": 0, "repair": 0, "news": 0},
            "club_switch_used": False,
            "club_weekly_done": set(),
            "club_events_seen": set(),
            "bond_flags": set(),
            "bond_pending_tasks": {},
            "bond_events_seen": set(),
            "virtue_service": 4,
            "virtue_innovation": 3,
            "virtue_gain_today": 0,
            "journal_entries": [],
            "journal_focus_counts": {"study": 0, "people": 0, "service": 0, "truth": 0, "memory": 0},
            "archive_items": set(),
            "archive_memories_seen": set(),
            "weather_hazard_level": 0,
            "consecutive_severe_weather": 0,
            "rain_gear_condition": 2,
            "classroom_warmth": 40,
            "dormitory_warmth": 45,
            "integrity_violations": 0,
            "newspaper_accuracy": 50,
            "newspaper_tasks_completed": 0,
            "minigame_results": {},
            "weekly_reflections": [],
            "final_evaluation": {},
            "day20_gate_applied": False,
            "daily_action_log": [],
            "last_night_summary": [],
            "night_return_modifier": 0,
            "night_return_notes": [],
        }
        for field_name, field_default in defaults.items():
            _campaign_add_missing(field_name, field_default)

        if not hasattr(store, "virtue_truth"):
            legacy_truth = int(getattr(store, "hidden_truthfulness", 5))
            store.virtue_truth = campaign_clamp(legacy_truth, 0, 20)

        _campaign_add_missing(
            "relationship",
            {"xu_nanzhi": 10, "gu_mingchuan": 5, "zhou_shunan": 0, "mentor": 10},
        )
        relationship_defaults = {"xu_nanzhi": 10, "gu_mingchuan": 5, "zhou_shunan": 0, "mentor": 10}
        for person_id, initial_value in relationship_defaults.items():
            if person_id not in store.relationship:
                store.relationship[person_id] = initial_value

        stock_defaults = {"wood": 8, "paper": 16, "lamp_oil": 10, "grain": 20, "medicine": 4}
        for stock_id, initial_value in stock_defaults.items():
            if stock_id not in store.campus_stock:
                store.campus_stock[stock_id] = initial_value

        club_defaults = {"academic": 0, "work_study": 0, "repair": 0, "news": 0}
        for club_id in club_defaults:
            if club_id not in store.club_xp:
                store.club_xp[club_id] = 0
            if club_id not in store.club_rank:
                store.club_rank[club_id] = 0

        for focus_id in ("study", "people", "service", "truth", "memory"):
            if focus_id not in store.journal_focus_counts:
                store.journal_focus_counts[focus_id] = 0

        for core_name in ("stat_knowledge", "stat_morality", "stat_practical", "stat_reputation", "stat_will"):
            _campaign_convert_core_scale(core_name)

        campaign_normalize_state()
        return True

    def campaign_gain_virtue(virtue_id, amount):
        """正向品格成长每日合计最多2点；负向结果不受此上限保护。"""
        field_name = {
            "truth": "virtue_truth",
            "service": "virtue_service",
            "innovation": "virtue_innovation",
        }[virtue_id]
        amount = int(amount)
        if amount > 0:
            allowed = max(0, 2 - store.virtue_gain_today)
            amount = min(amount, allowed)
            store.virtue_gain_today += amount
        current = int(getattr(store, field_name))
        setattr(store, field_name, campaign_clamp(current + amount, 0, 20))
        return amount

    def campaign_relationship_adjust(person_id, amount):
        current = int(store.relationship.get(person_id, 0))
        store.relationship[person_id] = campaign_clamp(current + int(amount), 0, 100)
        return store.relationship[person_id]

    def campaign_relationship_tier(person_id):
        value = int(store.relationship.get(person_id, 0))
        if value >= 85:
            return "同路"
        if value >= 65:
            return "知己"
        if value >= 40:
            return "信任"
        if value >= 20:
            return "熟悉"
        return "初识"

    def campaign_apply_canonical_effects(effects):
        """供羁绊、社团和随机事件共用的安全数值入口。"""
        core_fields = {
            "knowledge": "stat_knowledge",
            "morality": "stat_morality",
            "practical": "stat_practical",
            "reputation": "stat_reputation",
            "will": "stat_will",
        }
        world_fields = {
            "course": "world_course_continuity",
            "material": "world_material_integrity",
            "resident": "world_resident_trust",
            "dorm_order": "world_dorm_order",
            "public": "world_public_confidence",
            "migration": "world_migration_readiness",
            "panic": "world_panic",
        }
        for key, raw_amount in effects.items():
            amount = int(raw_amount)
            if key in core_fields:
                field = core_fields[key]
                setattr(store, field, campaign_clamp(int(getattr(store, field)) + amount, 0, 20))
            elif key == "health":
                store.stat_health = campaign_clamp(store.stat_health + amount, 0, 10)
            elif key == "stamina":
                store.stat_stamina = campaign_clamp(store.stat_stamina + amount, 0, store.stat_stamina_max)
            elif key == "warmth":
                store.stat_warmth = campaign_clamp(store.stat_warmth + amount, 0, 10)
            elif key == "prep":
                store.weekly_preparation = campaign_clamp(store.weekly_preparation + amount, 0, 100)
            elif key in world_fields:
                field = world_fields[key]
                setattr(store, field, campaign_clamp(int(getattr(store, field)) + amount, 0, 100))
            elif key in ("truth", "service", "innovation"):
                campaign_gain_virtue(key, amount)
            elif key.startswith("rel_"):
                campaign_relationship_adjust(key[4:], amount)
            elif key.startswith("stock_"):
                stock_id = key[6:]
                if stock_id in store.campus_stock:
                    store.campus_stock[stock_id] = max(0, int(store.campus_stock[stock_id]) + amount)
            elif key == "backlog":
                store.campus_repair_backlog = max(0, store.campus_repair_backlog + amount)
            elif key == "accuracy":
                store.newspaper_accuracy = campaign_clamp(store.newspaper_accuracy + amount, 0, 100)
            elif key == "integrity":
                store.integrity_violations = max(0, store.integrity_violations + amount)

    def campaign_migrate_legacy_state():
        """把已有 mc45 存档一次性映射到 V1.2，不删除旧字段。"""
        legacy_started = getattr(store, "mc45_started", False)
        if legacy_started and not store.campaign_started:
            store.campaign_started = True
            store.campaign_day = campaign_clamp(int(getattr(store, "mc45_day", 1)), 1, 45)
            store.campaign_period = campaign_clamp(int(getattr(store, "mc45_time", 0)), 0, 3)
            store.current_weather = getattr(store, "mc45_weather", "cloudy")
            store.stat_knowledge = campaign_clamp(int(getattr(store, "mc45_knowledge", 3)), 0, 20)
            store.stat_practical = campaign_clamp(int(getattr(store, "mc45_practice", 5)), 0, 20)
            store.stat_reputation = campaign_clamp(int(getattr(store, "mc45_reputation", 8)), 0, 20)
            store.stat_will = campaign_clamp(int(getattr(store, "mc45_will", 10)), 0, 20)
            store.stat_health = campaign_clamp(int(round(getattr(store, "mc45_health", 80) / 10.0)), 0, 10)
            store.stat_stamina = campaign_clamp(int(getattr(store, "mc45_stamina", 8)), 0, 10)
            store.stat_warmth = campaign_clamp(int(getattr(store, "mc45_warmth", 3)), 0, 10)
            store.hidden_truthfulness = campaign_clamp(int(getattr(store, "mc45_truth", 0)), -10, 10)
            store.days_completed = campaign_clamp(store.campaign_day - 1, 0, 45)

        migrate_gameplay_patch_save()
        campaign_normalize_state()

    def campaign_sync_legacy_view():
        """过渡期间让旧梅城界面显示同一套日期、时段和基础状态。"""
        if not hasattr(store, "mc45_day"):
            return
        store.mc45_started = store.campaign_started
        store.mc45_day = store.campaign_day
        store.mc45_time = store.campaign_period
        store.mc45_weather = store.current_weather
        store.mc45_knowledge = store.stat_knowledge
        store.mc45_practice = store.stat_practical
        store.mc45_reputation = store.stat_reputation
        store.mc45_will = store.stat_will
        store.mc45_truth = store.hidden_truthfulness
        store.mc45_stamina = store.stat_stamina
        store.mc45_health = store.stat_health * 10
        store.mc45_warmth = store.stat_warmth

    def campaign_import_legacy_turn():
        """旧界面完成一次行动后，把结果写回 V1.2 共享状态。"""
        if not getattr(store, "mc45_started", False):
            return
        store.campaign_started = True
        store.campaign_day = campaign_clamp(int(store.mc45_day), 1, 45)
        store.campaign_period = campaign_clamp(int(store.mc45_time), 0, 3)
        store.current_weather = store.mc45_weather
        store.stat_knowledge = campaign_clamp(int(store.mc45_knowledge), 0, 20)
        store.stat_practical = campaign_clamp(int(store.mc45_practice), 0, 20)
        store.stat_reputation = campaign_clamp(int(store.mc45_reputation), 0, 20)
        store.stat_will = campaign_clamp(int(store.mc45_will), 0, 20)
        store.stat_health = campaign_clamp(int(round(store.mc45_health / 10.0)), 0, 10)
        store.stat_stamina = campaign_clamp(int(store.mc45_stamina), 0, 10)
        store.stat_warmth = campaign_clamp(int(store.mc45_warmth), 0, 10)
        store.hidden_truthfulness = campaign_clamp(int(store.mc45_truth), -10, 10)
        store.action_count = min(135, len(store.mc45_event_history))
        store.days_completed = campaign_clamp(store.campaign_day - 1, 0, 45)
        if store.campaign_period == 3:
            store.current_location = "dormitory"
        campaign_normalize_state()

    def campaign_begin():
        campaign_migrate_legacy_state()
        migrate_gameplay_patch_save()
        if not store.campaign_started:
            store.campaign_started = True
            store.campaign_day = 1
            store.campaign_period = 0
            store.current_location = "dormitory"
            store.current_weather = "江雾"
            store.previous_weather = "江雾"
            store.weather_forecast = "江雾"
            store.active_meta_map = "jiande_exploration_map"
        campaign_normalize_state()
        campaign_sync_legacy_view()
