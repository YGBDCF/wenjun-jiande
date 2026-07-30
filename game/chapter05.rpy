# ================================================================
# 第五章：“黑板挂在我的胸前”
# 正式剧本编号：ZJU-1937-05
# ================================================================

define zhang = Character("章用", color="#cdbd92")
define asking_student = Character("提问学生", color="#bcc8d1")
define committee_worker = Character("情报委员会工作人员", color="#b9c2aa")

image ch5 alarm:
    "images/chapter05/scenes/class_alarm.png"
    xysize (1920, 1080)
image ch5 rollcall:
    "images/chapter05/scenes/shelter_rollcall.png"
    xysize (1920, 1080)
image ch5 returned_class:
    "images/chapter05/scenes/return_class.png"
    xysize (1920, 1080)
image ch5 pack:
    "images/chapter05/scenes/emergency_pack.png"
    xysize (1920, 1080)
image ch5 lessons:
    "images/chapter05/scenes/mobile_lessons.png"
    xysize (1920, 1080)
image ch5 verify:
    "images/chapter05/scenes/verification_night_v2.png"
    xysize (1920, 1080)

default ch5_scene = 1
default ch5_scene_tasks = []
default ch5_has_roll = False
default ch5_teaching_items = 0
default ch5_survival_items = 0

init python:
    CH5_SCENE_META = {
        1: (
            "第一堂课与警报",
            "1937年11月下旬 · 午后",
            "ch5 alarm",
            "按预定路线完成有序疏散",
            [
                ("lamp", "熄灭煤油灯", 155, 300, 360, 350),
                ("window", "关窗并拉粗布帘", 600, 370, 370, 300),
                ("exit", "带名册检查后排", 1040, 270, 390, 370),
            ],
        ),
        2: (
            "防空壕与返回课堂",
            "1937年11月下旬 · 警报期间",
            "ch5 rollcall",
            "点清人员，等待解除警报",
            [
                ("names", "核对全体名单", 155, 300, 360, 350),
                ("missing", "复核缺席原因", 600, 370, 370, 300),
                ("allclear", "确认解除警报", 1040, 270, 390, 370),
            ],
        ),
        3: (
            "方才讲到这里",
            "1937年11月下旬 · 警报解除后",
            "ch5 returned_class",
            "恢复课堂并接续中断的题目",
            [
                ("desks", "扶正课桌", 155, 300, 360, 350),
                ("chalk", "找回粉笔与讲义", 600, 370, 370, 300),
                ("blackboard", "安置小黑板", 1040, 270, 390, 370),
            ],
        ),
        4: (
            "应急背包",
            "1937年11月下旬 · 当日下午",
            "ch5 pack",
            "兼顾人员安全与课堂续接",
            [
                ("teaching", "选择教学物品", 155, 300, 360, 350),
                ("survival", "选择生存物品", 600, 370, 370, 300),
                ("capacity", "检查背包容量", 1040, 270, 390, 370),
            ],
        ),
        5: (
            "四个短课题",
            "1937年12月 · 第二次警报后",
            "ch5 lessons",
            "在安全位置完成移动课堂任务",
            [
                ("weight", "计算载重余量", 155, 300, 360, 350),
                ("route", "排列西行路线", 600, 370, 370, 300),
                ("evidence", "核对缺课记录", 1040, 270, 390, 370),
            ],
        ),
        6: (
            "未经核实，不宜遽书",
            "1937年12月 · 深夜",
            "ch5 verify",
            "把课堂求证方法带到公共消息中",
            [
                ("montage", "整理课堂凭借", 155, 300, 360, 350),
                ("uncertain", "标明待核事项", 600, 370, 370, 300),
                ("invitation", "接受核验训练", 1040, 270, 390, 370),
            ],
        ),
    }


label chapter_5:
    $ ch5_scene = 1
    $ ch5_scene_tasks = []
    $ ch5_has_roll = False
    $ ch5_teaching_items = 0
    $ ch5_survival_items = 0
    $ immersive_items = ["课程笔记", "粉笔"]
    $ immersive_archive_count = 4
    call screen chapter_title_card(
        "images/chapter05/scenes/class_alarm.png",
        "第五章",
        "黑板挂在我的胸前",
        "警报中的课堂",
        "1937年11月下旬至12月  建德"
    )
    jump ch5_scene_hub


