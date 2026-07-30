# ================================================================
# 第六章：《浙大日报》——从杂音中求其真
# 正式剧本编号：ZJU-1937-06
# ================================================================

define intelligence_member = Character("情报委员会成员", color="#bdc4ad")
define printer = Character("印刷处工人", color="#c2b08c")
define resident = Character("梅城居民", color="#c0b5a1")

image ch6 noise:
    "images/chapter06/scenes/radio_noise_v2.png"
    xysize (1920, 1080)
image ch6 wall:
    "images/chapter06/scenes/wall_newspaper.png"
    xysize (1920, 1080)
image ch6 proof:
    "images/chapter06/scenes/proofreading.png"
    xysize (1920, 1080)
image ch6 issue:
    "images/chapter06/scenes/first_issue.png"
    xysize (1920, 1080)
image ch6 sale:
    "images/chapter06/scenes/street_sale.png"
    xysize (1920, 1080)
image ch6 leave:
    "images/chapter06/scenes/departure.png"
    xysize (1920, 1080)

default ch6_scene = 1
default ch6_scene_tasks = []
default ch6_truth_score = 0
default ch6_public_trust = 0

init python:
    CH6_SCENE_META = {
        1: (
            "杂乱中找正确",
            "1937年11月中旬  深夜",
            "ch6 noise",
            "从无线电杂音中保留可确认信息",
            [
                ("fragment", "听辨短促片段", 155, 300, 360, 350),
                ("compare", "对照两份记录", 600, 370, 370, 300),
                ("unclear", "标记听辨未清", 1040, 270, 390, 370),
            ],
        ),
        2: (
            "壁报的新问题",
            "1937年11月下旬  午后",
            "ch6 wall",
            "让居民理解消息的时间、来源与位置",
            [
                ("date", "补写日期来源", 155, 300, 360, 350),
                ("map", "挂出地理位置图", 600, 370, 370, 300),
                ("traffic", "说明本地交通关系", 1040, 270, 390, 370),
            ],
        ),
        3: (
            "仔细纠错",
            "1937年11月下旬  印刷处",
            "ch6 proof",
            "在付印前完成内容校核",
            [
                ("time", "核对时间与地点", 155, 300, 360, 350),
                ("negative", "检查否定词", 600, 370, 370, 300),
                ("headline", "修正标题与版序", 1040, 270, 390, 370),
            ],
        ),
        4: (
            "一分钱",
            "1937年12月1日  清晨",
            "ch6 issue",
            "完成《浙大日报》创刊号交付",
            [
                ("count", "清点五百份报纸", 155, 300, 360, 350),
                ("price", "确认每份一分钱", 600, 370, 370, 300),
                ("routes", "划分分送路线", 1040, 270, 390, 370),
            ],
        ),
        5: (
            "信传希望",
            "1937年12月1日  梅城街头",
            "ch6 sale",
            "把经过核验的消息送到读者手中",
            [
                ("voice", "练习街头叫卖", 155, 300, 360, 350),
                ("questions", "回应居民询问", 600, 370, 370, 300),
                ("income", "记录工读收入", 1040, 270, 390, 370),
            ],
        ),
        6: (
            "再次启程",
            "1937年12月19日至26日",
            "ch6 leave",
            "课程不停，同时完成离开建德前清点",
            [
                ("classes", "维持最后课程", 155, 300, 360, 350),
                ("cargo", "封装图书仪器", 600, 370, 370, 300),
                ("keepsakes", "整理六件记录物", 1040, 270, 390, 370),
            ],
        ),
    }


label chapter_6:
    $ ch6_scene = 1
    $ ch6_scene_tasks = []
    $ ch6_truth_score = 0
    $ ch6_public_trust = 0
    $ immersive_items = ["广播记录纸", "校务布告"]
    $ immersive_archive_count = 5
    call screen chapter_title_card(
        "images/chapter06/scenes/first_issue.png",
        "第六章",
        "《浙大日报》",
        "从杂音中求其真",
        "1937年11月下旬至12月26日  建德"
    )
    jump ch6_scene_hub


