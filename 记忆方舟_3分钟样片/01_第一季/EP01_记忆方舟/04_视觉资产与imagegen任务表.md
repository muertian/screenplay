# EP01《记忆方舟》视觉资产与 `$imagegen` 任务表

本文件记录静态图、参考图和关键帧任务。当前已使用 `$imagegen_builtin_image_gen` 生成首批参考图并进入人工验收；关键帧仍只规划，不提交视频。所有新生成或返修静态图必须使用 `$imagegen_builtin_image_gen`，不得使用 Dreamina、Seedance、Web UI 或一次性SDK脚本。

## 视觉圣经

| 项目 | 当前内容 | 使用范围 | 状态 | 备注 |
|---|---|---|---|---|
| 主视觉风格 | 电影感写实漫画，低饱和末世废土，真实光影，强阴影 | 全片 | 已确认 | 避免卡通夸张和过度霓虹 |
| 画幅与质感 | 16:9，单张电影关键帧，浅景深可用 | 所有关键帧 | 已确认 | 不做竖屏 |
| 光影色彩 | 废土灰绿、冷白医疗光、脏橙应急灯、核心红色警报光 | 全片 | 已确认 | 红色只用于方舟骗局暴露和空白晶片 |
| 镜头语言 | 手持压迫近景、低机位、慢推、快速动作切换 | 分镜/关键帧 | 已确认 | 动作必须可见 |
| 统一负向 | 不要文字、字幕、UI、标签、水印、分屏、拼贴、九宫格、参考图入画、重复人物、复制单体道具、露骨血腥 | 所有正式图 | 已确认 | 可按镜头追加 |

## 角色锁点草案

| 角色ID | 角色 | 参考图任务 | 角色锚点短句 | 允许变化 | 禁止变化 | 状态 |
|---|---|---|---|---|---|---|
| CHAR_LC | 陆沉 | GEN_REF_001 | 32岁失忆士兵，短黑发，左眉浅疤，灰绿色破损战术外套，胸口磨损身份牌 | 灰尘、汗、轻微伤痕、光线变化 | 换脸、长发、年轻化、服装换成制服、出现第二个陆沉实体 | 小样锁定 |
| CHAR_XH | 小禾 | GEN_REF_002 | 17岁废土信使，短发，旧校服外套改防尘披肩，手腕红布条 | 灰尘、紧张表情、披肩摆动 | 儿童化、成熟化、红布条消失、服装大改 | 小样锁定 |
| CHAR_LUO | 罗医师 | GEN_REF_003 | 45岁方舟医师，灰白短发，白色隔离服，透明面罩，温和冷静 | 面罩反光、医疗手套、冷白光 | 变成战斗角色、过度邪恶表情、遮住全部五官 | 小样锁定 |
| CROWD_REF | 幸存者群像 | GEN_REF_004 | 末世幸存者，灰尘、防尘布、疲惫眼神，非特定主角 | 姿态和年龄变化 | 抢主角脸、出现可读标语、露骨伤害 | 待生成 |
| EMPTY_WITNESS_REF | 空壳证人 | GEN_REF_005 | 被抽空记忆的人，干净白衣，机械微笑，眼神空洞 | 同排坐姿变化 | 血腥病变、恐怖怪物化、文字标签 | 待生成 |

## 场景空间锚点清单

