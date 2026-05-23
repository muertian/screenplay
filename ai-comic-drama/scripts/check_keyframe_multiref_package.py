#!/usr/bin/env python3
"""Check keyframe_multiref_seedance segment packages.

This bundled checker is intentionally structural: it verifies that a formal
package is complete enough for human visual review or paid Seedance submission
through the local Dreamina/即梦 CLI. Project-specific pixel checks can live in
project-local tools.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


FINAL_SENTENCE = "不要在视频画面中出现文字信息。"
EXPECTED_ROUTE = "keyframe_multiref_seedance"
EXPECTED_SUBMISSION_MODE = "智能多帧/多模态参考"
EXPECTED_EXECUTION_PROVIDER = "dreamina_cli"
MIN_SHOTS = 4
MAX_SHOTS = 4
SHOT_DURATION_MIN = 3.0
SHOT_DURATION_MAX = 5.0
TEMPORAL_FRAME_MAX = 4
IMAGE_SOFT_CAP = 7
IMAGE_HARD_CAP = 9
AUDIO_HARD_CAP = 3
AUDIO_TOTAL_SECONDS_MAX = 15.0
VIDEO_HARD_CAP = 3
VIDEO_TOTAL_SECONDS_MAX = 15.0
ALLOWED_MODEL_VERSIONS = {"seedance2.0", "seedance2.0_vip"}
ALLOWED_EXECUTION_PROVIDERS = {
    "dreamina_cli",
    "dreamina cli",
    "dreamina-cli",
    "dreamina_cli_seedance2",
    "jimeng_cli",
    "jimeng cli",
    "即梦cli",
    "即梦_cli",
}
APPROVED_STATES = {
    "visual_pass",
    "pass",
    "passed",
    "approved",
    "accepted",
    "confirmed",
    "locked",
    "已通过",
    "已确认",
    "已确认可用",
    "小样锁定",
    "正式锁定",
    "全季锁定",
}
RETAKE_OR_PENDING_STATES = {
    "pending",
    "pending_user_review",
    "retake",
    "retake_requested",
    "rejected",
    "fail",
    "failed",
    "needs_retake",
    "待确认",
    "尚未验收",
    "等待审片",
    "需返修",
    "未通过",
}
READY_STATUSES = {
    "ready_to_submit",
    "ready_for_video_submit",
    "submitted",
    "downloaded",
    "accepted",
    "locked",
    "正式锁定",
    "ready_for_video_submit",
}
RETIRED_STATES = {
    "retired",
    "superseded",
    "rejected",
    "failed",
    "non_current",
    "not_current",
    "非当前",
    "废案",
    "已废弃",
    "已被替代",
}
HARD_BANNED_REF_MARKERS = {
    "9grid",
    "ninegrid",
    "nine_grid",
    "atlas",
    "contact",
    "contactsheet",
    "storyboard",
    "collage",
    "review",
    "gallery",
    "screenshot",
    "ui",
    "watermark",
    "label",
    "grid",
    "九宫格",
    "拼贴",
    "分镜板",
    "故事板",
    "审片",
    "验收",
    "截图",
    "水印",
    "标签",
}
SOFT_BANNED_SCENE_MARKERS = {
    "panorama",
    "overview",
    "map",
    "topdown",
    "top_down",
    "birdseye",
    "birds_eye",
    "全景",
    "俯瞰",
    "俯视",
    "地图",
}


def load_manifest(target: Path) -> tuple[Path, dict[str, Any]]:
    if target.is_file():
        manifest_path = target
        package_dir = target.parent
    else:
        package_dir = target
        candidates = [
            package_dir / "03_PACKAGE_MANIFEST.json",
            package_dir / "PACKAGE_MANIFEST.json",
            package_dir / "manifest.json",
        ]
        manifest_path = next((p for p in candidates if p.exists()), candidates[0])
    if not manifest_path.exists():
        return package_dir, {"__missing_manifest__": str(manifest_path)}
    try:
        return package_dir, json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return package_dir, {"__json_error__": f"{manifest_path}: {exc}"}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_state(value: Any) -> str:
    if isinstance(value, bool):
        return "approved" if value else "pending"
    return str(value or "").strip().lower()


def item_value(item: Any, *keys: str) -> Any:
    if not isinstance(item, dict):
        return None
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return item[key]
    return None


def item_path_value(item: Any) -> Any:
    return item_value(item, "path", "file", "src", "source", "image_path", "audio_path", "video_path")


def slot_number(value: Any, prefix: str) -> int | None:
    if value is None:
        return None
    text = str(value)
    match = re.search(rf"(?:@?{re.escape(prefix)})(\d+)", text)
    if match:
        return int(match.group(1))
    return None


def item_slot_number(item: Any, prefix: str) -> int | None:
    if not isinstance(item, dict):
        return None
    for key in ("slot", "upload_slot", "image_slot", "audio_slot", "video_slot", "label", "ref"):
        number = slot_number(item.get(key), prefix)
        if number is not None:
            return number
    return None


def prompt_slot_numbers(text: str, prefix: str) -> list[int]:
    if not text:
        return []
    return [int(match.group(1)) for match in re.finditer(rf"@{re.escape(prefix)}(\d+)", text)]


def is_ready_for_submit(manifest: dict[str, Any]) -> bool:
    status = normalize_state(manifest.get("status"))
    return (
        status in READY_STATUSES
        or bool(manifest.get("ready_for_video_submit"))
        or bool(manifest.get("submission_ready"))
        or bool(manifest.get("submit_ready"))
    )


def is_approved_state(value: Any) -> bool:
    return normalize_state(value) in APPROVED_STATES


def is_bad_or_pending_state(value: Any) -> bool:
    return normalize_state(value) in RETAKE_OR_PENDING_STATES


def is_retired_item(item: Any) -> bool:
    if isinstance(item, dict):
        for key in ("status", "state", "approval_status", "user_approval"):
            if normalize_state(item.get(key)) in RETIRED_STATES:
                return True
        if item.get("retired") or item.get("retired_usage") or item.get("superseded_by"):
            return True
        path = str(item_path_value(item) or "")
    else:
        path = str(item or "")
    normalized_path = path.replace("\\", "/").lower()
    return any(marker in normalized_path for marker in ("/废案/", "/retired/", "/superseded/", "/old/", "/failed/"))


def resolve_path(package_dir: Path, value: Any) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if not path.is_absolute():
        path = package_dir / path
    return path


def parse_seconds(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"(\d+(?:\.\d+)?)", value)
        if match:
            return float(match.group(1))
    return None


def duration_from_timecode(value: Any) -> float | None:
    if not isinstance(value, str):
        return None
    numbers = [float(x) for x in re.findall(r"\d+(?:\.\d+)?", value)]
    if len(numbers) >= 2 and numbers[1] >= numbers[0]:
        return numbers[1] - numbers[0]
    return None


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def add_file_check(
    report: dict[str, list[str]],
    package_dir: Path,
    field: str,
    value: Any,
    required: bool = True,
) -> list[Path]:
    paths = []
    values = as_list(value)
    if required and not values:
        report["errors"].append(f"Missing `{field}`.")
        return paths
    for item in values:
        path_value = item.get("path") if isinstance(item, dict) else item
        path = resolve_path(package_dir, path_value)
        if not path:
            continue
        paths.append(path)
        if not path.exists():
            report["errors"].append(f"`{field}` file not found: {path}")
    return paths


def check_prompt(report: dict[str, list[str]], package_dir: Path, manifest: dict[str, Any]) -> str:
    prompt_value = manifest.get("prompt") or manifest.get("prompt_path")
    if isinstance(prompt_value, dict):
        prompt_value = prompt_value.get("path")
    prompt_path = resolve_path(package_dir, prompt_value)
    if not prompt_path:
        candidates = sorted((package_dir / "prompts").glob("*seedance*.*")) if (package_dir / "prompts").exists() else []
        prompt_path = candidates[0] if candidates else None
    if not prompt_path or not prompt_path.exists():
        report["errors"].append("Missing prompt file.")
        return ""
    text = prompt_path.read_text(encoding="utf-8").strip()
    if not text.endswith(FINAL_SENTENCE):
        report["errors"].append(f"Prompt must end with exact sentence: `{FINAL_SENTENCE}`")
    for header in ["【参考内容说明】", "【视频内容】", "【连续性要求】"]:
        if header not in text:
            report["warnings"].append(f"Prompt missing recommended header: {header}")
    report["passes"].append(f"Prompt checked: {prompt_path}")
    return text


def check_shots(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    shots = as_list(manifest.get("shots"))
    if not shots:
        report["warnings"].append("Manifest has no `shots` list; cannot verify 4 consecutive SHOT rows.")
        return
    found = []
    total_duration = 0.0
    duration_count = 0
    for shot in shots:
        if not isinstance(shot, dict):
            continue
        sid = shot.get("shot_id") or shot.get("id")
        if sid:
            found.append(str(sid))
        duration = parse_seconds(shot.get("duration_seconds"))
        if duration is None:
            duration = parse_seconds(shot.get("duration"))
        if duration is None:
            duration = duration_from_timecode(shot.get("timecode") or shot.get("in_segment_timecode"))
        if duration is not None:
            total_duration += duration
            duration_count += 1
    shot_count = len(found)
    expected = [f"SHOT{i:02d}" for i in range(1, shot_count + 1)]
    missing = [s for s in expected if s not in found]
    out_of_range = [s for s in found if s not in [f"SHOT{i:02d}" for i in range(1, MAX_SHOTS + 1)]]
    if shot_count != MAX_SHOTS:
        report["errors"].append(f"Shot count must be exactly {MAX_SHOTS}; got {shot_count}.")
    if missing:
        report["errors"].append(f"Shot IDs must be consecutive from SHOT01; missing: {', '.join(missing)}")
    if out_of_range:
        report["warnings"].append(f"Unexpected shot ids above SHOT04: {', '.join(out_of_range)}")
    if total_duration and total_duration > 15:
        report["errors"].append(f"Shot durations total {total_duration:g}s, above 15s.")
    if duration_count == shot_count and total_duration < 14.5:
        report["warnings"].append(f"Shot durations total {total_duration:g}s; expected about 15s for a full segment.")
    for shot in shots:
        if not isinstance(shot, dict):
            continue
        sid = shot.get("shot_id") or shot.get("id")
        duration = parse_seconds(shot.get("duration_seconds"))
        if duration is None:
            duration = parse_seconds(shot.get("duration"))
        if duration is None:
            duration = duration_from_timecode(shot.get("timecode") or shot.get("in_segment_timecode"))
        if duration is not None and not (SHOT_DURATION_MIN <= duration <= SHOT_DURATION_MAX):
            report["warnings"].append(f"{sid or 'SHOT'} duration is {duration:g}s; expected roughly 3-5s in the current 4-shot rule.")
    if not missing and shot_count == MAX_SHOTS:
        report["passes"].append(f"{shot_count} consecutive SHOT rows present.")


def check_duration(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    duration = manifest.get("duration") or manifest.get("duration_seconds")
    if duration is None:
        report["warnings"].append("Manifest has no duration field; expected 15 seconds.")
        return
    try:
        seconds = float(duration)
    except (TypeError, ValueError):
        report["errors"].append(f"Invalid duration value: {duration!r}")
        return
    if seconds > 15:
        report["errors"].append(f"Duration is {seconds:g}s; above 15s hard fail.")
    elif seconds < 15:
        if not (manifest.get("duration_exception") or manifest.get("shorter_exception_reason")):
            report["warnings"].append(f"Duration is {seconds:g}s; shorter-than-15s exception reason is missing.")
    else:
        report["passes"].append("Duration is exactly 15s.")


def check_tail(report: dict[str, list[str]], package_dir: Path, manifest: dict[str, Any]) -> None:
    is_sequence_start = bool(manifest.get("sequence_start") or manifest.get("is_first_segment"))
    previous_tail = manifest.get("previous_tail_frame")
    if isinstance(previous_tail, dict):
        previous_tail = previous_tail.get("path")
    if is_sequence_start:
        report["passes"].append("Sequence start: previous tail frame may be omitted.")
    else:
        paths = add_file_check(report, package_dir, "previous_tail_frame", previous_tail, required=True)
        for path in paths:
            if path.exists():
                report["passes"].append(f"Previous tail frame exists: {path.name} sha256={file_hash(path)[:12]}")
    tail_output = manifest.get("tail_frame_path") or manifest.get("output_tail_frame")
    if tail_output:
        paths = add_file_check(report, package_dir, "tail_frame_path", tail_output, required=False)
        for path in paths:
            if path.exists():
                report["passes"].append(f"Output tail frame recorded: {path.name} sha256={file_hash(path)[:12]}")
    else:
        status = normalize_state(manifest.get("status"))
        if status in {"downloaded", "accepted"} or manifest.get("video_downloaded"):
            report["warnings"].append("No output tail frame recorded yet; required after video download.")


def check_keyframe_references(
    report: dict[str, list[str]],
    package_dir: Path,
    manifest: dict[str, Any],
) -> None:
    shots = [shot for shot in as_list(manifest.get("shots")) if isinstance(shot, dict)]
    shot_ids = [str(shot.get("shot_id") or shot.get("id")) for shot in shots if shot.get("shot_id") or shot.get("id")]
    is_sequence_start = bool(manifest.get("sequence_start") or manifest.get("is_first_segment"))
    values = (
        manifest.get("keyframe_references")
        or manifest.get("keyframes")
        or manifest.get("ordered_keyframes")
    )
    keyframes = as_list(values)
    if not keyframes:
        report["errors"].append("Missing `keyframe_references` / `keyframes`; ordered keyframes are required for this route.")
        return

    keyframe_shots = []
    temporal_slots: list[int] = []
    for item in keyframes:
        if isinstance(item, dict):
            sid = item.get("shot_id") or item.get("id")
            if sid:
                keyframe_shots.append(str(sid))
            slot = item_slot_number(item, "图片")
            if slot is not None:
                temporal_slots.append(slot)
            approval = item_value(item, "approval_status", "user_approval", "visual_status", "decision", "status")
            if approval is None:
                report["errors"].append(f"{sid or 'keyframe'} is missing explicit user approval status.")
            elif not is_approved_state(approval):
                severity = "errors" if is_bad_or_pending_state(approval) else "warnings"
                report[severity].append(f"{sid or 'keyframe'} is not approved for video submit: {approval!r}.")
            if is_retired_item(item):
                report["errors"].append(f"{sid or 'keyframe'} points to retired/superseded/rejected usage.")
    expected = shot_ids if is_sequence_start else [sid for sid in shot_ids if sid != "SHOT01"]
    if not is_sequence_start and "SHOT01" in keyframe_shots:
        report["warnings"].append("Non-first segment keyframe list includes SHOT01; expected SHOT01 to be `previous_tail_frame`.")
    missing = [sid for sid in expected if keyframe_shots and sid not in keyframe_shots]
    if missing:
        report["errors"].append(f"Missing keyframe references for: {', '.join(missing)}")

    min_expected = len(expected) if expected else (MIN_SHOTS if is_sequence_start else MIN_SHOTS - 1)
    if len(keyframes) < min_expected:
        report["errors"].append(f"Expected at least {min_expected} ordered keyframe references; got {len(keyframes)}.")
    temporal_count = len(keyframes) if is_sequence_start else len(keyframes) + 1
    if temporal_count > TEMPORAL_FRAME_MAX:
        report["errors"].append(
            f"Temporal frame count is {temporal_count}; formal route allows at most {TEMPORAL_FRAME_MAX} including previous tail."
        )
    out_of_temporal_range = [slot for slot in temporal_slots if slot > TEMPORAL_FRAME_MAX]
    if out_of_temporal_range:
        report["errors"].append(
            "Ordered keyframe upload slots must stay within @图片1-@图片4; got "
            + ", ".join(f"@图片{slot}" for slot in sorted(set(out_of_temporal_range)))
        )

    paths = add_file_check(report, package_dir, "keyframe_references", keyframes, required=True)
    existing = [p for p in paths if p.exists()]
    if existing:
        report["passes"].append(f"{len(existing)} ordered keyframe reference files exist.")


def first_manifest_value(manifest: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = manifest.get(key)
        if value:
            return value
    return None


def manifest_items(manifest: dict[str, Any], *keys: str) -> list[Any]:
    return as_list(first_manifest_value(manifest, *keys))


def collect_image_upload_items(manifest: dict[str, Any]) -> list[Any]:
    explicit = first_manifest_value(
        manifest,
        "uploaded_images",
        "upload_images",
        "image_uploads",
        "images_for_upload",
        "seedance_images",
    )
    if explicit:
        return as_list(explicit)

    items: list[Any] = []
    previous_tail = manifest.get("previous_tail_frame")
    if isinstance(previous_tail, dict) and item_slot_number(previous_tail, "图片") is not None:
        items.append(previous_tail)
    for key in (
        "keyframe_references",
        "ordered_keyframes",
        "keyframes",
        "character_references",
        "character_refs",
        "scene_references",
        "scene_refs",
        "prop_references",
        "prop_refs",
        "trace_references",
        "trace_refs",
        "creature_references",
        "creature_refs",
        "style_references",
        "style_refs",
    ):
        for item in as_list(manifest.get(key)):
            if isinstance(item, dict) and item_slot_number(item, "图片") is not None:
                items.append(item)
    return items


def integer_value(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def duration_value(item: Any) -> float | None:
    if isinstance(item, dict):
        return parse_seconds(
            item_value(item, "duration_seconds", "duration", "seconds", "total_duration_seconds")
        )
    return None


def check_submission_mode(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    modes = as_list(first_manifest_value(manifest, "submission_modes", "seedance_submission_modes"))
    mode = first_manifest_value(manifest, "seedance_submission_mode", "submission_mode", "video_mode")
    if mode:
        modes.append(mode)
    normalized_modes = [str(item).strip() for item in modes if str(item).strip()]
    unique_modes = sorted(set(normalized_modes))
    if len(unique_modes) > 1:
        report["errors"].append("Seedance submission modes are mixed: " + ", ".join(unique_modes))
    if not unique_modes:
        severity = "errors" if is_ready_for_submit(manifest) else "warnings"
        report[severity].append(f"Missing `seedance_submission_mode`; expected `{EXPECTED_SUBMISSION_MODE}`.")
        return
    if unique_modes[0] != EXPECTED_SUBMISSION_MODE:
        report["errors"].append(
            f"Seedance submission mode must be `{EXPECTED_SUBMISSION_MODE}` for this route; got `{unique_modes[0]}`."
        )
    else:
        report["passes"].append(f"Submission mode is `{EXPECTED_SUBMISSION_MODE}`.")


def check_execution_provider(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    provider = first_manifest_value(
        manifest,
        "execution_provider",
        "video_execution_provider",
        "submit_provider",
        "provider",
    )
    normalized = normalize_state(provider)
    if not normalized:
        severity = "errors" if is_ready_for_submit(manifest) else "warnings"
        report[severity].append("Missing execution provider; formal video upload must use local `dreamina` CLI.")
    elif normalized not in ALLOWED_EXECUTION_PROVIDERS:
        report["errors"].append(f"Execution provider is `{provider}`; expected local `dreamina` CLI.")
    else:
        report["passes"].append("Execution provider is local `dreamina` CLI.")


def check_upload_image_caps_and_slots(
    report: dict[str, list[str]],
    manifest: dict[str, Any],
    prompt_text: str,
) -> None:
    image_items = collect_image_upload_items(manifest)
    declared_count = integer_value(manifest.get("image_upload_count"))
    actual_count = declared_count if declared_count is not None else len(image_items)
    if declared_count is not None and image_items and declared_count != len(image_items):
        report["errors"].append(
            f"`image_upload_count` is {declared_count}, but {len(image_items)} uploaded image rows were found."
        )
    if actual_count == 0:
        severity = "errors" if is_ready_for_submit(manifest) else "warnings"
        report[severity].append("No uploaded image list/count recorded; cannot verify @图片 slots or provider cap.")
        return
    if actual_count > IMAGE_HARD_CAP:
        report["errors"].append(f"Image upload count is {actual_count}; provider hard cap is {IMAGE_HARD_CAP}.")
    elif actual_count > IMAGE_SOFT_CAP:
        if manifest.get("image_soft_cap_exception") or manifest.get("image_count_exception_reason"):
            report["warnings"].append(f"Image upload count is {actual_count}; above project soft cap with recorded exception.")
        else:
            report["warnings"].append(f"Image upload count is {actual_count}; project soft cap is {IMAGE_SOFT_CAP}.")
    else:
        report["passes"].append(f"Image upload count {actual_count} is within the {IMAGE_SOFT_CAP}-image soft cap.")

    slots = [item_slot_number(item, "图片") for item in image_items]
    slots = [slot for slot in slots if slot is not None]
    if image_items and not slots:
        report["errors"].append("Uploaded image rows are missing explicit @图片N slots.")
    if slots:
        duplicates = sorted({slot for slot in slots if slots.count(slot) > 1})
        if duplicates:
            report["errors"].append("Duplicate image upload slots: " + ", ".join(f"@图片{slot}" for slot in duplicates))
        expected = set(range(1, max(slots) + 1))
        missing = sorted(expected - set(slots))
        if missing:
            report["errors"].append("Image upload slots are not contiguous; missing " + ", ".join(f"@图片{slot}" for slot in missing))
        if min(slots) != 1:
            report["errors"].append("Image upload slots must start at @图片1.")
        if max(slots) > IMAGE_HARD_CAP:
            report["errors"].append(f"Highest image slot is @图片{max(slots)}; provider hard cap is @图片{IMAGE_HARD_CAP}.")
        if declared_count is not None and max(slots) != declared_count:
            report["errors"].append(f"Highest image slot @图片{max(slots)} does not match `image_upload_count` {declared_count}.")

    prompt_slots = prompt_slot_numbers(prompt_text, "图片")
    if prompt_slots and actual_count and max(prompt_slots) > actual_count:
        report["errors"].append(
            f"Prompt references @图片{max(prompt_slots)}, but only {actual_count} image uploads are recorded."
        )
    if slots and prompt_slots:
        unknown = sorted(set(prompt_slots) - set(slots))
        if unknown:
            report["errors"].append("Prompt references image slots not in manifest: " + ", ".join(f"@图片{slot}" for slot in unknown))
        unused = sorted(set(slots) - set(prompt_slots))
        if unused:
            severity = "errors" if is_ready_for_submit(manifest) else "warnings"
            report[severity].append("Uploaded image slots not mentioned in prompt: " + ", ".join(f"@图片{slot}" for slot in unused))


def check_audio_video_caps(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    audio_items = manifest_items(manifest, "uploaded_audio", "audio_uploads", "audio_for_video", "audio_references")
    audio_count = integer_value(manifest.get("audio_upload_count"))
    if audio_count is None:
        audio_count = len(audio_items)
    if audio_count > AUDIO_HARD_CAP:
        report["errors"].append(f"Audio upload count is {audio_count}; provider hard cap is {AUDIO_HARD_CAP}.")
    total_audio = 0.0
    known_audio_durations = 0
    for index, item in enumerate(audio_items, 1):
        duration = duration_value(item)
        if duration is None:
            continue
        known_audio_durations += 1
        total_audio += duration
        if duration > AUDIO_TOTAL_SECONDS_MAX:
            report["errors"].append(f"Audio item {index} is {duration:g}s; single clip must not exceed {AUDIO_TOTAL_SECONDS_MAX:g}s.")
        elif duration < 2:
            report["warnings"].append(f"Audio item {index} is {duration:g}s; Seedance-driving audio is expected to be 2-15s.")
    if total_audio > AUDIO_TOTAL_SECONDS_MAX:
        report["errors"].append(f"Uploaded audio totals {total_audio:g}s; provider total cap is {AUDIO_TOTAL_SECONDS_MAX:g}s.")
    elif audio_items and known_audio_durations == len(audio_items):
        report["passes"].append(f"Uploaded audio total {total_audio:g}s is within cap.")

    video_items = manifest_items(manifest, "uploaded_videos", "video_uploads", "video_references", "video_refs")
    video_count = integer_value(manifest.get("video_reference_count"))
    if video_count is None:
        video_count = len(video_items)
    if video_count > VIDEO_HARD_CAP:
        report["errors"].append(f"Video reference count is {video_count}; provider hard cap is {VIDEO_HARD_CAP}.")
    total_video = sum(duration for duration in (duration_value(item) for item in video_items) if duration is not None)
    if total_video > VIDEO_TOTAL_SECONDS_MAX:
        report["errors"].append(f"Uploaded video references total {total_video:g}s; provider total cap is {VIDEO_TOTAL_SECONDS_MAX:g}s.")


def check_clean_references(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    for field, keys in {
        "scene reference": ("scene_references", "scene_refs"),
        "prop reference": ("prop_references", "prop_refs"),
        "trace reference": ("trace_references", "trace_refs"),
    }.items():
        for item in manifest_items(manifest, *keys):
            path_value = item_path_value(item) if isinstance(item, dict) else item
            name = Path(str(path_value or "")).name.lower().replace("-", "_")
            if any(marker in name for marker in HARD_BANNED_REF_MARKERS):
                report["errors"].append(f"Formal {field} appears to be non-clean or review/source material: {path_value}")
            elif field == "scene reference" and any(marker in name for marker in SOFT_BANNED_SCENE_MARKERS):
                report["warnings"].append(f"Scene ref may be planning/spatial material rather than clean formal upload ref: {path_value}")


def check_retired_references(report: dict[str, list[str]], manifest: dict[str, Any]) -> None:
    for key in (
        "uploaded_images",
        "upload_images",
        "image_uploads",
        "keyframe_references",
        "ordered_keyframes",
        "character_references",
        "character_refs",
        "scene_references",
        "scene_refs",
        "prop_references",
        "prop_refs",
        "trace_references",
        "trace_refs",
        "audio_for_video",
        "uploaded_audio",
    ):
        for item in as_list(manifest.get(key)):
            if is_retired_item(item):
                report["errors"].append(f"`{key}` contains retired/superseded/rejected usage: {item_path_value(item) or item}")


def confirmation_recorded(package_dir: Path, value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, dict):
        if value.get("confirmed") is True:
            return True
        if normalize_state(value.get("status") or value.get("decision")) in {"confirmed", "approved", "已确认", "已通过"}:
            return True
        for key in ("path", "confirmation_path", "decision_path"):
            path = resolve_path(package_dir, value.get(key))
            if path and path.exists():
                return True
    if isinstance(value, str):
        if normalize_state(value) in {"confirmed", "approved", "已确认", "已通过"}:
            return True
        path = resolve_path(package_dir, value)
        return bool(path and path.exists())
    return False


def check_upload_viewer(report: dict[str, list[str]], package_dir: Path, manifest: dict[str, Any]) -> None:
    viewer = first_manifest_value(manifest, "upload_package_viewer", "upload_viewer", "viewer")
    viewer_path_value = item_path_value(viewer) if isinstance(viewer, dict) else viewer
    viewer_path = resolve_path(package_dir, viewer_path_value)
    ready = is_ready_for_submit(manifest)
    if viewer_path:
        if viewer_path.exists():
            report["passes"].append(f"Upload-package viewer exists: {viewer_path}")
        else:
            report["errors"].append(f"Upload-package viewer file not found: {viewer_path}")
    elif ready:
        report["errors"].append("Ready-to-submit package is missing local upload-package viewer path.")
    else:
        report["warnings"].append("No upload-package viewer recorded yet; required before formal video submit.")

    confirmation = first_manifest_value(
        manifest,
        "upload_package_viewer_confirmation",
        "viewer_confirmation",
        "upload_viewer_confirmation",
    )
    if isinstance(viewer, dict) and not confirmation:
        confirmation = first_manifest_value(viewer, "confirmation", "confirmation_path", "decision_path", "confirmed")
    if ready and not confirmation_recorded(package_dir, confirmation):
        report["errors"].append("Ready-to-submit package is missing explicit user confirmation after upload-package viewer review.")
    elif confirmation_recorded(package_dir, confirmation):
        report["passes"].append("Upload-package viewer confirmation is recorded.")


def check_gallery_decision_json(report: dict[str, list[str]], package_dir: Path, manifest: dict[str, Any]) -> None:
    source = normalize_state(first_manifest_value(manifest, "approval_source", "keyframe_approval_source"))
    gallery_used = "gallery" in source or "keyframe-review-gallery" in source or bool(manifest.get("keyframe_review_gallery"))
    if not gallery_used:
        return
    decision_value = first_manifest_value(
        manifest,
        "keyframe_decision_json",
        "keyframe_decisions_json",
        "decisions_confirmed_path",
        "review_decision_json",
    )
    if isinstance(manifest.get("keyframe_review_gallery"), dict) and not decision_value:
        decision_value = first_manifest_value(manifest["keyframe_review_gallery"], "decision_json", "decisions_path")
    path = resolve_path(package_dir, decision_value)
    if not path or not path.exists():
        report["errors"].append("Keyframe approval came from review gallery but no durable decision JSON was found.")
    else:
        report["passes"].append(f"Review-gallery decision JSON exists: {path}")


def check_package(target: Path) -> str:
    package_dir, manifest = load_manifest(target)
    report: dict[str, list[str]] = {"errors": [], "warnings": [], "passes": []}
    if "__missing_manifest__" in manifest:
        report["errors"].append(f"Manifest not found: {manifest['__missing_manifest__']}")
    if "__json_error__" in manifest:
        report["errors"].append(f"Manifest JSON error: {manifest['__json_error__']}")
    if report["errors"]:
        return format_report(package_dir, manifest, report)

    route = manifest.get("route") or manifest.get("continuity_strategy")
    if route != EXPECTED_ROUTE:
        report["errors"].append(f"Route must be `{EXPECTED_ROUTE}`, got `{route}`.")
    else:
        report["passes"].append(f"Route is `{EXPECTED_ROUTE}`.")

    check_submission_mode(report, manifest)
    check_execution_provider(report, manifest)
    check_duration(report, manifest)
    check_shots(report, manifest)
    check_tail(report, package_dir, manifest)
    if manifest.get("storyboard_board"):
        report["errors"].append("`storyboard_board` is deprecated; use ordered `keyframe_references` instead.")
    check_keyframe_references(report, package_dir, manifest)
    add_file_check(report, package_dir, "character_references", first_manifest_value(manifest, "character_references", "character_refs"), required=True)
    add_file_check(report, package_dir, "scene_references", first_manifest_value(manifest, "scene_references", "scene_refs"), required=True)
    add_file_check(report, package_dir, "prop_references", first_manifest_value(manifest, "prop_references", "prop_refs"), required=False)
    add_file_check(report, package_dir, "audio_for_video", first_manifest_value(manifest, "audio_for_video", "audio_references"), required=False)
    prompt_text = check_prompt(report, package_dir, manifest)
    check_upload_image_caps_and_slots(report, manifest, prompt_text)
    check_audio_video_caps(report, manifest)
    check_clean_references(report, manifest)
    check_retired_references(report, manifest)
    check_gallery_decision_json(report, package_dir, manifest)
    check_upload_viewer(report, package_dir, manifest)

    if not manifest.get("model_version"):
        report["warnings"].append("Missing `model_version`; formal route should record `seedance2.0`.")
    elif str(manifest.get("model_version")) not in ALLOWED_MODEL_VERSIONS:
        report["warnings"].append(
            f"Model version is `{manifest.get('model_version')}`; current defaults are `seedance2.0` / `seedance2.0_vip`."
        )

    return format_report(package_dir, manifest, report)


def format_report(package_dir: Path, manifest: dict[str, Any], report: dict[str, list[str]]) -> str:
    segment_id = manifest.get("segment_id", package_dir.name) if isinstance(manifest, dict) else package_dir.name
    status = "FAIL" if report["errors"] else ("WARN" if report["warnings"] else "PASS")
    lines = [
        f"# keyframe_multiref_seedance Package Check",
        "",
        f"- Package: `{package_dir}`",
        f"- Segment: `{segment_id}`",
        f"- Status: `{status}`",
        "",
    ]
    for key, title in [("errors", "Errors"), ("warnings", "Warnings"), ("passes", "Passes")]:
        lines.append(f"## {title}")
        items = report[key]
        if items:
            lines.extend(f"- {item}" for item in items)
        else:
            lines.append("- None")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a keyframe_multiref_seedance segment package.")
    parser.add_argument("targets", nargs="+", help="Segment package folder or manifest JSON path.")
    parser.add_argument("--out", help="Optional markdown report path. Only valid with one target.")
    args = parser.parse_args()
    if args.out and len(args.targets) != 1:
        parser.error("--out can only be used with one target")
    reports = [check_package(Path(t).expanduser()) for t in args.targets]
    output = "\n---\n\n".join(reports)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
