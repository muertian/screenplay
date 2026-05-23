# 《雨夜回声》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，雨夜都市，霓虹反光 |
| 色彩 | 冷蓝雨夜、红色保温灯、电话亭冷白光 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无车牌/品牌/号码、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| RYE_REF_CHAR_001 | 角色参考 | references/characters/CHAR_XURAN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 25岁外卖员，雨衣，头盔，疲惫 |
| RYE_REF_CHAR_002 | 角色参考 | references/characters/CHAR_XIAOMAN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 夜班护士，白伞，制服外套 |
| RYE_REF_CHAR_003 | 角色参考 | references/characters/CHAR_BLACK_CAR_DRIVER_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 雨夜司机，焦躁，普通人 |
| RYE_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_RAIN_PHONE_BOOTH_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 废弃电话亭，无号码文字 |
| RYE_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_RAIN_CROSSROAD_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 雨夜路口，霓虹，车灯 |
| RYE_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_MORNING_STREET_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 雨后清晨街道 |
| RYE_REF_PROP_001 | 道具参考 | references/props/PROP_DELIVERY_BOX_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 无品牌外卖箱，保温灯裂开 |
| RYE_REF_PROP_002 | 道具参考 | references/props/PROP_PHONE_RECEIVER_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 老式听筒，无号码 |
| RYE_REF_PROP_003 | 道具参考 | references/props/PROP_WHITE_UMBRELLA_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 小满白伞 |

## 关键帧规划

- 首段生成 `RYE_SEG001_SHOT01-SHOT04`。
- 后续段每段生成 `SHOT02-SHOT04`。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。

