# ================================================================
# 第三章：护送《四库全书》——为斯文存一线
# 正式剧本编号：ZJU-1937-03
# 史实边界：文澜阁藏书属于省立图书馆，不写作浙大校产。
# ================================================================

define mao = Character("毛春翔", color="#c7b58b")
define chen = Character("陈训慈", color="#c9b993")
define librarian = Character("图书馆员", color="#b9c3b3")

image ch3 tarp:
    "images/chapter03/scenes/rain_tarp_warehouse.png"
    xysize (1920, 1080)
image ch3 route:
    "images/chapter03/scenes/route_records.png"
    xysize (1920, 1080)
image ch3 numbers:
    "images/chapter03/scenes/two_numbers.png"
    xysize (1920, 1080)
image ch3 blurred:
    "images/chapter03/scenes/blurred_crate.png"
    xysize (1920, 1080)
image ch3 broken:
    "images/chapter03/scenes/broken_seal.png"
    xysize (1920, 1080)
image ch3 closed:
    "images/chapter03/scenes/warehouse_closed.png"
    xysize (1920, 1080)

default ch3_scene = 1
default ch3_scene_tasks = []
default ch3_sprite = ""
default ch3_evidence = 0
default ch3_chain = 0

init python:
    CH3_SCENE_META = {
        1: (
            "雨布之下",
            "1937年11月中旬 · 富阳玉山",
            "ch3 tarp",
            "按交接程序接收省立图书馆藏书",
            [
                ("vehicle", "核对车号与收据", 155, 295, 360, 350),
                ("tarp", "检查雨布与绳索", 600, 360, 370, 300),
                ("sorting", "划分三类箱况", 1040, 260, 390, 370),
            ],
        ),
        2: (
            "水路为何在桐庐中断",
            "1937年11月中旬 · 桐庐",
            "ch3 route",
            "依据四份记录复原可通行路线",
            [
                ("waterlog", "查阅水路日志", 160, 275, 360, 360),
                ("handover", "核对征用交接", 600, 380, 370, 285),
                ("request", "整理协运申请", 1040, 265, 390, 370),
            ],
        ),
        3: (
            "两种数字",
            "1937年11月中旬 · 桐庐交接处",
            "ch3 numbers",
            "处理一百三十九与一百四十两种箱数",
            [
                ("count139", "核查一百三十九", 165, 300, 350, 350),
                ("count140", "核查一百四十", 600, 370, 370, 300),
                ("uncertainty", "记录未知边界", 1040, 270, 390, 370),
            ],
        ),
        4: (
            "模糊箱号",
            "1937年11月中旬 · 转运途中",
            "ch3 blurred",
            "用至少三项独立证据判断箱号",
            [
                ("sealstroke", "比对封印笔画", 155, 285, 360, 360),
                ("neighbors", "比对相邻箱序", 600, 370, 370, 300),
                ("diagram", "查阅装载示意", 1040, 260, 390, 380),
            ],
        ),
        5: (
            "封条裂损",
            "1937年11月下旬 · 建德途中",
            "ch3 broken",
            "在见证下完成封条裂损处置",
            [
                ("document", "先记录裂口", 165, 300, 350, 350),
                ("witness", "确认责任与见证", 600, 370, 370, 300),
                ("reseal", "更换并补录封条", 1040, 270, 390, 370),
            ],
        ),
        6: (
            "仓门合拢",
            "1937年11月下旬 · 建德徐塘",
            "ch3 closed",
            "完成来源、箱号与经手链最终复核",
            [
                ("origin", "复核藏书来源", 160, 290, 360, 360),
                ("chain", "复核经手链", 600, 370, 370, 300),
                ("closure", "记录闭仓状态", 1040, 265, 390, 375),
            ],
        ),
    }


transform ch3_portrait:
    xpos 35
    yalign 1.0
    zoom 1.35
    alpha 0.0
    linear 0.18 alpha 1.0


screen ch3_character():
    zorder 5
    if ch3_sprite:
        add ch3_sprite at ch3_portrait


