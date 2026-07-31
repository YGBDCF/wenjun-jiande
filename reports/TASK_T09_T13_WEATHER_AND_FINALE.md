# T09 / T13：天气视觉与第45日终章实施报告

实施日期：2026-07-31（Asia/Shanghai）

## 1. 本轮范围

- 按任务书 T09 补齐建德45日地图的天气驱动视觉、环境声与恶劣天气地点限制。
- 按任务书 T13/T14 接通第45日“结束建德生活”按钮和固定终章节点链。
- 不重置 Git，不删除后续章节，不改写已有存档变量。

## 2. T09 天气系统

### 2.1 四类天气差分

已为第五章扩展前、扩展后两套梅城地图各制作四类差分，共八张：

- 小雨：湿润路面、雨幕、江面雨点。
- 连阴雨/暴雨：更密雨线、积水与压低的能见度。
- 江雾：江岸及远景雾层，保留地图建筑与热点辨识度。
- 寒潮/霜冻：冷色空气、霜意与低温氛围。

### 2.2 动态渲染

- 小雨与大雨使用不同密度、速度、长度的动态雨丝。
- 江雾使用两层低透明度缓慢漂移雾带。
- 寒潮使用克制的冷色空气层。
- 视觉叠加层不接管鼠标，不阻挡地点热点。

### 2.3 环境声

新增四条可循环环境声：

- 小雨
- 大雨
- 雾中江声
- 寒风

天气变化时自动淡入、淡出对应声景。

### 2.4 地点限制与结算

- 连阴雨、大雨、暴雨、冻雨、雨夹雪期间，梅城码头暂停装卸。
- 同类恶劣天气期间，林场因积水与落枝风险暂缓通行。
- 点击受限地点时显示具体原因，并给出孔庙、校务办公处、当铺、学生宿舍等室内替代地点。
- 寒潮时，宿舍保暖达到 2 以上，夜间健康额外恢复 2；保暖不足时健康额外下降 3。

## 3. T13/T14 第45日终章

第45日深夜按钮已改为：

```text
结束建德生活
```

按钮直接进入：

```text
jiande_finale_entry
```

固定节点顺序：

```text
night_roll_call
→ finale_calculation
→ map_retrospective
→ meicheng_departure
→ zhu_two_questions
→ player_final_answer
→ companion_farewells
→ character_epilogues
→ jian_taihe_teaser
→ ending_statistics
→ post_ending_menu
```

已实现：

- 深夜点名与四十五日收束。
- 七处建德地点回望。
- 梅城码头离城长段落。
- 竺可桢“两问”原句及历史转置说明。
- 四个玩家回答与四条评价路线。
- 许南枝、顾明川、周树南告别。
- 江西泰和动态文字海报。
- 结局统计、档案、物品与人物尾声回看。
- 结局后停留在菜单，不自动退出。

## 4. 新增与修改文件

### 脚本

- `game/campaign/weather_visuals.rpy`
- `game/jiande_finale.rpy`
- `game/meicheng_45_system.rpy`

### 天气图

- `game/images/meicheng_town/weather/pre_rain.png`
- `game/images/meicheng_town/weather/pre_heavy_rain.png`
- `game/images/meicheng_town/weather/pre_fog.png`
- `game/images/meicheng_town/weather/pre_cold.png`
- `game/images/meicheng_town/weather/post_rain.png`
- `game/images/meicheng_town/weather/post_heavy_rain.png`
- `game/images/meicheng_town/weather/post_fog.png`
- `game/images/meicheng_town/weather/post_cold.png`

### 声音与海报

- `game/audio/weather/rain_light.wav`
- `game/audio/weather/rain_heavy.wav`
- `game/audio/weather/fog_river.wav`
- `game/audio/weather/cold_wind.wav`
- `game/images/finale/jian_taihe_teaser.png`

## 5. 检查结果

对工作区与实际 D 盘运行项目分别执行 Ren’Py 8.5.3 Lint：

- 解析通过。
- 无脚本语法错误。
- 无重复 label 报错。
- 无缺失图片声明报错。
- 实际工程统计：417 个对话块、16 个菜单、79 张图片、62 个 screen。

## 6. 后续人工试玩重点

- 在小雨、江雾、寒潮和连阴雨日分别进入梅城地图，观察图片、动态层和环境声是否匹配。
- 连阴雨时点击码头、林场，确认显示限制原因且其他室内地点可进入。
- 将进度推进到第45日深夜，确认按钮文字与完整终章链。
- 终章后依次测试海报、人物尾声、档案、物品、读档与返回标题界面。