label ch5_scene_hub:
    $ ch5_meta = CH5_SCENE_META[ch5_scene]
    $ immersive_chapter = "第五章  警报中的课堂"
    $ immersive_date = ch5_meta[1]
    $ immersive_objective = ch5_meta[3]
    $ immersive_tasks = [(task[1], task[0] in ch5_scene_tasks) for task in ch5_meta[4]]
    $ immersive_secondary = ["人员安全优先", "警报解除后接续课堂"]
    scene expression ch5_meta[2]
    hide screen immersive_character
    show screen immersive_hud
    call screen chapter_task_scene(
        ch5_meta[2],
        ch5_meta[0],
        "坚持教学不是忽视危险，而是完成安全行动链",
        ch5_meta[4],
        ch5_scene_tasks,
    )
    $ ch5_selected = _return
    if ch5_selected == "continue":
        if ch5_scene < 6:
            $ ch5_scene += 1
            $ ch5_scene_tasks = []
            jump ch5_scene_hub
        jump ch5_ending
    call expression "ch5_task_" + ch5_selected
    if ch5_selected not in ch5_scene_tasks:
        $ ch5_scene_tasks.append(ch5_selected)
    jump ch5_scene_hub


label ch5_task_lamp:
    $ immersive_pose = "tense"
    show screen immersive_character
    zhang "停课。按预先路线疏散。先熄灯，关窗，带名册，不许逆行。"
    sy "煤油灯熄灭后再离开，避免倾倒起火。"
    hide screen immersive_character
    return

label ch5_task_window:
    $ immersive_pose = "tense"
    show screen immersive_character
    narrator_day1 "窗扇被扣紧，粗布帘拉住。后门的疏散通道没有被桌椅挡住。"
    hide screen immersive_character
    return

label ch5_task_exit:
    $ immersive_pose = "determined"
    show screen immersive_character
    $ ch5_has_roll = True
    sy "点名册在手。后排与角落无人滞留，行动慢的同学走在队伍中间。"
    gu "里面还有几件量具，经不起砸。"
    sy "先把人点清。器具再重，也是为人服务的。"
    hide screen immersive_character
    return

label ch5_task_names:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    narrator_day1 "防空壕里光线很暗，我按导师小组逐一核对姓名。"
    if ch5_has_roll:
        sy "名册齐全，实到人数与撤离记录相符。"
    else:
        sy "没有名册，只能依据座次和同伴确认逐项补核。"
    hide screen immersive_character
    return

label ch5_task_missing:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    xu "陈介白有派工条，邵兰有病假凭据。林若衡只有口述，只能写待核。"
    sy "听说不等于核实，不知道便写不知道。"
    hide screen immersive_character
    return

label ch5_task_allclear:
    $ immersive_pose = "calm"
    show screen immersive_character
    narrator_day1 "我们等待第二次明确的解除信号，没有因为外面暂时安静便擅自返回。"
    zhang "人员点清，警报解除。按原路线回教室。"
    hide screen immersive_character
    return

label ch5_task_desks:
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "桌椅被扶正，散落纸页按座位收拢。无人先去抢救器具的选择，保住了完整的撤离顺序。"
    hide screen immersive_character
    return

label ch5_task_chalk:
    $ immersive_pose = "calm"
    show screen immersive_character
    zhang "方才讲到这里。我们继续。"
    asking_student "章先生，警报响了，老百姓都躲飞机去了，我们还上课么？"
    zhang "怎么不上课？照上不误。我们走到哪里，课就上到哪里。"
    hide screen immersive_character
    return

label ch5_task_blackboard:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    asking_student "那么，黑板挂在哪里呢？"
    zhang "没有地方挂，就挂在我胸前。"
    narrator_day1 "他没有真的把大型黑板绑在身上，只扶住一块可移动的小黑板，把中断的式子重新写完。"
    hide screen immersive_character
    return

