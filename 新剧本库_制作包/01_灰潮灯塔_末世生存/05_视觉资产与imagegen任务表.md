# 《灰潮灯塔》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，低饱和末世海港，强阴影 |
| 色彩 | 灰绿色毒潮、冷白灯塔光、锈橙警报灯 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读文字、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| HLT_REF_CHAR_001 | 角色参考 | references/characters/CHAR_LINCHE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 37岁维修员，腿伤，灰绿防水外套 |
| HLT_REF_CHAR_002 | 角色参考 | references/characters/CHAR_AYAO_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 12岁灰潮孤儿，红绳，防潮披肩 |
| HLT_REF_CHAR_003 | 角色参考 | references/characters/CHAR_QI_STATION_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 温和冷感站长，洁白控制站制服 |
| HLT_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_GREY_STREET_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 灰潮吞街，废公交，远处灯塔光 |
| HLT_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_LIGHTHOUSE_HALL_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 空旷洁白灯塔大厅，接入椅 |
| HLT_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_LIGHT_CORE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 灯芯室、光管、导光核心 |
| HLT_REF_PROP_001 | 道具参考 | references/props/PROP_WORK_BADGE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 旧工牌，文字不可读 |
| HLT_REF_PROP_002 | 道具参考 | references/props/PROP_RED_ROPE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 阿遥红绳，唯一性强 |
| HLT_REF_PROP_003 | 道具参考 | references/props/PROP_LIGHTHOUSE_LOG_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 旧维修日志，封面文字不可读 |

## 关键帧规划

- 首段生成 `HLT_SEG001_SHOT01-SHOT04` 共4张。
- 后续段每段生成 `SHOT02-SHOT04`，`SHOT01` 等上一段真实尾帧。
- 全片计划关键帧：37张。
- 当前状态：未生成，未验收，不可提交视频。

