# Seedance Keyframe Multi-Reference Handoff

Load this before creating Seedance upload packages, segment video prompts, or video generation tables. Formal video upload, async query, and download must execute through the local Dreamina/即梦 CLI.

## Contents

- [Primary Route](#primary-route)
- [Official Seedance 2.0 Modes And Limits](#official-seedance-20-modes-and-limits)
- [Smart Multi-Frame Upload Priority](#smart-multi-frame-upload-priority)
- [Ordered Keyframe References](#ordered-keyframe-references)
- [Multi-Reference Video Package](#multi-reference-video-package)
- [Pre-Submit Upload Package Viewer](#pre-submit-upload-package-viewer)
- [Prompt Rules](#prompt-rules)
- [Formal Video Prompt Template](#formal-video-prompt-template)
- [Submission Checks](#submission-checks)
- [Dreamina CLI Execution](#dreamina-cli-execution)
- [Boundary Continuity](#boundary-continuity)
- [Manifests](#manifests)
- [Retake Rules](#retake-rules)

## Primary Route

Formal video generation uses `keyframe_multiref_seedance`.

One production unit equals one 15-second segment:

1. Build a fixed 4-shot script for the 15-second unit: `SHOT01-SHOT04`.
2. For an episode's first segment, generate and approve up to four 16:9 cinematic keyframes; `SHOT01` is the episode start keyframe.
3. For later adjacent segments, `SHOT01` is the previous video's real tail frame and the new video's starting reference. Generate and approve new action keyframes for `SHOT02-SHOT04`, then upload the tail frame plus at most 3 selected action keyframes, for 4 temporal frames total.
4. Upload the previous tail frame and selected ordered keyframes directly as separate Seedance references. Do not upload or cite omitted keyframe images; merge their story/action beats into the previous or next shot text. Do not compose or upload multi-panel storyboard boards, review sheets, contact sheets, nine-grid atlases, or collages.
5. Add locked character, clean scene, visible critical prop/trace references and Mimo audio as needed, then submit the Seedance `智能多帧/多模态参考` video through local `dreamina multimodal2video`.
6. Query and download with `dreamina query_result`; keep the raw video, then use Seedan's free functions in order: upscale resolution to `1080p`, then increase frame rate to `60fps`.
7. Extract the video's tail frame from the `1080p/60fps` current file and use it as the next segment's start reference.

If the previous tail is not available during a pre-build pass, leave the field blank in the manifest and continue preparing scripts, new keyframes, upload mappings, prompts, and package structure. Fill the real tail frame before formal sequential video submission.

## Official Seedance 2.0 Modes And Limits

Seedance 2.0 has separate official submission modes. Treat them as mutually exclusive package routes:

- `首帧`: use when the main requirement is a specific first frame.
- `首尾帧`: use when the main requirement is strict first-frame and last-frame matching. This is the route for pixel-level start/end continuity, but it gives up the broader multi-reference stack.
- `智能多帧/多模态参考`: use when the main requirement is combined control of character, scene, action rhythm, props, dialogue audio, or style across one continuous 15s clip. This is the default `keyframe_multiref_seedance` route.

Official caps for `智能多帧/多模态参考` packages:

- Images: upload 1-9 images.
- Videos: upload at most 3 video references; total referenced video duration must not exceed 15 seconds.
- Audio: upload at most 3 audio clips; total uploaded audio duration must not exceed 15 seconds.
- Audio cannot be submitted alone. A package with audio must include at least one image or video reference.

For adjacent short-drama segments, `@图片1` is the previous segment's extracted tail frame whenever the route is `智能多帧/多模态参考`; this gives the model the opening state. If the user asks for exact first-frame/last-frame matching, switch to `首尾帧` mode instead of mixing that route with multi-reference uploads.

## Smart Multi-Frame Upload Priority

This is the current upload-package rule. Do not fill all 9 image slots by habit. Official prompt guidance favors a smaller, clearer reference set; too many images can blur priority, create style conflicts, and increase subject drift. Prefer the minimum set that preserves story continuity.

Project soft cap: keep formal `智能多帧/多模态参考` image uploads at `7` images whenever possible. Ordered keyframes/start-tail, the primary character reference, current clean scene geography, and visible story-critical prop references have priority over auxiliary references. Future-scene references should not compete with the current segment's controls unless the character has already entered that scene.

If the reference stack exceeds 7 images, remove auxiliary references in this order:

1. Future-scene reference image; keep the future location only as text in the tail/next-shot handoff.
2. Optional style or supplementary reference.
3. Supporting-character reference image when the supporting character is already visible in temporal keyframes.
4. Auxiliary prop / trace reference image that is not visibly used, activated, contested, revealed, or plot-critical in this segment.
5. Current clean scene reference only as a last resort, and only if temporal keyframes already carry enough geography.

Record every removed image in the upload package's omitted-reference list, explain the reason, and compensate with concise prompt continuity. Do not change the plot, shot order, approved keyframes, audio, or locked asset files to satisfy the 7-image soft cap. The official 9-image cap remains the hard provider limit; exceeding the project 7-image soft cap requires explicit user direction or a documented blocker where keyframes/start-tail alone already need more slots.

Temporal frame cap: formal upload packages use at most 4 temporal frames total. For first segments, that means up to 4 ordered keyframes. For later segments, the previous video's tail frame counts as the first temporal frame, so choose at most 3 additional action keyframes. Omitted keyframe image files must not appear as uploaded references or prompt reference labels; keep their content only in the written shot beats by folding the omitted action into a neighboring shot description.

Representative-frame rule: each uploaded temporal image must match the current target SHOT's visible action requirement, not merely a filename order or automatic midpoint choice. If the user corrects a slot's visual requirement, treat that as a hard constraint and update the package mapping, prompt, and active manifest. Any superseded mapping/image usage becomes retired for current upload purposes and must not reappear in future viewers or submissions.

Recommended image order for formal `智能多帧/多模态参考` uploads:

| Slot | Use |
|---|---|
| `@图片1` | Starting image or main keyframe. For non-first adjacent segments, this is the previous video's extracted tail frame. For first segments, this is the approved opening `SHOT01` keyframe. |
| `@图片2-@图片4` | Middle action keyframes in story order. Each image should represent one clear action node. The total temporal frame count, including `@图片1` when it is a tail/start frame, must not exceed 4. |
| `@图片5` | Main character appearance reference. Use a clean single-character image; for fictional characters, prioritize face, hair, costume, body silhouette, and style stability. |
| `@图片6` | Clean scene reference. Use it only for space structure, lighting, color, material, and atmosphere. |
| `@图片7` | Visible story-critical prop, product, trace, or logo reference, only when it is important to the plot, display, or continuity. A core prop beats a future-scene mood reference. |
| `@图片8-@图片9` | Optional style or supplementary references. Leave these slots empty unless the added reference has a clear priority. |

For short-drama continuity, preserve the approved keyframe/start-tail sequence first, then add the primary character reference, current clean scene reference, and visible story-critical prop reference. Future-scene references are usually text-only destination or tail-frame hints; upload them only when the segment actually enters that location. Supporting-character and optional style references are included only while the 7-image soft cap allows them. Never upload nine-grid atlases, collage sheets, storyboard boards, approval galleries, watermarked images, UI screenshots, readable subtitles, or reference sheets as formal Seedance images.

## Ordered Keyframe References

- First segment: use `SHOT01` as `@图片1` / start reference, then select the clearest approved middle action keyframes in story order, with no more than 4 temporal frame references total.
- Later segment: upload the previous tail frame as `@图片1` / `SHOT01` / start reference, then select no more than 3 approved action keyframes from `SHOT02` through the actual last shot as middle/end anchors.
- Order is the shot order in the script. Do not infer order from filenames alone; record upload slots in the manifest.
- Keyframes are temporal anchors for one continuous 15s video, not panels to render as a grid, slideshow, split screen, or collage.
- Omitted keyframes are not references. Do not upload them, do not label them as `@图片N`, and do not mention their filenames or asset IDs in the prompt. Preserve their story content by adding the omitted beat to the previous or next shot's text.
- Retired keyframe usages are also not references. If an image was rejected, superseded, or corrected away for a specific upload slot, exclude that usage from current package generation even if the physical image remains on disk for audit or another historical shot.
- Inputs: character reference image(s), scene reference image(s), locked prop reference image(s) for every common or story-critical visible prop, previous tail/start state when available, script, and shot script.
- Output: a self-contained upload package with ordered keyframes and references. No storyboard board is created in the formal route.

Keyframe still-image prompt rules live only in `references/imagegen-staging.md`. Do not copy a separate keyframe-generation formula into this upload-package reference.

## Multi-Reference Video Package

Each 15s segment package should contain:

```text
SXXEXX_SEGXXX/
  keyframes/
    图片2_SHOT02关键帧.png             # later segments; first segments also include SHOT01
    图片3_SHOT03关键帧.png
    图片4_SHOT04关键帧.png
  boundary/
    图片1_上一段尾帧.png                # used when available before submit
  references/
    characters/
    scenes/
    props/
    traces/
  audio_for_video/
    音频1_角色_台词.wav
  audio_for_postmix/
  prompts/
    00_seedance多功能参考提示词.txt
  03_PACKAGE_MANIFEST.json
```

Upload order:

| Slot | Required | Purpose |
|---|---|---|
| `@图片1` | non-first segments before submit | previous video tail frame; use as the starting image and `SHOT01` |
| next image slots | yes | selected ordered action keyframes: first segments usually add `SHOT02-SHOT04`; later segments usually add `SHOT02-SHOT04` after the tail frame |
| next image slots | yes | main character reference images, preferably clean single-character images |
| next image slots | yes | clean scene reference image for structure, light, color, material, and atmosphere |
| next image slots | required when visible | locked prop/trace reference images for common, handheld, story-critical, merch-critical, or gameplay-critical props |
| optional image slots | optional | style or supplementary refs only when they have a clear priority; leaving slots empty is allowed |
| `@音频1...` | for dialogue | Mimo dialogue files used by this video |
| `@音色参考...` | when supplied/needed | voice or timbre reference audio for Seedance `seedance2.0` character voice consistency; map each reference to its character |

Keep the reference count within the active platform limit. Seedance `智能多帧/多模态参考` accepts 1-9 uploaded images, but the project default is a 7-image soft cap. If there are too many refs, keep the previous tail/start frame, approved ordered keyframes, primary character, current clean scene geography, and visible story-critical prop/trace references first. Remove future-scene references first and keep them as written tail/next-shot handoff only; then remove optional style/supplementary references, supporting-character references already recoverable from temporal keyframes, and finally auxiliary non-critical props/traces. Current-scene refs are removed only as a last resort. This standing project rule counts as user confirmation for omitting those auxiliary references, but the omission must still be written into the manifest/upload checklist with prompt-compensation notes. If a segment cannot preserve story continuity after these omissions, mark it as blocked for user review instead of silently changing the story.

Formal Seedance image inputs must be diegetic or clean reference images. Do not upload contact sheets, storyboard boards, review galleries, scene atlases, nine-grid layouts, multi-panel collages, screenshots with UI, subtitles, watermarks, or labels. If the only available scene reference is a grid/atlas/review image, create or select a clean single scene reference before formal submit.

## Pre-Submit Upload Package Viewer

Before every formal Seedance video submission:

1. Build a local browser upload-package viewer from the active segment manifest and prompt.
2. Show the selected Seedance submission mode and the exact upload order, including all selected `@图片N`, `@视频N`, `@音频N`, and `@音色参考N` slots that will be submitted.
3. Show `audio_for_postmix/` assets separately and label them as not uploaded for visible dialogue/lipsync unless the manifest explicitly says otherwise.
4. Show any available but omitted references, especially omissions caused by the active image cap, with the reason and prompt-compensation note.
5. Show the final prompt exactly as it will be submitted.
6. Open the viewer for the user and wait for explicit confirmation after they inspect it. A prior keyframe approval, audio approval, or package audit is not enough to submit video.
7. If any upload image, video reference, audio file, prompt text, omission list, duration, provider, model, ratio, resolution, submission mode, or scope changes after the viewer is shown, rebuild and reopen the viewer before submission.
8. Before showing or submitting the viewer, check the active project manifest for superseded packages, retired image usages, and user corrections. A package that points to a retired slot/image mapping is invalid even if all files exist.
9. Record the viewer path, decision, and active scope in the project logs or manifest before submitting.

Do not submit video until the user confirms the displayed upload package.

Use the bundled viewer builder unless the project has a stricter local tool:

```bash
python3 ~/.codex/skills/ai-comic-drama/scripts/build_upload_package_viewer.py \
  <segment-package-or-manifest> \
  --output <segment-package>/upload_package_viewer \
  --title "SXXEXX_SEGXXX 上传包核对"
```

On Windows PowerShell, use the installed skill path directly:

```powershell
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\build_upload_package_viewer.py" `
  "<segment-package-or-manifest>" `
  --output "<segment-package>\upload_package_viewer" `
  --title "SXXEXX_SEGXXX 上传包核对"
```

The script writes `index.html`, `UPLOAD_PACKAGE_VIEWER_STATE.json`, and `UPLOAD_PACKAGE_VIEWER_CONFIRMATION_TEMPLATE.json`, then prints the `file://` URL to open. The template is not a confirmation by itself; only a recorded user decision or manifest confirmation counts.

## Prompt Rules

The video prompt should:

1. Identify each uploaded image/audio role from the actual upload order.
2. Say the previous tail frame is the starting-state / opening composition reference when present. In `智能多帧/多模态参考`, do not write it as a pixel-level first-frame or first/last-frame hard lock; exact first/last-frame matching belongs to the separate `首帧` or `首尾帧` route.
3. Say the selected ordered keyframes are temporal anchors for one continuous 15s video, not a grid, slideshow, split screen, collage, or image sequence to render literally.
4. Merge ordered keyframe descriptions instead of repeating the same full sentence under every image. Prefer one compact line such as `@图片1-@图片4 是本段按镜头顺序上传的时序关键帧：@图片1=SXXEXX_SEGXXX SHOT01 关键帧; @图片2=SXXEXX_SEGXXX SHOT02 关键帧...。它们只作为时间顺序、画面状态和动作节拍参考，共同用于理解 15 秒内的连续视频节奏；不要生成拼贴、分屏、漫画格、幻灯片或图片序列。`
5. Describe the 15s action as a single continuous video, with `SHOT01` usually starting from the previous tail frame.
6. Bind every `@音频N` to role, dialogue line, story beat, and performance use. Use natural speaker binding plus braces, for example `黎霓说 {你们铁雨帮什么时候有售后了？}，口型匹配 @音频1` rather than relying on `{...}` alone.
7. Preserve scene geography, props, lighting, and motion direction. Use concise continuity language; detailed character/body/wardrobe locks belong in manifests and references.
8. For every uploaded scene reference, define it as a clean scene reference for space structure, lighting, color, material, and atmosphere; forbid the model from rendering it as a reference sheet, map, label, picture-in-picture, grid, or collage.
9. If the storyboard, shot description, or user script contains spoken character dialogue, explicitly include the spoken dialogue in the prompt using Seedance oral-dialogue braces, such as `{修这个，或者我们一起死。}`. Do not keep storyboard quotation marks inside braces. If the line is not in the project's primary language, label the language before the braces, such as `Says in Japanese: {こんにちは}`.
10. If the user supplied voice, timbre, or voice-reference audio for cross-shot character consistency, include it as a Seedance `seedance2.0` reference item and state which character uses which reference audio. Example: `@音色参考1 是角色A的音色参考，角色A所有可见对白都保持这个音色。`
11. Keep audio prompts clean. Uploaded audio rows should describe only dialogue, visible lip/performance timing, or timbre reference use. Do not put separate narration/voiceover text, postmix ambience, or complex SFX lists into the video prompt when those belong to `audio_for_postmix/`; write only a light note such as `environment sound stays subtle; postmix will add complex effects`.
12. Put negative constraints once near the end instead of repeating them under every shot unless a specific shot needs one. Always include `no music` and `no subtitles` for clean post-production.
13. End with this exact sentence:

```text
不要在视频画面中出现文字信息。
```

Seedance motion/dynamic order:

1. Camera: movement, shot change, or edit, such as `static -> push-in`, `cut to new angle`, `orbit`, or `pan`.
2. Subject: who acts, body-part-specific action, facial beat, and intensity. Describe hands, legs, head, shoulders, eyes, mouth, or breathing when relevant, including speed and force, such as `slowly raises one hand`, `snaps head left`, or `pushes hard off the ground`.
3. Space: position changes, depth/layout changes, background movement, and how characters/camera relate to the environment.
4. Audio: spoken dialogue in `{...}` when visible/synchronous, sound effects in `<...>`, music in `(...)` only when explicitly wanted, and `no music` otherwise.

For multiple beats in one prompt, write the primary action first, then secondary actions in story order. If the tool accepts a long prompt, label sequential camera/story beats as `镜头 1`, `镜头 2`, `镜头 3`; do not force exact seconds such as `0-3秒`, `3-6秒`, or `在2秒时`. Describe the order of events rather than a second-by-second schedule.

Seedance wrapper conventions:

| Content type | Wrapper | Rule |
|---|---|---|
| Music | `(...)` | Use only when the requested video should contain music, e.g. `(fast-paced rock playing in the background)`. Project default is `no music`. |
| Sound effect | `<...>` | Use for audible effects, e.g. `<distant metal impact>`. |
| Spoken dialogue | `{...}` | Use for character-spoken lines. Put only the line text inside braces. |
| Screen title/chapter/subtitle text | `【...】` | Use only when the user explicitly wants model-rendered screen text. Project default is no generated subtitles or readable screen text. |

If the brief is cinematic live action, light handheld micro-shake or subtle film grain may be added only as minor polish after the camera -> subject -> space -> audio order is satisfied.

Common prop rule:

- A recurring, handheld, story-critical, merch-critical, or gameplay-critical prop that appears on screen must have a locked prop ref in the package.
- If the prop has no locked ref, block formal video submit or mark the package draft-only.
- Mention the prop only in beats where it is visibly held, opened, observed, activated, dropped, revealed, or contested.
- If choosing between a visible core prop and a future-scene mood image, keep the visible core prop and describe the future scene as text-only handoff.

## Formal Video Prompt Template

Use this as the default template for formal Seedance 15s submissions after ordered keyframes, references, and Mimo audio are locked. Always build the reference map from the actual upload order before writing the prompt. Never leave stale labels from an earlier package.

```text
【参考内容说明】

@[上一段尾帧引用] 是上一段 [上一段ID] 视频尾帧 / 本段智能多帧开场状态参考；请参考其中的构图、角色姿态、空间方向、追逐关系和关键道具状态，让本段从这个画面状态自然延续。它对应本段 SHOT01。它不是首帧/首尾帧模式，不要求逐像素复制。

@[关键帧起止引用] 是本段按镜头顺序上传的时序关键帧，最多 4 帧且包含上一段尾帧（如有）：@[SHOT02关键帧引用]=本段 SHOT02 关键帧；@[SHOT04关键帧引用]=本段 SHOT04 关键帧；[继续列到已选上传关键帧]。它们只作为时间顺序、画面状态和动作节拍参考，共同用于理解 15 秒内的连续视频节奏；不要生成分屏、漫画格、幻灯片、拼贴画面或图片序列。未上传的关键帧不作为参考图引用，其动作内容已合并进相邻镜头文字。

@[角色A引用] 是[角色A]角色参考图。@[角色B引用] 是[角色B]角色参考图。

@[场景引用] 是[场景名]干净场景参考，只用于理解空间结构、光线、色调、材质和环境氛围，不能被画成参考图、地图、图解、标注、画中画、九宫格或拼贴。

@[道具引用] 是[道具名]关键道具参考，只在角色使用、展示、争夺、激活或观察该道具时出现。[没有上传关键道具时删除本行。]

@[未来场景省略说明] 不作为本段上传图片；如果它只是下一段目的地或尾帧暗示，只在对应镜头文字中写成[下方远处灯影/入口方向/空间深度]。[没有省略未来场景时删除本行。]

@[音频1引用] 是[角色A]在[镜头/动作节拍]的可见对白音频，台词为 `{[台词1]}`；只用于[表演/口型/语速/节奏要求]。

@[音色参考1引用] 是[角色A]的音色参考；[角色A]所有可见对白保持这个音色。仅在用户已上传或项目已锁定音色参考并需要 Seedance 参考时写入。



【视频内容】

请生成一段 16:9、15 秒、单一连续视频/连续剪辑：

镜头 1：[摄像机运动/剪辑变化]，[主体主要动作和表情]，[空间位置或环境变化]，[音频：如有可见角色对白，写成 `[角色]说 {台词}` 并口型匹配 @[对应音频引用]；没有上传音频时不要强写口型；环境声保持轻微，复杂音效后期补]。

镜头 2：[摄像机运动/剪辑变化]，[主体主要动作和表情]，[空间位置或环境变化]，[音频：如有可见角色对白，写成 `[角色]说 {台词}` 并口型匹配 @[对应音频引用]；没有上传音频时不要强写口型；环境声保持轻微，复杂音效后期补]。

镜头 3：[继续按故事顺序写下一动作节拍；先写主要动作，再写次要动作；动作细节尽量落到手、腿、头、肩膀、眼神、嘴部、呼吸等具体部位，并写清速度、幅度或力度]。

[继续写到本段第4个镜头节拍，对应SHOT04。不要写精确秒数或“在第几秒时”。]



【连续性要求】

人物、场景和道具保持上传参考图一致。[角色A连续性锁点]；[角色B连续性锁点]。[关键道具限制]。[场景地标、材质、光线锁点]。不要新增无关角色，不要把关键帧画成分屏/拼贴/幻灯片/图片序列，不要把场景参考画成九宫格、俯视地图、参考图拼贴、说明图或画中画。

no music. no subtitles.

不要在视频画面中出现文字信息。
```

Template rules:

- Keep the three headers exactly: `【参考内容说明】`, `【视频内容】`, `【连续性要求】`.
- Keep blank-line spacing; it makes reference roles and timing easier to audit before paid submit.
- The ordered keyframes must match the shot script order and the manifest upload slots.
- The ordered keyframes must satisfy the slot's current visual requirement. Do not reuse a superseded representative frame after a user correction just because it is still approved as a historical keyframe.
- Use actual uploaded reference IDs in every `口型匹配 @...` sentence, and include the same spoken line in `{...}` when the character dialogue is meant to be visible/synchronous in the video.
- Scene refs must be clean single scene images whenever possible. Do not use scene atlases, nine-grids, maps, contact sheets, review pages, labels, picture-in-picture, or collage images as formal Seedance refs.
- Bind every selected Mimo audio file to a role, line, story beat, and performance use.
- If voice/timbre references are uploaded or locked for Seedance consistency, bind each `音色参考` to the character that should use it.
- 每个镜头节拍按 `摄像机 -> 主体 -> 空间 -> 音频` 写全；动作尽量包括具体身体部位、幅度、速度或力度。
- 没有对白音频的镜头，省略音频引用和口型匹配句。
- Do not write narration/voiceover text in the video prompt when that narration belongs to `audio_for_postmix/`.
- Always include `no music` and `no subtitles` before the final no-text sentence.
- The final sentence must remain exactly `不要在视频画面中出现文字信息。`

If a segment is an explicit sequence start, `previous_tail_frame` may be blank when the manifest records `sequence_start` or a locked opening/start anchor. For first segments, upload `SHOT01` keyframe as the first keyframe reference.

## Submission Checks

Before paid Seedance generation through the local `dreamina` CLI, check:

- `dreamina -h`
- `dreamina multimodal2video -h`
- `dreamina user_credit`
- manifest records `execution_provider: dreamina_cli`
- selected submission mode is `智能多帧/多模态参考`; if the user needs exact first/last-frame matching, switch to `首尾帧` mode instead of mixing modes
- audio duration and total uploaded audio duration fit the active provider limit; for Seedance 2.0 multimodal reference, upload at most 3 audio clips with total duration no more than 15 seconds
- if video references are uploaded, use at most 3 video clips with total referenced duration no more than 15 seconds
- audio is not submitted alone; at least one image or video reference is present
- image reference counts fit the active Seedance limit; image count must be 9 or fewer
- image slots are not filled by habit; packages with 8-9 images must explain why every image is needed
- uploaded images are clean keyframes/references, not grids, collages, contact sheets, review pages, storyboards, watermarked images, or UI screenshots
- the expected previous tail frame exists and is usable for every non-first adjacent segment
- every uploaded keyframe is approved and mapped to its shot ID
- no uploaded image, package, prompt, or approval page is marked superseded, retired, rejected, or forbidden in the current project manifest
- ratio is 16:9
- video resolution is explicitly `720p` unless the user chose another resolution
- model version is explicitly `seedance2.0` unless the user chose another model, such as `seedance2.0_vip`

After download, check:

- raw Seedance output is preserved by `submit_id`
- Seedan `1080p` upscale exists
- Seedan `60fps` output exists after the `1080p` upscale
- the organized episode video and extracted tail frame come from the `1080p/60fps` output

## Dreamina CLI Execution

The content route remains Seedance 2.0 `智能多帧/多模态参考`; Dreamina/即梦 is the mandatory local CLI execution layer for submit, query, and download. Do not use Dreamina/即梦 for still-image generation or restore older Dreamina-specific still-image workflows.

Use `dreamina multimodal2video` for the default formal route:

```bash
dreamina multimodal2video \
  --image="uploads/SXXEXX_SEGXXX/图片1_上一段尾帧.png" \
  --image="uploads/SXXEXX_SEGXXX/图片2_SHOT02关键帧.png" \
  --image="uploads/SXXEXX_SEGXXX/图片3_SHOT03关键帧.png" \
  --image="uploads/SXXEXX_SEGXXX/图片4_SHOT04关键帧.png" \
  --image="uploads/SXXEXX_SEGXXX/图片5_主角参考.png" \
  --image="uploads/SXXEXX_SEGXXX/图片6_干净场景参考.png" \
  --image="uploads/SXXEXX_SEGXXX/图片7_关键道具参考.png" \
  --audio="uploads/SXXEXX_SEGXXX/音频1_角色对白.wav" \
  --prompt="$(cat prompts/00_seedance多功能参考提示词.txt)" \
  --duration=15 \
  --ratio=16:9 \
  --video_resolution=720p \
  --model_version=seedance2.0 \
  --poll=30
```

PowerShell equivalent:

```powershell
$prompt = Get-Content "prompts\00_seedance多功能参考提示词.txt" -Raw
dreamina multimodal2video `
  --image="uploads\SXXEXX_SEGXXX\图片1_上一段尾帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片2_SHOT02关键帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片3_SHOT03关键帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片4_SHOT04关键帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片5_主角参考.png" `
  --image="uploads\SXXEXX_SEGXXX\图片6_干净场景参考.png" `
  --image="uploads\SXXEXX_SEGXXX\图片7_关键道具参考.png" `
  --audio="uploads\SXXEXX_SEGXXX\音频1_角色对白.wav" `
  --prompt="$prompt" `
  --duration=15 `
  --ratio=16:9 `
  --video_resolution=720p `
  --model_version=seedance2.0 `
  --poll=30
```

Build the command only from the approved upload package and actual upload order. Record the command, prompt path, model, duration, input paths, `submit_id`, `logid` when available, credit/cost note, and queue status in the project manifest or video execution table. Query and download with:

```bash
dreamina query_result --submit_id=<submit_id> --download_dir=<download_dir>
```

If the CLI returns `AigcComplianceConfirmationRequired`, stop and ask the user to complete the Dreamina Web authorization confirmation before retrying. Do not fall back to web upload silently.

## Boundary Continuity

Within an episode:

```text
SXXEXX_SEG001 tail frame -> SXXEXX_SEG002 @图片1 / SHOT01
SXXEXX_SEG002 tail frame -> SXXEXX_SEG003 @图片1 / SHOT01
```

Across 4+1 agent boundaries, the controller owns the boundary:

- Agent A handles EP01-EP05.
- Agent B handles EP06-EP10.
- During batch production, the controller can define EP06's opening first-frame plan or placeholder boundary anchor for script/package prebuild only.
- During video execution, EP06's real opening frame must come from EP05's actual extracted tail frame or a controller/user-approved start anchor.
- Both workers must use that same boundary file/hash.

Workers must not invent cross-episode tail/start frames independently.

Temporary no-tail rule: a missing expected tail frame blocks video generation. Do not replace it with a copied keyframe, a newly generated bridge frame, or a newly invented "extracted tail"; wait for the real tail frame or a controller/user-approved start anchor.

## Manifests

Every current package manifest should record `execution_provider: dreamina_cli` before it can be marked ready for video submit.

Every current package manifest should record:

| Field | Meaning |
|---|---|
| `route` | `keyframe_multiref_seedance` |
| `execution_provider` | `dreamina_cli`; formal video submit/query/download must use local `dreamina` CLI |
| `seedance_submission_mode` | `智能多帧/多模态参考` unless the user explicitly chose `首帧` or `首尾帧` |
| `segment_id` | `SXXEXX_SEGXXX` |
| `duration` | usually `15` |
| `previous_tail_frame` | path/hash; `null` only for explicit sequence starts or locked start-anchor exceptions |
| `keyframe_references` | ordered list of shot IDs, paths, hashes, approval status, and upload slots |
| `character_refs` | current refs and hashes |
| `scene_refs` | current clean scene refs and hashes; formal Seedance refs must not be nine-grid atlases, collages, maps, contact sheets, or review pages |
| `prop_refs` | current refs and hashes |
| `image_upload_count` | actual number of uploaded images; explain why if using 8-9 images |
| `video_reference_count` | actual number of uploaded video refs, with total duration when used |
| `audio_for_video` | Mimo files, duration, text, role |
| `audio_upload_count` | actual number of uploaded audio clips and total uploaded duration |
| `audio_for_postmix` | non-video-driving audio |
| `prompt_path` | exact prompt file |
| `submit_id` | after submit |
| `raw_video_path` | after download |
| `seedan_1080p_video_path` | after Seedan resolution upscale |
| `seedan_60fps_video_path` | after Seedan frame-rate enhancement; current source for episode copy and tail frame |
| `episode_video_path` | organized review copy |
| `tail_frame_path` | extracted for next segment |
| `status` | draft / ready_to_submit / submitted / downloaded / accepted / retake / 视频阻塞-缺上一段尾帧 |
| `superseded_by` / `retired_usage` | when applicable, the active replacement package or the reason a prior image-slot mapping must not be reused |

## Retake Rules

Retake or rebuild the package if:

- the video starts far from the supplied previous-tail frame;
- the package mixed `首帧` / `首尾帧` / `智能多帧` assumptions or used the wrong mode for the continuity goal;
- the uploaded reference set is too crowded and causes subject drift, style conflict, or unclear action priority;
- any formal uploaded image is a nine-grid, collage, contact sheet, storyboard board, review gallery, watermarked image, UI screenshot, or label-heavy reference sheet;
- the output looks like a grid, split screen, contact sheet, slideshow, image sequence, or labeled UI;
- character face, hair, outfit, body silhouette, or signature prop drifts;
- scene geography flips or loses its main landmarks;
- dialogue audio is ignored, desynced, or assigned to the wrong visible speaker;
- readable text, captions, subtitles, labels, watermarks, or UI text appear in-frame;
- the tail frame is unusable for the next segment.

Preferred retake order: reduce reference clutter, prioritize the previous tail/start frame plus 2-4 clearest action anchors, replace non-clean references with clean single references, simplify over-busy keyframes, strengthen continuity in one sentence, split over-busy action, then change model/route only if needed.
