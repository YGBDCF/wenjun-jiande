# ================================================================
# V1.2 数值考试系统（Phase A0-5）
# 权威规格：docs/CODEX_IMPLEMENTATION_GUIDE.md §3
# ================================================================

define CAMPAIGN_EXAM_CONFIG = {
    1:  {"type": "diagnostic", "difficulty": 35, "credit": 0.0, "title": "孔庙摸底测验", "theme": "基础计算、路线辨认与文字核对"},
    8:  {"type": "official", "difficulty": 42, "credit": 1.0, "title": "正式周考一", "theme": "数学基础、装载与方位"},
    15: {"type": "official", "difficulty": 50, "credit": 1.0, "title": "正式周考二", "theme": "名册、数字与文书核对"},
    22: {"type": "official", "difficulty": 58, "credit": 1.2, "title": "正式周考三", "theme": "新闻标题、来源与真假判断"},
    29: {"type": "official", "difficulty": 65, "credit": 1.3, "title": "正式周考四", "theme": "天气、江运、道路与应变"},
    36: {"type": "official", "difficulty": 72, "credit": 1.5, "title": "正式周考五", "theme": "校舍、物资和迁移组织综合"},
    43: {"type": "official_final", "difficulty": 78, "credit": 2.0, "title": "行前综合考查", "theme": "综合题与撤离准备"},
}

define CAMPAIGN_EXAM_QUESTIONS = {
    1: [
        ("四只书箱每只重二十五斤，合计多少斤？", ("七十五斤", "一百斤", "一百二十五斤"), 1),
        ("从杭州沿钱塘江、富春江向建德行进，大体应向哪个方向？", ("向西", "向东", "向北"), 0),
        ("名册写有一百零二人，实到九十九人，应如何记录？", ("照抄名册人数", "写实到九十九并注明三人未到", "删去三人姓名"), 1),
    ],
    8: [
        ("一条船限载二百斤，已有三箱各四十斤，还能装多少斤？", ("六十斤", "八十斤", "一百二十斤"), 1),
        ("江面起雾、能见度很低时，最稳妥的做法是？", ("加速赶路", "减速靠岸并保持联络", "熄灯继续"), 1),
        ("地图上北方在上，队伍向地图左侧行进，方向是？", ("东", "西", "南"), 1),
    ],
    15: [
        ("箱号从甲一至甲二十，缺甲十三。最合适的记录是？", ("重新编号掩盖空缺", "注明甲十三未见并立即复核", "默认已经装船"), 1),
        ("名册原有八十七人，转入六人、离队两人，现有多少人？", ("九十一人", "九十三人", "八十九人"), 0),
        ("两份清单数字不符，首先应当？", ("采用较大的数字", "逐项核对原始凭据", "取平均数"), 1),
    ],
    22: [
        ("广播只听清地点和伤亡数字，标题应如何写？", ("直接断言战局", "注明消息未完全核实", "补写缺失细节"), 1),
        ("同一消息只有一个匿名来源，最稳妥的是？", ("立刻刊登", "寻找第二来源交叉验证", "按读者喜好改写"), 1),
        ("勘误最能维护报纸信誉的方式是？", ("悄悄删去错误", "公开说明错误与更正依据", "责怪收音机杂音"), 1),
    ],
    29: [
        ("寒潮与江雾同时出现，船运安排应优先？", ("按原时刻强行开船", "检查天气与航道后调整", "只增加货物"), 1),
        ("山路塌方后需要绕行，首先核对什么？", ("队伍名册与物资清单", "谁走得最快", "哪条路风景更好"), 0),
        ("湿书箱应怎样处理？", ("紧闭不管", "通风、隔潮并逐箱登记", "直接曝晒到卷曲"), 1),
    ],
    36: [
        ("校舍空间不足时，课程安排首先应避免？", ("分时使用教室", "同一地点同一时段冲突", "借用临时黑板"), 1),
        ("搬运精密仪器，最重要的记录是？", ("只记总箱数", "箱号、经手人、状态与去向", "只记价格"), 1),
        ("迁移准备与教学冲突时，合理原则是？", ("全部停课", "保证安全链并维持必要课程", "只顾考试"), 1),
    ],
    43: [
        ("行前核对发现一箱图书无去向签，应该？", ("跟最近车辆走", "暂停装运并追查交接记录", "写一个新箱号"), 1),
        ("警报中撤离课堂，正确顺序是？", ("先救个人行李", "组织人员安全转移并保护必要资料", "继续坐在原位"), 1),
        ("西迁办学最核心的连续性来自？", ("固定校舍", "师生、课程、书籍与求实传统", "某一条路线"), 1),
    ],
}

