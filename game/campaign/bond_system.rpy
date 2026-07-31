# ================================================================
# 固定羁绊事件：许南枝、顾明川、周树南（无恋爱路线）
# ================================================================

init python:
    BOND_EVENTS = (
        {
            "id": "XN_BOND_01", "person": "xu_nanzhi", "name": "许南枝",
            "days": (4, 9), "locations": ("kongmiao",), "periods": (0,), "relation": 10,
            "title": "缺页的课堂笔记",
            "body": "一页课堂笔记沾了雨，几个关键字已经模糊。许南枝不愿凭记忆把空白填满。",
            "choices": (
                ("找三名同学逐句核对", {"knowledge": 1, "truth": 1, "rel_xu_nanzhi": 8}, "xn_verified_notes"),
                ("按上下文补齐缺字", {"knowledge": 1, "rel_xu_nanzhi": 2}, "xn_context_guess"),
                ("缺一页并不碍事", {"will": 1, "rel_xu_nanzhi": -4}, None),
            ),
        },
        {
            "id": "XN_BOND_02", "person": "xu_nanzhi", "name": "许南枝",
            "days": (26, 31), "locations": ("dormitory",), "periods": (2,), "relation": 35,
            "title": "迟迟未到的家书",
            "body": "同乡捎来的家书没有许南枝家的消息。她把信封翻看了几遍，没有问出那句最担心的话。",
            "choices": (
                ("把已知与未知分开写下", {"truth": 1, "will": 1, "rel_xu_nanzhi": 12}, "xn_known_unknown"),
                ("先说家中一定平安", {"integrity": 1, "truth": -1, "rel_xu_nanzhi": 3}, None),
                ("明日去校务处核对邮路", {}, "xn_postal_route_pending"),
            ),
        },
        {
            "id": "XN_BOND_03", "person": "xu_nanzhi", "name": "许南枝",
            "days": (41, 44), "locations": ("minju", "dormitory"), "periods": (1, 2), "relation": 65,
            "title": "名单上的梅城人",
            "body": "离校前的感谢名单里，有几户居民的姓名和住址仍未核实。版面已经催了两次。",
            "choices": (
                ("逐户核对姓名再刊出", {"stock_paper": -1, "accuracy": 5, "resident": 5, "rel_xu_nanzhi": 12}, "xn_names_verified"),
                ("统称为“梅城百姓”", {"public": 1, "rel_xu_nanzhi": -2}, None),
                ("补一段未经核实的感人细节", {"public": -5, "integrity": 1, "rel_xu_nanzhi": -8}, None),
            ),
        },
        {
            "id": "GM_BOND_01", "person": "gu_mingchuan", "name": "顾明川",
            "days": (5, 12), "locations": ("dock",), "periods": (1,), "relation": 5,
            "title": "潮气先碰到谁",
            "body": "码头突然落雨。人、书箱和仪器同时挤在一块窄雨棚下。",
            "choices": (
                ("先安置人员，再铺防潮垫", {"practical": 1, "service": 1, "rel_gu_mingchuan": 8, "material": 4}, None),
                ("先抢救最贵的仪器", {"material": 2, "resident": -2}, None),
                ("等管事的人来决定", {"rel_gu_mingchuan": -3}, None),
            ),
        },
        {
            "id": "GM_BOND_02", "person": "gu_mingchuan", "name": "顾明川",
            "days": (17, 25), "locations": ("linchang",), "periods": (1,), "relation": 35,
            "title": "一块旧桌板",
            "body": "木料不够。顾明川指着一块旧桌板，问应当先补宿舍漏风，还是先搭教室讲台。",
            "choices": (
                ("先堵漏，再把旧板改作讲台", {"stock_wood": -2, "dorm_order": 5, "course": 2, "innovation": 1, "rel_gu_mingchuan": 10}, None),
                ("木料全部用于教室", {"course": 6, "dorm_order": -5, "rel_gu_mingchuan": 2}, None),
                ("两边各做一半", {"stock_wood": -2, "backlog": 2, "rel_gu_mingchuan": -4}, None),
            ),
        },
        {
            "id": "GM_BOND_03", "person": "gu_mingchuan", "name": "顾明川",
            "days": (38, 43), "locations": ("dock", "office"), "periods": (1, 2), "relation": 65,
            "title": "离校清单",
            "body": "再次启程前，杂乱的木箱必须重新归类。漏掉一项，下一站就可能再也找不到。",
            "choices": (
                ("按用途、箱号和接收人列清单", {"stamina": -1, "practical": 1, "migration": 7, "rel_gu_mingchuan": 12}, "gm_checklist"),
                ("暂装进杂物箱", {"migration": 2}, "gm_misc_box_risk"),
                ("无法辨认的先丢弃", {"material": -5, "rel_gu_mingchuan": -10}, None),
            ),
        },
        {
            "id": "ZS_BOND_01", "person": "zhou_shunan", "name": "周树南",
            "days": (2, 10), "locations": ("minju",), "periods": (2,), "relation": 0,
            "title": "写下自己的名字",
            "body": "周树南替家里送来热水，盯着登记簿上的姓名看了很久。",
            "choices": (
                ("教他一笔一画写自己的名字", {"reputation": 1, "service": 1, "rel_zhou_shunan": 10}, None),
                ("替他把名字写好", {"rel_zhou_shunan": 3}, None),
                ("等有空再教", {"rel_zhou_shunan": -2}, None),
            ),
        },
        {
            "id": "ZS_BOND_02", "person": "zhou_shunan", "name": "周树南",
            "days": (20, 28), "locations": ("minju", "dock"), "periods": (1, 2), "relation": 30,
            "title": "报纸上的标题",
            "body": "周树南认出了报头，却还读不完整条标题。他不愿每次都只听别人转述。",
            "choices": (
                ("把标题拆开教他认读", {"stamina": -1, "resident": 3, "rel_zhou_shunan": 12}, None),
                ("把整版新闻读给他听", {"rel_zhou_shunan": 6}, None),
                ("请他帮忙沿街卖报", {"rel_zhou_shunan": -3}, "zs_work_study_help"),
            ),
        },
        {
            "id": "ZS_BOND_03", "person": "zhou_shunan", "name": "周树南",
            "days": (42, 44), "locations": ("classroom",), "periods": (2,), "relation": 65,
            "title": "一本旧练习簿",
            "body": "周树南把一本写满姓名、日期和短句的练习簿递给你。这是他第一次完整写下自己的经历。",
            "choices": (
                ("收进档案并写清来历", {"service": 1, "rel_zhou_shunan": 15}, "local_literacy_notebook"),
                ("约定下一次继续学习", {"rel_zhou_shunan": 8}, None),
                ("只作口头告别", {"rel_zhou_shunan": 2}, None),
            ),
        },
    )

    BOND_PORTRAITS = {
        "xu_nanzhi": "images/chapter01/characters/xu_soft.png",
        "gu_mingchuan": "images/chapter02/characters/gu_manifest.png",
    }

    def campaign_bond_candidate(location_id):
        pending = store.bond_pending_tasks.get("xn_postal_route")
        if pending and store.campaign_day >= pending["day"] and location_id == "office":
            return {
                "id": "XN_POSTAL_ROUTE", "person": "xu_nanzhi", "name": "许南枝",
                "title": "核对邮路", "body": "校务处保留着近期邮路中断与恢复的记录。你终于能把确定的部分带回去。",
                "choices": (("逐项抄录可确认的邮路", {"reputation": 1, "rel_xu_nanzhi": 15}, "xn_postal_route_done"),),
            }
        for event in BOND_EVENTS:
            if event["id"] in store.bond_events_seen:
                continue
            if not (event["days"][0] <= store.campaign_day <= event["days"][1]):
                continue
            if location_id not in event["locations"] or store.campaign_period not in event["periods"]:
                continue
            if int(store.relationship.get(event["person"], 0)) < event["relation"]:
                continue
            return event
        return None

    def campaign_apply_bond_choice(event, choice_index):
        choice = event["choices"][choice_index]
        campaign_apply_canonical_effects(choice[1])
        flag = choice[2]
        if flag:
            store.bond_flags.add(flag)
            if flag == "xn_postal_route_pending":
                store.bond_pending_tasks["xn_postal_route"] = {"day": store.campaign_day + 1}
            elif flag == "xn_postal_route_done":
                store.bond_pending_tasks.pop("xn_postal_route", None)
            elif flag == "local_literacy_notebook":
                store.archive_items.add("local_literacy_notebook")
            elif flag == "zs_work_study_help":
                store.club_xp["work_study"] += 8
                store.club_rank["work_study"] = campaign_club_rank_from_xp(store.club_xp["work_study"])
        store.bond_events_seen.add(event["id"])
        store.stat_stamina = max(0, store.stat_stamina - 1)
        store.action_count = min(135, store.action_count + 1)
        store.mc45_time = min(3, store.mc45_time + 1)
        store.campaign_period = store.mc45_time
        campaign_sync_legacy_view()


