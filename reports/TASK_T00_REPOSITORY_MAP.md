# TASK T00：仓库基线与路径审计

审计时间：2026-07-31（Asia/Shanghai）  
审计方式：全新只读审计；未沿用上一次阻塞审计结果。  
审计对象：

```text
D:\RenPy\文军长征_建德四十五日_RenPy原型_v0.1\文军长征_建德四十五日_RenPy原型_v0.1\wenjun-jiande
```

## 1. T00 边界与结论

- 本轮只读取文件、搜索符号并记录 Git 基线。
- 没有修改 `game/`、`docs/`、素材、存档或其他游戏文件。
- 五份指导文件均存在、可完整读取。
- T00 六项验收中 4 项通过、2 项未通过。
- 按任务书“任意一项找不到：停止并上报”的规则，本轮结论为 **T00 未通过**。
- 本报告提交用户审阅后停止，不进入 T01。

## 2. 五份指导文件完整性

以下文件均位于实际运行工程的 `docs/` 目录，均可按 UTF-8 完整读取，未出现替换字符。

| 序号 | 文件 | 大小（字节） | SHA-256 |
|---:|---|---:|---|
| 1 | `docs/CODEX_IMPLEMENTATION_GUIDE.md` | 126234 | `197849825CB23B7F27B07C63FF52D84638A1EEE7A46E7CA37974B59CE29FBD2C` |
| 2 | `docs/PATCH_NEW_GAMEPLAY_SYSTEMS.md` | 49982 | `FCEC24B8EC60ADB8628B7D0B285C909E48D6DA1362FDFADAD978BBC50CF0FABE` |
| 3 | `docs/CODEX_SUPERVISION_REWORK_ORDER.md` | 18699 | `AC90068608450E5E5589AE5754025A835B156C2EFACB76A0756733F73B1252FA` |
| 4 | `docs/PATCH_POSITIVE_STORY_AND_DAY45_FINALE_HOTFIX.md` | 19332 | `BD3B768505E99B862797E0DEB08B8DD29B131666FD5CBF9A08A12313F8A39D0A` |
| 5 | `docs/CODEX_EXECUTION_TASKBOOK_EVENT_AND_FINALE_REWORK (2).md` | 25192 | `1BB32B7D6D30DC039B588D1F3449780C6A32B000643AA479424018C73C8E7FA4` |

说明：第五份文件的实际文件名带有 ` (2)` 后缀；内容中包含 T00—T15 的任务顺序及 T00 验收标准。

## 3. 仓库结构概览

```text
wenjun-jiande/
├─ .git/
├─ docs/                       五份指导文件及规格资料
├─ game/                       Ren’Py 游戏源码与资源
│  ├─ campaign/                45日玩法、事件、社团、考试等系统
│  ├─ data/                    运行时 JSON 数据
│  ├─ images/                  场景、地图与人物图片
│  ├─ script.rpy               Ren’Py 起点
│  ├─ meicheng_45_data.rpy     旧版/回退事件数据
│  └─ meicheng_45_system.rpy   建德地图与45日循环
├─ reports/                    审计报告
├─ tools/
└─ v2.1/                       已构建发行副本；非当前源码基线
```

## 4. 必须路径地图

### 4.1 Ren’Py 入口文件

- `game/script.rpy:82`：`label start:`
- `game/script.rpy` 是游戏启动后的主脚本入口。

### 4.2 83 个事件的实际运行时来源

- `game/data/random_event_catalog.json`：解析后恰好 83 条。
- `game/campaign/random_event_system.rpy:9`：`renpy.open_file("data/random_event_catalog.json")`
- `game/campaign/random_event_system.rpy:10`：解析 JSON 并赋给 `RANDOM_EVENT_CATALOG`
- `game/campaign/random_event_system.rpy:12`：构造 `RANDOM_EVENT_BY_ID`
- `game/campaign/dev_assertions.rpy:47`：断言事件数为 83。

另有 `docs/random_event_catalog.json`，也有 83 条，但运行时代码没有读取该副本；因此它不是实际运行时来源。

