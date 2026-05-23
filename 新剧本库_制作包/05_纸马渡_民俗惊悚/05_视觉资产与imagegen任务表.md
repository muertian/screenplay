# 《纸马渡》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，湿冷山村，民俗仪式感 |
| 色彩 | 纸扎白、红烛光、黑水河、青灰石板 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读符纸/牌匾、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| PMD_REF_CHAR_001 | 角色参考 | references/characters/CHAR_SHENYAN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 29岁民俗摄影师，相机，疲惫 |
| PMD_REF_CHAR_002 | 角色参考 | references/characters/CHAR_FATHER_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 纸扎匠父亲，温和苍老 |
| PMD_REF_CHAR_003 | 角色参考 | references/characters/CHAR_APO_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 渡口守灯阿婆，红灯 |
| PMD_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_QINGSHI_VILLAGE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 湿冷青石村夜路 |
| PMD_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_PAPER_SHOP_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 纸扎铺，红烛，白纸马 |
| PMD_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_BLACK_RIVER_FERRY_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 黑水河渡口，雾，灯火 |
| PMD_REF_PROP_001 | 道具参考 | references/props/PROP_PAPER_HORSE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 白纸马，红眼，非怪物化 |
| PMD_REF_PROP_002 | 道具参考 | references/props/PROP_RED_LANTERN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 红灯，手持比例 |
| PMD_REF_PROP_003 | 道具参考 | references/props/PROP_CAMERA_RELIC_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 破碎相机，无品牌文字 |

## 关键帧规划

- 首段生成 `PMD_SEG001_SHOT01-SHOT04`。
- 后续段每段生成 `SHOT02-SHOT04`。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。

