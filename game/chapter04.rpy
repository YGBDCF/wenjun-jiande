label chapter_4:
    scene bg ch4
    with fade

    centered "{size=50}第四章  建德梅城{/size}\n{size=32}四十五天建起一所大学{/size}"
    pause 0.8

    $ immersive_setup("第四章  建德梅城", "1937年11月  梅城", "在城中重新建立临时校园", [("布置孔庙课堂", False), ("安顿民居宿舍", False), ("建立林场办公点", False), ("整理当铺住宿区", False), ("设置校务办公处", False), ("接收码头物资", False)], ["尊重居民原有生活", "恢复教学秩序"], ["梅城简图", "房屋登记册"], 3, "calm")
    call immersive_show from _call_immersive_show_2

    narrator_day1 "师生抵达梅城后，办公室、教室和宿舍被分散安置在城中各处。"
    yq "你们带来的人比我想象得还多。"
    sy "还有书、仪器和家属。"
    yq "梅城不大，空房也不是凭空长出来的。"
    sy "我们会尽量不影响居民生活。"
    yq "‘尽量’是最好说的一句话，也是最难做到的一句话。"
    narrator_day1 "叶青禾是本地青年，熟悉街巷和住户。"
    yq "孔庙可以摆课桌，林场能办公，东门街有几户人家愿意腾房。"
    sy "那已经够组成一所学校了。"
    yq "不够。你们还需要水、灯、床铺、厨房和能躲警报的地方。"
    sy "那就一处处解决。"
    yq "好。你先别把梅城当作一张空白地图。这里的每一间屋子都有人生活。"
    narrator_day1 "六处地点会随安置工作的推进分批解锁。"

    $ ch4_places = []
    jump chapter_4_hub


label chapter_4_hub:
    hide screen immersive_character
    $ immersive_tasks = [("布置孔庙课堂", "kongmiao" in ch4_places), ("安顿民居宿舍", "minju" in ch4_places), ("建立林场办公点", "linchang" in ch4_places), ("整理当铺住宿区", "pawnshop" in ch4_places), ("设置校务办公处", "office" in ch4_places), ("接收码头物资", "dock" in ch4_places)]
    if len(ch4_places) >= 6:
        jump chapter_4_finish
    $ ch4_unlocked = ["kongmiao", "minju"]
    if "kongmiao" in ch4_places and "minju" in ch4_places:
        $ ch4_unlocked += ["linchang", "pawnshop"]
    if "linchang" in ch4_places and "pawnshop" in ch4_places:
        $ ch4_unlocked += ["office", "dock"]
    call screen historical_location_map("bg ch4", "建德梅城  临时校园", [("kongmiao", "孔庙", 100, 210, 420, 300), ("minju", "民居", 530, 420, 300, 270), ("linchang", "林场", 650, 100, 350, 270), ("pawnshop", "当铺", 920, 430, 300, 270), ("office", "校务办公处", 1110, 120, 350, 270), ("dock", "梅城码头", 1280, 430, 280, 300)], ch4_places, ch4_unlocked)
    if _return == "kongmiao":
        jump chapter_4_kongmiao
    elif _return == "linchang":
        jump chapter_4_linchang
    elif _return == "minju":
        jump chapter_4_minju
    elif _return == "pawnshop":
        jump chapter_4_pawnshop
    elif _return == "office":
        jump chapter_4_office
    else:
        jump chapter_4_dock