default exam_current_answers = []
default exam_current_correct = 0
default exam_current_conduct_bonus = 0
default exam_current_cheated = False
default exam_current_detected = False
default exam_last_result = None

init python:
    def campaign_exam_completed(day):
        if day == 1:
            return store.diagnostic_score is not None
        return any(item.get("day") == day for item in store.exam_history)

    def campaign_exam_is_due():
        return (
            store.campaign_day in CAMPAIGN_EXAM_DAYS
            and store.campaign_period == 0
            and not campaign_exam_completed(store.campaign_day)
        )

    def campaign_exam_weather_penalty():
        weather = str(store.current_weather)
        if weather == "雨夹雪":
            return 3.0
        if weather == "寒潮":
            return 2.0
        if weather in ("小雨", "江雾"):
            return 1.0
        return 0.0

    def campaign_score_to_gpa(score, full_mark_ok):
        if score >= 96:
            return 5.0 if full_mark_ok else 4.8
        for minimum, value in (
            (92, 4.8), (89, 4.5), (86, 4.2), (83, 4.0),
            (80, 3.7), (76, 3.3), (72, 3.0), (68, 2.7),
            (64, 2.3), (60, 2.0), (0, 0.0),
        ):
            if score >= minimum:
                return value
        return 0.0

    def campaign_calculate_exam(day, correct, conduct_bonus, cheated=False, detected=False):
        config = CAMPAIGN_EXAM_CONFIG[day]
        attendance = store.weekly_attendance_present / float(max(1, store.weekly_attendance_possible)) * 100.0
        knowledge_fit = campaign_clamp(65.0 + (store.stat_knowledge * 5 - config["difficulty"]) * 1.5, 0.0, 100.0)
        question_score = correct / 3.0 * 100.0
        academic = (
            0.55 * knowledge_fit
            + 0.20 * store.weekly_preparation
            + 0.10 * question_score
            + 0.08 * (store.stat_will * 5)
            + 0.07 * (store.stat_health * 10)
        )
        conduct = (
            0.65 * (store.stat_morality * 5)
            + 0.20 * campaign_clamp(50 + store.hidden_truthfulness * 5, 0, 100)
            + 0.15 * attendance
        )
        fatigue = max(0, 5 - store.stat_stamina) * 2.5 + max(0, 6 - store.stat_health) * 2
        score = campaign_clamp(
            0.72 * academic + 0.28 * conduct + conduct_bonus
            - fatigue - campaign_exam_weather_penalty(),
            0.0,
            100.0,
        )
        if detected:
            score = 0.0

        threshold = {8: 13, 15: 15, 22: 16, 29: 17, 36: 18, 43: 20}.get(day, 99)
        full_mark_ok = (
            store.stat_knowledge >= threshold
            and store.stat_morality >= 18
            and store.hidden_truthfulness >= 6
            and store.weekly_preparation >= 85
            and attendance >= 90
            and correct >= 2
            and store.academic_misconduct_count == 0
            and not cheated
        )
        return {
            "day": day,
            "date": campaign_date_text(day),
            "title": config["title"],
            "theme": config["theme"],
            "difficulty": config["difficulty"],
            "credit": config["credit"],
            "correct": correct,
            "academic_score": round(academic, 2),
            "conduct_score": round(conduct, 2),
            "score": round(score, 2),
            "gpa": campaign_score_to_gpa(score, full_mark_ok),
            "full_mark_gate": full_mark_ok,
            "cheated": cheated,
            "detected": detected,
            "attendance": round(attendance, 1),
        }

    def campaign_update_cumulative_gpa():
        credits = sum(item["credit"] for item in store.exam_history)
        store.cumulative_gpa = 0.0 if credits <= 0 else round(
            sum(item["gpa"] * item["credit"] for item in store.exam_history) / credits,
            2,
        )

    def campaign_exam_comment(result):
        if result["detected"]:
            return "诚信失守，卷面成绩作废。先把事实写清楚，再谈学问。"
        if result["gpa"] == 5.0:
            return "卷面、学行与平日准备相互印证。可贵的不只是满分，而是无愧于求是二字。"
        if result["score"] >= 86:
            return "基础扎实，但仍要检查每一处依据，切勿以熟练代替求实。"
        if result["score"] >= 72:
            return "能够完成主要判断，弱项在准备与细节核对。"
        if result["score"] >= 60:
            return "勉强达到要求。建议补课、复盘，并恢复规律出勤。"
        return "基础尚未稳固。先厘清错误来源，再重新安排本周学习。"


