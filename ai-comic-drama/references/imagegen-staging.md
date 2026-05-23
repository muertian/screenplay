# Imagegen Staging And Source Records

Load this when preparing still images, visual references, keyframes, or any generated image that may enter review, locked assets, upload packages, or manifests.

## Contents

- [Core Rules](#core-rules)
- [Character Reference Default](#character-reference-default)
- [Keyframe Prompt Continuity Rule](#keyframe-prompt-continuity-rule)
- [Image Asset Register](#image-asset-register)
- [Image Generation Task Table](#image-generation-task-table)
- [Codex Imagegen Source Record](#codex-imagegen-source-record)
- [Promotion Checklist](#promotion-checklist)

## Core Rules

- Still-image generation, edits, retakes, character/scene/prop references, and keyframes must use `$imagegen` with the built-in `image_gen` route.
- Do not use Dreamina/即梦, Seedance, ChatGPT Web, OpenAI SDK one-off scripts, or any other image provider for generated still images in this skill. User-provided reference images may still be used as references, but newly generated or retaken stills must come from `$imagegen`.
- Visual references must be actually loaded into the current imagegen context. Prompt-only filenames, paths, or asset IDs do not count as reference binding.
- Generated images first land in tool output or a temporary cache, then must be copied into project-local `imagegen_staging/`, then promoted into the final project folder only after review.
- Do not place global `.codex/generated_images` paths directly into current manifests or upload packages.
- Every promoted image needs a source record with selected source, staged path, final path, hashes, tool, prompt path/summary, and loaded reference list.
- Locked images are never overwritten in place. Create a new version, update indexes after acceptance, and retire the old version explicitly.
- One image task should produce one clear asset: character reference, clean scene reference, keyframe, prop reference, trace reference, or previous-tail frame.
- Scene references used for formal video should be clean single scene images whenever possible. Atlases, maps, contact sheets, review pages, and panoramas may remain as internal planning/source material, but they should not be uploaded as formal Seedance refs.
- Keyframe prompts use a small, explicit reference set. Each reference image must have one job, and each keyframe prompt must include a previous-state handoff, current action, and next-shot handoff.

## Character Reference Default

Unless the user provides a newer approved character-reference style, all new or retaken character reference images must follow the current project's approved protagonist reference format:

- 16:9 horizontal, single-character multi-view reference sheet.
- Left side: same character in front full body, side full body, and back full body.
- Right side: same character's face/hair closeups plus wardrobe, hand/glove, bag, weapon/tool, implant, or signature equipment detail panels as applicable.
- Background: pure white or near-white seamless studio background only; no story location, wall, street, city, floor texture, signage, or environmental narrative.
- Visual style: match the current project's approved protagonist reference style and visual bible; do not import a past project's world, palette, costume language, or character identity.
- Quality: clean, clear asset reference; low noise and low grain; sharp silhouettes and material details; use large readable light/shadow blocks instead of random particles.
- Entity rule: this is one character shown from several reference angles, not multiple people; keep face, hair, body silhouette, wardrobe, and props consistent across all views.
- Identity role: use this clean reference as the character's main identity source. Do not use dark, dirty, action-heavy story keyframes as the primary identity reference unless the user explicitly approves that exception.
- Ban text, subtitles, UI, labels, arrows, numbers, watermarks, readable signs/logos, QR codes, storyboard panels, scene action, extra characters, face swap, age drift, outfit drift, and real-actor likeness.

## Keyframe Prompt Continuity Rule

Use this as the sole current rule for all formal keyframe still images and retakes intended for review or video upload packages. Keep image references few and clear; adding more references is not automatically more stable.

### Reference Roles

Use a small reference set and assign one clear job to each image. Default 4-reference formula when available:

```text
图1 = character_identity_ref: main character identity only.
图2 = current_scene_ref: current location only.
图3 = visible_core_prop_ref: visible core prop only.
图4 = previous_state_ref: previous shot/tail continuity only.
```

Full priority order:

1. `character_identity_ref`: controls face, hair, wardrobe, body silhouette, and signature wearable details only.
2. `current_scene_ref`: controls the current shot's geography, lighting, materials, screen direction, and camera-safe space.
3. `visible_core_prop_ref`: controls the visible story-critical prop's shape, scale, material, and current state.
4. `previous_state_ref`: controls continuity from the previous shot or previous accepted tail frame: pose, position, screen direction, and active prop state.
5. `supporting_character_ref`: controls a supporting character only when that character is prominent and cannot be recovered from temporal keyframes.
6. `style_ref`: controls palette, texture, and finish only when the project style is not already locked.
7. `future_scene_ref`: avoid for current-shot keyframes unless the character has already entered that scene. Usually describe the future scene only as a next-shot handoff in text.

Default priority:

```text
character_identity_ref > current_scene_ref > visible_core_prop_ref > previous_state_ref > supporting_character_ref > style_ref > future_scene_ref
```

Do not mix role types inside one reference image for formal production. Do not use review pages, contact sheets, storyboard boards, UI screenshots, maps, nine-grid atlases, multi-view prop sheets, or future-location references as if they were current-shot images.

### Keyframe Prompt Shape

Every formal keyframe prompt should include these blocks in this order:

```text
镜头: [segment + shot id], 16:9 单张电影关键帧。
引用图职责: 图1=..., 图2=..., 图3=...。每张引用图只按指定职责使用。

承接上一镜头: [上一镜头的人物位置、动作方向、道具状态、空间方向]
当前画面: [景别/机位 + 主体动作 + 关键身体部位 + 道具状态 + 场景互动]
角色/表演: [脸、眼神、手、肩、腿、姿态、力度、速度]
为下一镜头承接: [下一动作的预备姿态、尾帧钩子、空间出口或道具状态]

连续性锁点: [只出现一个主角；单一道具只出现一个；场景方向不翻转；配角/载具关系不变]
禁止: 文字、字幕、UI、二维码、水印、分屏、拼贴、九宫格、参考图入画、画中画、多实体重复。
```

### Writing Rules

- Write the current shot, not the whole scene. Put only the necessary identity, geography, prop state, and action in the prompt.
- Keep the prompt short and structured: purpose, subject, action, location, visual style, and limits. Avoid adjective piles or repeating the same lock in several places.
- Describe action through body parts and measurable motion: hands, shoulders, head, legs, gaze, weight shift, speed, force, and direction.
- Preserve screen direction across adjacent shots. If a chase moves rightward, keep the runner, pursuer, exits, and hazards in the same spatial relationship unless the script calls for a turn.
- Use the previous accepted frame or tail frame as a state reference when continuity matters, but do not demand pixel-perfect copying unless the generation mode supports it.
- If a future location is only a destination, describe it in the next-shot handoff instead of uploading it as a reference image.
- For retakes, change one variable at a time: reference set, action, pose, camera, prop state, or lighting. Do not change all of them in one prompt unless the previous version is unusable.

### Minimal Keyframe Prompt

```text
镜头: SXXEXX_SEGXXX_SHOTXX, 16:9 单张电影关键帧。
引用图职责: 图1=主角身份参考，只参考脸、发型、服装、体态；图2=当前场景参考，只参考空间结构、光线、材质和方向；图3=核心道具参考，只参考外形、比例、材质和当前状态；图4=上一镜头状态参考，只参考动作承接和构图方向。

承接上一镜头: [上一动作状态、人物位置、道具状态、空间方向]。
当前画面: [景别和主体动作]。
角色/表演: [身体部位、表情、力度、速度]。
为下一镜头承接: [下一动作预备姿态或尾帧钩子]。

连续性锁点: 主角只出现一个真实实体；核心道具只出现一个并保持在正确身体部位/位置；场景方向不翻转。
禁止: 文字、字幕、UI、二维码、水印、分屏、拼贴、九宫格、参考图入画、画中画、多个主角、多个单一道具。
```

## Image Asset Register

```markdown
# 图片资产清单

使用规则：

- 只登记项目本地路径或已确认/锁定资产路径；不要把全局 `.codex/generated_images` 缓存路径作为当前资产。
- 每张图必须有类型、用途、版本、状态和来源段落/场景。
- `小样锁定`、`正式锁定`、`全季锁定` 图不得原地覆盖；返修生成新版本。

| 图片ID | 文件路径 | 状态 | 类型 | 质量档位 | 用途 | 来源段落/场景 | 正向提示词 | 负向提示词 | 参考素材 | 连续性备注 | 版本 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| IMG_SXXEXX_SEGXXX_SHOTXX | keyframes/SXXEXX_SEGXXX_SHOTXX_v01.png | 待生成/已生成-待确认/已确认可用/小样锁定/正式锁定/全季锁定/需返修 | 关键帧/角色参考图/场景俯视图/场景多视角图/场景全景图/道具参考图/线索参考图/上一段尾帧 | draft/pilot/final | [关键帧验收/上传包/锁定参考] | SXXEXX_SEGXXX_SHOTXX | [提示词路径或摘要] | [画面禁区] | [角色/场景/道具/上一段尾帧] | [接上一段尾帧/保持方向] | v01 |
```

## Image Generation Task Table

```markdown
# 生图任务表

使用规则：

- 每个任务只生成一个明确资产，不把角色参考、场景参考、关键帧混成一个任务。
- 任务完成后必须进入 `$imagegen内置生图记录`，再从 staging 晋升到正式资产目录。
- 关键帧任务必须对应分镜表里的 `段落ID + 镜头ID`。

| 任务ID | 图片ID | 类型 | 质量意图 | 目标比例 | 保存目录 | 推荐文件名 | 依赖参考 | 可复制提示词 | 验收标准 | 状态 | 返修提示词 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| GEN_IMG_001 | IMG_SXXEXX_SEGXXX_SHOTXX | 关键帧 | final keyframe for user approval | 16:9 | keyframes/ | SXXEXX_SEGXXX_SHOTXX_v01.png | [角色/场景/道具/上一段尾帧] | [完整提示词或路径] | 单张电影画面；动作清楚；无文字；不重复人物/道具 | 待生成 |  |
```

## $imagegen Source Record

```markdown
# $imagegen内置生图记录

使用规则：

- `$imagegen` built-in `image_gen` 输出先记 `默认输出路径`，再复制到项目本地 `imagegen_staging/`，最后晋升到正式目录。
- `工具` 必须记录为 `$imagegen_builtin_image_gen`；其他静态图生成工具不得晋升为当前关键帧、锁定参考或上传包图片。
- 记录 source/staging/final 三段路径和验收状态，防止误用其他项目或全局缓存图。

| 任务ID | 图片ID | 类型 | 工具 | 质量意图 | 提示词 | 默认输出路径 | Staging路径 | 最终保存路径 | 已加载参考 | 哈希 | 验收标准 | 状态 | 返修备注 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GEN_IMG_001 | IMG_SXXEXX_SEGXXX_SHOTXX | 关键帧 | $imagegen_builtin_image_gen | 用户验收用正式关键帧 | [提示词路径或摘要] | [.codex/generated_images/...] | imagegen_staging/[date_scope]/... | keyframes/... | [实际加载的参考图路径列表] | sha256:... | [验收标准] | 已生成-待确认/已确认可用/需返修 |  |
```

## Promotion Checklist

Before an image is promoted into a keyframe review pack, locked reference, upload package, or current manifest, confirm:

- the final path is project-local;
- the source record tool is `$imagegen_builtin_image_gen`;
- the source/staging/final paths are recorded;
- the prompt and negative constraints are recoverable;
- all loaded visual references are listed;
- the image does not duplicate named characters, single creatures, single props, or forbidden background figures;
- scene assets intended for video have a clean single scene reference when the scene is reusable or spatially important.
