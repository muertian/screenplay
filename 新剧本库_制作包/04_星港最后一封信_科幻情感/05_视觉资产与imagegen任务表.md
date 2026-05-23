# 《星港最后一封信》视觉资产与imagegen任务表

本文件只规划静态参考图和关键帧任务，不生成图片。所有静态图任务必须使用 `$imagegen_builtin_image_gen`。

## 视觉方向

| 项目 | 内容 |
|---|---|
| 主风格 | 电影写实漫画，冷白深空设施，情感克制 |
| 色彩 | 冷白星港、深蓝宇宙、琥珀色家书投影 |
| 禁区 | 无字幕、无UI、无二维码、无水印、无可读文字、无露骨血腥 |

## 参考图任务

| 任务ID | 类型 | 文件建议 | provider | 状态 | 验收重点 |
|---|---|---|---|---|---|
| SGL_REF_CHAR_001 | 角色参考 | references/characters/CHAR_CENZHOU_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 31岁星际信使，深空制服，信箱 |
| SGL_REF_CHAR_002 | 角色参考 | references/characters/CHAR_LIAN_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 殖民地工程师，投影形态 |
| SGL_REF_CHAR_003 | 角色参考 | references/characters/CHAR_CENFATHER_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 老信使，救援服，温和 |
| SGL_REF_SCENE_001 | 场景参考 | references/scenes/SCENE_STARPORT_HALL_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 冷白空旷星港大厅 |
| SGL_REF_SCENE_002 | 场景参考 | references/scenes/SCENE_DELIVERY_ROOM_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 家书胶囊阵列，琥珀光 |
| SGL_REF_SCENE_003 | 场景参考 | references/scenes/SCENE_ORBIT_DECAY_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 星港坠落外景 |
| SGL_REF_PROP_001 | 道具参考 | references/props/PROP_LETTER_CAPSULE_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 家书胶囊，无文字标签 |
| SGL_REF_PROP_002 | 道具参考 | references/props/PROP_OLD_LETTER_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 旧信纸，文字不可读 |
| SGL_REF_PROP_003 | 道具参考 | references/props/PROP_DATA_BOX_v01.png | `$imagegen_builtin_image_gen` | 待生成 | 情感遗存数据盒 |

## 关键帧规划

- 首段生成 `SGL_SEG001_SHOT01-SHOT04`。
- 后续段每段生成 `SHOT02-SHOT04`。
- 全片计划关键帧37张；当前未生成、未验收、不可提交视频。

