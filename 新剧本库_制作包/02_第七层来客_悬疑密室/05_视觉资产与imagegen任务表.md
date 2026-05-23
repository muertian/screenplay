# 《第七层来客》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，潮湿老楼，幽闭走廊 |
| 色彩 | 冷绿电梯灯、暖黄门厅灯、灰黑雨夜 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读门牌/楼层数字、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| QLC_REF_CHAR_001 | 角色参考 | references/characters/CHAR_MENGWAN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 28岁插画师，疲惫，画筒 |
| QLC_REF_CHAR_002 | 角色参考 | references/characters/CHAR_BAIYU_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 失踪邻居，冷光半遮脸 |
| QLC_REF_CHAR_003 | 角色参考 | references/characters/CHAR_GUARD_CHEN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 一楼门卫，保温杯，回避眼神 |
| QLC_REF_CHAR_004 | 角色参考 | references/characters/CHAR_404_MAN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 中年男住户，手套，行李箱 |
| QLC_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_OLD_ELEVATOR_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 老电梯，无可读数字 |
| QLC_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_SEVENTH_CORRIDOR_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 冷绿第七层走廊，无门牌文字 |
| QLC_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_LOBBY_NOTICE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 门厅公告栏，照片但无可读文字 |
| QLC_REF_PROP_001 | 道具参考 | references/props/PROP_TAPE_RECORDER_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 旧录音机，无品牌字 |
| QLC_REF_PROP_002 | 道具参考 | references/props/PROP_SUITCASE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 深色行李箱，压迫感 |

## 关键帧规划

- 首段生成 `QLC_SEG001_SHOT01-SHOT04` 共4张。
- 后续段每段生成 `SHOT02-SHOT04`。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。

