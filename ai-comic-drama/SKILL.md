---
name: ai-comic-drama
description: Use when creating or refining Chinese AI漫剧, 动态漫画短剧, AI短剧, or comic-video production packages, especially tasks involving character/scene continuity, locked assets, Mimo audio, 15s shot-video units, ordered keyframes, Seedance multi-reference generation, mandatory Dreamina/即梦 CLI video submission, scripts, batch production, retakes, or pilot validation.
---

# AI Comic Drama

This skill is the router and hard-gate layer for Chinese AI comic-drama production. Keep this file lean. Load detailed references only when the current task needs them.

## Core Contract

- Work in Simplified Chinese by default.
- Treat user-provided novels, outlines, scripts, references, audio, and style examples as source of truth unless the user supersedes them.
- Keep project state out of the skill. Write current choices, approved assets, scope, costs, blockers, and paths into project files such as `00_项目设定/03_当前运行设置.md`.
- Write durable artifacts to project files and summarize decisions in chat.
- Do not overwrite locked assets. Create versioned replacements, then update indexes only after acceptance.
- Keep current indexes authoritative. Retired drafts, failed outputs, and superseded material must not stay active in current package manifests.
- When the user asks to discard or isolate old cases, archive/isolate old packages and update active manifests so production scripts do not traverse them.
- Keep prompts short once references are locked. Put durable identity/body/wardrobe/prop facts in manifests and reference tables; put current action, timing, audio mapping, and essential continuity in the active prompt.

## Hard Gates

- Before story baselines, episode scripts, shot scripts, image batches, or multi-segment planning, present a compact episode-spec menu and wait for the user's explicit choice. Do not independently choose season format, episode count, target runtime, aspect ratio, platform, content boundary, delivery depth, or whether a "pilot/sample" spec differs from the final episode spec.
- Before paid generation, locked-asset replacement, current-package replacement, or multi-segment work, update the run settings contract.
- `批量生产` never includes Dreamina/即梦 CLI Seedance video submission, queue polling, downloads, Seedan processing, or tail-frame extraction. Those belong to a separate `视频提交/下载` stage with explicit active scope.
- Before any formal video submit, the user must approve every keyframe image in the active video scope. Script rows and prompts are reference material only unless the user explicitly asks to approve text.
- Before any formal video submit, build and open a local upload-package viewer with `scripts/build_upload_package_viewer.py` for the exact active segment/scope, showing actual upload order, selected images, omitted references, video audio, postmix-only audio, and the final prompt. Wait for explicit user confirmation after the viewer is shown.
- Formal video upload/query/download must use the local Dreamina/即梦 CLI: `dreamina multimodal2video` for the default Seedance 2.0 multi-reference route and `dreamina query_result` for async result download. Do not use the web UI or a separate Seedance API route.
- When keyframe approval uses a review gallery, the gallery is only a decision UI. Use `$keyframe-review-gallery` if available; otherwise run `scripts/build_keyframe_review_gallery.py`. Read submitted state and persist a project JSON confirmation before treating keyframes as approved.
- Still-image generation, retakes, edits, character/scene/prop references, and keyframes must use the system `$imagegen` skill with built-in `image_gen`. Do not route generated still-image work through Dreamina/即梦, Seedance, web UI, one-off SDK scripts, or other image providers.
- Image reference loading and project-local source records are authoritative in `references/imagegen-staging.md`.
- Character, scene, prop, trace, and clue lock requirements are authoritative in `references/continuity-locks.md`.
- Keyframe still-image prompts must follow the reference-role and continuity-bridge rule in `references/imagegen-staging.md`: each reference image has one explicit job, current-scene and visible-prop references take priority over future-scene references, and every keyframe prompt states previous-state handoff, current action, and next-shot handoff.
- Generated content must preserve entity uniqueness: one named character is not duplicated into multiple people, and one named single prop is not copied into several objects unless the script requires multiples.
- Seedance upload caps, ordered-keyframe priority, video prompt rules, Seedan processing, and tail-frame handoff are authoritative in `references/seedance-2-handoff.md`.
- Current Seedance 2.0 upload packages must follow the official-tuned rule set in `references/seedance-2-handoff.md`: fixed `SHOT01-SHOT04` / 4 temporal frames for each 15s unit, previous tail frame counted as `SHOT01` when present, 7-image project soft cap / 9-image provider hard cap, actual `@图片N` slot validation, compact ordered-keyframe wording, clean speaker/audio binding, retired-usage exclusion, current clean scene and visible story-critical prop priority, future-scene refs text-only until the character enters that scene, and no mixed `首帧` / `首尾帧` / `智能多帧` modes.

