#!/usr/bin/env python3
"""Build a local Seedance upload-package review viewer for Dreamina CLI submission."""

from __future__ import annotations

import argparse
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from check_keyframe_multiref_package import (
    as_list,
    collect_image_upload_items,
    first_manifest_value,
    item_path_value,
    item_slot_number,
    load_manifest,
    manifest_items,
    resolve_path,
)


def rel_or_uri(path: Path | None, base: Path) -> str:
    if not path:
        return ""
    try:
        return os.path.relpath(path, base)
    except ValueError:
        return path.as_uri()


def item_text(item: Any, *keys: str) -> str:
    if not isinstance(item, dict):
        return ""
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def normalize_item(package_dir: Path, item: Any, prefix: str, fallback_index: int) -> dict[str, Any]:
    path_value = item_path_value(item) if isinstance(item, dict) else item
    path = resolve_path(package_dir, path_value)
    slot_number = item_slot_number(item, prefix) if isinstance(item, dict) else None
    slot = f"@{prefix}{slot_number}" if slot_number else f"@{prefix}?"
    return {
        "slot": slot,
        "path": str(path) if path else "",
        "exists": bool(path and path.exists()),
        "label": item_text(item, "label", "name", "role", "type") or (path.name if path else f"{prefix}{fallback_index}"),
        "role": item_text(item, "purpose", "role", "usage", "description"),
        "shot_id": item_text(item, "shot_id", "id"),
        "duration_seconds": item_text(item, "duration_seconds", "duration"),
        "text": item_text(item, "text", "line", "dialogue", "note"),
    }


def read_prompt(package_dir: Path, manifest: dict[str, Any]) -> tuple[str, str]:
    prompt_value = first_manifest_value(manifest, "prompt", "prompt_path")
    if isinstance(prompt_value, dict):
        prompt_value = prompt_value.get("path")
    prompt_path = resolve_path(package_dir, prompt_value)
    if not prompt_path and (package_dir / "prompts").exists():
        candidates = sorted((package_dir / "prompts").glob("*seedance*.*"))
        prompt_path = candidates[0] if candidates else None
    if not prompt_path or not prompt_path.exists():
        return "", ""
    return str(prompt_path), prompt_path.read_text(encoding="utf-8")


def build_state(package_dir: Path, manifest: dict[str, Any], title: str, version: str) -> dict[str, Any]:
    image_items = collect_image_upload_items(manifest)
    audio_video_items = manifest_items(manifest, "uploaded_audio", "audio_uploads", "audio_for_video", "audio_references")
    postmix_items = manifest_items(manifest, "audio_for_postmix", "postmix_audio")
    omitted_items = manifest_items(manifest, "omitted_references", "omitted_refs", "removed_references")
    prompt_path, prompt_text = read_prompt(package_dir, manifest)
    return {
        "title": title,
        "version": version,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "package_dir": str(package_dir),
        "segment_id": manifest.get("segment_id", package_dir.name),
        "route": manifest.get("route") or manifest.get("continuity_strategy"),
        "execution_provider": (
            manifest.get("execution_provider")
            or manifest.get("video_execution_provider")
            or manifest.get("submit_provider")
        ),
        "submission_mode": manifest.get("seedance_submission_mode") or manifest.get("submission_mode"),
        "model_version": manifest.get("model_version"),
        "duration": manifest.get("duration") or manifest.get("duration_seconds"),
        "image_upload_count": manifest.get("image_upload_count") or len(image_items),
        "audio_upload_count": manifest.get("audio_upload_count") or len(audio_video_items),
        "images": [normalize_item(package_dir, item, "图片", index) for index, item in enumerate(image_items, 1)],
        "audio_for_video": [normalize_item(package_dir, item, "音频", index) for index, item in enumerate(audio_video_items, 1)],
        "audio_for_postmix": [normalize_item(package_dir, item, "后期音频", index) for index, item in enumerate(postmix_items, 1)],
        "omitted_references": [
            {
                "name": item_text(item, "name", "label", "id") or str(item),
                "path": str(resolve_path(package_dir, item_path_value(item))) if isinstance(item, dict) and item_path_value(item) else "",
                "reason": item_text(item, "reason", "omit_reason"),
                "compensation": item_text(item, "prompt_compensation", "compensation", "note"),
            }
            for item in omitted_items
        ],
        "prompt_path": prompt_path,
        "prompt_text": prompt_text,
    }


def render_table_rows(rows: list[dict[str, Any]], base: Path, image: bool = False) -> str:
    if not rows:
        return '<tr><td colspan="6">未记录</td></tr>'
    rendered = []
    for row in rows:
        path = Path(row["path"]) if row.get("path") else None
        preview = ""
        if image and path and path.exists():
            preview = f'<img class="thumb" src="{html.escape(rel_or_uri(path, base))}" alt="{html.escape(row["slot"])}" />'
        rendered.append(
            "<tr>"
            f"<td>{html.escape(row.get('slot', ''))}</td>"
            f"<td>{preview}{html.escape(row.get('label', ''))}</td>"
            f"<td>{html.escape(row.get('shot_id', ''))}</td>"
            f"<td>{html.escape(row.get('role', ''))}</td>"
            f"<td>{html.escape(row.get('duration_seconds', ''))}</td>"
            f"<td>{'存在' if row.get('exists') else '缺失'}<br><code>{html.escape(row.get('path', ''))}</code></td>"
            "</tr>"
        )
    return "\n".join(rendered)


