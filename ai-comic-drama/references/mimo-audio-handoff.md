# Mimo Audio Handoff

Load this reference when the user chooses Mimo for audio generation.

## Contents

- [Working Assumptions](#working-assumptions)
- [API Connectivity Gate](#api-connectivity-gate)
- [Character Voice Standard Rule](#character-voice-standard-rule)
- [Voice Design Prompt Pattern](#voice-design-prompt-pattern)
- [Dialogue Prompt Pattern](#dialogue-prompt-pattern)
- [File Naming](#file-naming)
- [Audio Asset And Layer Tables](#audio-asset-and-layer-tables)
- [Mimo Audio Generation Table](#mimo-audio-generation-table)
- [Mimo Character Voice Library](#mimo-character-voice-library)
- [Quality Checks](#quality-checks)
- [Test Audio Policy](#test-audio-policy)
- [Video Submission Gate](#video-submission-gate)
- [Video Audio Package Rule](#video-audio-package-rule)

## Working Assumptions

Verify current Xiaomi MiMo / MiMo Studio / MiMo API limits when possible before generating final batch instructions. If the user's platform account shows different limits or formats, follow the user's active platform.

Use these modes:

- Built-in voice: fastest and cheapest for tests, background roles, temporary audio, and non-unique voices.
- VoiceDesign: default for original fictional characters. Use `mimo-v2.5-tts-voicedesign` to create a new voice from a text description and preserve its character voice standard file, plus voice ID if the platform returns one, for the whole project.
- VoiceClone: default for formal character dialogue. Use `mimo-v2.5-tts-voiceclone` with the locked character standard voice audio plus target text. Use only project-owned/generated voices or explicitly authorized voice samples.

Recommended environment variables:

```env
MIMO_PROVIDER=platform_api
MIMO_PLATFORM_URL=https://platform.xiaomimimo.com/
MIMO_STUDIO_URL=https://aistudio.xiaomimimo.com/
MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
MIMO_API_KEY=
XIAOMI_API_KEY=
MIMO_TTS_ENDPOINT=/chat/completions
MIMO_TTS_PAYLOAD_STYLE=chat_audio
MIMO_TARGET_SERIES=MiMo-V2.5-TTS-Series
MIMO_TTS_MODEL=mimo-v2.5-tts
XIAOMI_TTS_MODEL=mimo-v2.5-tts
XIAOMI_TTS_VOICE=mimo_default
XIAOMI_TTS_FORMAT=wav
MIMO_VOICE_DESIGN_MODEL=mimo-v2.5-tts-voicedesign
MIMO_VOICE_CLONE_MODEL=mimo-v2.5-tts-voiceclone
MIMO_DEFAULT_MODE=VoiceDesign
MIMO_DEFAULT_VOICE=mimo_default
MIMO_ALLOW_VOICE_CLONE=true
MIMO_AUDIO_FORMAT=wav
MIMO_SAMPLE_RATE=44100
MIMO_OUTPUT_DIR=assets/06_音频
```

`MIMO_API_KEY` and `XIAOMI_API_KEY` are aliases in local helper scripts; use whichever name the active console provides. Never write the actual key into this skill, source-controlled examples, manifests, or reports. Keep real keys only in a local uncommitted `.env.mimo`; examples must leave key values blank. Current project-compatible settings use the CN token-plan base URL and OpenAI-style chat-completions audio payload. Confirm `MIMO_BASE_URL`, `MIMO_TTS_ENDPOINT`, model ID, and payload fields against the user's MiMo console before batch generation. If no API key is available, create `Mimo音频生成表` and do not claim audio files exist.

## API Connectivity Gate

Before generating project audio through the API:

1. Create local `.env.mimo` from the project/template with blank key placeholders filled locally by the user.
2. Confirm the project-local helper exists if commands below are used: `tools/mimo_tts_generate.py`. This helper is not bundled with the skill; create it in the project or replace commands with the active project's Mimo tooling.
3. Run a dry run without printing secrets:

```bash
python3 tools/mimo_tts_generate.py \
  --env-file .env.mimo \
  --text "Mimo 连通性测试。" \
  --out /tmp/mimo_connectivity_probe.wav \
  --dry-run
```

4. Run one smoke-test audio only after dry-run shows `has_api_key=true` and the expected base URL/model. Save it under `assets/06_音频/99_连通性测试/` with `do_not_use` in the filename.
5. Mark smoke-test audio `non_audio_reference`, `non_final`, and never include it in formal Seedance packages.

## Character Voice Standard Rule

For every speaking character, create a reusable `角色音色标准文件` before final line generation.

Default sequence:

1. Read the character bible and generate a character voice design prompt from age, identity, temperament, speech pattern, emotional range, and forbidden voice changes.
2. Use the fixed standard line: `大家好，我是[角色名]。`
3. Use Mimo VoiceDesign with `MIMO_VOICE_DESIGN_MODEL` (default: `mimo-v2.5-tts-voicedesign`) plus the voice design prompt and fixed standard line to generate the character's voice standard audio file.
4. Save the selected standard file under `assets/06_音频/00_角色音色标准/角色名_音色标准.wav`.
5. Store the standard file path in `Mimo角色音色库`. If Mimo returns a reusable voice ID, store it too; if it does not, the standard file is still the required voice reference.
6. Generate all later dialogue, inner voice, OS, efforts, breaths, laughs, and cries with `MIMO_VOICE_CLONE_MODEL` (default: `mimo-v2.5-tts-voiceclone`) by uploading the locked character standard audio plus the target text. If the platform returns a reusable voice ID, record it too, but the locked standard audio remains the production reference.

Do not generate final character dialogue with only a text voice description when a character is meant to have a stable voice across the season. Text descriptions are allowed only before the `角色音色标准文件` exists or for temporary scratch audio. Use `mimo-v2.5-tts-voicedesign` only for character voice design / standard voice generation. Use `mimo-v2.5-tts-voiceclone` for production dialogue generation by uploading the locked standard voice audio and the target line text. Use normal TTS such as `mimo-v2.5-tts` only for background or non-character-stable audio.

VoiceDesign helper pattern:

```bash
python3 tools/mimo_tts_generate.py \
  --env-file .env.mimo \
  --voice-design \
  --text "大家好，我是[角色名]。" \
  --style "Create an original voice for [角色名]. Age impression: [年龄感]. Timbre: [声线质感]. Do not imitate any real person or celebrity." \
  --out "assets/06_音频/00_角色音色标准/角色名_音色标准_v01.wav"
```

API note: `mimo-v2.5-tts-voicedesign` must not receive an `audio.voice` field. It should receive the requested audio format only; the generated voice comes from the VoiceDesign style prompt. The local helper handles this by omitting `audio.voice` whenever `--voice-design` is used.

Generate 2-3 auditions per key role when quality matters, then have the user/controller choose one locked standard. Do not overwrite a locked standard voice file; create a new version and update the voice library.

## Voice Design Prompt Pattern

```text
Create an original voice for [角色名].
Age impression: [年龄感].
Timbre: [清亮/沙哑/低沉/温暖/冷感/磁性].
Pitch: [偏高/中低/低].
Texture: [气声/颗粒感/干净/压迫感].
Pace: [语速].
Emotion range: [可承载的情绪].
Acting style: [表演方式].
Accent: [普通话/轻微方言/无明显口音].
Do not imitate any real person or celebrity.
Sample line: [角色代表台词].
```

For the character voice standard file, the default sample line is:

```text
大家好，我是[角色名]。
```

If the user gives a project-specific standard line, use it for that project and record it in `Mimo角色音色库`; do not modify this reference for one project's wording.

## Dialogue Prompt Pattern

```text
Voice reference: [角色音色标准文件 from Mimo角色音色库].
Voice clone model: mimo-v2.5-tts-voiceclone.
Voice ID: [Mimo音色ID if available].
Character: [角色名].
Line type: dialogue / inner voice / narration / effort / breath / laugh / cry.
Emotion: [情绪].
Intensity: [1-5].
Pace: [slow / normal / fast].
Delivery: [表演要求].
Text: [台词].
Timing target: [秒数].
Output: [wav/mp3 if supported by the active platform].
```

Local helper pattern for production dialogue, assuming the project has its own `tools/mimo_tts_generate.py`:

```bash
python3 tools/mimo_tts_generate.py \
  --env-file .env.mimo \
  --voice-clone \
  --voice-reference "assets/06_音频/00_角色音色标准/角色名_音色标准.wav" \
  --text "[角色台词]" \
  --style "Character: [角色名]. Emotion: [情绪]. Pace: [语速]. Do not imitate any real person." \
  --out "assets/06_音频/SXXEXX_第XX集/SXXEXX_SEGXXX_角色名_L001.wav"
```

`--voice-clone` must use project-owned/generated standard voice audio or explicitly authorized voice samples. Never use an unauthorized real-person recording.

If the model requires a different field name for uploaded reference audio, keep the high-level rule and override the payload with `--extra-json` rather than changing the production policy.

Current API-compatible VoiceClone shape for the local helper:

- `messages[0]` must be an `assistant` message containing the exact target text to speak.
- Optional acting/style guidance goes in a `user` message.
- `audio.voice` must be a DataURL made from the locked standard voice audio, such as `data:audio/wav;base64,...`.
- `audio.format` should be the requested output format, usually `wav`.
- Do not send the reference voice only as `messages[].input_audio`; the CN token-plan endpoint rejects that shape for `mimo-v2.5-tts-voiceclone`.

## File Naming

Use stable names:

For character voice standard files:

`角色名_音色标准.wav`

`SXXEXX_SCXX_SEGXXX_角色名_L001_对白.wav`

For inner voice:

`SXXEXX_SCXX_SEGXXX_角色名_OS001_内心.wav`

For narration:

`SXXEXX_SCXX_SEGXXX_旁白_N001.wav`

For efforts and nonverbal acting:

`SXXEXX_SCXX_SEGXXX_角色名_FX001_喘息.wav`

If the platform exports another extension, keep the same basename.

## Audio Asset And Layer Tables

Use these tables when planning or auditing audio files before Mimo generation or video upload.

```markdown
# 配音音效音乐方案

使用规则：

- `audio_for_video/` 只放会影响画面口型、动作节奏或表演的 Mimo 对白。
- `audio_for_postmix/` 放旁白、BGM、环境声、音效、遮挡口型台词、无线电/远处声音。
- 正式角色对白必须引用 `正式锁定` 或 `全季锁定` 的角色音色标准；没有锁定音色时，只能标记为试听/草稿。
- 音频短于平台上传下限时，保留原始锁定文件，另做补静音上传版。

| 角色 | 声线 | 语速 | 情绪范围 | 表演禁区 | 锁定音色文件 | 状态 |
|---|---|---:|---|---|---|---|
| [角色名] | [年龄感/质感/气息] | [慢/中/快] | [冷静/紧张/崩溃上限等] | 禁止模仿真人；禁止过度播音腔/夹子音/情绪乱跳 | [path] | 待试听/小样锁定/正式锁定/全季锁定 |
```

```markdown
# 音频分层清单

| 音频用途 | 放置文件夹 | 是否上传给视频生成 | 备注 |
|---|---|---|---|
| 可见角色对白 | audio_for_video/ | 是 | 必须填写音频引用/口型要求 |
| 旁白/OS | audio_for_postmix/ | 默认否 | 除非明确需要影响画面节奏 |
| 环境声/BGM/音效 | audio_for_postmix/ | 默认否 | 后期混音使用 |
| 临时试听 | audio_temp_smoke_only/ | 否 | 不进入正式交付 |
```

```markdown
# 音频资产清单

| 音频ID | 文件路径 | 状态 | 角色/用途 | 文本 | 情绪 | 时长 | 音色ID | 使用段落 | Seedance上传版 | 生成/录制提示词 | 返修备注 |
|---|---|---|---|---|---|---:|---|---|---|---|---|
| AUD_SXXEXX_SEGXXX_001 | audio_for_video/[文件名].wav | 待生成/试听级/小样锁定/正式锁定/全季锁定/需返修 | [角色名]/可见对白 | [台词] | [情绪强度] | 0.0 | [voice_id] | SXXEXX_SEGXXX_SHOTXX | audio_for_video_upload/[文件名]_upload.wav | [Mimo生成提示词或录制说明] |  |
```

If an audio file is shorter than the active platform's upload minimum, keep the original locked file and create a padded upload copy. Record the upload copy path in `Seedance上传版`.

## Mimo Audio Generation Table

Use this table for `Mimo音频生成表`:

| 音频ID | 集/场/段 | 角色/用途 | Mimo模式 | Mimo音色ID | 音色提示词 | 台词/文本 | 情绪强度 | 目标时长 | 输出文件名 | Seedance映射 | 状态 | 返修指令 |
|---|---|---|---|---|---|---|---:|---:|---|---|---|---|

`Mimo模式` should be `Built-in Voice`, `VoiceDesign`, or `VoiceClone`.

For formal character dialogue, add/track the locked reference path in the row or adjacent notes:

```text
音色参考文件: assets/06_音频/00_角色音色标准/角色名_音色标准.wav
生成命令: 项目本地 tools/mimo_tts_generate.py --voice-clone --voice-reference ...
```

`Seedance映射` should use Chinese ordered web labels such as `@音频1`, `@音频2`, and `@音频3` after the audio is selected for a specific video segment. The matching upload package files must use the same ordered prefix, such as `音频1_旁白_N001.wav`; do not use raw audio filenames as prompt tags.

## Mimo Character Voice Library

Use this table for `Mimo角色音色库`:

| 角色 | 音色状态 | Mimo模式 | Mimo音色ID | 角色音色标准文件 | VoiceDesign提示词 | 标准台词 | 入选原因 | 禁止变化 | 适用范围 | 返修备注 |
|---|---|---|---|---|---|---|---|---|---|---|

`音色状态` values:

- `待设计`: character needs VoiceDesign prompt.
- `待生成标准音`: prompt exists, but the standard line has not been generated.
- `待确认标准音`: a standard audio file exists, but the user or agent has not selected it as the final standard.
- `已锁定`: this `角色音色标准文件`, plus `Mimo音色ID` if available, must be used for all final lines unless the user requests a recast.
- `临时`: scratch voice for tests only.

Final line audio rows in `Mimo音频生成表` should reference only `已锁定` standard files unless explicitly marked as scratch.

## Quality Checks

- Confirm every major role has one stable `角色音色标准文件` before batch dialogue generation.
- Confirm final dialogue rows use `mimo-v2.5-tts-voiceclone` with the locked standard voice audio, and `Mimo音色ID` when available, not only a descriptive prompt.
- Confirm dialogue duration fits the target video segment.
- Confirm emotional intensity matches the shot script and ordered keyframes.
- Confirm inner voice and spoken dialogue are labeled separately.
- Confirm audio filenames match the Seedance handoff table.
- Confirm no real-person imitation is requested without authorization.

## Test Audio Policy

When Mimo is selected for the project, test audio should also come from Mimo:

- Use Mimo audition files or locked character standards for pilot videos, effect review, and paid Seedance multimodal tests.
- If no Mimo output exists yet, block effect-review video generation and create the Mimo handoff table instead.
- Do not use non-Mimo throwaway audio for project tests or official manifests once Mimo is selected.

## Video Submission Gate

Before a final Seedance video task is submitted through the local `dreamina` CLI for a segment with dialogue, narration, breathing, music, or SFX, the audio handoff must provide:

- a `Mimo角色音色库` with required speaking roles locked or explicitly marked scratch-only;
- a `Mimo音频生成表` for the target segments;
- actual audio file paths, not only planned filenames;
- a separate upload copy for any audio shorter than the platform minimum;
- ordered `@音频1`, `@音频2`, `@音频3` mapping that matches the video handoff table.

If these are missing, block final dialogue video delivery and either create the audio package first or mark the run as a visual-base-only clip.

## Video Audio Package Rule

For every segment that enters Seedance multi-reference video generation, split audio by use:

| Folder | Contents | Final Rule |
|---|---|---|
| `audio_for_video/` | official Mimo dialogue files intended to influence the generated video, lips, gestures, or timing | only these files may drive video/audio timing |
| `audio_for_postmix/` | narration, breaths, SFX, ambience, masked-speaker lines, radio/filter voices, unclear-mouth dialogue | mix after generation; do not drive video timing |

Post-mix examples:

- narration and inner voice;
- running breaths and effort sounds when mouth is not visible;
- masked or helmeted speakers;
- environmental SFX, UI beeps, weapons, vehicles, rain, electricity;
- lines delivered from off-screen, back view, far shot, radio, PA, or phone.

If the mouth visibility is uncertain, place the audio in `audio_for_postmix/` and mark the video-audio decision `postmix_unclear_mouth` until a visual review says otherwise. Dedicated lip-sync repair packages are separate from the main video generation manifest.
