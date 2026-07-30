# ================================================================
# V1.2 双地图联动（Phase A0-2）
# 普通地图往返不得推进时段、改变天气或重抽事件。
# ================================================================

init python:
    def can_switch_meta_map():
        return (
            store.campaign_period != 3
            and not store.in_forced_story
            and not store.in_chapter_episode
        )

    def campaign_prepare_map_switch(target):
        if not can_switch_meta_map():
            return False
        store.map_return_context = campaign_snapshot()
        store.active_meta_map = target
        return True

    def campaign_assert_map_switch_unchanged():
        if store.map_return_context is None:
            return True
        if campaign_snapshot() != store.map_return_context:
            raise Exception("V1.2地图往返错误：日期、时段、天气、体力、缓存事件或行动数发生变化。")
        return True


label jiande_campaign_bootstrap:
    $ campaign_begin()
    $ active_meta_map = "jiande_exploration_map"
    jump jiande_map_hub


label chapter_world_map_hub:
    $ campaign_migrate_legacy_state()
    if campaign_started:
        $ campaign_assert_map_switch_unchanged()
        $ map_return_context = None
    $ active_meta_map = "chapter_world_map"
    jump day1_map_hub


label jiande_map_hub:
    $ campaign_begin()
    $ campaign_assert_map_switch_unchanged()
    $ map_return_context = None
    $ active_meta_map = "jiande_exploration_map"
    $ campaign_sync_legacy_view()
    jump meicheng_town_hub


label campaign_go_to_chapter_map:
    if not can_switch_meta_map():
        return
    $ campaign_prepare_map_switch("chapter_world_map")
    jump chapter_world_map_hub


label campaign_go_to_jiande_map:
    if not can_switch_meta_map():
        return
    $ campaign_prepare_map_switch("jiande_exploration_map")
    jump jiande_map_hub
