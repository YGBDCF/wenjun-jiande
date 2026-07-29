# ================================================================
# 第二章：江干码头——把一所大学装上船
# 正式剧本编号：ZJU-1937-02
# ================================================================

define gu = Character("顾明川", color="#c9b27d")
define xu = Character("许南枝", color="#c7d1c0")
define history_teacher = Character("历史系教师", color="#cabd9a")
define boatman = Character("船工", color="#bca785")

image ch2 water_list:
    "images/chapter02/scenes/water_damaged_list.png"
    xysize (1920, 1080)
image ch2 loading:
    "images/chapter02/scenes/jianggan_loading.png"
    xysize (1920, 1080)
image ch2 cabin:
    "images/chapter02/scenes/boat_six_cabin.png"
    xysize (1920, 1080)
image ch2 manifest:
    "images/chapter02/scenes/lost_manifest.png"
    xysize (1920, 1080)
image ch2 tonglu:
    "images/chapter02/scenes/tonglu_transfer.png"
    xysize (1920, 1080)
image ch2 arrival:
    "images/chapter02/scenes/jiande_arrival.png"
    xysize (1920, 1080)

image ch2 gu_manifest = "images/chapter02/characters/gu_manifest.png"
image ch2 gu_rope = "images/chapter02/characters/gu_rope.png"
image ch2 gu_crate = "images/chapter02/characters/gu_crate.png"
image ch2 gu_directing = "images/chapter02/characters/gu_directing.png"
image ch2 gu_inspecting = "images/chapter02/characters/gu_inspecting.png"
image ch2 gu_relief = "images/chapter02/characters/gu_relief.png"

default ch2_scene = 1
default ch2_scene_tasks = []
default ch2_sprite = ""
default ch2_safety = 0
default ch2_integrity = 0
default ch2_accuracy = 0

init python:
    CH2_SCENE_META = {
        1: (
            "建德的水痕",
            "1937年11月中旬 · 建德",
            "ch2 water_list",
            "从残损清单复原大学的可搬运形态",
            [
                ("classify", "辨认六类装运物", 165, 250, 330, 330),
                ("watermark", "检查水损页角", 575, 335, 350, 300),
                ("provenance", "确认清单来源", 1030, 235, 360, 360),
            ],
        ),
        2: (
            "第三装运区",
            "1937年11月11日 · 江干码头 · 夜",
            "ch2 loading",
            "完成六号船的装载前检查",
            [
                ("risk", "判断三类风险", 170, 310, 350, 340),
                ("padding", "选择垫料与油布", 610, 380, 350, 280),
                ("knot", "完成双套结拉力测试", 1050, 280, 380, 360),
            ],
        ),
        3: (
            "再想一层",
            "1937年11月12日 · 凌晨三时 · 六号船",
            "ch2 cabin",
            "在不放弃人员和仪器的前提下重排船舱",
            [
                ("space", "寻找可释放空间", 150, 310, 360, 330),
                ("instrument", "调整仪器姿态", 590, 360, 380, 300),
                ("roles", "分配拆装与照料", 1050, 275, 370, 370),
            ],
        ),
        4: (
            "落入江中的纸",
            "1937年11月12日 · 黎明前 · 三号船",
            "ch2 manifest",
            "依据可验证证据补录落水清单",
            [
                ("master", "查阅总表", 170, 270, 350, 360),
                ("physical", "核对实物箱号", 600, 390, 360, 270),
                ("note", "写明补录依据", 1040, 260, 380, 370),
            ],
        ),
        5: (
            "桐庐换船",
            "1937年11月中旬 · 桐庐",
            "ch2 tonglu",
            "将原有船次重新分配到小船",
            [
                ("families", "安排家属通道", 155, 300, 360, 350),
                ("books", "保护图书与仪器", 600, 350, 380, 310),
                ("roster", "配置名册副本", 1050, 270, 370, 370),
            ],
        ),
        6: (
            "学校得以继续的凭借",
            "1937年11月15日前后 · 建德",
            "ch2 arrival",
            "反向清点人、箱、舱位与临时库区",
            [
                ("rollcall", "完成到埠点名", 160, 315, 350, 340),
                ("zones", "划分四类库区", 600, 375, 370, 285),
                ("wetcrates", "隔离受潮木箱", 1040, 280, 390, 370),
            ],
        ),
    }


transform ch2_portrait:
    xpos 35
    yalign 1.0
    zoom 1.35
    alpha 0.0
    linear 0.18 alpha 1.0


screen ch2_character():
    zorder 5
    if ch2_sprite:
        add ch2_sprite at ch2_portrait