label chapter_3:
    $ ch3_scene = 1
    $ ch3_scene_tasks = []
    $ ch3_evidence = 0
    $ ch3_chain = 0
    $ immersive_items = ["转运交接单", "油布与封签记录"]
    $ immersive_archive_count = 2
    scene black
    with fade
    centered "{size=58}第三章　护送《四库全书》{/size}\n\n{size=32}为斯文存一线{/size}\n\n{size=22}1937年11月　富阳、桐庐至建德{/size}"
    pause 1.4
    jump ch3_scene_hub


label ch3_scene_hub:
    $ ch3_meta = CH3_SCENE_META[ch3_scene]
    $ immersive_chapter = "第三章  护送《四库全书》"
    $ immersive_date = ch3_meta[1]
    $ immersive_objective = ch3_meta[3]
    $ immersive_tasks = [(task[1], task[0] in ch3_scene_tasks) for task in ch3_meta[4]]
    $ immersive_secondary = ["保留来源信息", "不越过权限开箱", "标明不确定性"]
    $ ch3_sprite = ""
    hide screen ch3_character
    scene expression ch3_meta[2]
    show screen immersive_hud
    call screen chapter_task_scene(ch3_meta[2], ch3_meta[0], "藏书属于省立图书馆；点击场景标记调查", ch3_meta[4], ch3_scene_tasks)
    $ ch3_selected = _return

    if ch3_selected == "continue":
        if ch3_scene < 6:
            $ ch3_scene += 1
            $ ch3_scene_tasks = []
            jump ch3_scene_hub
        jump ch3_ending

    call expression "ch3_task_" + ch3_selected
    if ch3_selected not in ch3_scene_tasks:
        $ ch3_scene_tasks.append(ch3_selected)
    jump ch3_scene_hub


label ch3_task_vehicle:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    narrator_day1 "货车抵达仓前，箱子尚未卸下。毛春翔先让所有人停在雨布外。"
    mao "先报号，后移箱。号码未明者，不得离开车旁。"
    gu "车号、收据、箱数三项一致。现在才可以开始卸车。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_tarp:
    $ ch3_sprite = "ch2 gu_rope"
    show screen ch3_character
    narrator_day1 "雨布边缘没有破口，四角绳结却有一处被水泡松。"
    gu "先补绳，再抬箱。移动途中失去遮盖，比在原地多等片刻危险。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_sorting:
    $ ch3_sprite = "ch2 gu_directing"
    show screen ch3_character
    mao "号码不明、外箱受潮、箱况完好，分成三列。不要为了队形整齐把问题混在一起。"
    sy "我原以为要先问一共有多少箱。"
    mao "先问是否安全到达，再问有多少。"
    hide screen ch3_character
    return

label ch3_task_waterlog:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    narrator_day1 "水路日志显示，藏书从杭州经富阳抵桐庐；再往前，水势与运力都难以保证。"
    xu "这不是纸面上最短的路，却是当时还能走通的路。"
    $ ch3_evidence += 1
    hide screen ch3_character
    return

label ch3_task_handover:
    $ ch3_sprite = "ch2 gu_inspecting"
    show screen ch3_character
    chen "从水运改为陆运，必须留下交接。车是谁派的、箱是谁点的、到哪里由谁接，都不能省。"
    gu "学校车辆协助省立图书馆转运，但藏书来源不因此改变。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_request:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    chen "这不是私下借车。没有正式申请、目录和来源，便谈不上保存。"
    narrator_day1 "路线被复原为：杭州至富阳、桐庐走水路，桐庐以后由浙大车辆协助转往建德。"
    $ immersive_archive_count = 3
    hide screen ch3_character
    return

label ch3_task_count139:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    librarian "一份交接单写一百三十九箱，笔迹清楚，经手章完整。"
    sy "它能证明这一份记录的数字，却不能自动推翻另一份。"
    $ ch3_evidence += 1
    hide screen ch3_character
    return

