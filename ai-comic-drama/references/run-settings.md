# Run Settings Contract

Use this before execution to prevent open-ended production drift.

## Contents

- [Required Fields](#required-fields)
- [Confirmation Rule](#confirmation-rule)
- [Source Authority Options](#source-authority-options)
- [Parallel Agent Options](#parallel-agent-options)
- [Scale-Up Confirmation Options](#scale-up-confirmation-options)
- [Formal Start Checklist](#formal-start-checklist)
- [Stop Conditions](#stop-conditions)
- [Seedance And Dreamina CLI Settings](#seedance-and-dreamina-cli-settings)
- [Mimo Audio Settings](#mimo-audio-settings)
- [Suggested File](#suggested-file)

## Required Fields

Use menu-style settings. Every field must record:

- `当前选择`
- `可选项` with 2-4 compact choices
- `是否需要用户确认`

If a choice is already locked by the project, mark it `已确认，不再询问`.

| Field | Purpose | Typical Options |
|---|---|---|
| `RUN_INTENT` | What kind of work is happening now | `规划/审查`, `单段小样`, `连续性测试`, `最终交付包`, `批量生产`, `视频提交/下载` |
| `SOURCE_AUTHORITY` | Which source wins when materials conflict | `用户提供素材优先`, `当前锁定资产优先`, `用户素材+锁定资产混合`, `等待用户指定` |
| `ACTIVE_SCOPE` | Exact project, season, episode, segment IDs, and folders | `当前段`, `相邻两段`, `整集`, `整季` |
| `EPISODE_SPEC` | User-confirmed series/episode specs before story or shot work | `90秒概念短片`, `3分钟样片`, `5-7分钟单集`, `10分钟+正片`, `自定义` |
| `QUALITY_STAGE` | draft, pilot, continuity test, final package, batch | `草稿`, `小样`, `连续性测试`, `最终包`, `批量` |
| `PROVIDERS` | image/audio/video tools and model versions | image: `$imagegen_builtin_image_gen` only; audio: `mimo`, `manifest_only`; video: `dreamina_cli_seedance2` |
| `COST_POLICY` | paid generation permission and cap | `不消耗额度`, `每次提交前确认`, `本轮N条/额度上限`, `已授权当前小样` |
| `CONTINUITY_STRATEGY` | how adjacent clips connect | `keyframe_multiref_seedance`（正式方案：上一段尾帧/SHOT01 + 有序关键帧 -> 多功能参考视频 -> 提取尾帧） |
| `LOCKED_ASSETS` | current manifest, versions, no-overwrite rule | `使用当前锁定清单`, `只读检查`, `允许新版本不覆盖`, `等待用户指定` |
| `OUTPUT_CONTRACT` | what files/folders the user will receive/check | `文件夹`, `上传包`, `视频路径`, `报告`, `zip` |
| `VERIFICATION` | checks before claiming ready | `JSON/脚本检查`, `CLI状态`, `视觉人工检查`, `连续性评分`, `用户验收` |
| `PARALLEL_PLAN` | whether/how agents work in parallel | `不并行`, `4+1制片厂结构`, `每集一个agent`, `自定义分区` |
| `SCALE_UP_ANCHORS` | confirmations required before broad creation | `小说/剧情基线`, `角色参考图`, `场景图`, `视觉风格`, `视频链路`, `黄金样片` |
| `CONSISTENCY_LOCKS` | character/scene/prop/keyframe/boundary readiness | `角色锁点`, `场景锁点`, `道具锁点`, `有序关键帧`, `上一段尾帧`, `音频映射` |

## Confirmation Rule

Before creating or revising story baselines, episode scripts, shot scripts, keyframe plans, or multi-segment packages, present a compact episode-spec menu and wait for the user's explicit choice. Do not infer the runtime or format from prior examples. Record the chosen value in `EPISODE_SPEC`, including:

- project format: `系列单元剧`, `单季完整闭环`, `多季主线`, or custom;
- episode count: explicit number or `待定`;
- per-episode target runtime: `90秒`, `3分钟`, `5-7分钟`, `10分钟+`, or custom;
- aspect ratio/platform/content boundary/delivery depth;
- whether the current run is a pilot/sample spec or the intended final episode spec.

Do not re-confirm stable choices that have already been accepted in the project. Record them as:

```text
图片：$imagegen built-in image_gen（强制已确认，不再询问；不使用 chatgpt_web/openai/Dreamina/即梦/Seedance 或自写 SDK 脚本生成静态图）
音频：Mimo / manifest（已确认，不再询问）
视频：Seedance 多功能参考 / keyframe_multiref_seedance / dreamina_cli_seedance2（正式方案已选；15秒单元，上一段尾帧/SHOT01 + 有序关键帧 + Mimo音频 + 人物/场景/道具参考；视频上传/查询/下载必须通过本地 `dreamina` CLI；视频提交/下载不属于批量生产）
```

Ask again only when a confirmed provider fails, the user asks to change it, cost changes materially, or a locked/current asset would be replaced.

## Source Authority Options

When the user has already provided novels, outlines, scripts, character references, scene references, style examples, or audio, set `SOURCE_AUTHORITY` to `用户提供素材优先` unless the user says otherwise.

Use these compact choices:

- `用户提供素材优先`: treat provided materials as canon; integrate and map them before creating new assets.
- `当前锁定资产优先`: use the existing locked manifest as canon; new user files need review before replacement.
- `用户素材+锁定资产混合`: use when both are valid; flag contradictions and ask only for conflicts that affect production.
- `等待用户指定`: use when source ownership is unclear.

Resource integration duties: preserve original file paths, avoid overwriting, classify each material by story/character/scene/style/audio/video, map it to episodes/segments when possible, record gaps and contradictions, and only propose regeneration when the supplied material is missing or unsuitable.

## Parallel Agent Options

For a 20-episode season, prefer:

```text
PARALLEL_PLAN：4+1制片厂结构（推荐）
总控：全季连续性、锁定资产、最终合并、待视频提交清单
Agent A：EP01-EP05
Agent B：EP06-EP10
Agent C：EP11-EP15
Agent D：EP16-EP20
```

Other options:

- `不并行`: safer for early pilot work.
- `每集一个agent`: fast but high merge/continuity risk; avoid unless templates are very mature.
- `自定义分区`: use for non-20-episode seasons or uneven episode complexity.

Before parallel work starts, confirm ownership folders and make shared files read-only by convention. Workers write inside `40_并行生产/Agent_X_EPxx-yy/`; only the controller updates current official season tables, indexes, locked manifests, and the ready-to-submit package backlog. Batch production does not include `dreamina` CLI submit, queue polling, download, or tail-frame extraction.

## Scale-Up Confirmation Options

Before broad writing, batch image generation, batch package generation, full-season work, or parallel agents, create/update `大规模创作前确认表`.

Use these compact choices:

- `待确认`: unresolved; dependent broad work is blocked until a choice is made.
- `已确认可用`: usable for the current scope.
- `小样锁定`: locked for pilot/continuity tests only; broad production still needs a scale-up review.
- `正式锁定`: reusable baseline for the active episode/batch; never overwrite in place.
- `全季锁定`: season-wide canon; controller approval is required for replacement.
- `当前草案可用`: drafting may proceed, but final media generation is blocked.
- `需返修`: dependent broad work is blocked.
- `缺失`: dependent broad work is blocked.
- `明确跳过`: user/controller accepts the risk; record reason and scope.

At minimum confirm: story/novel baseline, episode beat map, main character reference sheets, character lock blocks, key scene/reference images, scene lock blocks, prop locks, 15s segmentation, fixed 4-shot ordered keyframe pattern, visual style bible, audio policy or voice standard, Seedance route/model/cost policy, and pilot/continuity result.

Episode spec is a prerequisite for story, script, shot, and keyframe planning. If `EPISODE_SPEC` is `待确认`, treat story baselines, episode scripts, and multi-segment plans as blocked.

Lock level rule:

- `当前草案可用`: use for outlining and rough prompt work only.
- `小样锁定`: use for pilot keyframes/video tests, not full-season batch generation.
- `正式锁定`: use for the current official episode or assigned batch.
- `全季锁定`: use as canon for every worker and downstream package.

## Formal Start Checklist

Before a formal large-scale run, record one compact row per item in `00_项目设定/03_当前运行设置.md` or the project's `大规模创作前确认表`. Use the same lock levels above.

| Item | Options | Default | Blocks If Missing |
|---|---|---|---|
| Novel/story baseline | `当前草案可用`, `已确认可用`, `正式锁定`, `全季锁定` | `已确认可用` | script and shot generation |
| Episode beat map/hooks | `当前草案可用`, `已确认可用`, `正式锁定` | `已确认可用` | runtime and hook control |
| Main character refs | `待确认`, `小样锁定`, `正式锁定`, `全季锁定` | `正式锁定` | character keyframes/video |
| Character lock blocks | `待确认`, `正式锁定`, `全季锁定` | `正式锁定` | continuity checks |
| Main scene refs/maps | `待确认`, `小样锁定`, `正式锁定`, `全季锁定` | `正式锁定` | scene keyframes/video |
| Visual style bible | `当前草案可用`, `已确认可用`, `正式锁定`, `全季锁定` | `正式锁定` | visual generation |
| Prop/trace refs | `无本段需求`, `待确认`, `正式锁定`, `全季锁定` | `正式锁定` when visible | formal keyframes/video |
| Audio policy | `Mimo已确认`, `临时manifest_only`, `待确认` | project setting | dialogue-heavy video |
| Video route/model | `seedance2.0`, `seedance2.0_vip`, `待确认` | `seedance2.0` | paid video submit |
| Pilot/continuity result | `已通过`, `通过-有警告`, `明确跳过`, `待测试` | `已通过` | batch package production |

Do not ask again for image/audio providers if the project already marks them confirmed. Reconfirm video only when the route, model, cost, or pilot result changes.

## Stop Conditions

Stop for user confirmation before:

- spending credits beyond the active cap;
- submitting more than the stated segment count;
- submitting a non-first segment whose expected previous tail frame is missing, unavailable, or unusable;
- overwriting locked/current assets;
- changing continuity strategy after a test has started;
- cloning or imitating a real voice/person without explicit rights;
- switching provider/model when cost or quality changes materially.

## Seedance And Dreamina CLI Settings

For `keyframe_multiref_seedance`, settle these before submit. This is the default primary video-continuity route:

Video execution boundary: these settings are used when preparing upload packages during batch production, but actual Seedance submits are a separate `视频提交/下载` run and must execute through local `dreamina` CLI. Batch production can mark packages `READY_FOR_VIDEO_SUBMIT`; it must not submit, poll, download, or extract tail frames.

- `execution_provider`: must be `dreamina_cli` for formal video upload/query/download.
- `model_version`: use `seedance2.0` by default, or `seedance2.0_vip` when the user has selected VIP. Always pass it explicitly with `--model_version=...`; do not rely on the CLI default.
- `duration`: default 15 seconds per segment; record exceptions explicitly.
- `shot_count`: each formal 15s segment has exactly 4 scripted shots, `SHOT01` through `SHOT04`; each beat should be roughly 3-5 seconds and the total remains 15 seconds.
- `keyframes`: for an episode's first segment, use up to 4 approved 16:9 cinematic keyframes matching `SHOT01`-`SHOT04`; for later segments, use the previous video's real tail frame as `SHOT01` plus up to 3 approved new keyframes for `SHOT02`-`SHOT04`.
- `keyframe_references`: ordered approved keyframes uploaded directly as separate references; never cite omitted keyframes, and merge their story/action content into the nearest kept shot text.
- `previous_tail_frame`: for non-first adjacent segments, extract/read the previous video's tail frame from the Seedan `1080p/60fps` current file and upload it as the segment start reference when video generation is being submitted. During pre-build-only passes, the field may stay blank and must be filled before formal sequential submission.
- `boundary_handoff`: at 4+1 agent boundaries, the controller owns cross-episode tail/start frames; workers do not invent them independently.
- `consistency_locks`: current character, scene, and prop lock blocks must exist for recurring elements before batch generation.
- `concurrency`: submit one task at a time unless the account proves it supports parallel video generation.
- `prompt_safety`: keep prompts short and anchored to lock blocks; every video prompt must end with `不要在视频画面中出现文字信息。`
- `result_policy`: download outputs, keep the raw file, use Seedan free processing to upscale to `1080p` and then `60fps`, record `submit_id` plus raw/1080p/60fps/current paths, and pause for user inspection when requested.
- `audio_policy`: Mimo dialogue files mapped to visible roles can be uploaded for video generation; narration/SFX/ambience/unclear-mouth audio defaults to post-mix.

## Mimo Audio Settings

When `PROVIDERS` includes Mimo, record these without real API keys:

- `MIMO_BASE_URL`: default `https://token-plan-cn.xiaomimimo.com/v1` unless the user's console says otherwise.
- `MIMO_TTS_ENDPOINT`: `/chat/completions`.
- `MIMO_TTS_MODEL`: `mimo-v2.5-tts` for non-character-stable or background audio only.
- `MIMO_VOICE_DESIGN_MODEL`: `mimo-v2.5-tts-voicedesign` for character standard voice generation.
- `MIMO_VOICE_CLONE_MODEL`: `mimo-v2.5-tts-voiceclone` for formal dialogue generation by uploading the locked standard voice audio plus target text.
- `API_KEY_POLICY`: never write actual keys into settings, skill files, examples, manifests, reports, or chat; keep keys only in local uncommitted `.env.mimo`.
- `VOICE_STANDARD_POLICY`: formal dialogue is blocked until the role has a locked standard voice file and the generated dialogue references that file.
- `UPLOAD_AUDIO_POLICY`: every Seedance-driving audio copy must be 2-15 seconds; pad/upload copies separately without overwriting the locked source.

Do not use contact sheets, review collages, comparison boards, labeled grids, or multi-panel storyboards as video references. The primary route uploads ordered keyframes directly.

## Suggested File

Create or update:

```text
00_项目设定/03_当前运行设置.md
```

Suggested headings:

```markdown
# 当前运行设置

| 字段 | 当前选择 | 可选项 | 是否需要用户确认 |
|---|---|---|---|
| RUN_INTENT |  |  |  |
| SOURCE_AUTHORITY |  |  |  |
| ACTIVE_SCOPE |  |  |  |
| EPISODE_SPEC |  |  |  |
| QUALITY_STAGE |  |  |  |
| PROVIDERS |  |  |  |
| COST_POLICY |  |  |  |
| CONTINUITY_STRATEGY |  |  |  |
| LOCKED_ASSETS |  |  |  |
| OUTPUT_CONTRACT |  |  |  |
| VERIFICATION |  |  |  |
| PARALLEL_PLAN |  |  |  |
| SCALE_UP_ANCHORS |  |  |  |
| CONSISTENCY_LOCKS |  |  |  |

## 已确认

## 待确认

## 本轮不得做
```
