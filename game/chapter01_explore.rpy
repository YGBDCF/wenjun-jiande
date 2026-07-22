# ================================================================
# 第一章：西天目山——寺庙里的大学
# 史实框架：1937-09-21 前后，一年级生迁往禅源寺并推行导师制；
# 1937 年 11 月下旬，因形势危急离开西天目山，前往建德会合。
# ================================================================

define ch1_mentor = Character("林导师", color="#c9b98b")
define ch1_student = Character("陈同学", color="#bdc9d6")
define ch1_radio = Character("广播", color="#9fb7bd", what_italic=True)

image ch1 courtyard:
    "images/chapter01/backgrounds/temple_courtyard_rain.png"
    xysize (1920, 1080)
image ch1 dormitory:
    "images/chapter01/backgrounds/dormitory_rain.png"
    xysize (1920, 1080)
image ch1 study:
    "images/chapter01/backgrounds/mentor_radio_room.png"
    xysize (1920, 1080)
image ch1 shenyan = "images/chapter01/characters/shenyan_painterly.png"

default ch1_dorm_done = False
default ch1_mentor_done = False
default ch1_radio_done = False
default ch1_intro_done = False
default ch1_items = []
default ch1_archives = []
default ch1_task_hint = "走进禅源寺，找到新生报到处"
default ch1_reflection = ""
default ch1_pose = "calm"

transform ch1_portrait_calm:
    xalign -0.25
    yalign 1.0
    zoom 0.90
    linear 2.6 yoffset -4
    linear 2.6 yoffset 0
    repeat

transform ch1_portrait_thoughtful:
    xalign -0.27
    yalign 1.0
    zoom 0.92
    yoffset 5

transform ch1_portrait_tense:
    xalign -0.23
    yalign 1.0
    zoom 0.93
    matrixcolor TintMatrix("#d7e3ea")

screen ch1_character():
    zorder 5
    if ch1_pose == "thoughtful":
        add "ch1 shenyan" at ch1_portrait_thoughtful
    elif ch1_pose == "tense":
        add "ch1 shenyan" at ch1_portrait_tense
    else:
        add "ch1 shenyan" at ch1_portrait_calm

screen ch1_hud():
    zorder 30

    # 顶部功能区，作为本项目后续章节的固定规范。
    hbox:
        xpos 1540
        ypos 24
        spacing 9
        textbutton "存档" action ShowMenu("save") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "读档" action ShowMenu("load") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "回顾" action ShowMenu("history") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"
        textbutton "设置" action ShowMenu("preferences") xsize 78 ysize 52 background "images/chapter01/ui/top_button.png" text_size 18 text_color "#d9c18b"

    frame:
        xpos 1540
        ypos 94
        xsize 356
        ysize 560
        background "images/chapter01/ui/task_panel.png"
        padding (30, 30)

        vbox:
            spacing 13
            text "第一章  西天目山" size 26 color "#dfc480"
            text "1937年秋  禅源寺" size 18 color "#aeb6b1"
            null height 10
            text "当前目标" size 25 color "#e8d6a7"
            text "[ch1_task_hint]" size 19 color "#ffffff" xmaximum 300
            null height 14
            text "任务进度" size 22 color "#e8d6a7"
            text ("完成  僧舍安顿" if ch1_dorm_done else "待办  僧舍安顿") size 18 color ("#b9d49e" if ch1_dorm_done else "#b9b2a2")
            text ("完成  拜访导师" if ch1_mentor_done else "待办  拜访导师") size 18 color ("#b9d49e" if ch1_mentor_done else "#b9b2a2")
            text ("完成  核实广播" if ch1_radio_done else "待办  核实广播") size 18 color ("#b9d49e" if ch1_radio_done else "#b9b2a2")
            null height 14
            text "次要目标" size 22 color "#e8d6a7"
            text "了解山外局势" size 18 color "#b9b2a2"
            text "保护课程与记录" size 18 color "#b9b2a2"

    frame:
        xpos 1540
        ypos 670
        xsize 356
        ysize 310
        background "images/chapter01/ui/inventory_panel.png"
        padding (14, 16)

        vbox:
            spacing 12
            hbox:
                spacing 3
                textbutton "返回地图" action Jump("ch1_map_hub") xsize 104 ysize 44 background "images/chapter01/ui/tab_idle.png" text_size 17 text_color "#e2c987" text_hover_color "#fff0bd"
                textbutton "档案" action NullAction() xsize 104 ysize 44 background "images/chapter01/ui/tab_idle.png" text_size 20 text_color "#c3ad7c"
                textbutton "物件" action NullAction() xsize 104 ysize 44 background "images/chapter01/ui/tab_active.png" text_size 20 text_color "#f0d799"
            text "随身物件" size 21 color "#dfc480"
            if ch1_items:
                for item in ch1_items:
                    frame:
                        xsize 324 ysize 42 background Solid("#171b19cc")
                        text "[item]" size 17 color "#d8cfbd" xalign 0.5 yalign 0.5
            else:
                text "尚未获得物件" size 18 color "#898a86"
            text "历史档案  [len(ch1_archives)] / 3" size 18 color "#c9b98b"