| 场景ID | 场景名称 | 干净场景参考 | 可选空间源图 | 用途 | 状态 | 上传优先级 | 备注 |
|---|---|---|---|---|---|---:|---|
| SCENE_WRECK | 废弃装甲车车厢 | references/scenes/SCENE_WRECK_CLEAN_REF.png | references/scenes/SCENE_WRECK_LAYOUT_SOURCE.png | 冷开场、狭窄压迫、灰尘和破损金属 | 小样锁定 | 2 | 不得出现可读军标 |
| SCENE_WASTE_CITY | 废城外景 | references/scenes/SCENE_WASTE_CITY_CLEAN_REF.png | references/scenes/SCENE_WASTE_CITY_OVERVIEW_SOURCE.png | 方舟光柱和废城方向 | 小样锁定 | 3 | 远景只做环境，不上传地图 |
| SCENE_MEMORY_STREET | 记忆交易废街 | references/scenes/SCENE_MEMORY_STREET_CLEAN_REF.png | references/scenes/SCENE_MEMORY_STREET_LAYOUT_SOURCE.png | 人群、摊位、记忆交易 | 待生成 | 2 | 摊位不得有可读招牌 |
| SCENE_ALLEY | 窄巷与地下入口 | references/scenes/SCENE_ALLEY_CLEAN_REF.png | references/scenes/SCENE_ALLEY_LAYOUT_SOURCE.png | 追逐和探照灯 | 待生成 | 2 | 保持左进右出方向 |
| SCENE_MEMORY_MARKET | 地下记忆市场 | references/scenes/SCENE_MEMORY_MARKET_CLEAN_REF.png | references/scenes/SCENE_MEMORY_MARKET_OVERVIEW_SOURCE.png | 晶片罐、潮湿管线、地下交易 | 待生成 | 2 | 可有光罐，不可有文字标签 |
| SCENE_ARK_GATE | 方舟外墙与筛查门 | references/scenes/SCENE_ARK_GATE_CLEAN_REF.png | references/scenes/SCENE_ARK_GATE_LAYOUT_SOURCE.png | 方舟门、筛查线、外墙广播 | 小样锁定 | 1 | 正式上传关键场景 |
| SCENE_TRIAGE_HALL | 方舟洁白筛查通道 | references/scenes/SCENE_TRIAGE_HALL_CLEAN_REF.png | references/scenes/SCENE_TRIAGE_HALL_LAYOUT_SOURCE.png | 冷白医疗空间、空壳证人 | 待生成 | 1 | 避免医院文字导视 |
| SCENE_EXTRACTION_ROOM | 记忆抽取室 | references/scenes/SCENE_EXTRACTION_ROOM_CLEAN_REF.png | references/scenes/SCENE_EXTRACTION_ROOM_LAYOUT_SOURCE.png | 环形机器、抽取椅、核心红光 | 小样锁定 | 1 | 不露骨，靠机械压迫 |
| SCENE_MEMORY_CORE | 记忆核心竖井 | references/scenes/SCENE_MEMORY_CORE_CLEAN_REF.png | references/scenes/SCENE_MEMORY_CORE_LAYOUT_SOURCE.png | 记忆罐、管道、核心接口 | 小样锁定 | 1 | 上传优先级最高 |
| SCENE_COMMAND_ROOM | 废弃指挥室记忆空间 | references/scenes/SCENE_COMMAND_ROOM_CLEAN_REF.png | references/scenes/SCENE_COMMAND_ROOM_LAYOUT_SOURCE.png | 过去陆沉录下遗言 | 待生成 | 3 | 屏幕可发光但不可有可读文字 |

## 道具与线索参考清单