label ch5_task_teaching:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    menu:
        "教学物品中先装哪些？"
        "点名册、粉笔、核心讲义":
            $ ch5_teaching_items = 3
        "地图、计算尺":
            $ ch5_teaching_items = 2
        "只带大型黑板":
            $ ch5_teaching_items = 0
            zhang "大型黑板不适合疏散。课堂续接要依靠可携带之物。"
    hide screen immersive_character
    return

label ch5_task_survival:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    menu:
        "生存物品中先装哪些？"
        "水壶、急救包、防水油布":
            $ ch5_survival_items = 3
        "干粮、绳索":
            $ ch5_survival_items = 2
        "什么也不带":
            $ ch5_survival_items = 0
            xu "保存课堂，先要保存人。必须重配。"
    hide screen immersive_character
    return

label ch5_task_capacity:
    $ immersive_pose = "determined"
    show screen immersive_character
    if ch5_teaching_items >= 2 and ch5_survival_items >= 2:
        zhang "点名册必带，教学与生存物品都有最低保障。背包可以封口。"
        $ immersive_items = ["点名册", "粉笔与讲义", "急救包", "防水油布"]
    else:
        xu "只顾教学或只顾生存都不能完成行动链。我们补入点名册、讲义、急救包和油布。"
        $ ch5_teaching_items = 2
        $ ch5_survival_items = 2
    hide screen immersive_character
    return

label ch5_task_weight:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    menu:
        "小船安全载重800斤。已有仪器300斤、行李120斤、人员200斤。每箱书20斤，最多还能装几箱？"
        "九箱":
            $ day1_records += 1
            zhang "对。算清余量，是为了知道何处该停。"
        "十箱":
            zhang "还需留出安全余量，不能只看算术上限。"
        "十二箱":
            zhang "载重已经超过安全范围。重新核算。"
    hide screen immersive_character
    return

label ch5_task_route:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    sy "杭州、建德、金华、玉山、吉安。地图把下一段西行写成了一条可以检查的顺序。"
    zhang "地理题不是催促立刻出发，而是让人知道自己将往何处。"
    hide screen immersive_character
    return

label ch5_task_evidence:
    $ immersive_pose = "determined"
    show screen immersive_character
    sy "派工有派工条，病假有凭据；只有口述的林若衡仍标待核。"
    zhang "地方小些，字便写清楚些；时间短些，话便说准确些。"
    hide screen immersive_character
    return

label ch5_task_montage:
    $ immersive_pose = "relieved"
    show screen immersive_character
    narrator_day1 "门板、小黑板、油布、粉笔和点名册在不同屋檐下反复出现。老师在，学生在，求证的秩序仍在。"
    $ immersive_archive_count = 5
    hide screen immersive_character
    return

label ch5_task_uncertain:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    zhang "怕忘，尚不足以成其为真。记得快，更要辨得明。"
    sy "课堂上求证一道题，课堂外求证一句话，道理相通。"
    hide screen immersive_character
    return

label ch5_task_invitation:
    $ immersive_pose = "determined"
    show screen immersive_character
    committee_worker "若给你一些不那么规整的消息，你可愿学一学，如何从杂音里分出真假？"
    sy "我愿意学。但若记错了呢？"
    committee_worker "所以才要核。"
    hide screen immersive_character
    return


label ch5_ending:
    hide screen immersive_character
    hide screen immersive_hud
    scene ch5 lessons
    with fade
    narrator_day1 "“黑板挂在胸前”不是忽视警报，也不是夸饰性的表演。它发生在熄灯、关窗、带名册、点清人员之后。"
    zhang "保存课堂，先要保存人。人到了，课也要有办法接上。"
    if in_chapter_episode:
        if 5 not in day1_completed_chapters:
            $ day1_completed_chapters.append(5)
        centered "{size=46}第五章完成{/size}\n\n梅城的临时教室即将启用"
        jump campaign_complete_chapter5
    $ day1_finish_chapter(5)
    centered "{size=46}第五章完成{/size}"
    jump day1_map_hub