label ch6_scene_hub:
    $ ch6_meta = CH6_SCENE_META[ch6_scene]
    $ immersive_chapter = "第六章  《浙大日报》"
    $ immersive_date = ch6_meta[1]
    $ immersive_objective = ch6_meta[3]
    $ immersive_tasks = [(task[1], task[0] in ch6_scene_tasks) for task in ch6_meta[4]]
    $ immersive_secondary = ["注明消息来源", "不把传言写成定论"]
    scene expression ch6_meta[2]
    hide screen immersive_character
    show screen immersive_hud
    call screen chapter_task_scene(
        ch6_meta[2],
        ch6_meta[0],
        "一字之差，足以改变读者对道路与亲友安危的判断",
        ch6_meta[4],
        ch6_scene_tasks,
    )
    $ ch6_selected = _return
    if ch6_selected == "continue":
        if ch6_scene < 6:
            $ ch6_scene += 1
            $ ch6_scene_tasks = []
            jump ch6_scene_hub
        jump ch6_ending
    call expression "ch6_task_" + ch6_selected
    if ch6_selected not in ch6_scene_tasks:
        $ ch6_scene_tasks.append(ch6_selected)
    jump ch6_scene_hub


label ch6_task_fragment:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    radio "……车队……杭州……未证实……"
    menu:
        "杂音掩住了关键字，应怎样记录？"
        "按自己认为最合理的词补齐":
            $ ch6_truth_score -= 1
            xu "合理不等于听见。"
        "听辨未清，待复核":
            $ ch6_truth_score += 1
            sy "不确定本身也是需要记录的信息。"
    hide screen immersive_character
    return

label ch6_task_compare:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    xu "你听见的是‘已经’，我听见的是‘预计’。两字之差，足以使整条消息改变意思。"
    sy "两份记录并列，不抢先选择其中一个。等下一次播报或其他来源。"
    $ ch6_truth_score += 1
    hide screen immersive_character
    return

label ch6_task_unclear:
    $ immersive_pose = "determined"
    show screen immersive_character
    intelligence_member "确认的字用墨写，未确认的字用铅笔，听不清的位置留空并标时间。"
    sy "广播不会停下来等我们，但记录可以诚实地留下边界。"
    $ ch6_truth_score += 1
    hide screen immersive_character
    return

label ch6_task_date:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    resident "这消息是哪一天的？从哪里听来的？"
    xu "壁报补上接收日期、广播来源和复核状态。没有这些，消息看似完整，实际无法使用。"
    $ ch6_public_trust += 1
    hide screen immersive_character
    return

label ch6_task_map:
    $ immersive_pose = "calm"
    show screen immersive_character
    resident "此处离建德有多远？"
    narrator_day1 "许南枝把地图挂在壁报旁，标出地点与大致方向。"
    sy "名字若离开地图，读者仍不知道消息与自己有何关系。"
    hide screen immersive_character
    return

label ch6_task_traffic:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    xu "道路受影响，不等于所有交通已经断绝。壁报只写已经确认的路段。"
    sy "把与本地船期、课程和出行有关的部分另列一栏。"
    $ ch6_public_trust += 1
    hide screen immersive_character
    return

label ch6_task_time:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    sy "这条消息的时间比原记录早了一日，地点也被排到了相邻县。两处都要改。"
    printer "若不在付印前发现，五百份都会把错误带出去。"
    $ ch6_truth_score += 1
    hide screen immersive_character
    return

label ch6_task_negative:
    $ immersive_pose = "tense"
    show screen immersive_character
    narrator_day1 "一行排字漏掉了一个“不”字。原句的意思因此完全反转。"
    sy "这里必须停印重排。文字的失误同样可能伤人。"
    $ ch6_truth_score += 2
    hide screen immersive_character
    return

label ch6_task_headline:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    menu:
        "头版标题应怎样处理一条尚未证实的传言？"
        "用醒目标题抢先刊登":
            $ ch6_public_trust -= 2
            printer "报纸会卖得快，恐慌也会跑得更快。"
        "不写成定论，注明待复核":
            $ ch6_truth_score += 1
            $ ch6_public_trust += 1
            sy "迫切不能替代证据。"
    hide screen immersive_character
    return

