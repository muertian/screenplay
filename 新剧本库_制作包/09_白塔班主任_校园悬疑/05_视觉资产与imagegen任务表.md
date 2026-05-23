# 《白塔班主任》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，校园悬疑 类型质感 |
| 色彩 | 校园冷雾、白塔石灰、晨光金 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读文字、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| BTT_REF_CHAR_001 | 角色参考 | references/characters/CHAR_MAIN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 梁知夏 主角身份、服装、表演锚点 |
| BTT_REF_CHAR_002 | 角色参考 | references/characters/CHAR_SUPPORT_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 周眠 关键配角身份和情绪状态 |
| BTT_REF_CHAR_003 | 角色参考 | references/characters/CHAR_FORCE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 校董会 反派/机制代言人的视觉锚点 |
| BTT_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_BTT_01.png | `$imagegen_builtin_image_gen` | 待生成 | 寄宿学校操场，无可读文字 |
| BTT_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_BTT_02.png | `$imagegen_builtin_image_gen` | 待生成 | 白塔楼梯，无可读文字 |
| BTT_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_BTT_03.png | `$imagegen_builtin_image_gen` | 待生成 | 证词教室，无可读文字 |
| BTT_REF_PROP_001 | 道具参考 | references/props/PROP_BTT_01.png | `$imagegen_builtin_image_gen` | 待生成 | 白塔钥匙，单一道具不复制 |
| BTT_REF_PROP_002 | 道具参考 | references/props/PROP_BTT_02.png | `$imagegen_builtin_image_gen` | 待生成 | 空课桌名牌，单一道具不复制 |
| BTT_REF_PROP_003 | 道具参考 | references/props/PROP_BTT_03.png | `$imagegen_builtin_image_gen` | 待生成 | 旧录音笔，单一道具不复制 |

## 关键帧规划
- 首段生成 BTT_SEG001_SHOT01-SHOT04 共4张。
- 后续段每段生成 `SHOT02-SHOT04`，`SHOT01` 等上一段真实尾帧。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。