| 参考ID | 类型 | 文件路径 | 状态 | 对应段落 | 必须保持 | 禁止变化 | 上传条件 |
|---|---|---|---|---|---|---|---|
| PROP_BLANK_CHIP | 道具参考图 | references/props/PROP_BLANK_CHIP_v01.png | 小样锁定 | 全片 | 透明小晶片，内部可出现红色脉冲，单枚 | 复制成多枚、变成手机或屏幕、有文字 | 可见且剧情关键时必传 |
| PROP_MEMORY_CHIP | 道具参考图 | references/props/PROP_MEMORY_CHIP_v01.png | 待生成 | SEG002-006,012 | 金色或淡蓝记忆晶片，保存影像回声 | 变成纸张、出现文字标签 | 晶片特写必传 |
| PROP_ID_TAG | 道具参考图 | references/props/PROP_ID_TAG_v01.png | 小样锁定 | SEG001,004,010,012 | 磨损金属身份牌，不能读清姓名 | 出现可读姓名或编号 | 身份反转镜头必传 |
| PROP_EARPIECE | 道具参考图 | references/props/PROP_EARPIECE_v01.png | 小样锁定 | SEG001 | 破损战术通讯耳机，小型贴耳装置，无屏幕无文字 | 变成手机、屏幕、耳麦文字标签 | SEG001耳机恢复镜头可传 |
| PROP_ELECTRO_RIFLE | 道具参考图 | references/props/PROP_ELECTRO_RIFLE_v01.png | 待生成 | SEG004,007 | 非致命电击枪，短管，冷白电弧 | 变成真实血腥枪战武器 | 动作镜头可传 |
| PROP_EXTRACTOR_CHAIR | 道具参考图 | references/props/PROP_EXTRACTOR_CHAIR_v01.png | 小样锁定 | SEG007-008 | 环形记忆椅、束带、头顶光环 | 血腥医疗器械化 | 抽取室镜头必传 |
| PROP_SCAN_SLOT | 道具参考图 | references/props/PROP_SCAN_SLOT_v01.png | 待生成 | SEG006 | 透明筛查槽，用光色表达判定 | 出现UI文字或读数 | 方舟门筛查镜头必传 |
| PROP_MEMORY_JARS | 道具参考图 | references/props/PROP_MEMORY_JARS_v01.png | 待生成 | SEG005,010 | 发光记忆罐，管道连接 | 标签文字、拼贴展示 | 场景远近景可传 |

## `$imagegen` 参考图任务表