### 4.3 “迟到的仪器船”

- 精确标题存在于 `game/meicheng_45_data.rpy:120`。
- 精确标题及改写规格存在于：
  - `docs/CODEX_SUPERVISION_REWORK_ORDER.md:37`
  - `docs/CODEX_SUPERVISION_REWORK_ORDER.md:60`
  - `docs/CODEX_SUPERVISION_REWORK_ORDER.md:217`
- 实际 83 事件目录中没有精确标题“迟到的仪器船”，对应事件是：
  - `game/data/random_event_catalog.json`：`MT_003`，标题“迟到的船”。

结论：可以定位原事件与规格，但旧事件源和实际 83 事件目录存在标题/来源分叉，T01 需要专门核对，T00 不修改。

### 4.4 事件选择生成代码

当前存在两套相关实现：

1. 83 事件目录的选择渲染：
   - `game/campaign/random_event_system.rpy:348`
   - `game/campaign/random_event_system.rpy:352-353`
   - `game/campaign/random_event_system.rpy:368-369`
   - 这里遍历 `event["choices"]`，显示各事件数据中的选择。

2. 旧建德事件的三个通用按钮：
   - `game/meicheng_45_system.rpy:332`：“动手解决”
   - `game/meicheng_45_system.rpy:341`：“核对记录”
   - `game/meicheng_45_system.rpy:350`：“先照料人”

此外，社团活动也有固定三按钮：

- `game/campaign/club_system.rpy:203`
- `game/campaign/club_system.rpy:211`
- `game/campaign/club_system.rpy:219`

### 4.5 社团系统文件

- 主文件：`game/campaign/club_system.rpy`
- 社团活动 screen：`game/campaign/club_system.rpy:185`
- 入口调用可见于 `game/campaign/classroom_actions.rpy:72`。

### 4.6 天气变量文件

- `game/campaign/state.rpy:17`：`default current_weather = "cloudy"`
- `game/campaign/state.rpy:19-20`：天气预报及准确度。
- `game/meicheng_45_system.rpy:9`：旧循环变量 `mc45_weather = "江雾"`。
- 两套状态的导入/同步位于 `game/campaign/state.rpy:392-457`。

### 4.7 建德地图 screen

- 当前主建德地图：`game/meicheng_45_system.rpy:74`，`screen mc45_world_map()`
- 主调用：`game/meicheng_45_system.rpy:497`，`call screen mc45_world_map`
- 另一套旧地图：`game/meicheng_town_explore.rpy:76`，`screen meicheng_town_map()`

主地图在 `game/meicheng_45_system.rpy:79` 根据 `map_visual_phase` 选择前/后期地图图片，并在 `:154-206` 生成地点按钮。

### 4.8 Day7 地图状态

- 默认状态：
  - `game/campaign/state.rpy:37`：`classroom_unlocked = False`
  - `game/campaign/state.rpy:38`：`map_visual_phase = "pre_classroom"`
- Day7 章节门：
  - `game/campaign/chapter_gates.rpy:126`：`label day7_chapter5_gate`
  - `game/campaign/chapter_gates.rpy:151`：解锁教室
  - `game/campaign/chapter_gates.rpy:152`：切换为 `post_classroom`
- 地图读取：
  - `game/meicheng_45_system.rpy:78-100`
  - `game/meicheng_45_system.rpy:192-206`：第五章完成后显示临时教室。

### 4.9 周考实现文件

- 主文件：`game/campaign/exam_system.rpy`
- 总分计算函数：`game/campaign/exam_system.rpy:96`，`campaign_calculate_exam(...)`
- 分项与总分公式：`game/campaign/exam_system.rpy:98-119`
- 考试触发状态：`game/campaign/state.rpy:79`
- 地图入口前检查：`game/meicheng_45_system.rpy:483-491`

### 4.10 Day45 按钮位置

- `game/meicheng_45_system.rpy:456`：

```renpy
textbutton ("进入下一日" if mc45_day < 45 else "结束建德篇"):
```

- 结束分支：`game/meicheng_45_system.rpy:575-580`