label chapter_4_kongmiao:
    scene ch4 kongmiao with dissolve
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    sy "孔庙正殿宽敞，屋檐也能遮雨。"
    yq "但祭器、旧匾额和居民平日使用的空间都不能随意搬走。"
    sy "如果只使用两侧，能坐下的人会少很多。"
    yq "如果全占下来，附近的人会觉得学校一来，自己的地方就没有了。"
    sy "课堂要建立，关系也不能毁掉。"

    menu:
        "如何布置临时课堂？"

        "保留原有陈设，只使用两侧空间":
            $ day1_trust += 1
            yq "人挤一些，但至少大家愿意继续借给你们。"
            sy "我们把长凳排得更紧，让高年级学生轮流使用。"

        "集中陈设，尽量多摆课桌":
            $ day1_morale += 1
            yq "能坐更多学生，不过每天都要有人负责整理和看守。"
            sy "我把这项工作写进值日表。"

    sy "第一块黑板挂起来时，整个正殿忽然像一间真正的教室。"
    yq "只是像。"
    sy "课程开始以后，就是。"
    if "kongmiao" not in ch4_places:
        $ ch4_places.append("kongmiao")
    hide screen immersive_character
    jump chapter_4_location_return


label chapter_4_linchang:
    scene ch4 linchang with dissolve
    $ immersive_pose = "calm"
    show screen immersive_character
    narrator_day1 "林场被安排为教师住处和行政办公地点。"
    sy "这里离街市远，夜里很安静。"
    yq "也很黑。你们带来的油灯不够。"
    sy "课程表、布告和物资清单都需要连夜整理。"
    yq "教师也要备课。两边都不能完全停。"

    menu:
        "有限的油灯先给哪里？"

        "优先给收发公文和课程安排的办公室":
            $ day1_supplies += 1
            sy "布告在夜里写好，第二天一早就能贴到各处。"
            yq "至少不会再有人走错教室。"

        "优先给教员备课的房间":
            $ day1_morale += 1
            sy "老师们把第二天要讲的内容重新整理出来。"
            yq "看来你们是真的准备在这里继续上课。"

    zc "临时并不意味着可以无序。越是分散，越需要每一份通知准确。"
    sy "竺校长站在门边，鞋上还带着泥。"
    zc "一所大学可以暂时没有校门，但不能没有秩序。"
    if "linchang" not in ch4_places:
        $ ch4_places.append("linchang")
    hide screen immersive_character
    jump chapter_4_location_return


label chapter_4_minju:
    scene ch4 minju with dissolve
    $ immersive_pose = "worried"
    show screen immersive_character
    narrator_day1 "东门街一户居民愿意腾出两间房，条件是学校不能完全占用厨房和前厅。"
    yq "这家人有老人和孩子。你们住进来以后，不能把他们挤到角落里。"
    sy "可学生人数比床位多一倍。"
    yq "所以要谈，不是命令。"
    sy "我明白。"

    menu:
        "如何安排住宿？"

        "减少床位，保证居民继续使用厨房和前厅":
            $ day1_trust += 2
            yq "地方更挤，但屋主愿意长期借下去。"
            sy "学生分成两班，一部分打地铺，一部分轮流值夜。"

        "由学校负责修缮和搬运，换取更多空间":
            $ day1_supplies -= 1
            $ day1_trust += 1
            yq "只要说到做到，街坊会接受。"
            sy "我们修好漏雨的屋瓦，又把居民的家具原样搬回。"

    yq "你们总说自己只是暂住。"
    sy "因为我们不知道什么时候又要走。"
    yq "可只要住进来一天，就会留下痕迹。"
    sy "那我们应该让留下的痕迹尽量不只是麻烦。"
    if "minju" not in ch4_places:
        $ ch4_places.append("minju")
    hide screen immersive_character
    jump chapter_4_location_return


label chapter_4_dock:
    scene ch4 dock with dissolve
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "码头又到了一批书籍和仪器，部分木箱已经受潮。"
    ls "受潮书籍先晾，箱号不清的单独放，仪器不能堆在外面。"
    sy "人手不够。"
    yq "我可以叫几个熟悉码头的人来帮忙，但你们得告诉他们怎么分。"
    sy "那就先把规则写在木牌上。"
    ls "很好。不要让每个人都来问同一个问题。"

    menu:
        "首先处理哪一批物资？"

        "优先抢救受潮书籍":
            $ day1_records += 1
            sy "我们把书页一册册分开，屋里很快全是潮湿的纸味。"
            yq "这些书晒干以后，还能继续用吗？"
            ls "有些能，有些只能尽力保住内容。"

        "优先登记仪器和箱号，避免继续混放":
            $ day1_supplies += 2
            sy "清单写得很慢，却让之后每一次搬运都更快。"
            yq "原来秩序也能节省力气。"
            ls "尤其是在所有人都很疲惫的时候。"

    oldzhou "下一条船明早到。你们今晚最好把空地腾出来。"
    sy "我们点亮两盏灯，继续整理到深夜。"
    if "dock" not in ch4_places:
        $ ch4_places.append("dock")
    hide screen immersive_character
    jump chapter_4_location_return