label chapter_2:
    $ ch2_scene = 1
    $ ch2_scene_tasks = []
    $ ch2_safety = 0
    $ ch2_integrity = 0
    $ ch2_accuracy = 0
    $ immersive_items = ["顾明川的水损清单"]
    $ immersive_archive_count = 1
    scene black
    with fade
    centered "{size=58}第二章　江干码头{/size}\n\n{size=32}把一所大学装上船{/size}\n\n{size=22}1937年11月　杭州至建德{/size}"
    pause 1.4
    jump ch2_scene_hub


label ch2_scene_hub:
    $ ch2_meta = CH2_SCENE_META[ch2_scene]
    $ immersive_chapter = "第二章  江干码头"
    $ immersive_date = ch2_meta[1]
    $ immersive_objective = ch2_meta[3]
    $ immersive_tasks = [(task[1], task[0] in ch2_scene_tasks) for task in ch2_meta[4]]
    $ immersive_secondary = ["人员安全", "校产完整", "记录准确"]
    $ ch2_sprite = ""
    hide screen ch2_character
    scene expression ch2_meta[2]
    show screen immersive_hud
    call screen chapter_task_scene(ch2_meta[2], ch2_meta[0], "退出对话后人物隐藏；点击场景标记继续调查", ch2_meta[4], ch2_scene_tasks)
    $ ch2_selected = _return

    if ch2_selected == "continue":
        if ch2_scene < 6:
            $ ch2_scene += 1
            $ ch2_scene_tasks = []
            jump ch2_scene_hub
        jump ch2_ending

    call expression "ch2_task_" + ch2_selected
    if ch2_selected not in ch2_scene_tasks:
        $ ch2_scene_tasks.append(ch2_selected)
    jump ch2_scene_hub


label ch2_task_classify:
    $ ch2_sprite = "ch2 gu_manifest"
    show screen ch2_character
    narrator_day1 "建德的石阶边，顾明川摊开一册被江水浸坏的清单。右下角已经缺去一块。"
    sy "这些都是从杭州带出来的？"
    gu "带出来的，只是来得及带出的。先别急着数箱子，看看它们原本属于什么。"
    narrator_day1 "物理仪器、化学器皿、图书档案、教务文件、教职员行李、学生铺盖，被分成六类记录。"
    $ ch2_accuracy += 1
    hide screen ch2_character
    return

label ch2_task_watermark:
    $ ch2_sprite = "ch2 gu_inspecting"
    show screen ch2_character
    xu "这一页少了右角。"
    gu "另一半掉进江里了。纸页受损不等于箱子遗失，但缺口必须留在记录里。"
    sy "所以不能把看不见的部分凭空补齐。"
    $ ch2_accuracy += 1
    hide screen ch2_character
    return

label ch2_task_provenance:
    $ ch2_sprite = "ch2 gu_manifest"
    show screen ch2_character
    gu "看船号、舱位、经手人和复核笔迹。清单若离开这些来源，只剩下一串无法核验的字。"
    narrator_day1 "档案更新：大学的可搬运形态。"
    $ immersive_archive_count = 2
    $ immersive_items = ["水损清单", "六类装运目录"]
    hide screen ch2_character
    return

label ch2_task_risk:
    $ ch2_sprite = "ch2 gu_directing"
    show screen ch2_character
    boatman "书放下层，仪器不能贴舱壁。单套结遇水会滑，要打双套。"
    gu "水浸、撞击、倾斜，三类风险分别标出。每装完一层再核一次。"
    $ ch2_integrity += 1
    hide screen ch2_character
    return

label ch2_task_padding:
    $ ch2_sprite = "ch2 gu_inspecting"
    show screen ch2_character
    menu:
        "精密仪器与书箱之间应该怎样处理？"
        "木条固定、棉垫缓冲、油布防水":
            $ ch2_integrity += 2
            gu "对。材料各有用途，不能只多裹几层便算妥当。"
        "只用油布全部裹紧":
            gu "油布防水，却不能吸收撞击。重新配垫料。"
        "把铺盖随意塞入空隙":
            gu "铺盖可以缓冲，但必须记录位置，不能妨碍取用。"
    hide screen ch2_character
    return

label ch2_task_knot:
    $ ch2_sprite = "ch2 gu_rope"
    show screen ch2_character
    gu "箱号、船号、舱位三处都要对上。双套结打完，向两边做一次拉力测试。"
    narrator_day1 "湿绳在掌心勒出红痕，绳结却没有继续滑动。"
    $ ch2_integrity += 1
    hide screen ch2_character
    return

label ch2_task_space:
    $ ch2_sprite = "ch2 gu_inspecting"
    show screen ch2_character
    narrator_day1 "陈家母子已经到了舱口，精密仪器箱却占着最后一段平稳舱位。"
    menu:
        "不能丢下人，也不能抛下仪器。先从哪里腾出空间？"
        "拆除两只空置木架":
            $ ch2_safety += 1
            gu "再想一层——总还有办法。空架拆掉，木条留下做支撑。"
        "让母子等待下一班船":
            gu "下一班没有保证。先检查舱内有没有无效空间。"
        "把仪器移到无遮蔽的船头":
            gu "那会把空间问题变成损坏问题。重新想。"
    hide screen ch2_character
    return