重要差异：全仓库没有找到任务书验收要求的精确按钮文字 **“结束建德生活”**；现有文字为 **“结束建德篇”**。

### 4.11 `Quit`、`MainMenu`、`renpy.quit` 调用位置

- `game/day1_map.rpy:136`：`MainMenu()`
- `game/screens.rpy:373`：`MainMenu()`
- `game/screens.rpy:385`：`Quit(confirm=not main_menu)`
- `game/screens.rpy:469`：`Quit(confirm=False)`
- 游戏源码中未找到直接 `renpy.quit` 调用。
- Day45 分支 `game/meicheng_45_system.rpy:575-580` 没有直接调用 `Quit`、`MainMenu` 或 `renpy.quit`，而是完成第四章并跳回六章地图。

### 4.12 结局、尾声、海报资源

已找到脚本尾声：

- `game/chapter02.rpy:355`：`label ch2_ending`
- `game/chapter03.rpy:337`：`label ch3_ending`
- `game/chapter05.rpy:331`：`label ch5_ending`
- `game/chapter06.rpy:323`：`label ch6_ending`
- `game/chapter06.rpy:334-338`：三种文字尾声。

未找到以 `ending`、`epilogue`、`poster`、`teaser`、`finale`、`结局`、`尾声`或`海报`命名的独立图片/资源目录。当前可定位的是文字脚本结尾，不是任务书描述的独立结局、尾声或海报资源。

### 4.13 既有测试目录

- 当前源码 `game/` 下未找到项目自有的 `test/` 或 `tests/` 目录。
- 仅在 `v2.1/` 的打包运行库内发现 Ren’Py/Python 第三方测试目录；它们不是本项目的自动验收测试。
- 当前可见的开发断言文件为 `game/campaign/dev_assertions.rpy`，但它不是测试目录。

## 5. 地图天气渲染核对

地图已实现：

- `game/meicheng_45_system.rpy:105`：`add Solid(MC45_TIME_TINTS[mc45_time])`
- 该层只按早晨、午间、傍晚、深夜改变全图色调。
- `game/meicheng_45_system.rpy:119` 只把 `[mc45_weather]` 作为文字显示。

全项目没有找到由 `current_weather` 或 `mc45_weather` 驱动的地图雨层、雾层、雪层、亮度矩阵、色彩矩阵或天气专用图片切换。因此不能把时段色调认定为“地图天气渲染”。

## 6. T00 验收表

| 验收项 | 结果 | 证据 |
|---|---|---|
| 找到 83 个事件实际来源 | 通过 | `game/data/random_event_catalog.json`；加载点 `game/campaign/random_event_system.rpy:9-12` |
| 找到“迟到的仪器船” | 通过（有分叉风险） | `game/meicheng_45_data.rpy:120`；实际 83 目录对应 `MT_003` 标题为“迟到的船” |
| 找到通用按钮生成位置 | 通过 | `game/meicheng_45_system.rpy:332,341,350` |
| 找到 Day45“结束建德生活”按钮 | **未通过** | 仅找到 `game/meicheng_45_system.rpy:456` 的“结束建德篇” |
| 找到周考总分计算函数 | 通过 | `game/campaign/exam_system.rpy:96-119` |
| 找到地图天气渲染位置 | **未通过** | 仅有 `game/meicheng_45_system.rpy:105` 的时段色调和 `:119` 的天气文字 |

## 7. 最终状态

**T00_FAIL — 停止，不进入 T01。**

阻塞原因：

1. Day45 按钮文字与任务书要求不一致，找不到“结束建德生活”。
2. 建德地图尚未实现天气驱动的视觉渲染，只有时段色调。

附加风险（不改变上述判定）：

1. “迟到的仪器船”存在于旧事件源，但实际 83 事件目录使用“迟到的船”，需要在 T01 明确唯一来源与稳定 ID。
2. 没有找到项目自有测试目录。
3. 没有找到独立结局、尾声和海报图片资源。
4. T00 开始前工作树已有多项未提交修改与 `v2.1/docs/` 删除，本轮没有触碰这些改动。