screen ch1_temple_map():
    modal True
    add "ch1 courtyard"
    add Solid("#07101255")

    frame:
        xpos 52
        ypos 45
        xsize 520
        ysize 138
        background Solid("#101718dc")
        padding (24, 18)
        vbox:
            text "禅源寺  临时校园" size 34 color "#ead49e"
            text "选择一处地点调查；完成后可再次返回。" size 19 color "#d9ddda"

    button:
        xpos 285 ypos 350 xsize 300 ysize 185
        background Solid("#182020b8")
        hover_background Solid("#b4873d99")
        action Return("dorm")
        vbox:
            xalign 0.5 yalign 0.5 spacing 8
            text "僧舍" size 34 color "#ffffff" xalign 0.5
            text ("已经安顿" if ch1_dorm_done else "安顿行李与书册") size 19 color "#e7d6ad" xalign 0.5

    button:
        xpos 670 ypos 260 xsize 300 ysize 185
        background Solid("#182020b8")
        hover_background Solid("#b4873d99")
        action Return("mentor")
        vbox:
            xalign 0.5 yalign 0.5 spacing 8
            text "导师住处" size 34 color "#ffffff" xalign 0.5
            text ("已经拜访" if ch1_mentor_done else "领取课程安排") size 19 color "#e7d6ad" xalign 0.5

    button:
        xpos 1060 ypos 350 xsize 300 ysize 185
        background Solid("#182020b8")
        hover_background Solid("#b4873d99")
        action Return("radio")
        vbox:
            xalign 0.5 yalign 0.5 spacing 8
            text "广播室" size 34 color "#ffffff" xalign 0.5
            text ("已经核实" if ch1_radio_done else "收听杭州消息") size 19 color "#e7d6ad" xalign 0.5

    frame:
        xpos 1530 ypos 36 xsize 350 ysize 690
        background Solid("#101718dc")
        padding (24, 22)
        vbox:
            spacing 13
            text "当前目标" size 24 color "#e4c783"
            text "[ch1_task_hint]" size 19 color "#ffffff" xmaximum 300
            null height 6
            text "进度" size 22 color "#e8dcc0"
            text ("已完成：僧舍安顿" if ch1_dorm_done else "未完成：僧舍安顿") size 19
            text ("已完成：拜访导师" if ch1_mentor_done else "未完成：拜访导师") size 19
            text ("已完成：核实广播" if ch1_radio_done else "未完成：核实广播") size 19
            null height 8
            text "随身物品" size 22 color "#e8dcc0"
            if ch1_items:
                for item in ch1_items:
                    text "[item]" size 18 color "#d7d0be"
            else:
                text "（尚无）" size 18 color "#898a86"
            null height 8
            text "档案 [len(ch1_archives)] / 3" size 20 color "#c9b98b"