## Formal Route

The default production video route is `keyframe_multiref_seedance`, using Seedance 2.0 `智能多帧/多模态参考` unless the user explicitly chooses another mode. Load `references/seedance-2-handoff.md` for the actual formal workflow, official input caps, upload order, prompt template, provider constraints, post-download processing, and tail-frame rules. Do not duplicate those rules in this file.

## Load Map

Load only the reference needed for the current task:

| Task | Read |
|---|---|
| User copy-paste prompts and operating manual | `references/user-manual-prompts.md` |
| User asks to view/open/browse the manual | run `scripts/build_user_manual_browser.py`, then return the `file://` URL for the generated `references/user-manual-browser.html` in the current skill folder |
| Human-facing current formal workflow | `references/official-usage-guide.md` |
| Run settings, scope, cost policy, stop conditions | `references/run-settings.md` |
| File/path template router | `references/output-templates.md` |
| Story, episode structure, 15s shot scripts | `references/story-and-shot-templates.md` |
| Keyframe prompt rewriting from uploaded references and shot rows | `references/story-and-shot-templates.md`, `references/imagegen-staging.md`, and `references/continuity-locks.md` |
| Image generation staging and source records | `references/imagegen-staging.md` |
| Asset manifests and ordered keyframe package tables | `references/asset-package-tables.md` |
| Keyframe approval pages, retake notes, batch visual decisions | use `$keyframe-review-gallery` if available; otherwise run `scripts/build_keyframe_review_gallery.py` |
| Character, scene, prop, trace, and drift locks | `references/continuity-locks.md` |
| Mimo voice and dialogue handoff | `references/mimo-audio-handoff.md` |
| Seedance upload modes, 1-9 image cap, reference priority, prompt template, dialogue braces, voice/timbre refs, tail handoff | `references/seedance-2-handoff.md` |
| Pre-submit upload-package viewer | run `scripts/build_upload_package_viewer.py`, then open the generated `file://` URL and record explicit user confirmation |
| Delivery, QC, retakes, archive, final video assembly/export tables | `references/delivery-qc-templates.md` |
| Script/keyframe/video/final quality gates | `references/quality-gates.md` |
| Visual style option menus | `references/style-options.md` |

`references/output-templates.md` is only a router. Avoid deep reference chasing; open one detailed reference at a time.

## Stop And Ask

Stop for user confirmation before:

- choosing or changing episode/season specs, including project scope, episode count, per-episode target runtime, target platform, aspect ratio, content boundary, delivery depth, or pilot-vs-final runtime;
- spending Dreamina/即梦 CLI Seedance video credits;
- submitting any video segment;
- submitting more than the explicitly active segment;
- replacing locked/current assets;
- omitting a normally required character, prop, trace, or scene anchor because of provider limits;
- cloning or imitating a real voice without clear rights;
- changing model, provider, CLI execution route, duration, ratio, resolution, cost policy, or Seedance submission mode;
- using any non-`$imagegen` path for generated still images or keyframe retakes;
- promoting a raw or unprocessed video tail when the formal route requires processed handoff output.

## Verification

Before calling work ready:

- Confirm referenced files exist and JSON manifests parse.
- Confirm active keyframes were user-approved before formal video submit.
- If approval came from `$keyframe-review-gallery` or `scripts/build_keyframe_review_gallery.py`, confirm the submitted browser state was read and saved as a durable project decision JSON.
- Confirm no active package points to old cases, global generated-image cache, contact sheets, storyboard boards, or failed outputs.
- Confirm current-stage required assets and prompts satisfy their authoritative references.
- Confirm formal video packages pass `references/seedance-2-handoff.md` readiness checks, including provider caps, mode consistency, post-download processing, tail-frame handoff, retired-usage exclusion, and clean diegetic references.
- Record unresolved warnings in project logs or reports instead of hiding them.

## Maintenance

- Do not duplicate long rules in this file. Put detailed workflows in references and keep this file as trigger, routing, and hard gates.
- When provider defaults, imagegen rules, approval gates, package structure, lock levels, checker scripts, Dreamina/即梦 CLI execution, Seedance/Seedan behavior, or batch workflow change, update the relevant reference and the user-facing manual if the user will need a new prompt.
- When the user-facing manual changes, rebuild `references/user-manual-browser.html` with `scripts/build_user_manual_browser.py` before giving the local manual URL.