label ch2_task_instrument:
    $ ch2_sprite = "ch2 gu_crate"
    show screen ch2_character
    gu "把仪器由竖放改成平放，重心降低；棉垫重新托住四角，铺盖卷可作靠背。"
    narrator_day1 "仪器仍被完整固定，舱边也腾出了能让母子坐下的位置。"
    $ ch2_integrity += 1
    hide screen ch2_character
    return

label ch2_task_roles:
    $ ch2_sprite = "ch2 gu_directing"
    show screen ch2_character
    gu "三个人拆架，两个人托住仪器，一人照看孩子。我来重新垫箱。"
    narrator_day1 "没有英雄式的取舍，只有一群人在有限空间里不断重排工作。"
    $ ch2_safety += 1
    hide screen ch2_character
    return

label ch2_task_master:
    $ ch2_sprite = "ch2 gu_manifest"
    show screen ch2_character
    gu "第四页副本落水。先找总表，再找同船其他页，最后才问经手人。"
    sy "记忆只能作为口述证据，不能单独填进空白。"
    $ ch2_accuracy += 1
    hide screen ch2_character
    return

label ch2_task_physical:
    $ ch2_sprite = "ch2 gu_inspecting"
    show screen ch2_character
    narrator_day1 "我们逐只核对实物箱号、旧标签和船舱位置。两名经手人的回忆被分开记录。"
    gu "箱子没有丢，丢的是记录。记录也要找回来。"
    $ ch2_accuracy += 1
    hide screen ch2_character
    return

label ch2_task_note:
    $ ch2_sprite = "ch2 gu_manifest"
    show screen ch2_character
    sy "补录说明写作：第四页副本落水，以下条目据总表、实物与两人口述复核补录。"
    gu "把不知道的边界也写清楚，后来的人才不会把推测当成事实。"
    $ ch2_accuracy += 2
    hide screen ch2_character
    return

label ch2_task_families:
    $ ch2_sprite = "ch2 gu_directing"
    show screen ch2_character
    narrator_day1 "桐庐水路变窄，原有船次必须改分到小船。"
    gu "先留出家属通道。重箱不能挡住老人和孩子上下船。"
    $ ch2_safety += 1
    hide screen ch2_character
    return

label ch2_task_books:
    $ ch2_sprite = "ch2 gu_crate"
    show screen ch2_character
    gu "图书箱离开湿舱底，仪器保持原有方向。省立图书馆的书箱另记来源，不得混入校产。"
    narrator_day1 "远处还有一批文澜阁藏书等待转运。那将成为下一段任务。"
    $ ch2_integrity += 1
    hide screen ch2_character
    return

label ch2_task_roster:
    $ ch2_sprite = "ch2 gu_manifest"
    show screen ch2_character
    gu "领船携带完整名册副本，各船只带本船名单。若再换船，先改名册再动人。"
    $ ch2_accuracy += 1
    hide screen ch2_character
    return

label ch2_task_rollcall:
    $ ch2_sprite = "ch2 gu_manifest"
    show screen ch2_character
    narrator_day1 "到达建德后，点名从最后一条小船开始反向进行。"
    gu "先点人，再按舱位找箱。不能因为木箱先到，就把未到的人忘在清单外。"
    $ ch2_safety += 1
    hide screen ch2_character
    return

label ch2_task_zones:
    $ ch2_sprite = "ch2 gu_directing"
    show screen ch2_character
    gu "物理、化学、图书、文件分成四区。七只补录箱暂放中间，复核后再归位。"
    narrator_day1 "码头边第一次出现了临时库区的秩序。"
    $ ch2_integrity += 1
    hide screen ch2_character
    return

label ch2_task_wetcrates:
    $ ch2_sprite = "ch2 gu_relief"
    show screen ch2_character
    gu "受潮箱单独隔离，先通风，不急着开封。"
    history_teacher "带出来的，是学校得以继续的凭借。仪器可以重开实验，图书可以重开课堂，档案可以重排课表。"
    xu "那几只书箱的编号不像学校的。"
    gu "还有三车在桐庐。"
    xu "怕不全是学校的书。"
    hide screen ch2_character
    return


label ch2_ending:
    hide screen ch2_character
    hide screen immersive_hud
    scene ch2 arrival
    with fade
    narrator_day1 "一所大学没有被完整装进某一艘船。它被拆成名字、箱号、舱位和彼此照应的人，又将在建德重新建立。"
    sy "我们带出来的不是校园本身，而是让学校能够继续的凭借。"
    $ day1_finish_chapter(2)
    centered "{size=46}第二章完成{/size}\n\n第三章　护送《四库全书》已解锁"
    jump day1_map_hub