| 任务ID | 图片ID | 类型 | 工具 | 目标比例 | 保存目录 | 推荐文件名 | 可复制提示词摘要 | 验收标准 | 状态 |
|---|---|---|---|---|---|---|---|---|---|
| GEN_REF_001 | IMG_CHAR_LC_REF | 角色参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/characters/ | CHAR_LC_ref_v01.png | 16:9单人多视图参考表，陆沉，短黑发、左眉浅疤、灰绿色破损战术外套、身份牌，纯白背景，无文字 | 同一角色多角度一致，无文字，无场景 | 小样锁定 |
| GEN_REF_002 | IMG_CHAR_XH_REF | 角色参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/characters/ | CHAR_XH_ref_v01.png | 16:9单人多视图参考表，小禾，短发、旧校服防尘披肩、红布条，纯白背景，无文字 | 不儿童化，服装锚点清楚 | 小样锁定 |
| GEN_REF_003 | IMG_CHAR_LUO_REF | 角色参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/characters/ | CHAR_LUO_ref_v01.png | 16:9单人多视图参考表，罗医师，灰白短发、白色隔离服、透明面罩，纯白背景，无文字 | 温和冷感，不怪物化 | 小样锁定 |
| GEN_REF_004 | IMG_CROWD_REF | 角色/群像参考 | `$imagegen_builtin_image_gen` | 16:9 | references/characters/ | CROWD_REF_v01.png | 末世幸存者群像参考，灰尘、防尘布、疲惫眼神，无主角脸，无文字 | 可作为背景群体参考 | 待生成 |
| GEN_REF_005 | IMG_EMPTY_WITNESS_REF | 角色/状态参考 | `$imagegen_builtin_image_gen` | 16:9 | references/characters/ | EMPTY_WITNESS_REF_v01.png | 空壳证人状态参考，干净白衣、机械微笑、眼神空洞，无血腥 | 恐怖靠表演，不靠露骨伤害 | 待生成 |
| GEN_SCENE_001 | IMG_SCENE_ARK_GATE | 干净场景参考 | `$imagegen_builtin_image_gen` | 16:9 | references/scenes/ | SCENE_ARK_GATE_CLEAN_REF.png | 巨大白色方舟外墙与筛查门，废城尽头，冷白光，无文字标语 | 空间入口、外墙、光源清楚 | 小样锁定 |
| GEN_SCENE_002 | IMG_SCENE_EXTRACTION_ROOM | 干净场景参考 | `$imagegen_builtin_image_gen` | 16:9 | references/scenes/ | SCENE_EXTRACTION_ROOM_CLEAN_REF.png | 环形记忆抽取室，中央抽取椅，冷白医疗光和少量红色警报光，无文字 | 可用于多个抽取室镜头 | 小样锁定 |
| GEN_SCENE_003 | IMG_SCENE_MEMORY_CORE | 干净场景参考 | `$imagegen_builtin_image_gen` | 16:9 | references/scenes/ | SCENE_MEMORY_CORE_CLEAN_REF.png | 巨大记忆核心竖井，发光记忆罐和管道，压迫纵深，无文字 | 空间层级和接口清楚 | 小样锁定 |
| GEN_SCENE_004 | IMG_SCENE_WRECK | 干净场景参考 | `$imagegen_builtin_image_gen` | 16:9 | references/scenes/ | SCENE_WRECK_CLEAN_REF.png | 废弃装甲车车厢内部，破损金属、灰尘、冷光缝隙，无军标文字 | 冷开场空间方向清楚，无可读标识 | 小样锁定 |
| GEN_SCENE_005 | IMG_SCENE_WASTE_CITY | 干净场景参考 | `$imagegen_builtin_image_gen` | 16:9 | references/scenes/ | SCENE_WASTE_CITY_CLEAN_REF.png | 低饱和末世废城远景，远处白色方舟光柱，脏橙应急灯，无文字 | 方舟方向和城市尺度清楚 | 小样锁定 |
| GEN_PROP_001 | IMG_PROP_BLANK_CHIP | 道具参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/props/ | PROP_BLANK_CHIP_v01.png | 透明空白记忆晶片，小型手持物，内部可红色脉冲，纯道具图，无文字 | 只出现一枚晶片 | 小样锁定 |
| GEN_PROP_002 | IMG_PROP_EXTRACTOR_CHAIR | 道具参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/props/ | PROP_EXTRACTOR_CHAIR_v01.png | 记忆抽取椅，环形光环、束带、冷白医疗机械，无血腥、无文字 | 结构可读，非恐怖血腥 | 小样锁定 |
| GEN_PROP_003 | IMG_PROP_ID_TAG | 道具参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/props/ | PROP_ID_TAG_v01.png | 磨损金属身份牌道具图，编号与姓名不可读，冷硬金属质感，无文字 | 不能读出任何姓名或编号 | 小样锁定 |
| GEN_PROP_004 | IMG_PROP_EARPIECE | 道具参考图 | `$imagegen_builtin_image_gen` | 16:9 | references/props/ | PROP_EARPIECE_v01.png | 破损战术通讯耳机，小型贴耳装置，灰尘划痕，无屏幕无文字 | 形体清楚，不像手机或UI设备 | 小样锁定 |

## 关键帧生成矩阵

规则：首段生成 `SHOT01-SHOT04` 共4张关键帧；后续段 `SHOT01` 来自上一段真实尾帧，本轮只为 `SHOT02-SHOT04` 规划新关键帧。因此全片计划关键帧为37张。

