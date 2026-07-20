# Day 1：游戏入口与六章最小可玩流程

define sy = Character("沈砚", color="#d8bc7d")
define narrator_day1 = Character("旁白", color="#d7d0be")


label start:
    scene black
    with fade

    centered "{size=58}文军长征：建德四十五日{/size}\n\n{size=32}Day 1 · 章节地图与顺序解锁原型{/size}"

    pause 1.0
    jump day1_map_hub


label day1_map_hub:
    call screen day1_chapter_map
    $ selected_chapter = _return

    if selected_chapter == 1:
        jump day1_chapter_1
    elif selected_chapter == 2:
        jump day1_chapter_2
    elif selected_chapter == 3:
        jump day1_chapter_3
    elif selected_chapter == 4:
        jump day1_chapter_4
    elif selected_chapter == 5:
        jump day1_chapter_5
    elif selected_chapter == 6:
        jump day1_chapter_6

    jump day1_map_hub


label day1_chapter_1:
    scene black
    with fade

    centered "{size=52}第一章　西天目山{/size}\n寺庙里的大学"

    narrator_day1 "全面抗战爆发后，浙大一年级新生迁往西天目山禅源寺。"
    sy "寺庙成了校园。我们刚刚熟悉这里，却不断从广播中听见杭州局势恶化。"

    menu:
        "进入寺院后，先做什么？"

        "拜访导师，确认课程安排":
            $ day1_trust += 1
            sy "导师告诉我：校舍可以迁移，学习不能停止。"

        "帮助同学整理僧舍":
            sy "陌生的房间渐渐有了宿舍的样子。"

        "记录广播中的杭州消息":
            $ day1_records += 1
            sy "我把听清的每一个地名都写进笔记。"

    narrator_day1 "不久，新的迁移命令抵达：前往建德，与校本部会合。"

    $ day1_finish_chapter(1)
    centered "第一章完成\n第二章已解锁"
    jump day1_map_hub


label day1_chapter_2:
    scene black
    with fade

    centered "{size=52}第二章　江干码头{/size}\n把一所大学装上船"

    narrator_day1 "深夜的码头上堆满木箱、仪器、教材和行李。"
    sy "船位有限。每装上一件东西，就意味着另一件东西需要等待。"

    menu:
        "第一批船位优先安排什么？"

        "老人、儿童和身体不适者":
            $ day1_trust += 1

        "精密仪器和教材":
            $ day1_records += 1

        "尽可能多装箱子":
            pass

    $ day1_finish_chapter(2)
    centered "第二章完成\n第三章已解锁"
    jump day1_map_hub


label day1_chapter_3:
    scene black
    with fade

    centered "{size=52}第三章　护送《四库全书》{/size}\n守护文化的记忆"

    narrator_day1 "玩家核对箱号、封签和目录，确认需要重点保护的典籍箱。"

    menu:
        "哪项证据最可靠？"

        "箱子最重":
            narrator_day1 "重量并不能说明其中一定是典籍。"

        "目录号、旧封签和馆藏印能够互相对应":
            $ day1_records += 1
            narrator_day1 "证据彼此吻合，才能确认书箱身份。"

        "箱子外观最完整":
            narrator_day1 "外观完整不等于记录可靠。"

    $ day1_finish_chapter(3)
    centered "第三章完成\n第四章已解锁"
    jump day1_map_hub


label day1_chapter_4:
    scene black
    with fade

    centered "{size=52}第四章　建德梅城{/size}\n四十五天建起一所大学"

    narrator_day1 "孔庙成为课堂，林场承担办公，当铺和民居被改作宿舍。"

    menu:
        "最先需要解决什么？"

        "让课程尽快恢复":
            $ day1_records += 1

        "先与居民协商住宿":
            $ day1_trust += 1

        "先清点图书和仪器":
            $ day1_records += 1

    $ day1_finish_chapter(4)
    centered "第四章完成\n第五章已解锁"
    jump day1_map_hub


label day1_chapter_5:
    scene black
    with fade

    centered "{size=52}第五章　黑板挂在我的胸前{/size}\n警报中的课堂"

    narrator_day1 "防空警报打断了课堂。师生转移后，教师决定继续讲课。"
    sy "没有教室，没有黑板，可这堂课仍然没有结束。"

    menu:
        "避难时优先带走什么？"

        "行动较慢的同学":
            $ day1_trust += 1

        "课程笔记和粉笔":
            $ day1_records += 1

        "照明用的油灯":
            pass

    $ day1_finish_chapter(5)
    centered "第五章完成\n第六章已解锁"
    jump day1_map_hub


label day1_chapter_6:
    scene black
    with fade

    centered "{size=52}第六章　《浙大日报》{/size}\n战争中的信息战"

    narrator_day1 "学生从广播中整理消息，编辑报纸并在梅城街头分发。"

    menu:
        "报纸应该采用哪类信息？"

        "已经由可靠来源确认的消息":
            $ day1_records += 1
            $ day1_trust += 1

        "所有听到的消息":
            pass

        "最能吸引读者的传闻":
            $ day1_trust -= 1

    $ day1_finish_chapter(6)

    scene black
    with fade

    centered "{size=54}Day 1 原型完成{/size}\n\n信任记录：[day1_trust]\n史料判断：[day1_records]\n\n地图、点击、顺序解锁和选择流程已经跑通。"

    pause 1.0

    menu:
        "接下来做什么？"

        "返回章节地图":
            jump day1_map_hub

        "返回主菜单":
            return
