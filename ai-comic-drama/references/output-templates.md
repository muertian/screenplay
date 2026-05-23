# Output Templates Router

Use this file as a compact index. Load only the reference that matches the current task.

## Contents

- Story and shot writing: `references/story-and-shot-templates.md`
- Image generation staging/source records: `references/imagegen-staging.md`
- Asset package and ordered keyframe tables: `references/asset-package-tables.md`
- Audio and Mimo handoff tables: `references/mimo-audio-handoff.md`
- Seedance delivery, final QC, batch control, locks, and tool notes: `references/delivery-qc-templates.md`

## Relative Path Index

Use project-relative paths in production tables. Keep skill-bundled script paths separate from project-local helper tools.

| Name | Path | Purpose |
|---|---|---|
| Current package | `00_当前Seedance上传包.md` | current video package index |
| Season tables | `01_第一季/` | season/episode production tables |
| Current locked assets JSON | `01_第一季/00_当前锁定资产清单.json` | active continuity and package manifest |
| Project-local tools | `工具脚本/` | optional project-specific helpers; create separately when needed |
| Skill package checker | `~/.codex/skills/ai-comic-drama/scripts/check_keyframe_multiref_package.py` | bundled formal route package checker |

## Usage

- Start with `references/run-settings.md` when scope, providers, source authority, or cost are unclear.
- Load `story-and-shot-templates.md` for season synopsis, episode hooks, detailed scripts, 15s units, shot tables, and image/video prompt skeletons.
- Load `imagegen-staging.md` for still-image tasks, source records, image asset tables, and project-local staging.
- Load `asset-package-tables.md` for clean scene refs, prop/trace refs, and fixed 4-shot ordered keyframe package tables.
- Load `mimo-audio-handoff.md` for character voice, audio asset tables, Mimo generation rows, upload copies, and video audio mapping.
- Load `delivery-qc-templates.md` for Seedance upload package tables, final video archive tables, batch control, retake strategy, scale-up confirmation, continuity tests, locked assets, and tool script notes.

## Current Focus Rules

- Each formal video unit is exactly 15s and fixed to 4 shot rows, `SHOT01-SHOT04`.
- First segment: up to 4 reviewed keyframes become the temporal frame set.
- Later segments: the previous video's real tail frame is `SHOT01`; select at most 3 new action keyframes for `SHOT02-SHOT04`.
- Ordered keyframes are direct video references, not a grid, slideshow, or target video layout.
- Do not upload review contact sheets as production references.
- The previous segment tail frame becomes the next segment start reference before formal sequential video submission.
