# Continuity Locks

Load this reference before creating or checking character references, recurring scenes, prop references, ordered keyframes, multi-reference video packages, boundary tail frames, or retakes.

## Contents

- [Core Rule](#core-rule)
- [Character Lock Block](#character-lock-block)
- [Scene Lock Block](#scene-lock-block)
- [Prop Lock Block](#prop-lock-block)
- [Keyframe Segment Unit](#keyframe-segment-unit)
- [Boundary Tail Frames](#boundary-tail-frames)
- [Audio Package](#audio-package)
- [Retake Rules](#retake-rules)

## Core Rule

Lock identity and geography before scale. A production prompt should reference current lock blocks and describe only the current action, camera, and boundary state. Long descriptive prompts are allowed for exploration, but final/batch prompts should be short and anchored.

## Character Lock Block

Create one block per recurring character and keep it current:

```markdown
# CHAR_[ID]_CONSISTENCY_BLOCK

- Current reference: [path + version + SHA-256]
- Face: [face shape, eye shape, nose/mouth, age impression]
- Hair: [style, length, color, bangs/parting, movement rule]
- Body silhouette: [height impression, proportions, build, posture]
- Wardrobe: [core outfit, materials, color blocks, exposure boundary]
- Signature prop/implant: [must appear / side / glow / shape]
- Allowed changes: [wet/dry, damage, lighting, emotion, pose]
- Forbidden drift: [face swap, hair change, outfit swap, prop loss, age drift, body distortion]
- Prompt anchor: [one compact sentence for image/video prompts]
```

Rules:

- Use the lock block, not only the asset ID, whenever a main character appears.
- User-accepted reference images override inferred descriptions.
- If the character changes outfit for story reasons, create a new wardrobe state under the same character, not a new character.
- Do not fix identity drift in lip-sync or post; retake the image/video source.

## Scene Lock Block

Create one block per recurring or geography-critical scene:

```markdown
# SCENE_[ID]_CONSISTENCY_BLOCK

- Current reference: [path + version + SHA-256]
- Geography: [levels, corridors, entrances/exits, left/right landmarks]
- Camera map: [screen direction, movement lanes, safe angles]
- Lighting/weather: [time, color, rain/fog/smoke, practical lights]
- Materials/props: [floor, walls, signs, machines, rails, doors]
- Allowed changes: [crowd density, damage, light intensity, weather]
- Forbidden drift: [location flip, impossible doorway, random landmark, color-theme swap]
- Prompt anchor: [one compact sentence for image/video prompts]
```

Rules:

- Use scene maps or multi-view references when geography matters.
- Track screen direction across adjacent segments.
- If a new angle reveals new geography, update the scene block before batching more assets.

## Prop Lock Block

Create one block per recurring, handheld, story-critical, merch-critical, or gameplay-critical prop:

```markdown
# PROP_[ID]_CONSISTENCY_BLOCK

- Current reference: [path + version + SHA-256]
- Function: [plot / gameplay / character signature / merch / UI-visible]
- Shape and scale: [silhouette, size relative to hands/body, thickness]
- Materials: [paper, cloth, metal, wood, glow, wear, damage]
- Required states: [closed/open/held/activated/damaged/empty]
- Allowed changes: [lighting, wet/dry, glow intensity, angle, small wear]
- Forbidden drift: [wrong object class, wrong scale, modernized version, readable text, missing signature detail]
- Prompt anchor: [one compact sentence for image/video prompts]
```

Rules:

- Do not use text-only prompts for common props. Generate and lock a prop reference first.
- If a prop repeatedly appears in hands, drives the plot, becomes merchandise, appears in gameplay, or affects UI, it is a required prop reference.
- A prop reference should include enough states for production: multi-view when shape matters, hand-held scale when size matters, and activated/inactive state when effects matter.
- In shot prompts, include a prop reference only when the prop is visibly held, observed, opened, activated, dropped, revealed, or contested.
- If a formal segment needs a visible common prop but no locked prop reference exists, block the submit or mark it draft-only.

## Keyframe Segment Unit

For the primary `keyframe_multiref_seedance` route:

- Each formal 15s segment must have exactly 4 shot rows and ordered temporal references matching `SHOT01` through `SHOT04`.
- Formal packages do not create or upload multi-panel storyboard boards.
- Shot 1 is the previous video's real tail frame and also the new video's first frame when a previous tail exists. Shots 2 through 4 use newly generated or approved representative keyframes.
- Keyframe inputs are current character refs, current clean scene refs, locked visible prop refs, the fixed 4-shot script, and the previous generated tail frame when available.
- The keyframes are temporal anchors only. Video prompts must say not to generate split screen, comic panels, slideshow, image sequence, labels, captions, subtitles, or readable UI.
- Every video package stores the previous generated video's tail frame when available; the next segment uses that tail frame as `@图片1`.

Minimal ordered keyframe note:

```text
上传上一段真实尾帧作为SHOT01，并按分镜脚本顺序上传本段已通过的新16:9关键帧SHOT02-SHOT04。它们只作为15秒连续视频的时间顺序和画面状态锚点；被省略的动作节拍只能合并进相邻SHOT文字，不得引用被省略图片，不得生成分屏、拼贴、幻灯片或图片序列。
```

## Boundary Tail Frames

Adjacent continuity is file/hash based:

```text
SXXEXX_SEG002 tail frame -> SXXEXX_SEG003 previous_tail_frame
```

Rules:

- Extract and store the final usable tail frame after every accepted video.
- A cross-agent boundary is controlled by the controller, not workers. For example, EP06's opening first frame can be locked as EP05's planned tail frame.
- If a generated video cannot provide a usable tail frame, retake before generating the next segment.

## Audio Package

For each segment:

- `audio_for_video/`: official Mimo dialogue files intended to influence video/lips/gesture timing.
- `audio_for_postmix/`: narration, breaths, SFX, ambience, masked speakers, unclear-mouth lines, radio/filter voices.
- `audio_temp_smoke_only/`: temporary TTS/SFX only; never final.
- A segment with no clear visible speaker should still carry Mimo audio for post-mix/subtitles, but should not force mouth movement.

Minimal video prompt ending:

```text
不要在视频画面中出现文字信息。
```

If mouth timing needs separate repair after visual approval, create a dedicated post video/audio package and keep it out of the main generation manifest.

## Retake Rules

Hard retake triggers:

- face/age/hair/body silhouette drift for a locked character;
- costume or signature prop changes without story reason;
- recurring or story-critical prop changes shape, scale, material, state, or object class without story reason;
- scene flips, impossible entrances/exits, or landmark changes;
- ordered keyframe upload mapping is wrong or contains unapproved files;
- generated video looks like a grid/split screen/slideshow/image sequence instead of a continuous video;
- previous tail frame is ignored or next tail frame is unusable;
- dialogue audio is assigned to the wrong speaker or badly desynced;
- post-mix audio is placed into `audio_for_video/` by mistake.

Record repeated failures in a retake strategy library instead of adding longer prompts blindly.
