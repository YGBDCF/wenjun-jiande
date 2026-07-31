# ================================================================
# 建德天气视觉与环境声
# 同一张地图按天气切换真实绘制差分，并叠加克制的动态雨丝。
# ================================================================

init -20 python:
    renpy.music.register_channel(
        "weather",
        mixer="sfx",
        loop=True,
        stop_on_mute=True,
        tight=True,
    )

    MC45_WEATHER_MAP_VARIANTS = {
        "rain": {
            "pre": "images/meicheng_town/weather/pre_rain.png",
            "post": "images/meicheng_town/weather/post_rain.png",
        },
        "heavy_rain": {
            "pre": "images/meicheng_town/weather/pre_heavy_rain.png",
            "post": "images/meicheng_town/weather/post_heavy_rain.png",
        },
        "fog": {
            "pre": "images/meicheng_town/weather/pre_fog.png",
            "post": "images/meicheng_town/weather/post_fog.png",
        },
        "cold": {
            "pre": "images/meicheng_town/weather/pre_cold.png",
            "post": "images/meicheng_town/weather/post_cold.png",
        },
    }

    MC45_WEATHER_AUDIO = {
        "rain": "audio/weather/rain_light.wav",
        "heavy_rain": "audio/weather/rain_heavy.wav",
        "fog": "audio/weather/fog_river.wav",
        "cold": "audio/weather/cold_wind.wav",
    }

    def mc45_weather_kind(weather):
        if weather == "小雨":
            return "rain"
        if weather in ("连阴雨", "大雨", "暴雨", "冻雨", "雨夹雪"):
            return "heavy_rain"
        if weather == "江雾":
            return "fog"
        if weather in ("北风", "寒潮", "霜冻"):
            return "cold"
        return "clear"

    def mc45_weather_map_image(weather, post_classroom=False):
        phase = "post" if post_classroom else "pre"
        kind = mc45_weather_kind(weather)
        if kind in MC45_WEATHER_MAP_VARIANTS:
            return MC45_WEATHER_MAP_VARIANTS[kind][phase]
        if post_classroom:
            return "images/meicheng_town/meicheng_town_post_ch5_v4.png"
        return "images/meicheng_town/meicheng_town_base_v1.png"

    def mc45_weather_location_access(place_id, weather):
        """Return (available, explanation) for weather-driven outdoor locks."""
        kind = mc45_weather_kind(weather)
        if kind == "heavy_rain" and place_id == "dock":
            return (
                False,
                "江面风雨太密，码头暂停装卸。可改去孔庙、校务办公处、当铺或学生宿舍。",
            )
        if kind == "heavy_rain" and place_id == "linchang":
            return (
                False,
                "林间道路积水并有落枝危险，教师区暂缓通行。可改做室内校务或课堂整理。",
            )
        return True, ""

    def mc45_weather_notice(weather):
        kind = mc45_weather_kind(weather)
        if kind == "rain":
            return "小雨压低了街巷的声响，青石路湿滑，江面不断泛起细小雨圈。"
        if kind == "heavy_rain":
            return "连阴雨使码头和林间道路暂时封闭；室内地点仍可行动。"
        if kind == "fog":
            return "江雾遮住远船，地点仍可通行；涉及船期的消息需要额外复核。"
        if kind == "cold":
            return "寒气贴着江面上来。厚衣与宿舍保暖会影响今夜的健康恢复。"
        return "江面与道路清晰，城中行动照常进行。"

    def mc45_sync_weather_ambience(weather):
        kind = mc45_weather_kind(weather)
        path = MC45_WEATHER_AUDIO.get(kind)
        volume_by_kind = {
            "rain": 0.18,
            "heavy_rain": 0.46,
            "fog": 0.10,
            "cold": 0.16,
        }
        current = renpy.music.get_playing(channel="weather")
        if path:
            renpy.music.set_volume(
                volume_by_kind.get(kind, 0.18),
                delay=1.2,
                channel="weather",
            )
            if current != path:
                renpy.music.play(path, channel="weather", loop=True, fadein=2.0)
        elif current:
            renpy.music.stop(channel="weather", fadeout=2.0)


transform mc45_rain_streak(x_value=0, delay_value=0.0, travel_time=1.0):
    xpos x_value
    ypos -130
    alpha 0.0
    pause delay_value
    alpha 0.42
    linear travel_time xpos (x_value - 145) ypos 1160
    repeat


transform mc45_fog_drift(start_x=-850, end_x=1550, travel_time=42.0, peak_alpha=0.42):
    xpos start_x
    alpha 0.0
    easein 4.0 alpha peak_alpha
    linear travel_time xpos end_x
    easeout 4.0 alpha 0.0
    repeat


screen mc45_weather_overlay(weather):
    zorder 2
    $ weather_kind = mc45_weather_kind(weather)

    if weather_kind in ("rain", "heavy_rain"):
        $ rain_count = 18 if weather_kind == "rain" else 34
        $ rain_alpha = "#dce8ec6a" if weather_kind == "rain" else "#e5edf19a"
        for rain_index in range(rain_count):
            $ rain_x = (rain_index * 113 + 47) % 2070
            $ rain_delay = (rain_index % 9) * 0.11
            $ rain_speed = 1.15 if weather_kind == "rain" else 0.72
            add Solid(rain_alpha, xysize=(2, 88 if weather_kind == "rain" else 116)) at mc45_rain_streak(rain_x, rain_delay, rain_speed)

    elif weather_kind == "fog":
        # Transparent, soft-edged mist wisps. The painted fog map supplies
        # the atmospheric base; these layers add only restrained motion.
        add "assets/weather/fog_wisp_wide.svg" at mc45_fog_drift(-1000, 1500, 46.0, 0.32):
            ypos 145
            zoom 1.10
        add "assets/weather/fog_wisp_wide.svg" at mc45_fog_drift(-1450, 1320, 58.0, 0.22):
            ypos 500
            zoom 1.35
            xzoom -1.0

    elif weather_kind == "cold":
        add Solid("#d7e0e712")
