# Quality Gates

Use this reference before pilot approval, continuity tests, batch production, or final delivery. The goal is not to make more paperwork; it is to prevent weak scripts, soft hooks, runtime drift, broken continuity, and mediocre final clips from entering scale production.

## Contents

- [Pass Policy](#pass-policy)
- [Episode Runtime Gate](#episode-runtime-gate)
- [Hook Gate](#hook-gate)
- [Dramatic Tension Gate](#dramatic-tension-gate)
- [Script Quality Gate](#script-quality-gate)
- [Character Intro Text Gate](#character-intro-text-gate)
- [Shot And Keyframe Gate](#shot-and-keyframe-gate)
- [Continuity Gate](#continuity-gate)
- [Final Product Gate](#final-product-gate)
- [Batch Readiness Gate](#batch-readiness-gate)
- [Scale-Up Confirmation Gate](#scale-up-confirmation-gate)

Detailed Seedance upload order, mandatory Dreamina/即梦 CLI execution, image-count cap, prompt shape, Seedan `1080p -> 60fps`, and tail-frame handoff are authoritative in `references/seedance-2-handoff.md`. This file only decides whether the current artifact passes.

## Pass Policy

Use a 1-5 score for subjective categories. Default pass line:

- `5`: lockable baseline.
- `4`: usable with minor notes.
- `3`: not batch-ready; fix before scaling.
- `1-2`: hard fail.

Hard failures override average score:

- episode has no visible first hook;
- a main character first appears in the active production scope without an approved intro text, unless the user explicitly skips it;
- episode lacks dramatic pressure, conflict, stakes, or a clear emotional/plot reversal;
- episode runtime is outside the accepted range without a recorded reason;
- ending does not create forward pull;
- a scene depends mainly on exposition that cannot be shown visually;
- any formal 15s video unit does not use exactly 4 shots without a recorded dramatic/technical exception;
- any video segment is shorter than 10 seconds without explicit exception, or longer than 15 seconds under any circumstance;
- adjacent segment boundary frames do not match;
- main character face, hair, costume, or signature prop drifts;
- final video has obvious watermark/random text, severe morphing, broken geography, unusable audio, or wrong first/last frame.
- downloaded final videos are not organized into per-episode folders, or current files do not sort by segment/shot order.

## Episode Runtime Gate

Default production target: 20 episodes per season, about 3 minutes per episode. Use project settings if they differ.

Recommended bands:

- Target: `170-190s` per episode.
- Acceptable with note: `150-210s`.
- Hard review: below `150s` or above `210s`.
- Shot density: exactly `4` shots per formal 15s unit, with each beat roughly 3-5 seconds.
- Segment plan: each Seedance clip defaults to exactly `15s`; shorter clips need a recorded story/technical exception, and any clip above `15s` is a hard fail. A 3-minute episode usually needs about 12 clips, with exceptions recorded by pacing need.

Check every episode:

| Episode | Script seconds | Shot seconds | Segment seconds | Segment count | Runtime status | Fix |
|---|---:|---:|---:|---:|---|---|

Runtime fixes:

- Too short: add visual obstacle, reaction beat, reveal setup, or consequence beat.
- Too long: cut repeated explanation, merge low-value shots, remove duplicated reaction, split into next episode if the hook improves.
- Uneven timing: move payoff or reveal closer to the episode end.

## Hook Gate

Every episode should have four pull points:

| Hook Point | Timing | Requirement |
|---|---:|---|
| Cold open | 0-5s | immediate conflict, danger, mystery, reversal, striking image, or emotionally loaded question |
| First turn | 15-30s | situation changes; protagonist must choose/react |
| Midpoint escalation | 80-110s | new cost, new information, or plan failure |
| End button | final 5-10s | cliffhanger, reversal, reveal, emotional decision, or irreversible action |

Reject hooks that are only atmosphere, lore, vague mood, or a character thinking without a visual problem.

## Dramatic Tension Gate

Every episode and every major scene needs pressure. Do not accept a scene whose only function is explanation, travel, mood, or setup.

Required tension sources:

- desire: what the character wants right now;
- obstacle: who or what blocks it;
- stakes: what gets worse if they fail;
- turn: what changes by the end of the scene;
- visible pressure: a choice, deadline, threat, reveal, pursuit, betrayal, temptation, loss, or irreversible action.

Tension audit table:

| Episode/Scene | Desire | Obstacle | Stakes | Turn | Visible pressure | Score | Fix |
|---|---|---|---|---|---|---:|---|

Hook audit table:

| Episode | Cold open | First turn | Midpoint escalation | End button | Score | Required fix |
|---|---|---|---|---|---:|---|

## Script Quality Gate

For each episode, confirm:

- protagonist has a concrete visible goal;
- every main character's first appearance has a compact intro text or an explicit skip note;
- scene conflict is externalized into action, pressure, choice, or obstacle;
- dialogue changes the situation rather than explaining what the viewer already sees;
- each scene has a turn: new information, new danger, new cost, relationship shift, or irreversible decision;
- visual motifs, props, wounds, knowledge, and emotional states match continuity files;
- every important beat can be staged in image/video form.

Scene audit table:

| Scene | Goal | Conflict | Turn | Visualizable action | Dialogue risk | Continuity risk | Status |
|---|---|---|---|---|---|---|---|

Common fixes:

- Replace exposition with a visible object, action, alert, interruption, wound, or choice.
- Compress repeated emotional beats into one stronger reaction.
- Move backstory after the viewer has a present-tense reason to care.
- Give minor scenes a practical function: reveal, obstacle, cost, setup, payoff, or relationship change.

## Character Intro Text Gate

For every main character first appearance:

- the intro text uses current user-provided/locked character facts;
- the text states only what the viewer should know at that moment: identity, role, relationship, visible trait, immediate desire, pressure, or dramatic function;
- the line is visually stylish and concise, usually 12-36 Chinese characters or 1-2 short narration sentences;
- the presentation method is specified: subtitle, title card, dossier/card UI, narration, or graphic overlay;
- typography/color/material notes match the visual style bible;
- it avoids spoilers, lore dumps, generic biography, and facts contradicted by the script;
- readable text is planned as post-production overlay/subtitle/title-card material unless a reliable typography workflow is already proven.

Intro text audit table:

| Character | First appearance | Text | Style match | Spoiler risk | Overlay/audio plan | Status | Fix |
|---|---|---|---|---|---|---|---|

## Shot And Keyframe Gate

For every shot script:

- each formal 15s segment has exactly 4 shot rows, numbered consecutively from `SHOT01` through `SHOT04`;
- keyframe/upload order is explicit and follows the actual shot order; do not create filler frames to force six shots;
- in-segment timecodes cover the segment without gaps or overlaps and never exceed 15 seconds total;
- the first segment's `SHOT01` is an approved episode start keyframe; later segments' `SHOT01` is the previous video's real tail frame;
- each shot has a clear dramatic/hook function, not only a camera description;
- shot duration is plausible for the action;
- shot count is fixed at `4` per 15s unit; merge extra story beats into the previous or next shot text instead of adding upload frames;
- shot size changes serve comprehension or emotion;
- camera movement is simple enough for AI video generation;
- geography is clear: entrances, exits, screen direction, landmarks, and character positions;
- each shot has one primary action, not a pile of simultaneous details;
- dialogue/audio aligns with visible mouth, reaction, or narration timing;
- if a shot uses video-driving dialogue audio, the audio reference, speaker, line, and lip-sync timing are explicit;
- every non-inherited shot has keyframe path/status and user approval state before formal video submit;
- role, scene, prop, trace, previous-tail, and audio references are explicit enough to build the segment package without guessing;
- character intro/subtitle plans are treated as post-production overlay/narration plans, not as text to render inside the generated video;
- visual forbidden items are explicit enough to protect against text, UI, duplicate characters, cloned unique props, reference sheets, grids, and unrelated entities;
- high-risk shots are marked for simplification, split, or reference strengthening.

Shot/keyframe audit table:

| Segment | Shot | Upload order | Timecode | Duration | Dramatic function | Visual action | Camera | Geography | Audio/lip-sync | Required references | Keyframe status | User approval | Forbidden visuals | AI risk | Status |
|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|

Shot density audit:

| Episode/Scene | Duration seconds | Shot count | Shots per minute | Target band | Status | Fix |
|---|---:|---:|---:|---|---|---|

For segment planning, each segment must have:

- duration normally `15s`; shorter exceptions need a recorded reason; `>15s` is a hard fail and must be split;
- exactly 4 shot rows and a script-specific beat plan;
- entry frame or previous tail frame;
- approved source frames matching the 4-shot unit: first segment has up to 4 approved keyframes; later segments have the previous tail frame plus up to 3 approved new keyframes;
- ordered keyframe references matching the kept 4 temporal frames; no formal multi-panel storyboard board and no citation of omitted keyframes;
- exit/tail-frame target for the next segment;
- character hard locks;
- scene hard locks, preferably clean single scene references; atlases, maps, contact sheets, review pages, and panoramas are internal planning/source material, not formal Seedance image refs;
- visible prop/trace hard locks;
- audio/dialogue timing;
- retake strategy if the motion fails.

## Continuity Gate

Check continuity at four levels:

| Level | What to Check | Hard Fail |
|---|---|---|
| Character | face, hair, age, body, costume, prop, injury, voice | identity drift, outfit swap, prop disappears |
| Scene | geography, light, weather, screen direction, entrances/exits | location flips, impossible movement, lighting jump without reason |
| Story | knowledge, motivation, relationship, wounds, timeline | character knows/forgets wrong information |
| Segment boundary | previous extracted tail frame and next start reference same path/hash when used | mismatch or untracked boundary |

Perform file/hash checks for boundary frames, then visually review the first and last seconds of generated videos.

Continuity score table:

| Item | Character | Costume/prop | Scene geography | Lighting | Action cause/effect | Audio | Score | Fix |
|---|---:|---:|---:|---:|---:|---:|---:|---|

## Final Product Gate

Do not call a clip final until it passes:

| Dimension | Pass Standard |
|---|---|
| First frame | matches supplied first frame closely enough for continuity |
| Last frame | approaches supplied last frame closely enough for next segment |
| Character | face, hair, costume, signature prop stable |
| Motion | action is readable, not chaotic or smeared |
| Camera | movement supports the scene and does not random-cut |
| Scene | geography and lighting remain coherent |
| Audio | correct file, intelligible speech, no clipping, useful ambience/music |
| Prompt artifacts | no random text, watermark, split-screen, collage, or reference-frame layout |
| Hook/pacing | clip advances the episode hook, reversal, or end button |
| Delivery | raw video path, organized episode video path, manifest, report, and retake notes are recorded |

Episode video archive checks:

- every episode has one folder, default `assets/07_视频分段/SXXEXX_第XX集/`;
- current playable files are named in segment order, such as `SXXEXX_SEG001_v01.mp4`, `SXXEXX_SEG002_v01.mp4`;
- raw Seedance downloads remain traceable by `submit_id`;
- each raw download has a Seedan `1080p` upscale output and then a Seedan `60fps` output; current episode files use the `1080p/60fps` version;
- each segment has exactly one current organized episode video path;
- retakes use `_v02`, `_v03`; superseded files are moved to backup or clearly marked non-current.

Final clip review table:

| Segment | First frame | Last frame | Character | Scene | Motion | Audio | Artifacts | Dramatic value | Verdict | Retake action |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|

Verdicts:

- `锁定`: can be used as baseline.
- `可用-小修`: usable after prompt/asset note.
- `需返修`: regenerate before batch or final delivery.
- `非当前`: do not use in current package or index.

## Batch Readiness Gate

Before large-scale production:

- scale-up confirmation table is complete and has no unresolved blocking items such as `待确认`, `需返修`, or `缺失` for the active scope;
- generated still-image provider is locked to `$imagegen` built-in `image_gen`, and promoted keyframes/references have `$imagegen` source records;
- season novel/story baseline is accepted or explicitly marked as the current draft baseline;
- main character reference sheets are accepted, current, and protected from overwrite;
- key recurring scene top-down maps and scene reference images are accepted;
- visual style bible is accepted and matches current character/scene references;
- episode beat map and key hooks are accepted for the batch range;
- at least one pilot segment is accepted;
- 2-3 adjacent segments pass continuity review;
- episode runtime and hook tables are complete for the batch range;
- locked character/scene/audio references exist;
- Seedance model policy is explicit;
- video execution provider is explicit and set to local `dreamina` CLI;
- all workers have write scopes and cannot edit official shared files directly;
- `批量生产总控表` shows no unresolved blocker for locked assets, scripts, segment plans, upload-package readiness, or generation route. It must not treat submitted videos, downloaded videos, or extracted tail frames as part of batch production.

## Scale-Up Confirmation Gate

Use this before any large writing pass, many image generations, batch upload-package production, full-episode production, full-season production, or parallel agent work. Many video submissions are a separate `视频提交/下载` run.

Required confirmations:

| Anchor | Must Confirm | Blocking If Missing |
|---|---|---|
| User source inventory | user-provided novels, outlines, scripts, references, and media are indexed, classified, and mapped | all downstream adaptation and production |
| Novel/story baseline | current season novel or episode beat map is accepted enough to adapt | broad script/shot generation |
| Character references | main and recurring character reference sheets are accepted/current | character keyframes, batch images, video generation |
| Scene references | key recurring scene maps/reference images are accepted/current | scene keyframes, batch images, video generation |
| Image generation route | `$imagegen` built-in `image_gen` is the only allowed generated-still path, with source records for promoted assets | all generated references, keyframes, retakes, and video-upload stills |
| Visual style bible | palette, lens language, texture, era, and forbidden style drift are accepted | all visual generation |
| Voice/audio baseline | required voice standards or temporary audio policy are accepted | dialogue-heavy video packages |
| Video route | `keyframe_multiref_seedance`, `execution_provider: dreamina_cli`, model, 15s duration rules, fixed 4-frame ordered keyframe rule, previous-tail continuity, no-tail blocking rule, Mimo audio mapping, and cost policy are accepted | paid video generation |
| Pilot/continuity | at least one pilot and adjacent-boundary test are accepted or explicitly waived | batch upload-package production |

Confirmation table:

| Item | Current File/Asset | Status | User/Controller Decision | Blocks | Next Action |
|---|---|---|---|---|---|

Allowed statuses:

- `待确认`: unresolved; dependent broad work is blocked until a choice is made.
- `已确认可用`: can be used for the active scope.
- `当前草案可用`: acceptable for drafting, not final generation.
- `小样锁定`: usable for pilot/continuity tests, not broad production.
- `正式锁定`: reusable baseline for the active episode/batch; never overwrite in place.
- `全季锁定`: season-wide canon; replacement requires controller/user approval.
- `需返修`: cannot be used for scale-up.
- `缺失`: cannot proceed for dependent work.
- `明确跳过`: user/controller accepts the risk; record scope and reason.

Scale-up rule: if a dependency is `待确认`, `需返修`, or `缺失`, dependent work remains local/pilot only. Do not start broad generation and hope to fix it later.

Source authority rule: if user-provided material exists and is marked current, it overrides inferred, generated, or older draft material. When user material conflicts with locked assets, flag the conflict and ask only for the affected decision; do not silently blend the two.
