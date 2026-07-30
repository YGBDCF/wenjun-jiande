# Codex任务：实现建德四十五日V1.2

目标仓库：`YGBDCF/wenjun-jiande`（Ren'Py）。

唯一权威规格：`docs/CODEX_IMPLEMENTATION_GUIDE.md`。机器可读辅助数据：`docs/random_event_catalog.json`、`docs/map_exam_progression_spec.json`。

先只完成以下顺序，不要跳步，不要删除现有六章标签或图片声明：

1. 保留两张大地图并共享状态，地图往返不消耗时段。
2. Day1-Day6正式学习仅在孔庙；建德地图显示七地点和锁定空地。
3. Day7第一项自由行动前强制完成第五章；章节不消耗回合。
4. 完成第五章后将空地热点和地图局部资产替换为“临时教室”，正式课程迁入教室。
5. 实现0-20核心属性、0-10生存属性、活动门槛与所有事件选项非零后果校验。
6. Day1孔庙摸底不计GPA；Day8/15/22/29/36/43在教室固定周考，考试占用早晨回合。
7. 实现三道互动题、学行抉择、考试公式、5.0 GPA严格门槛、累计GPA成绩单。
8. 导入83个事件；教室8事件必须受`classroom_unlocked`门控。
9. 保持晚间行动后强制回学生宿舍，深夜不可行动。
10. 完成lint和开发断言后再进入Day10-Day20报纸系统。

每次提交保持项目可启动。建议提交：

- `feat: add quantitative player stats and activity checks`
- `feat: gate chapter five and transform jiande map`
- `feat: add classroom location and weekly exams`
- `data: add classroom events and morality consequences`
- `test: cover map phase and GPA gates`
