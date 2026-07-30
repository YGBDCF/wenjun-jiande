define sy = Character("沈砚", color="#d8bc7d")
define yq = Character("叶青禾", color="#c98d67")
define zc = Character("竺校长", color="#d5c79f")
define zs = Character("章先生", color="#d7cfb9")
define ls = Character("林先生", color="#a9c5bd")
define ct = Character("陈同学", color="#c7b5d9")
define az = Character("阿卓", color="#b9b183")
define oldzhou = Character("老周", color="#bca785")
define radio = Character("广播声", color="#9cb9c1", what_italic=True)
define narrator_day1 = Character("旁白", color="#d7d0be")

image bg ch1 = "images/chapter_01.jpg"
image bg ch2:
    "images/chapter02/jianggan_wharf.png"
    xysize (1920, 1080)
image bg ch3:
    "images/chapter03/siku_cargo_hold.png"
    xysize (1920, 1080)
image bg ch4:
    "images/chapter04/meicheng_campus.png"
    xysize (1920, 1080)
image bg ch5:
    "images/chapter05/air_raid_classroom.png"
    xysize (1920, 1080)
image bg ch6:
    "images/chapter06/newspaper_room.png"
    xysize (1920, 1080)

# 沈砚的六套动态立绘。人物只在对话中出现，地图探索时自动隐藏。
image shenyan calm = "images/chapter01/characters/shenyan_calm.png"
image shenyan thoughtful = "images/chapter01/characters/shenyan_thoughtful.png"
image shenyan tense = "images/chapter01/characters/shenyan_tense.png"
image shenyan determined = "images/chapter01/characters/shenyan_determined.png"
image shenyan worried = "images/chapter01/characters/shenyan_worried.png"
image shenyan relieved = "images/chapter01/characters/shenyan_relieved.png"

image ch2 crates:
    "images/chapter02/crate_inspection.png"
    xysize (1920, 1080)
image ch2 boat:
    "images/chapter02/boat_cabin.png"
    xysize (1920, 1080)
image ch3 seals:
    "images/chapter03/seal_desk.png"
    xysize (1920, 1080)
image ch3 gangplank:
    "images/chapter03/gangplank_transfer.png"
    xysize (1920, 1080)
image ch4 kongmiao:
    "images/chapter04/kongmiao_classroom.png"
    xysize (1920, 1080)
image ch4 linchang:
    "images/chapter04/linchang_office.png"
    xysize (1920, 1080)
image ch4 minju:
    "images/chapter04/minju_lodging.png"
    xysize (1920, 1080)
image ch4 pawnshop:
    "images/chapter04/pawnshop_dormitory.png"
    xysize (1920, 1080)
image ch4 dock:
    "images/chapter04/meicheng_dock.png"
    xysize (1920, 1080)
image ch4 office:
    "images/chapter04/school_affairs_office.png"
    xysize (1920, 1080)
image ch5 alley:
    "images/chapter05/evacuation_alley.png"
    xysize (1920, 1080)
# 暂未另画的避难课堂与印刷场景使用章节正式背景的裁切构图，后续可无缝替换。
image ch5 shelter:
    "images/chapter05/shelter_classroom.png"
    xysize (1920, 1080)
image ch6 radio:
    "images/chapter06/radio_room.png"
    xysize (1920, 1080)
image ch6 press:
    "images/chapter06/print_room.png"
    xysize (1920, 1080)


label start:
    $ opening_card = renpy.random.choice(OPENING_HISTORY_CARDS)
    call screen opening_history_card(opening_card[0], opening_card[1], opening_card[2])
    jump day1_map_hub


label day1_map_hub:
    hide screen ch1_character
    hide screen ch1_hud
    hide screen immersive_character
    hide screen immersive_hud
    $ immersive_active = False
    call screen day1_chapter_map
    $ selected_chapter = _return

    if selected_chapter == "meicheng_town":
        jump meicheng_town_hub

    if isinstance(selected_chapter, str) and selected_chapter.startswith("meicheng:"):
        $ selected_place = selected_chapter.split(":", 1)[1]
        $ ch4_return_to_world_map = True
        if selected_place == "kongmiao":
            jump chapter_4_kongmiao
        elif selected_place == "minju":
            jump chapter_4_minju
        elif selected_place == "linchang":
            jump chapter_4_linchang
        elif selected_place == "pawnshop":
            jump chapter_4_pawnshop
        elif selected_place == "office":
            jump chapter_4_office
        elif selected_place == "dock":
            jump chapter_4_dock

    if selected_chapter == 1:
        jump chapter_1
    elif selected_chapter == 2:
        jump chapter_2
    elif selected_chapter == 3:
        jump chapter_3
    elif selected_chapter == 4:
        jump chapter_4
    elif selected_chapter == 5:
        jump chapter_5
    elif selected_chapter == 6:
        jump chapter_6

    jump day1_map_hub