label ch1_start:
    $ ch1_dorm_done = False
    $ ch1_mentor_done = False
    $ ch1_radio_done = False
    $ ch1_items = []
    $ ch1_archives = []
    $ ch1_task_hint = "走进禅源寺，找到新生报到处"

    scene black
    with fade
    centered "{size=56}第一章{/size}\n{size=38}西天目山  寺庙里的大学{/size}\n\n{size=24}1937年9月21日前后{/size}"
    pause 1.5

    scene ch1 courtyard
    with dissolve
    show screen ch1_hud
    show screen ch1_character
    narrator_day1 "雨从山雾里落下来，沿着瓦当连成细线。"
    narrator_day1 "1937年秋，浙江大学一年级新生离开杭州，来到西天目山禅源寺。"
    sy "入学通知书上写的是浙江大学。可我真正抵达的，却是一座藏在山里的寺院。"
    ch1_student "新生吗？行李先放廊下。木箱别挡着路，后面还有人上山。"
    sy "请问……报到处在哪里？"
    ch1_student "穿过前院就是。教室、宿舍、办公室都还在找地方，你别指望看见完整的校园。"
    narrator_day1 "他怀里夹着一沓被雨打湿边角的名册，鞋上沾满山泥。"
    sy "今天还上课吗？"
    ch1_student "当然。先生们说，学生到了，课就该开始。"

    $ ch1_pose = "thoughtful"
    menu:
        "第一次看见这座临时校园，我心里想的是"
        "先把这里当成真正的学校":
            $ day1_morale += 1
            $ ch1_reflection = "校园不只是一组建筑。"
            sy "只要课程开始，这里就不是借住的寺院，而是我们的校园。"
        "先弄清局势还能不能安定":
            $ day1_records += 1
            $ ch1_reflection = "先辨清形势，才能决定怎么走。"
            sy "安顿以前，我得先知道杭州和山外究竟发生了什么。"
        "先帮身边的人搬完行李":
            $ day1_trust += 1
            $ ch1_reflection = "学校是由彼此照应的人组成的。"
            sy "想得再多也无用。先把廊下这些箱子搬进去吧。"

    narrator_day1 "报到册上，我的名字旁边落下一枚小小的墨点。"
    $ ch1_archives.append("西天目山办学")
    $ ch1_task_hint = "完成僧舍、导师住处与广播室的调查"
    narrator_day1 "【历史档案已收录：西天目山办学】"
    hide screen ch1_character
    hide screen ch1_hud
    jump ch1_map_hub

label ch1_map_hub:
    if ch1_dorm_done and ch1_mentor_done and ch1_radio_done:
        jump ch1_night
    call screen ch1_temple_map
    if _return == "dorm":
        jump ch1_dorm
    elif _return == "mentor":
        jump ch1_mentor
    else:
        jump ch1_radio_event

label ch1_dorm:
    scene ch1 dormitory
    with dissolve
    show screen ch1_hud
    show screen ch1_character
    if ch1_dorm_done:
        sy "草席已经铺好，书册也移到了不会漏雨的地方。"
        hide screen ch1_character
        hide screen ch1_hud
        jump ch1_map_hub

    narrator_day1 "偏殿被临时改作僧舍。床位不够，许多人只能把草席铺在地上。"
    ch1_student "靠窗那张空着，但雨大时会漏。你若不介意，就睡那里。"
    sy "昨晚你们也这样住？"
    ch1_student "一半睡床，一半睡走廊。早课钟一响，大家就起来搬桌子。"
    narrator_day1 "一滴水从窗棂落在我的箱盖上。箱里最上面，是课本和母亲塞来的信。"

    $ ch1_pose = "thoughtful"
    menu:
        "只有一块油布，我决定"
        "先盖住大家共用的课本":
            $ day1_trust += 1
            ch1_student "你的衣箱怎么办？"
            sy "衣服湿了还能晒，书页黏住就很难分开了。"
        "先补好漏雨的窗缝":
            $ day1_morale += 1
            sy "把源头堵住，今晚所有人都能少挪几次铺位。"
            ch1_student "我去找木片。你把这条旧布递给我。"
        "先把名册与家信移到高处":
            $ day1_records += 1
            sy "这些纸记录着谁已经到校，也让家里知道我们还平安。"
            ch1_student "那就放到壁橱上层，离窗最远。"

    narrator_day1 "我们忙了许久。房间仍然简陋，却终于有了一点可以住下的样子。"
    sy "原来开学的第一件事，不是领书，而是学会在雨里保护书。"
    $ ch1_dorm_done = True
    $ ch1_items.append("油布包好的笔记本")
    $ ch1_task_hint = "继续探索寺院中的临时校园"
    narrator_day1 "【获得物品：油布包好的笔记本】"
    hide screen ch1_character
    hide screen ch1_hud
    jump ch1_map_hub