label chapter_4_pawnshop:
    scene ch4 pawnshop with dissolve
    $ immersive_pose = "thoughtful"
    show screen immersive_character
    narrator_day1 "旧当铺的高柜台后堆着木箱，空地可以铺下数十张草席。"
    yq "这里能住人，也能存放不怕潮的物资，但不能把通道堵死。"
    sy "我们把寝铺沿墙安排，中间留出搬运和夜间疏散的路。"
    menu:
        "当铺内部怎样分区？"
        "柜台后存放物资，外间安置学生":
            $ day1_supplies += 1
            sy "物资与寝铺分开，清点时不会踩过别人的被褥。"
        "先留出最宽的中央通道":
            $ day1_trust += 1
            yq "拥挤是免不了的，至少不能让拥挤变成危险。"
    sy "最后一盏灯挂起来时，当铺不再只是仓库，也成了临时宿舍。"
    if "pawnshop" not in ch4_places:
        $ ch4_places.append("pawnshop")
    hide screen immersive_character
    jump chapter_4_location_return


label chapter_4_office:
    scene ch4 office with dissolve
    $ immersive_pose = "determined"
    show screen immersive_character
    narrator_day1 "校务办公处里，名册、课程表、房屋登记和运输清单占满长桌。"
    zc "地点分散以后，准确的记录就是学校的经纬。"
    sy "我把各处联络人、灯火使用和次日课程逐项抄进总册。"
    menu:
        "今晚优先整理哪份记录？"
        "先核对师生与住宿名册":
            $ day1_records += 1
            zc "先知道每个人在哪里，遇到警报才不会遗漏。"
        "先发布次日课程与地点":
            $ day1_morale += 1
            sy "布告送到各住处后，学生终于知道明早该往哪里走。"
    narrator_day1 "分散在城里的房屋，因为这张总表第一次被连成了一所大学。"
    if "office" not in ch4_places:
        $ ch4_places.append("office")
    hide screen immersive_character
    jump chapter_4_location_return


label chapter_4_location_return:
    if len(ch4_places) >= 6 and 4 not in day1_completed_chapters:
        $ ch4_return_to_world_map = False
        jump chapter_4_finish
    if ch4_return_to_world_map:
        $ ch4_return_to_world_map = False
        jump day1_map_hub
    jump chapter_4_hub


label chapter_4_finish:
    scene bg ch4
    $ immersive_pose = "relieved"
    show screen immersive_character
    narrator_day1 "数日后，孔庙里传出读书声，林场亮起办公灯，民居住进学生，码头上的木箱也有了去处。"
    yq "我原以为你们只是在城里借几间房。"
    sy "现在呢？"
    yq "现在我觉得，你们是在把许多互不相干的地方，连成一所学校。"
    sy "而且这所学校没有围墙。"
    zc "没有围墙并不可怕。可怕的是人心先散了。"
    sy "梅城只让我们停留四十五天，可在最初几天里，我们已经重新建立了一套生活。"
    yq "你们很快还会走吗？"
    sy "我不知道。"
    yq "又是这句话。"
    sy "但这次我知道，在离开之前，我们会继续上课。"
    narrator_day1 "临时校园在整座梅城中展开，而新的警报声也越来越近。"

    $ day1_finish_chapter(4)
    call immersive_hide from _call_immersive_hide_2
    centered "{size=44}第四章完成{/size}\n“黑板挂在我的胸前”已解锁"
    jump day1_map_hub