label ch3_task_count140:
    $ ch3_sprite = "ch2 gu_inspecting"
    show screen ch3_character
    mao "另一份清册写一百四十箱，也有自己的形成时间与经手环节。"
    xu "差的一箱究竟来自重复登记、空箱还是另一次交接，目前没有证据。"
    $ ch3_evidence += 1
    hide screen ch3_character
    return

label ch3_task_uncertainty:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    menu:
        "面对一百三十九与一百四十两种数字，记录应怎样写？"
        "只保留一百三十九":
            mao "证据不足以删去另一种数字。"
        "取中间数":
            mao "数字不是可以求平均的意见。"
        "两种数字并存，并注明原因未明":
            $ ch3_evidence += 2
            mao "对。不知道，便写不知道。"
            narrator_day1 "档案更新：两种箱数并存，差异原因待考。"
    hide screen ch3_character
    return

label ch3_task_sealstroke:
    $ ch3_sprite = "ch2 gu_inspecting"
    show screen ch3_character
    narrator_day1 "模糊箱号只剩半道墨痕。封印末笔向右上挑，与相邻批次的写法相同。"
    mao "这是一项证据，还不能下结论。"
    $ ch3_evidence += 1
    hide screen ch3_character
    return

label ch3_task_neighbors:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    xu "前后两箱的编号连续，旧侧标也保留了同一组批次字样。"
    gu "八九不离十。"
    xu "仍有一二。继续找第三项独立证据。"
    $ ch3_evidence += 1
    hide screen ch3_character
    return

label ch3_task_diagram:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    gu "装载示意图显示，这一舱位原本安排的正是缺号箱。"
    mao "记录结论时要把封印笔画、相邻箱序、旧侧标和装载图逐项写出。"
    $ ch3_evidence += 1
    hide screen ch3_character
    return

label ch3_task_document:
    $ ch3_sprite = "ch2 gu_inspecting"
    show screen ch3_character
    narrator_day1 "一只箱子的封条沿折痕裂开。毛春翔没有让人立刻开箱。"
    mao "先写裂口位置、长度与发现时间，再画一张简图。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_witness:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    chen "由责任人确认运输经过，另请见证人在场。未经授权，谁也不能以检查为名自行开箱。"
    xu "保护内容，也要保护程序。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_reseal:
    $ ch3_sprite = "ch2 gu_rope"
    show screen ch3_character
    narrator_day1 "众人在见证下更换油纸、木片与封条，并补写原因、结果、更换人和见证人。"
    mao "新封条不是把旧裂口抹掉，而是把处置过程接续下去。"
    $ ch3_chain += 2
    hide screen ch3_character
    return

label ch3_task_origin:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    mao "最后再读一遍：文澜阁藏书，由浙江省立图书馆保管；浙江大学在转运中提供车辆与协助。"
    sy "帮助保护，不等于改变归属。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_chain:
    $ ch3_sprite = "ch2 gu_manifest"
    show screen ch3_character
    chen "从杭州、富阳、桐庐到建德，每一次交接都有日期、地点、经手与见证。"
    narrator_day1 "箱子仍然沉默，记录却让它们的来路没有消失。"
    $ ch3_chain += 1
    hide screen ch3_character
    return

label ch3_task_closure:
    $ ch3_sprite = "ch2 gu_relief"
    show screen ch3_character
    mao "眼下先让它们平安度过这些年。等太平了，再回去。"
    chen "保存的不只是书页，也包括来源、目录和经手的秩序。"
    narrator_day1 "仓门合拢。门外的雨还在下，门内的箱号已逐一落在纸上。"
    hide screen ch3_character
    return


label ch3_ending:
    hide screen ch3_character
    hide screen immersive_hud
    scene ch3 closed
    with fade
    narrator_day1 "我们没有替未知写下一个看似完整的答案，也没有让保护之名越过权限。"
    sy "为斯文存一线，靠的不只是把书搬到安全处，还要让它们的身份和来路一同抵达。"
    $ day1_finish_chapter(3)
    centered "{size=46}第三章完成{/size}\n\n第四章　建德梅城已解锁"
    jump day1_map_hub
