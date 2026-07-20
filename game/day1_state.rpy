default day1_current_chapter = 1
default day1_completed_chapters = []

default day1_trust = 0
default day1_records = 0
default day1_morale = 0
default day1_supplies = 0

default ch4_places = []
default newspaper_choice = ""


init python:
    DAY1_CHAPTER_INFO = {
        1: ("西天目山", "寺庙里的大学"),
        2: ("江干码头", "把一所大学装上船"),
        3: ("护送《四库全书》", "守护文化的记忆"),
        4: ("建德梅城", "四十五天建起一所大学"),
        5: ("黑板挂在我的胸前", "警报中的课堂"),
        6: ("《浙大日报》", "战争中的信息战"),
    }

    def day1_is_unlocked(chapter_id):
        return chapter_id <= store.day1_current_chapter

    def day1_finish_chapter(chapter_id):
        if chapter_id not in store.day1_completed_chapters:
            store.day1_completed_chapters.append(chapter_id)

        if chapter_id < 6:
            store.day1_current_chapter = max(
                store.day1_current_chapter,
                chapter_id + 1
            )
