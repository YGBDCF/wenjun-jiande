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
image bg ch2 = "images/chapter_02.jpg"
image bg ch3 = "images/chapter_03.jpg"
image bg ch4 = "images/chapter_04.jpg"
image bg ch5 = "images/chapter_05.jpg"
image bg ch6 = "images/chapter_06.jpg"


label start:
    scene black
    with fade

    centered "{size=58}文军长征：建德四十五日{/size}\n\n{size=32}六章扩写版 · v0.2{/size}"
    pause 1.0
    jump day1_map_hub


label day1_map_hub:
    call screen day1_chapter_map
    $ selected_chapter = _return

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