screen campaign_exam_precheck(config):
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#080a0870")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1120
        ysize 720
        background Solid("#11140ff2")
        padding (60, 44)
        vbox:
            spacing 18
            text config["title"] size 45 color "#ead296" xalign 0.5
            text config["theme"] size 23 color "#c8c0af" xalign 0.5
            null height 12
            grid 2 4:
                spacing 20
                text "天气" size 23 color "#a99b7d"
                text "[current_weather]" size 23 color "#e1d9c8"
                text "体力 / 健康" size 23 color "#a99b7d"
                text "[stat_stamina] / [stat_health]" size 23 color "#e1d9c8"
                text "本周准备" size 23 color "#a99b7d"
                text "[weekly_preparation]" size 23 color "#e1d9c8"
                text "出勤" size 23 color "#a99b7d"
                text "[weekly_attendance_present] / [weekly_attendance_possible]" size 23 color "#e1d9c8"
            null height 24
            text "本次测试包含三道实际作答题与一项学行抉择。成绩一经记录，不允许无限重考。":
                size 22
                color "#d4ccbc"
                xalign 0.5
                text_align 0.5
            textbutton "领取试卷":
                xalign 0.5
                xsize 340
                ysize 64
                text_size 23
                text_color "#f0d89b"
                background Solid("#3a2f20e8")
                hover_background Solid("#594528ee")
                action Return()


screen campaign_exam_question(number, question_data):
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#080a0850")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1280
        ysize 700
        background Solid("#11140ff0")
        padding (58, 42)
        vbox:
            xfill True
            spacing 24
            text "第 [number] 题" size 27 color "#bca775"
            text question_data[0] size 31 color "#e6dece" xmaximum 1120 line_spacing 8
            null height 12
            for index, answer in enumerate(question_data[1]):
                textbutton answer:
                    xfill True
                    ysize 76
                    text_size 24
                    text_color "#d9d0bf"
                    text_hover_color "#fff0bd"
                    background Solid("#25251fe8")
                    hover_background Solid("#514027ef")
                    action Return(index)


screen campaign_exam_conduct(day):
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#080a085d")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1320
        ysize 720
        background Solid("#11140ff2")
        padding (60, 42)
        vbox:
            xfill True
            spacing 22
            text "学行抉择" size 39 color "#ead296"
            text "监考教师去取缺页试卷时，邻座将一张写有答案的草稿推到你桌边。":
                size 27
                color "#e0d8c8"
                xmaximum 1180
            textbutton "拒绝查看，并提醒他收回草稿（关系可能受损）":
                xfill True
                ysize 72
                text_size 23
                action Return("refuse")
            textbutton "把草稿交给监考教师说明来由（承担同学怨气）":
                xfill True
                ysize 72
                text_size 23
                action Return("report")
            textbutton "看一眼再推回去（提高眼前把握，但留下失信记录）":
                xfill True
                ysize 72
                text_size 23
                action Return("cheat")


