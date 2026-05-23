# Asset Package Tables

Load this when building image/reference indexes, ordered keyframe upload plans, or a segment package before Seedance handoff. For still-image generation source records, use `references/imagegen-staging.md`. For formal video prompt and upload rules, use `references/seedance-2-handoff.md`.

## Contents

- [Scene Spatial Anchors](#scene-spatial-anchors)
- [Prop And Trace References](#prop-and-trace-references)
- [Ordered Keyframe Upload Plan](#ordered-keyframe-upload-plan)
- [Ordered Keyframe List](#ordered-keyframe-list)
- [Package Readiness Notes](#package-readiness-notes)

## Scene References

Each reusable or spatially important scene should keep a clean scene reference for formal video upload. Atlas or panorama files may remain in the project as internal planning/source material, but formal Seedance image slots should prefer a clean single scene reference.

```markdown
# 场景空间锚点清单

| 场景ID | 场景名称 | 干净场景参考 | 可选空间源图 | 用途 | 状态 | 上传优先级 | 备注 |
|---|---|---|---|---|---|---:|---|
| SCENE_ID | [场景名] | references/scenes/[scene]_CLEAN_REF.png | references/scenes/[scene]_OVERVIEW_SOURCE.png | 空间、材质、入口出口、行进方向、纵深关系 | 待生成/已确认可用/正式锁定/全季锁定 | 1 | 只作空间参考，不得生成九宫格、地图或拼贴画面 |
```

In video prompts, describe uploaded scene images as spatial-only references. The generated video must not show grids, diagrams, maps, contact sheets, picture-in-picture, or reference boards.

## Prop And Trace References

```markdown
# 道具与线索参考清单

| 参考ID | 类型 | 文件路径 | 状态 | 对应角色/场景/段落 | 必须保持 | 禁止变化 | 上传条件 | 备注 |
|---|---|---|---|---|---|---|---|---|
| REF_PROP_001 | 道具参考图 | references/props/[prop]_v01.png | 待确认/正式锁定/全季锁定 | SXXEXX_SEGXXX | [形状/材质/颜色/磨损/大小] | 不复制成多件；不改文字/符号；不变成其他物件 | 可见、手持、剧情关键、商品关键时必传 |  |
| REF_TRACE_001 | 线索/痕迹参考图 | references/traces/[trace]_v01.png | 待确认/正式锁定/全季锁定 | SXXEXX_SEGXXX | [脚印/尾光/残痕/损伤等] | 不生成额外异兽/人形/可读文字 | 线索推动剧情或镜头特写时必传 |  |
```

## Ordered Keyframe Upload Plan

```markdown
# 有序关键帧上传规划表

使用规则：

- 正式路线取消多宫格故事板，直接上传有序关键帧作为视频参考。
- 每个段落最多使用4个时序节拍锚点，固定对应 `SHOT01-SHOT04`。
- 首段上传最多4张已通过关键帧；后续段第一张上传上一段真实尾帧，其余最多上传3张已通过新关键帧。
- 关键帧只作为时间顺序和画面状态参考，不得提示模型生成分屏、拼贴、幻灯片或图片序列。
- 正式上传包默认7图软上限：时序帧/上一段尾帧优先，其次主角、当前干净场景、可见剧情关键道具/痕迹。超出时先把未来场景参考改为文字承接，再省略可选风格/补充参考、可由时序帧恢复的配角参考和非关键道具；当前场景参考最后才省略。

| 段落ID | 上传顺序 | 镜头ID | 时间点 | 构图/景别 | 画面动作 | 角色表演 | 镜头运动 | 音频提示 | 参考图 | 单帧提示词 | 风险 |
|---|---:|---|---|---|---|---|---|---|---|---|---|
| SXXEXX_SEGXXX | @图片1/@图片2/... | SHOT01/SHOT02/... | [来自分镜脚本] | [景别/机位] | [动作] | [表演] | [运动] | [@音频N/无] | [关键帧或上一段尾帧] | [单帧提示词路径] | [风险] |
```

## Ordered Keyframe List

```markdown
# 有序关键帧清单

使用规则：

- `来源镜号` 必须覆盖本段正式镜头：`SHOT01-SHOT04`。
- `使用参考图` 只写关键帧、上一段尾帧和锁定参考，不写审稿联系表。
- 只有所有待提交关键帧通过用户验收后，有序关键帧清单才能成为当前正式参考。

| 段落ID | 上传顺序清单 | 状态 | 来源镜号 | 镜头数 | 总时长 | 关键角色 | 场景 | 使用参考图 | 视频提示词 | 返修备注 |
|---|---|---|---|---:|---:|---|---|---|---|---|
| SXXEXX_SEGXXX | keyframes/00_有序关键帧上传清单.md | 待生成/SELF_CHECK_PASS/VISUAL_PASS/需返修 | SHOT01-SHOT04 | 4 | 15 | [角色] | [场景] | [上一段尾帧+已通过关键帧+必要锁定参考] | prompts/00_seedance多功能参考提示词.txt |  |
```

## Package Readiness Notes

- The package is not video-submit-ready until all active keyframes in the video scope are user-approved.
- Non-first segments need the previous processed video tail as `SHOT01` before formal video submission.
- Audio rows and upload copies come from `references/mimo-audio-handoff.md`.
- Formal video upload order, Seedance image cap, prompt structure, Seedan postprocess, and tail handoff are authoritative in `references/seedance-2-handoff.md`.