label ch1_mentor:
    scene ch1 study
    with dissolve
    show screen ch1_hud
    show screen ch1_character
    if ch1_mentor_done:
        ch1_mentor "课程表收好。地点会变，约定的时间不会变。"
        hide screen ch1_character
        hide screen ch1_hud
        jump ch1_map_hub

    narrator_day1 "导师住处只有一张木桌。桌上摊着课程安排和一幅旧地图。"
    ch1_mentor "沈砚？坐吧。从今天起，我负责指导你的学业，也过问你的生活。"
    sy "学校以前就这样安排导师吗？"
    ch1_mentor "学校决定在这里推行导师制。你们刚入学，又遇上战事，更不能任由谁在混乱里掉队。"
    sy "可是教室都还没有安顿好。"
    ch1_mentor "斋堂能讲国文，偏殿能讲数学。物理仪器没到，就先讲原理。"
    ch1_mentor "大学不是等一切齐备才开始。越是不齐备，越要知道什么不能停。"

    $ ch1_pose = "thoughtful"
    menu:
        "我最想问导师的是"
        "课程是否还能按计划完成？":
            $ day1_morale += 1
            ch1_mentor "计划会改，学习不会取消。每周来找我一次，我们一起调整。"
        "我们会在这里停留多久？":
            $ day1_records += 1
            ch1_mentor "没人知道。也许几个月，也许几周。不要拿未知替今天做决定。"
        "如果再次迁校，我应该带走什么？":
            $ day1_trust += 1
            ch1_mentor "先照顾人，再保护无法补回的记录。至于行李，要学会放下。"

    narrator_day1 "他把一张临时课程表递给我，上面的地点都是寺院房间。"
    ch1_mentor "记住：导师制不是要替你做选择，而是让你在无路可循时，仍有人可以商量。"
    sy "我把课程表折进笔记本。那一刻，这座寺院第一次有了校园的秩序。"
    $ ch1_mentor_done = True
    $ ch1_items.append("临时课程表")
    $ ch1_archives.append("导师制")
    $ ch1_task_hint = "继续探索，并留意山外的消息"
    narrator_day1 "【获得物品：临时课程表】"
    narrator_day1 "【历史档案已收录：导师制】"
    hide screen ch1_character
    hide screen ch1_hud
    jump ch1_map_hub