screen campaign_exam_report(result, comment):
    modal True
    add "images/chapter05/scenes/return_class.png":
        xysize (1920, 1080)
    add Solid("#080a0876")
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1180
        ysize 820
        background Solid("#10130ff3")
        padding (58, 42)
        vbox:
            xfill True
            spacing 14
            text result["title"] size 42 color "#ead296" xalign 0.5
            text result["date"] size 20 color "#a9a190" xalign 0.5
            null height 10
            grid 2 6:
                spacing 18
                text "互动题" size 22 color "#ad9e7d"
                text ("%s / 3" % result["correct"]) size 22 color "#ded6c6"
                text "卷面倾向" size 22 color "#ad9e7d"
                text str(result["academic_score"]) size 22 color "#ded6c6"
                text "学行评定" size 22 color "#ad9e7d"
                text str(result["conduct_score"]) size 22 color "#ded6c6"
                text "总分" size 22 color "#ad9e7d"
                text str(result["score"]) size 22 color "#f0d897"
                text "单次 GPA" size 22 color "#ad9e7d"
                text str(result["gpa"]) size 22 color "#f0d897"
                text "累计 GPA" size 22 color "#ad9e7d"
                text "[cumulative_gpa]" size 22 color "#f0d897"
            null height 18
            text comment:
                size 22
                color "#d6cebd"
                text_align 0.5
                xalign 0.5
                xmaximum 980
                line_spacing 7
            if result["score"] >= 96 and not result["full_mark_gate"]:
                text "总分虽达到满绩区间，但未同时满足学识、道德、求实、准备、出勤与诚信门槛，本次 GPA 封顶 4.8。":
                    size 18
                    color "#c19d72"
                    text_align 0.5
                    xalign 0.5
            textbutton "收起成绩单":
                xalign 0.5
                xsize 340
                ysize 64
                text_size 22
                text_color "#f0d89b"
                action Return()


label campaign_forced_exam:
    $ exam_config = CAMPAIGN_EXAM_CONFIG[campaign_day]
    $ exam_current_answers = []
    $ exam_current_correct = 0
    $ exam_current_conduct_bonus = 0
    $ exam_current_cheated = False
    $ exam_current_detected = False
    $ exam_pending = True
    $ current_location = "kongmiao" if campaign_day == 1 else "classroom"
    call screen campaign_exam_precheck(exam_config)

    $ exam_questions = CAMPAIGN_EXAM_QUESTIONS[campaign_day]
    $ exam_question_number = 1
    while exam_question_number <= 3:
        $ exam_question = exam_questions[exam_question_number - 1]
        call screen campaign_exam_question(exam_question_number, exam_question)
        $ exam_answer = _return
        $ exam_current_answers.append(exam_answer)
        if exam_answer == exam_question[2]:
            $ exam_current_correct += 1
        $ exam_question_number += 1

    call screen campaign_exam_conduct(campaign_day)
    $ exam_conduct_choice = _return
    if exam_conduct_choice == "refuse":
        $ exam_current_conduct_bonus = 2
        $ relationship["gu_mingchuan"] = relationship.get("gu_mingchuan", 0) - 1
        $ hidden_truthfulness = campaign_clamp(hidden_truthfulness + 1, -10, 10)
    elif exam_conduct_choice == "report":
        $ exam_current_conduct_bonus = 4
        $ stat_morality = campaign_clamp(stat_morality + 1, 0, 20)
        $ relationship["mentor"] = relationship.get("mentor", 0) + 1
        $ hidden_truthfulness = campaign_clamp(hidden_truthfulness + 1, -10, 10)
    else:
        $ exam_current_conduct_bonus = -5
        $ exam_current_cheated = True
        $ academic_misconduct_count += 1
        $ stat_morality = campaign_clamp(stat_morality - 2, 0, 20)
        $ hidden_truthfulness = campaign_clamp(hidden_truthfulness - 2, -10, 10)
        $ exam_current_detected = renpy.random.random() < 0.35
        if exam_current_detected:
            $ stat_morality = campaign_clamp(stat_morality - 3, 0, 20)
            $ relationship["mentor"] = relationship.get("mentor", 0) - 3
            $ hidden_zhu_impression -= 2

    $ exam_last_result = campaign_calculate_exam(
        campaign_day,
        exam_current_correct,
        exam_current_conduct_bonus,
        exam_current_cheated,
        exam_current_detected,
    )

    if campaign_day == 1:
        $ diagnostic_score = exam_last_result["score"]
        $ exam_last_result["gpa"] = "不计"
        $ exam_comment = "这是摸底测验，不计入 GPA。请根据错题决定接下来六日的学习安排。"
    else:
        $ exam_history.append(exam_last_result.copy())
        $ campaign_update_cumulative_gpa()
        $ exam_comment = campaign_exam_comment(exam_last_result)
        $ weekly_preparation = 20
        $ weekly_attendance_present = 0
        $ weekly_attendance_possible = 0
        $ current_week += 1

    $ exam_pending = False
    $ action_count = min(135, action_count + 1)
    $ mc45_time = 1
    $ campaign_period = 1
    $ campaign_sync_legacy_view()
    call screen campaign_exam_report(exam_last_result, exam_comment)
    jump jiande_map_hub
