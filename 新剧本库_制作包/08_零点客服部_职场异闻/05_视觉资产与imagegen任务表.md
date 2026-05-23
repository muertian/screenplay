# 《零点客服部》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，职场异闻 类型质感 |
| 色彩 | 办公冷光、屏幕蓝、午夜红色工单 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读文字、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| ZKF_REF_CHAR_001 | 角色参考 | references/characters/CHAR_MAIN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 温岚 主角身份、服装、表演锚点 |
| ZKF_REF_CHAR_002 | 角色参考 | references/characters/CHAR_SUPPORT_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 许主管 关键配角身份和情绪状态 |
| ZKF_REF_CHAR_003 | 角色参考 | references/characters/CHAR_FORCE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 零点系统 反派/机制代言人的视觉锚点 |
| ZKF_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_ZKF_01.png | `$imagegen_builtin_image_gen` | 待生成 | 午夜客服大厅，无可读文字 |
| ZKF_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_ZKF_02.png | `$imagegen_builtin_image_gen` | 待生成 | 录音审听室，无可读文字 |
| ZKF_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_ZKF_03.png | `$imagegen_builtin_image_gen` | 待生成 | 断电办公楼，无可读文字 |
| ZKF_REF_PROP_001 | 道具参考 | references/props/PROP_ZKF_01.png | `$imagegen_builtin_image_gen` | 待生成 | 红色工单，单一道具不复制 |
| ZKF_REF_PROP_002 | 道具参考 | references/props/PROP_ZKF_02.png | `$imagegen_builtin_image_gen` | 待生成 | 降噪耳麦，单一道具不复制 |
| ZKF_REF_PROP_003 | 道具参考 | references/props/PROP_ZKF_03.png | `$imagegen_builtin_image_gen` | 待生成 | 话术手册，单一道具不复制 |

## 关键帧规划
- 首段生成 ZKF_SEG001_SHOT01-SHOT04 共4张。
- 后续段每段生成 `SHOT02-SHOT04`，`SHOT01` 等上一段真实尾帧。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。


