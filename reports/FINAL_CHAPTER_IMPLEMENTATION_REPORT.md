# 终章实施与验收报告

## 交付范围

已按照《FINAL_CHAPTER_SCRIPT_AND_ART_TASKBOOK》完成建德四十五日终章，固定流程如下：

1. 最后一次点名
2. 七处地点回望
3. 离开梅城
4. 竺可桢两问
5. 玩家作答
6. 许南枝、顾明川、周顺安告别
7. 吉安—泰和路线预告
8. 五页结局统计
9. 十项终章菜单

Day 45 的唯一结局入口已经连接至 `finale_roll_call`，并保留兼容入口，避免旧存档或旧脚本跳转失效。

## 功能实现

- “竺可桢两问”完整演出与四种自由回答，无数值门槛。
- 回答分别写入求知、实务、守护、同行路线，并计入最终评价。
- 三名主要同伴拥有独立告别段落，并根据既有关系、任务与记录追加条件文本。
- 结局统计包含学习、生活、服务、社会、综合评价五页。
- 综合称号支持最高评价“弦歌不绝”及其他路线称号。
- 结局数据与选择记录写入 `persistent`，支持重看与收集。
- 终章菜单固定十项，退出游戏仅在终章菜单提供，并采用二次确认。
- 终章画廊、人物告别重看、统计重看、泰和海报、保存、返回标题等入口已接通。

## 美术素材

共交付 26 张 WebP 素材，目录为：

`game/images/finale/`

包括：

- 点名 2 张
- 七处地点回望 7 张
- 离开梅城与启航 4 张
- 竺可桢两问 2 张
- 四种玩家回答 4 张
- 三名人物告别 3 张
- 吉安—泰和路线与海报 2 张
- 结局统计 1 张
- 终章菜单 1 张

图片统一采用 1937 年浙大西迁历史纪实方向：低饱和灰蓝与土金色、普通人物、民国服装、真实材质、克制电影光线；图片本身不焊死正文、按钮、校徽或现代文字，所有界面文字由 Ren’Py 动态显示。

## 修改文件

- `game/jiande_finale.rpy`
- `game/meicheng_45_system.rpy`（Day 45 唯一终章入口）
- `game/images/finale/answers/*`
- `game/images/finale/departure/*`
- `game/images/finale/farewells/*`
- `game/images/finale/menu/*`
- `game/images/finale/questions/*`
- `game/images/finale/retrospective/*`
- `game/images/finale/roll_call/*`
- `game/images/finale/route/*`
- `game/images/finale/statistics/*`
- `game/images/finale/teaser/*`

## 验证结果

- Ren’Py 版本：8.5.3.26051504
- Lint：通过，无脚本语法、重复 label、重复 screen 或缺失图片报错
- 项目统计：495 个对话块、16 个菜单、79 张引擎识别图片、65 个 screen
- 实际启动：通过
- 虚拟分辨率：1920×1080
- 实际运行测试：直接进入终章后持续运行 10 秒，无崩溃、无立即 traceback、图形界面正常初始化
- 实际项目素材计数：26 张
- 工作副本与实际项目中的 `jiande_finale.rpy` SHA-256 一致

## 实际项目位置

已同步至：

`D:\RenPy\文军长征_建德四十五日_RenPy原型_v0.1\文军长征_建德四十五日_RenPy原型_v0.1\wenjun-jiande`

在 Ren’Py Launcher 选择 `wenjun-jiande`，执行“强制重新编译”后即可运行。

## 建议 Git 提交

`feat: complete Jiande finale narrative, statistics, gallery and art`