label ch1_radio_event:
    scene ch1 study
    with dissolve
    show screen ch1_hud
    show screen ch1_character
    if ch1_radio_done:
        sy "广播仍有杂音。写下的消息必须注明来源和是否确认。"
        hide screen ch1_character
        hide screen ch1_hud
        jump ch1_map_hub

    narrator_day1 "入夜以后，导师的桌旁围了几个人。收音机里只剩断续的电流声。"
    ch1_radio "……杭州湾方向……局势紧张……各单位注意疏散准备……"
    ch1_student "我家在杭州。刚才是不是提到了城站？"
    sy "我只听清了‘杭州湾’和‘疏散’，其他不能确定。"
    ch1_student "可外面已经有人说学校明早就要撤。"
    ch1_mentor "传言跑得总比命令快。沈砚，把你听见的分开记。"

    $ ch1_pose = "tense"
    menu:
        "我怎样整理这段消息？"
        "只记录确定听清的词句":
            $ day1_records += 2
            sy "确认：杭州湾方向局势紧张；学校需注意疏散准备。其余内容标为未确认。"
            ch1_mentor "很好。信息不完整时，诚实地留下空白。"
        "结合传言补成一条完整通知":
            $ day1_records -= 1
            sy "也许可以写成‘学校明早撤离’……"
            ch1_mentor "不行。听不清的部分不能靠恐惧补齐。把它划掉。"
        "先安慰同学，不再继续记录":
            $ day1_trust += 1
            sy "陈同学，广播没有说杭州已经失守。我们先等正式通知。"
            ch1_mentor "照顾人是对的，但之后仍要把确切内容补记下来。"

    narrator_day1 "我在纸上画出两栏：确认、未确认。窗外的雨声盖过了后半段广播。"
    ch1_student "原来记录一句话，也需要做选择。"
    sy "乱世里，消息会影响每个人下一步往哪里走。写错比漏写更危险。"
    $ ch1_radio_done = True
    $ ch1_items.append("广播记录纸")
    $ ch1_archives.append("战时广播记录")
    $ ch1_task_hint = "三项事务已完成，等待夜间通知"
    narrator_day1 "【获得物品：广播记录纸】"
    narrator_day1 "【历史档案已收录：战时广播记录】"
    hide screen ch1_character
    hide screen ch1_hud
    jump ch1_map_hub

label ch1_night:
    scene ch1 courtyard
    with fade
    show screen ch1_hud
    show screen ch1_character
    $ ch1_task_hint = "收拾书册，准备前往建德会合"
    narrator_day1 "日子在钟声、雨声和读书声里向前。寺院逐渐有了课表、点名册和固定的讨论时间。"
    narrator_day1 "到了十一月下旬，山外的形势急剧恶化。那天深夜，一份正式通知终于送上山。"
    ch1_mentor "校本部来电。一年级学生尽快离开西天目山，前往建德与学校会合。"
    ch1_student "又要走？我们的床铺才刚修好。"
    sy "课程表上的教室，也才刚刚记熟。"
    ch1_mentor "这就是迁校。不是等一个地方住不下去才走，而是在还能完整带走师生时就走。"
    narrator_day1 "廊下重新响起捆扎行李的声音。几周前打开的木箱，又被一只只钉上。"

    $ ch1_pose = "tense"
    menu:
        "离开前，我最后做了一件事"
        "核对同学名单，确认无人掉队":
            $ day1_trust += 1
            sy "名字要一个个念到。人比箱子更不能遗漏。"
        "抄下课程安排，路上继续温习":
            $ day1_morale += 1
            sy "教室会再变，但下一次上课不必从头开始。"
        "把广播记录交给导师保存":
            $ day1_records += 1
            sy "这张纸记录了我们为什么离开。以后应当有人能说清楚。"

    ch1_student "沈砚，你觉得我们还算是在上大学吗？"
    sy "我望着被油布裹住的课本、课程表和那张广播记录。"
    sy "如果大学是一群人共同守住的事情，那么它此刻就在这些行李里，也在我们每个人身上。"
    narrator_day1 "清晨，寺门在身后合上。山雾很快遮住了来路。"
    narrator_day1 "1937年11月下旬，浙大一年级学生离开西天目山，转赴建德。"
    hide screen ch1_character
    hide screen ch1_hud

    $ day1_finish_chapter(1)
    scene black
    with fade
    centered "{size=50}第一章完成{/size}\n\n{size=30}江干码头已解锁{/size}\n\n{size=22}档案 3 / 3  物品 3 / 3{/size}"
    pause 2.0
    jump day1_map_hub