label ch6_task_count:
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "1937年12月1日清晨，创刊号按五十份一叠清点，共约五百份。"
    sy "学校、街口和较远住处分别装袋，避免途中再拆乱。"
    hide screen immersive_character
    return

label ch6_task_price:
    $ immersive_pose = "calm"
    show screen immersive_character
    printer "每份一分钱。账目按领取数、售出数和退回数分别登记。"
    zhou "浙江大学和今日消息——这几个字我都认得了。"
    hide screen immersive_character
    return

label ch6_task_routes:
    $ immersive_pose = "determined"
    show screen immersive_character
    sy "孔庙、林场、方宅与东门街各有人负责。最远路线先出发。"
    narrator_day1 "一张报纸开始把分散的校园和梅城居民重新连接起来。"
    $ immersive_items = ["广播记录纸", "壁报地图", "《浙大日报》创刊号"]
    hide screen immersive_character
    return

label ch6_task_voice:
    $ immersive_pose = "relieved"
    show screen immersive_character
    zhou "《浙大日报》——今日消息！"
    gu "《浙大日报》——今、日、消、息！"
    xu "顾同学，你怎么喊得像报数一样。"
    hide screen immersive_character
    return

label ch6_task_questions:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    resident "学校是不是马上又要走？杭州那边究竟怎样？"
    sy "我们只回答报纸上已经注明来源的部分。未证实的，不因有人急问便变成事实。"
    $ ch6_public_trust += 1
    hide screen immersive_character
    return

label ch6_task_income:
    $ immersive_pose = "calm"
    show screen immersive_character
    narrator_day1 "工读学生记录售出数，收入的一部分用于帮助生活困难的学生。"
    sy "新闻传递远方消息，也在现实中维持一些学生继续求学的可能。"
    hide screen immersive_character
    return

label ch6_task_classes:
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "12月19日，学校决定迁移准备期间课程不停止，抵达吉安后继续上课。"
    gu "教室照常开，船也照常装。最后一堂课不能因为箱子已经封好便提前取消。"
    hide screen immersive_character
    return

label ch6_task_cargo:
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "12月22日起，图书仪器开始运往金华。箱号、封条、课程讲义与人员名单再次逐项核对。"
    xu "12月26日，最后一批师生也将离开建德。"
    hide screen immersive_character
    return

label ch6_task_keepsakes:
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    narrator_day1 "蓝布笔记本里夹着银杏叶、码头清单抄件、文澜阁箱号纸、梅城校舍图、一截粉笔和创刊号。"
    xu "带着这些纸，不嫌沉么？"
    sy "总要有人记得，我们曾在何处读书，又曾如何离开。"
    $ immersive_archive_count = 6
    hide screen immersive_character
    return


label ch6_ending:
    hide screen immersive_character
    hide screen immersive_hud
    scene ch6 leave
    with fade
    zhou "你们何时回来？"
    sy "我也不知。待再见之时，我希望你能写下日期给我看。"
    narrator_day1 "船缓缓离岸。教师仍在批阅作业，学生整理讲义，顾明川复核木箱，许南枝清点人员。"
    sy "我们并非待安定之后，方始读书；正是在安定一再失去之时，弦歌仍未曾中绝。"
    $ day1_finish_chapter(6)
    if ch6_truth_score >= 5 and ch6_public_trust >= 3:
        centered "{size=50}尾声　共同的记录{/size}\n\n你让消息的来源、边界与责任一同抵达读者。"
    elif ch6_truth_score >= 5:
        centered "{size=50}尾声　求其真{/size}\n\n你的记录保留了未知，没有让迫切替代证据。"
    else:
        centered "{size=50}尾声　仍在学习{/size}\n\n纸页已经印出，而公共记录的责任仍需继续学习。"
    pause 1.0
    if in_chapter_episode:
        jump campaign_complete_chapter6
    menu:
        "浙江篇六章体验完成。"
        "返回章节地图":
            jump day1_map_hub
        "返回主菜单":
            return
