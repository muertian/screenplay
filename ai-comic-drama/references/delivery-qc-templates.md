# Delivery And QC Templates

## Contents

- [Seedance2.0多功能参考生成交付表](#seedance20多功能参考生成交付表)
- [Seedance正式上传清单](#seedance正式上传清单)
- [样片验证与返修记录](#样片验证与返修记录)
- [最终成片质量检查表](#最终成片质量检查表)
- [每集视频归档表](#每集视频归档表)
- [成片组装与导出](#成片组装与导出)
- [Seedance上传包自动检查报告](#seedance上传包自动检查报告)
- [批量生产总控表](#批量生产总控表)
- [返修策略库](#返修策略库)
- [黄金样片基线](#黄金样片基线)
- [大规模创作前确认表](#大规模创作前确认表)
- [用户原始素材整合清单](#用户原始素材整合清单)
- [连续性测试方案](#连续性测试方案)
- [连续性测试记录表](#连续性测试记录表)
- [连续性锁点表](#连续性锁点表)
- [锁定资产保护规则](#锁定资产保护规则)
- [工具脚本](#工具脚本)

Formal video route, Dreamina/即梦 CLI execution, upload order, Seedance image cap, prompt structure, Seedan `1080p -> 60fps`, and tail-frame handoff are authoritative in `references/seedance-2-handoff.md`. Keep this file focused on tables, QC records, archive fields, and delivery evidence.

## Seedance2.0多功能参考生成交付表

```markdown
# Seedance2.0多功能参考生成交付表

| 段落ID | 集/场 | 时长 | 镜头数 | 比例 | 模式 | 上一段尾帧/SHOT01 | 有序关键帧 | 人物参考 | 场景参考 | 道具参考 | @图片映射 | @音频映射 | Seedance提示词 | 尾帧输出 | 备注/重生成策略 |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|
```

本表只登记交付字段。正式视频路线以 `references/seedance-2-handoff.md` 为准：`keyframe_multiref_seedance`、`execution_provider: dreamina_cli`、15秒单元、有序关键帧、非首段真实尾帧/SHOT01、Seedance 9图上限、Seedan `1080p -> 60fps` 后处理和尾帧交接都不要在本表另写一套规则。批量生产阶段只准备关键帧、提示词、上传包、manifest和检查报告，并可标记 `READY_FOR_VIDEO_SUBMIT`；不进入 `dreamina` CLI 提交、排队、下载或抽尾帧。若非首段缺少或无法确认上一段真实尾帧，暂时不要生成视频；只准备可预构建材料并标记 `视频阻塞-缺上一段尾帧`。

```text
【参考内容说明】@图片1-@图片4 是本段4个时间顺序画面锚点：首段使用已验收关键帧，非首段@图片1使用上一段真实尾帧并对应SHOT01，@图片2-@图片4对应本段SHOT02-SHOT04。这些关键帧只用于理解15秒连续视频的时间顺序、画面状态和动作节拍，不要生成分屏、漫画格、幻灯片或图片序列；被省略关键帧的剧情只能合并进相邻SHOT文字，不要引用被省略图片。后续@图片是[角色/场景/道具]参考图；场景参考使用干净单张场景图，避免九宫格、拼贴、地图、审稿页或带文字图片。@音频1 是[角色]台词：“[台词]”。

请生成一段16:9、15秒、单一连续镜头/连续剪辑的视频：[按固定4镜头分镜顺序写SHOT01动作]；[写SHOT02动作]；[写SHOT03动作]；[写SHOT04动作并自然收束]。保持[角色]脸、发型、服装、道具、场景空间、光线、运动方向和上一段尾帧状态一致。不要分屏、不要漫画格、不要字幕、不要新增无关角色、不要改脸、不要改服装、不要改道具。

不要在视频画面中出现文字信息。
```

上传用提示词应保持为可直接复制到 Seedance 的纯提示词，文件名映射放在上传清单和交付表中。

正式 Seedance 生成直接上传有序关键帧作为参考，不生成也不上传多宫格故事板。不得上传连续性对照图、验收联系表、带编号/文字的拼贴图或审稿用联系表。

## Seedance正式上传清单

```markdown
# Seedance正式上传清单

## 使用规则

- 每个15秒段落在本清单中只保留一个当前上传包入口。
- 正式上传包遵守 `references/seedance-2-handoff.md` 的 `keyframe_multiref_seedance` 规则：固定4帧时间锚点、上一段尾帧/SHOT01、最多3张新关键帧、人物参考、干净场景参考、必要道具参考、Mimo音频、提示词；正式上传优先7图以内，绝不超过9图。
- 非首段缺少或无法确认上一段真实尾帧时，不得上传或生成视频；该段状态写为 `视频阻塞-缺上一段尾帧`。
- 历史测试包只作追溯，不进入当前上传清单。
- 提示词最后一句固定为：`不要在视频画面中出现文字信息。`

## 段落上传包

| 段落ID | 上传文件夹 | 分镜剧情描述 | 分镜完整提示词 |
|---|---|---|---|

## 逐项上传顺序

| 段落ID | 上传顺序 | 打开文件夹 | Web引用标签 | 上传文件 | 素材类型 | 用途 | 是否已上传 | 分镜剧情描述 | 分镜完整提示词 | 备注 |
|---|---:|---|---|---|---|---|---|---|---|---|
```

For each current multi-reference package, include:

```json
{
  "schema_version": 1,
  "route": "keyframe_multiref_seedance",
  "execution_provider": "dreamina_cli",
  "segment_id": "SXXEXX_SEGXXX",
  "duration": 15,
  "previous_tail_frame": {"path": "boundary/图片1_上一段尾帧.png", "sha256": "..."},
  "tail_frame_gate": "required_for_non_first_segments; block_video_if_missing",
  "keyframe_references": [
    {"shot_id": "SHOT02", "path": "keyframes/图片2_SHOT02关键帧.png", "upload_slot": "@图片2", "approved": true, "sha256": "..."},
    {"shot_id": "SHOT03", "path": "keyframes/图片3_SHOT03关键帧.png", "upload_slot": "@图片3", "approved": true, "sha256": "..."}
  ],
  "character_refs": [],
  "scene_refs": [
    {"scene_id": "SCENE_ID", "kind": "clean_scene_ref", "path": "references/scenes/图片X_SCENE_ID_CLEAN_REF.png", "upload_slot": "@图片X", "sha256": "..."}
  ],
  "prop_refs": [],
  "audio_for_video": [],
  "prompt_path": "prompts/00_seedance多功能参考提示词.txt",
  "tail_frame_path": null,
  "status": "draft"
}
```

## 样片验证与返修记录

```markdown
# 第X季样片验证与返修记录

## 样片基线

| 项目 | 内容 |
|---|---|
| 样片段落 |  |
| 目标时长 | 默认15秒，例外必须记录，绝不超过15秒 |
| 画幅 |  |
| 核心验证目标 |  |
| 当前基线状态 | 素材已准备 / Seedance待生成 / 已通过 / 需返修 |

## 当前使用素材

| 类型 | 文件 | 状态 | 验收重点 |
|---|---|---|---|

## Seedance实机验证记录

| 轮次 | 日期 | 使用上传包 | 使用提示词 | 输出视频 | 结果 | 问题 | 返修动作 | 是否锁定 |
|---|---|---|---|---|---|---|---|---|

## 验收标准

| 维度 | 通过标准 | 常见返修动作 |
|---|---|---|
```

## 最终成片质量检查表

```markdown
# 第X季最终成片质量检查表

| 段落ID | 分镜顺序 | 原始下载视频 | 每集顺序视频 | 首帧匹配 | 尾帧匹配 | 角色稳定 | 场景稳定 | 动作清晰 | 音频可用 | 无随机文字/水印 | 戏剧价值 | 结论 | 返修动作 |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
```

## 每集视频归档表

```markdown
# 第X季每集视频归档表

规则：生成并下载完成后，保留 Seedance 原始下载文件；再用 Seedan 免费功能先把分辨率提升到 `1080p`，然后把刷新率/帧率提升到 `60fps`。`1080p/60fps` 文件是当前可检查版本，再复制/移动到对应集文件夹。每集一个文件夹，文件名按分镜段落顺序排序。

默认目录：

- `assets/07_视频分段/Seedance原始下载/<submit_id>/<raw_video>.mp4`
- `assets/07_视频分段/Seedan后处理/<submit_id>/<segment>_1080p.mp4`
- `assets/07_视频分段/Seedan后处理/<submit_id>/<segment>_1080p_60fps.mp4`
- `assets/07_视频分段/SXXEXX_第XX集/SXXEXX_SEG001_v01.mp4`
- `assets/07_视频分段/SXXEXX_第XX集/SXXEXX_SEG002_v01.mp4`

| 集数 | 段落ID | 分镜顺序 | submit_id | 原始下载路径 | Seedan 1080p路径 | Seedan 60fps路径 | 每集顺序视频路径 | 版本 | 当前状态 | 是否唯一当前版本 | 备注 |
|---|---|---:|---|---|---|---|---|---|---|---|---|
| SXXEXX | SXXEXX_SEG001 | 1 |  |  |  |  | assets/07_视频分段/SXXEXX_第XX集/SXXEXX_SEG001_v01.mp4 | v01 | 待确认 | 是/否 |  |

命名规则：`SXXEXX_SEGXXX_v01.mp4`；返修为 `_v02`、`_v03`。同一个段落只能有一个当前版本，旧版必须移动到 `99_旧版备份/视频分段/` 或在清单中标记为 `已被v2替代`。
```

## 成片组装与导出

Use this only after the needed segment videos are approved/current and post-production audio assets are available. This is a post-production assembly stage, not a Seedance prompt or submit stage.

Assembly rules:

- Assemble all approved/current segment videos in storyboard and timeline order.
- Add narration/voiceover tracks from `audio_for_postmix/` at their timeline positions; do not retroactively write narration text into Seedance video prompts.
- Add BGM and sound effects as post-production tracks when the project calls for them. Keep Seedance prompts at `no music` unless model-generated music was explicitly requested.
- Preserve the approved segment order, current-version paths, raw/Seedan provenance, and tail-frame handoff records.
- When the edit is ready, guide the user to export the assembled episode/sequence. Do not submit or re-submit Seedance video from this stage unless the user explicitly starts a video submit/retake task.

```markdown
# 第X季第X集成片组装表

| 时间轴顺序 | 段落ID | 当前视频版本 | 视频路径 | 旁白/对白后期音轨 | BGM/音效 | 起点状态 | 终点状态 | QC状态 | 备注 |
|---:|---|---|---|---|---|---|---|---|---|
```

## Seedance上传包自动检查报告

```markdown
# Seedance上传包自动检查报告

| 项目 | 内容 |
|---|---|
| 检查时间 |  |
| 上传包 |  |
| 结果 | 通过 / 通过-有警告 / 未通过 |
| 错误数 |  |
| 警告数 |  |
| 通过项 |  |

## 错误

## 警告

## 通过项
```

When there are multiple upload packages, use segment-specific report filenames such as `24_第X季_Seedance上传包自动检查报告_SEGXXX_v2.md` rather than overwriting one generic report.

## 批量生产总控表

```markdown
# 第X季批量生产总控表

| 段落ID | 集/场 | 时长 | 剧本状态 | 分镜状态 | 单元状态 | 角色音频 | 旁白/音效 | 角色参考 | 场景参考 | 道具参考 | 有序关键帧 | 上一段尾帧 | 上传包 | 自动检查 | 待视频提交状态 | 返修次数 | 锁定状态 | 当前阻塞 | 下一步 |
|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---:|---|---|---|
```

状态建议：`待生成`、`生成中`、`已生成-待确认`、`已确认可用`、`READY_FOR_VIDEO_SUBMIT`、`小样锁定`、`正式锁定`、`全季锁定`、`需返修`、`已被v2替代`、`非当前`、`暂缓`、`视频阻塞-缺上一段尾帧`。
批量生产总控表不记录实际 `dreamina` CLI 提交、排队、下载或尾帧提取结果。若需要视频执行，另建 `视频提交执行表` 或使用 `每集视频归档表`。
历史测试包或错误包标为 `非当前`，并从当前上传清单与相对路径索引中移除。

## 返修策略库

```markdown
# 第X季返修策略库

| 问题ID | 问题类型 | 典型症状 | 可能原因 | 优先返修动作 | 提示词调整 | 素材调整 | 是否需要重跑音频 | 是否需要拆分段落 | 适用段落 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
```

返修原因分类建议：

| 优先级 | 问题类型 | 默认处理 |
|---|---|---|
| P0 | 时长超过15秒、非首段缺真实尾帧、提示词末句缺失、关键帧未验收就提交、包内引用文件缺失 | 阻塞提交，先修包或拆段 |
| P0 | 人物身份漂移、唯一道具复制/丢失、参考图/拼贴/文字/UI入画 | 回到关键帧或视频提示词修正，必要时重做源帧/道具纯参考 |
| P0 | 相邻段首尾帧不连、场景方向反转、动作因果断裂 | 校正上一段尾帧引用、重做有序关键帧映射和待提交包；视频重跑属于单独视频执行阶段 |
| P1 | 剧情张力不足、镜头没有目标/障碍/转折、钩子弱 | 先修分镜脚本，再重做关键帧/视频 |
| P1 | 15秒单元不是固定4镜头、节奏失衡、动作过满 | 调整为4个SHOT并合并多余动作节拍 |
| P1 | 口型/音频错位、对白情绪不对、环境声压住对白 | 重做音频映射或Mimo行，必要时只重跑音频/视频 |
| P2 | 画面质感弱、镜头语言平、光色不够统一 | 先改风格/镜头提示词，保留已通过锁点 |
| P2 | 命名、归档、manifest、检查报告不规范 | 不重跑媒体，修元数据和文件夹 |

返修范围选项：`脚本重写`、`关键帧重生`、`上传映射/提示词重建`、`视频重跑`、`音频重跑`、`只修manifest/归档`。每次返修必须记录原因分类、影响范围和是否生成新版本。

## 黄金样片基线

```markdown
# 第X季黄金样片基线

## 基线结论

| 项目 | 内容 |
|---|---|
| 黄金样片段落 | SXXEXX_SEGXXX |
| 确认日期 | YYYY-MM-DD |
| 验收结论 | 通过/需返修 |
| 用户反馈 | [用户原话或简述] |
| 使用范围 | 后续15秒段落的角色、音频、画面、上传包和提示词基线 |

## 锁定素材

| 类型 | 文件/文件夹 | 状态 | 使用规则 |
|---|---|---|---|
| Seedance上传包 | [上传包路径] | 正式锁定 | 后续上传包沿用同样命名和提示词结构 |
| 完整提示词 | [00_完整提示词.txt] | 正式锁定 | 上传用提示词从 `【参考内容说明】` 开始 |
| 自动检查报告 | [检查报告路径] | 已通过 | 后续每个上传包都必须检查 |
| 角色参考图 | [角色参考图路径] | 正式锁定/全季锁定 | 后续角色画面优先引用 |
| 有序关键帧 | [keyframes路径/清单] | 已确认可用 | 作为15秒4帧动作节拍参考 |
| 上一段尾帧 | [尾帧路径] | 已确认可用 | 作为下一段开始画面参考 |
| 角色音色标准 | [音色标准路径] | 正式锁定/全季锁定 | 后续角色对白/OS/反应音以此为参考 |
```

## 大规模创作前确认表

## 用户原始素材整合清单

```markdown
# 第X季用户原始素材整合清单

使用时机：用户已经提供小说、大纲、剧本、人物参考图、场景图、风格图、音频或视频素材时，先做本清单，再进入改编、分镜、生图或视频生产。

总原则：用户提供素材优先。保留原始文件，不覆盖、不改名破坏来源；如需整理到项目目录，创建副本并记录原始路径。只有在素材缺失、质量不够或与已锁定资产冲突时，才提出补生成或返修建议。

| 素材ID | 原始文件/来源 | 项目副本路径 | 类型 | 对应角色/场景/集/段 | 状态 | 是否正本 | 质量/可用性 | 冲突/缺口 | 下一步 |
|---|---|---|---|---|---|---|---|---|---|
| SRC001 |  |  | 小说/大纲/剧本/角色图/场景图/风格图/音频/视频 |  | 待确认 | 是/否 |  |  |  |

状态选项：`待确认`、`当前草案可用`、`已确认可用`、`小样锁定`、`正式锁定`、`全季锁定`、`需返修`、`缺失`、`明确跳过`。
类型建议：`小说`、`剧本大纲`、`分集梗概`、`完整剧本`、`人物参考图`、`服装/道具参考图`、`场景俯视图`、`场景参考图`、`视觉风格参考`、`音频参考`、`视频参考`。
```

```markdown
# 第X季大规模创作前确认表

使用时机：进入整集/整季剧本分镜、大量生图、批量上传包生产、批量生产或并行agent前。大量视频提交不属于批量生产，需单独建 `视频提交/下载` 运行设置。

规则：`待确认`、`需返修` 或 `缺失` 的锚点会阻塞依赖它的批量工作。只能继续小样、局部测试或返修；不能大面积生成后再补救。

| 锚点 | 当前文件/资产 | 状态 | 确认结论 | 阻塞范围 | 下一步 |
|---|---|---|---|---|---|
| 用户原始素材整合清单 |  | 待确认 |  | 所有下游改编、分镜、资产生产 |  |
| 小说/剧情基线 |  | 待确认 |  | 整季剧本、分镜、批量生产 |  |
| 集纲/节拍图 |  | 待确认 |  | 每集剧本、钩子、时长 |  |
| 主要角色参考图 |  | 待确认 |  | 角色关键帧、批量生图、视频生成 |  |
| 重要配角参考图 |  | 待确认 |  | 相关集/场视频生成 |  |
| $imagegen生图链路/source record |  | 待确认 |  | 角色/场景/道具参考图、关键帧、返修图、上传包图片 |  |
| 核心场景俯视图 |  | 待确认 |  | 场景关键帧、空间连续性 |  |
| 核心场景参考图 |  | 待确认 |  | 批量生图、视频生成 |  |
| 视觉风格圣经 |  | 待确认 |  | 所有视觉生成 |  |
| 角色音色标准/音频策略 |  | 待确认 |  | 对白密集段落、最终成片 |  |
| Seedance链路/模型/成本策略 |  | 待确认 |  | 付费视频提交 |  |
| 即梦CLI执行状态 |  | 待确认 |  | 付费视频提交/查询/下载 |  |
| 黄金样片/连续性测试 |  | 待确认 |  | 批量上传包生产 |  |

状态选项：`待确认`、`当前草案可用`、`已确认可用`、`小样锁定`、`正式锁定`、`全季锁定`、`需返修`、`缺失`、`明确跳过`。
```

## 连续性测试方案

```markdown
# 第X季连续性测试方案

## 测试目的

- 图片素材连续性：同一角色、同一场景、同一道具在不同关键帧、尾帧和场景参考图中是否稳定。
- 视频段落连续性：相邻15秒段落之间，人物位置、服装、道具、光线、场景方向、动作因果是否顺滑衔接。

## 测试批次

| 测试ID | 类型 | 覆盖段落 | 目的 | 状态 |
|---|---|---|---|---|
| T01 | 图片锁点测试 | SEG001-SEG003 | 先用少量对照图测试角色/场景/道具稳定性 | 待测试 |
| T02 | 视频衔接测试 | SEG001-SEG003 | 再用相邻Seedance段落测试转场连续性 | 待T01通过 |
```

连续性测试图是内部质检素材，不作为最终交付物。最终交付给用户的仍是每个视频段落的 Seedance 上传包。

正式视频包必须使用 `keyframe_multiref_seedance`：每段直接上传固定4帧时间锚点，上一段视频尾帧作为下一段开始画面和SHOT01，最多3张新关键帧对应SHOT02-SHOT04，Mimo台词音频进入多功能参考；非首段缺尾帧时暂时不要生成视频；提示词末句固定为“不要在视频画面中出现文字信息。”

## 连续性测试记录表

```markdown
# 第X季连续性测试记录表

| 测试图ID | 测试素材 | 角色脸 | 发型 | 服装 | 标志道具 | 场景方向 | 光线色彩 | 动作因果 | 总结 | 是否通过 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|

| 转场ID | 前一段 | 后一段 | 检查范围 | 人物位置 | 动作接续 | 场景方向 | 光线连续 | 服装道具 | 总结 | 是否通过 |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
```

## 连续性锁点表

```markdown
# 连续性锁点表

| 锁点类型 | 必须保持 | 允许变化 | 禁止变化 |
|---|---|---|---|
| 角色身份 | [年龄、脸、发型、体态、气质] | [情绪/姿态变化] | [换脸、发型大变、年龄漂移] |
| 服装道具 | [固定服装、标志道具] | [光线/雨水反射] | [道具消失、服装暴露或大变] |
| 场景方向 | [地标、行动方向、空间关系] | [镜头角度变化] | [无解释反向、地点跳变] |
```

## 锁定资产保护规则

```markdown
# 第X季锁定资产保护规则

## 锁定原则

- 已锁定资产不得原地覆盖。
- 修改已锁定资产时，必须创建新版本文件，例如 `_v3`。
- 新版本通过人工确认后，旧版本才能标为 `已被v3替代`。
- Seedance上传包只引用当前已确认的版本。
- 历史测试包不得继续出现在当前索引中。

## 锁定等级

- `当前草案可用`：只允许剧本、分镜、提示词草稿引用。
- `小样锁定`：允许小样和连续性测试引用；不得直接进入整季批量。
- `正式锁定`：允许当前正式集/批次引用；替换必须出新版本。
- `全季锁定`：全季共享基准；只有总控可提出替换。

## 锁定资产表

| 资产ID | 资产类型 | 当前锁定版本 | 锁定等级 | 文件路径 | 使用范围 | 锁定原因 | 替换条件 | 禁止操作 | 备注 |
|---|---|---|---|---|---|---|---|---|---|
```

Create `00_当前锁定资产清单.json` beside the season tables after the pilot or continuity assets are accepted. Keep paths relative to the season folder and include only current final-package packages under `packages`.

```json
{
  "schema_version": 1,
  "updated_at": "YYYY-MM-DD",
  "assets": [
    {
      "asset_id": "IMG001_V2",
      "kind": "character_reference",
      "status": "locked",
      "current": true,
      "path": "assets/01_角色参考图/角色_五宫格_v2.png",
      "role": "主角身份锁定参考"
    }
  ],
  "packages": [
    {
      "segment_id": "SXXEXX_SEGXXX",
      "current": true,
      "path": "20_Seedance上传包/SXXEXX_SEGXXX_上传用_v2",
      "route": "keyframe_multiref_seedance",
      "execution_provider": "dreamina_cli",
      "previous_tail_frame": "boundary/图片1_上一段尾帧.png",
      "keyframe_references": ["keyframes/图片2_SHOT02关键帧.png", "keyframes/图片3_SHOT03关键帧.png", "keyframes/图片4_SHOT04关键帧.png"],
      "character_references": ["references/characters/图片3_主角锁定参考.png"],
      "scene_references": ["references/scenes/图片4_场景参考.png"],
      "prop_references": ["references/props/图片5_道具参考.png"],
      "raw_video_path": "assets/07_视频分段/Seedance原始下载/<submit_id>/SXXEXX_SEGXXX_raw.mp4",
      "seedan_1080p_video_path": "assets/07_视频分段/Seedan后处理/<submit_id>/SXXEXX_SEGXXX_1080p.mp4",
      "seedan_60fps_video_path": "assets/07_视频分段/Seedan后处理/<submit_id>/SXXEXX_SEGXXX_1080p_60fps.mp4",
      "episode_video_path": "assets/07_视频分段/SXXEXX_第XX集/SXXEXX_SEGXXX_v01.mp4",
      "tail_frame_path": "boundary_outputs/SXXEXX_SEGXXX_tail.png"
    }
  ],
  "continuity_links": [
    {
      "from_segment": "SXXEXX_SEGXXX",
      "to_segment": "SXXEXX_SEGYYY",
      "from_tail": "boundary_outputs/SXXEXX_SEGXXX_tail.png",
      "to_previous_tail_frame": "SXXEXX_SEGYYY/boundary/图片1_上一段尾帧.png",
      "rule": "same_file_hash"
    }
  ]
}
```

## 工具脚本

```markdown
# 工具脚本

| 工具 | 文件 | 用途 | 运行时机 | 输出 |
|---|---|---|---|---|
| Skill内置正式路线检查脚本 | ~/.codex/skills/ai-comic-drama/scripts/check_keyframe_multiref_package.py | 检查keyframe_multiref_seedance包的manifest、15秒规则、4个连续SHOT、上一段尾帧、有序关键帧、人物/场景/道具参考、Mimo音频映射、提示词末句和尾帧记录 | 每次生成或更新正式上传包后 | Markdown检查报告 |
| 项目本地Seedance上传包检查脚本 | 工具脚本/检查Seedance上传包.py 或 .ps1 | 项目特定素材规格、平台上传限制、中文格式和批量路径检查；需要另行存在，不随skill捆绑 | 项目需要自动化检查时 | 项目本地检查报告 |
| 项目本地Mimo生成脚本 | tools/mimo_tts_generate.py | 调用Mimo API生成音色标准和正式对白；需要另行存在，不随skill捆绑 | 音频生产/连通性测试 | wav/mp3与音频生成日志 |
```