def render_html(state: dict[str, Any], output_dir: Path) -> str:
    prompt = html.escape(state.get("prompt_text") or "未找到提示词")
    omitted_rows = state["omitted_references"]
    omitted_html = "\n".join(
        "<tr>"
        f"<td>{html.escape(row.get('name', ''))}</td>"
        f"<td>{html.escape(row.get('reason', ''))}</td>"
        f"<td>{html.escape(row.get('compensation', ''))}</td>"
        f"<td><code>{html.escape(row.get('path', ''))}</code></td>"
        "</tr>"
        for row in omitted_rows
    ) or '<tr><td colspan="4">未记录</td></tr>'
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(state['title'])}</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; background: #f6f5f0; color: #202a30; line-height: 1.55; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 28px 22px 60px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    h2 {{ margin: 30px 0 12px; font-size: 20px; }}
    .meta, .note {{ color: #5d6972; }}
    .chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 14px 0 24px; }}
    .chip {{ border: 1px solid #d6d1c5; background: #fffdfa; border-radius: 8px; padding: 5px 9px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border: 1px solid #d6d1c5; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid #e8e3d8; vertical-align: top; text-align: left; }}
    th {{ background: #ebe7dc; }}
    code, pre {{ font-family: SFMono-Regular, Consolas, "Liberation Mono", monospace; }}
    code {{ color: #53616b; overflow-wrap: anywhere; }}
    pre {{ white-space: pre-wrap; background: #172126; color: #ecf3ef; border-radius: 8px; padding: 16px; overflow: auto; }}
    .thumb {{ display: block; width: 210px; max-height: 118px; object-fit: contain; background: #111; margin-bottom: 6px; border-radius: 6px; }}
    .warn {{ background: #fff7ed; border-left: 4px solid #b45309; padding: 10px 12px; }}
  </style>
</head>
<body>
<main>
  <h1>{html.escape(state['title'])}</h1>
  <div class="meta">生成时间：{html.escape(state['built_at'])} | 包：<code>{html.escape(state['package_dir'])}</code></div>
  <div class="chips">
    <span class="chip">Segment: {html.escape(str(state.get('segment_id', '')))}</span>
    <span class="chip">Route: {html.escape(str(state.get('route', '')))}</span>
    <span class="chip">Execution: {html.escape(str(state.get('execution_provider', '')))}</span>
    <span class="chip">Mode: {html.escape(str(state.get('submission_mode', '')))}</span>
    <span class="chip">Model: {html.escape(str(state.get('model_version', '')))}</span>
    <span class="chip">Duration: {html.escape(str(state.get('duration', '')))}s</span>
    <span class="chip">Images: {html.escape(str(state.get('image_upload_count', '')))}</span>
    <span class="chip">Video Audio: {html.escape(str(state.get('audio_upload_count', '')))}</span>
  </div>
  <p class="warn">提交视频前请逐项核对：上传顺序、图片/音频是否缺失、被省略引用是否合理、最终提示词是否就是要提交的版本。确认后在项目 manifest 里记录 viewer 路径和用户确认。</p>

  <h2>上传图片顺序</h2>
  <table><thead><tr><th>槽位</th><th>预览/名称</th><th>SHOT</th><th>职责</th><th>时长</th><th>文件</th></tr></thead><tbody>
  {render_table_rows(state['images'], output_dir, image=True)}
  </tbody></table>

  <h2>视频驱动音频</h2>
  <table><thead><tr><th>槽位</th><th>名称</th><th>SHOT</th><th>用途</th><th>时长</th><th>文件</th></tr></thead><tbody>
  {render_table_rows(state['audio_for_video'], output_dir)}
  </tbody></table>

  <h2>后期音频，不上传给视频口型</h2>
  <table><thead><tr><th>槽位</th><th>名称</th><th>SHOT</th><th>用途</th><th>时长</th><th>文件</th></tr></thead><tbody>
  {render_table_rows(state['audio_for_postmix'], output_dir)}
  </tbody></table>

  <h2>省略引用</h2>
  <table><thead><tr><th>引用</th><th>省略原因</th><th>提示词补偿</th><th>文件</th></tr></thead><tbody>
  {omitted_html}
  </tbody></table>

  <h2>最终提交提示词</h2>
  <div class="note">提示词路径：<code>{html.escape(state.get('prompt_path', ''))}</code></div>
  <pre>{prompt}</pre>
</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Segment package folder or manifest JSON path.")
    parser.add_argument("--output", help="Output viewer folder. Defaults to <package>/upload_package_viewer.")
    parser.add_argument("--title", default="Seedance / 即梦CLI 上传包核对页")
    parser.add_argument("--version", default="")
    args = parser.parse_args()

    package_dir, manifest = load_manifest(Path(args.target).expanduser())
    if "__missing_manifest__" in manifest or "__json_error__" in manifest:
        raise SystemExit("Cannot build viewer: manifest is missing or invalid JSON.")
    output_dir = Path(args.output).expanduser() if args.output else package_dir / "upload_package_viewer"
    output_dir.mkdir(parents=True, exist_ok=True)
    version = args.version or datetime.now().strftime("%Y%m%d-%H%M%S")
    state = build_state(package_dir, manifest, args.title, version)
    state_path = output_dir / "UPLOAD_PACKAGE_VIEWER_STATE.json"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    confirmation_template = {
        "confirmed": False,
        "confirmed_at": "",
        "confirmed_by": "user",
        "segment_id": state["segment_id"],
        "viewer_path": str(output_dir / "index.html"),
        "note": "用户看过上传包核对页后，把 confirmed 改为 true 或另存为正式确认记录。",
    }
    (output_dir / "UPLOAD_PACKAGE_VIEWER_CONFIRMATION_TEMPLATE.json").write_text(
        json.dumps(confirmation_template, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    html_text = render_html(state, output_dir)
    html_path = output_dir / "index.html"
    html_path.write_text(html_text, encoding="utf-8")
    print(html_path.resolve().as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
