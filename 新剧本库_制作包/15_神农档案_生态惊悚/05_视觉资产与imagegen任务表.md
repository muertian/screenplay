# 《神农档案》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，生态惊悚 类型质感 |
| 色彩 | 实验站冷绿、泥土黑、作物荧黄 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读文字、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| SND_REF_CHAR_001 | 角色参考 | references/characters/CHAR_MAIN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 许禾 主角身份、服装、表演锚点 |
| SND_REF_CHAR_002 | 角色参考 | references/characters/CHAR_SUPPORT_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 孟教授 关键配角身份和情绪状态 |
| SND_REF_CHAR_003 | 角色参考 | references/characters/CHAR_FORCE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 掩埋工程 反派/机制代言人的视觉锚点 |
| SND_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_SND_01.png | `$imagegen_builtin_image_gen` | 待生成 | 农业实验棚，无可读文字 |
| SND_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_SND_02.png | `$imagegen_builtin_image_gen` | 待生成 | 地下根系通道，无可读文字 |
| SND_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_SND_03.png | `$imagegen_builtin_image_gen` | 待生成 | 废弃村址，无可读文字 |
| SND_REF_PROP_001 | 道具参考 | references/props/PROP_SND_01.png | `$imagegen_builtin_image_gen` | 待生成 | 根系样本盒，单一道具不复制 |
| SND_REF_PROP_002 | 道具参考 | references/props/PROP_SND_02.png | `$imagegen_builtin_image_gen` | 待生成 | 旧土壤档案，单一道具不复制 |
| SND_REF_PROP_003 | 道具参考 | references/props/PROP_SND_03.png | `$imagegen_builtin_image_gen` | 待生成 | 荧光麦穗，单一道具不复制 |

## 关键帧规划
- 首段生成 SND_SEG001_SHOT01-SHOT04 共4张。
- 后续段每段生成 `SHOT02-SHOT04`，`SHOT01` 等上一段真实尾帧。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。