| 段落ID | 需生成关键帧 | 跳过原因 | 关键角色 | 当前场景 | 核心道具 | provider | 状态 |
|---|---|---|---|---|---|---|---|
| S01E01_SEG001 | SHOT01, SHOT02, SHOT03, SHOT04 | 首段无上一段尾帧 | 陆沉 | 废弃装甲车、废城 | 空白晶片、身份牌、耳机 | `$imagegen_builtin_image_gen` | VISUAL_PASS |
| S01E01_SEG002 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG001真实尾帧 | 陆沉、小禾、幸存者 | 记忆交易废街 | 记忆晶片 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG003 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG002真实尾帧 | 陆沉、小禾 | 窄巷 | 记忆晶片、方舟探照灯 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG004 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG003真实尾帧 | 陆沉、小禾、清剿队 | 窄巷地下入口 | 电击枪、身份牌 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG005 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG004真实尾帧 | 陆沉、小禾、交易员 | 地下记忆市场 | 记忆晶片、记忆罐 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG006 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG005真实尾帧 | 陆沉、小禾、人群 | 方舟外墙 | 筛查槽、空白晶片 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG007 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG006真实尾帧 | 陆沉、罗医师、空壳证人 | 方舟筛查通道 | 空白晶片、电击枪 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG008 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG007真实尾帧 | 陆沉、罗医师 | 记忆抽取室 | 抽取椅、空白晶片 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG009 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG008真实尾帧 | 陆沉 | 抽取室、伪造记忆空间 | 空白晶片、身份牌 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG010 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG009真实尾帧 | 陆沉 | 记忆核心 | 身份牌、记忆液、空白晶片 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG011 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG010真实尾帧 | 陆沉、小禾、人群 | 记忆核心、方舟外墙 | 空白晶片、广播光柱 | `$imagegen_builtin_image_gen` | 待生成 |
| S01E01_SEG012 | SHOT02, SHOT03, SHOT04 | SHOT01用SEG011真实尾帧 | 陆沉、小禾、人群 | 指挥室记忆空间、方舟外墙、记忆核心 | 空白晶片、身份牌、记忆晶片 | `$imagegen_builtin_image_gen` | 待生成 |

## 关键帧提示词示例

### S01E01_SEG001_SHOT01

```text
镜头: S01E01_SEG001_SHOT01，16:9 单张电影关键帧。
引用图职责: 图1=陆沉身份参考，只参考脸、发型、服装、体态；图2=废弃装甲车车厢场景参考，只参考空间结构、光线、材质和方向；图3=空白记忆晶片参考，只参考外形、比例、材质和当前状态。

承接上一镜头: 本片起始，无上一镜头。
当前画面: 废弃装甲车内部低机位近景，陆沉从座椅上猛然醒来，灰尘从车顶落下，右手紧攥一枚透明空白记忆晶片。
角色/表演: 陆沉眼神空白，呼吸急促，肩膀紧绷，左眉浅疤可见。
为下一镜头承接: 他的手摸向胸口身份牌，准备确认自己是谁。

连续性锁点: 只出现一个陆沉；空白记忆晶片只出现一枚；车厢方向不翻转。
禁止: 文字、字幕、UI、二维码、水印、分屏、拼贴、九宫格、参考图入画、画中画、多个陆沉、多个空白晶片、露骨血腥。
```

### S01E01_SEG012_SHOT04

```text
镜头: S01E01_SEG012_SHOT04，16:9 单张电影关键帧。
引用图职责: 图1=陆沉身份参考，只参考脸、发型、服装、体态；图2=记忆核心场景参考，只参考空间结构、光线、材质和方向；图3=空白记忆晶片参考，只参考外形、比例、材质和当前发光状态；图4=上一段尾帧状态参考，只参考动作承接和构图方向。

承接上一镜头: 方舟外墙人群听见抽取室真实声音，真相正在外泄。
当前画面: 记忆核心红白交错的强光中，陆沉坐在核心接口前，眼神彻底空白，但嘴角保留一点笑；空白晶片悬在胸前，红色脉冲沿管道扩散。
角色/表演: 表情安静、疲惫、完成任务后的微弱释然；身体放松但像被掏空记忆。
为下一镜头承接: 方舟广播崩成噪声，外墙人群即将反应。

连续性锁点: 只出现一个陆沉；空白晶片只出现一枚；红色脉冲从核心向外扩散。
禁止: 文字、字幕、UI、二维码、水印、分屏、拼贴、九宫格、参考图入画、画中画、多个陆沉、多个晶片、露骨血腥、黑屏文字。
```