screen campaign_bond_event(event):
    modal True
    add campaign_location_background(current_location):
        xysize (1920, 1080)
    add Solid("#08090844")
    if event["person"] in BOND_PORTRAITS:
        add BOND_PORTRAITS[event["person"]]:
            xpos 40
            yalign 1.0
            zoom 0.62
    frame:
        xpos 600
        ypos 130
        xsize 1190
        ysize 790
        background Solid("#10130eed")
        padding (52, 40)
        vbox:
            spacing 18
            text event["name"] size 25 color "#b89b60"
            text event["title"] size 42 color "#ead296"
            text event["body"] size 25 color "#ddd5c5" xmaximum 1050 line_spacing 8
            null height 12
            for index, choice in enumerate(event["choices"]):
                textbutton choice[0]:
                    xsize 1060
                    ysize 72
                    text_size 22
                    text_color "#ead39a"
                    text_hover_color "#fff0bd"
                    background Solid("#25271fef")
                    hover_background Solid("#514023ef")
                    action Return(index)
            textbutton "暂时离开":
                text_size 19
                text_color "#aaa598"
                action Return(None)


label campaign_bond_event_label(event):
    call screen campaign_bond_event(event)
    $ bond_choice_index = _return
    if bond_choice_index is not None:
        $ campaign_apply_bond_choice(event, bond_choice_index)
        $ mc45_last_result = "你完成了羁绊事件“%s”。%s关系：%d（%s）。" % (event["title"], event["name"], relationship[event["person"]], campaign_relationship_tier(event["person"]))
        return True
    return False
