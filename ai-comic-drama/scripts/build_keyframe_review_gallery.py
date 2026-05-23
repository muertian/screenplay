#!/usr/bin/env python3
"""Build a local keyframe review gallery for AI comic-drama packages.

The gallery is a human decision surface only. It cannot make keyframes
approved by itself; after review, persist a project-local confirmed decision
JSON and update the active manifest before any video submission.
"""

from __future__ import annotations

import argparse
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}
MANIFEST_CANDIDATES = (
    "03_PACKAGE_MANIFEST.json",
    "PACKAGE_MANIFEST.json",
    "manifest.json",
)
KEYFRAME_KEYS = (
    "review_keyframes",
    "keyframe_references",
    "ordered_keyframes",
    "keyframes",
)
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
RETAKE_STATES = {
    "retake",
    "retake_requested",
    "rejected",
    "fail",
    "failed",
    "needs_retake",
    "需返修",
    "未通过",
}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def first_value(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = item.get(key)
        if value not in (None, ""):
            return value
    return None


def normalize_state(value: Any) -> str:
    if isinstance(value, bool):
        return "visual_pass" if value else "pending"
    return str(value or "").strip().lower()


def state_to_decision(value: Any) -> str:
    state = normalize_state(value)
    if state in APPROVED_STATES:
        return "VISUAL_PASS"
    if state in RETAKE_STATES:
        return "RETAKE_REQUESTED"
    return "PENDING"


def load_manifest(target: Path) -> tuple[Path, Path | None, dict[str, Any]]:
    target = target.expanduser()
    if target.is_file():
        if target.suffix.lower() != ".json":
            return target.parent, None, {}
        return target.parent, target, json.loads(target.read_text(encoding="utf-8"))

    for name in MANIFEST_CANDIDATES:
        candidate = target / name
        if candidate.exists():
            return target, candidate, json.loads(candidate.read_text(encoding="utf-8"))
    return target, None, {}


def resolve_path(package_dir: Path, value: Any) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if not path.is_absolute():
        path = package_dir / path
    return path


def rel_or_uri(path: Path | None, base: Path) -> str:
    if not path:
        return ""
    try:
        return os.path.relpath(path, base)
    except ValueError:
        return path.as_uri()


def is_tail_or_start(item: dict[str, Any]) -> bool:
    role_text = " ".join(
        str(value or "")
        for value in (
            first_value(item, "role", "purpose", "usage", "type", "label"),
            first_value(item, "path", "file", "src", "source", "image_path"),
        )
    ).lower()
    return any(marker in role_text for marker in ("previous_tail", "tail frame", "上一段尾帧", "边界尾帧"))


def collect_manifest_keyframes(package_dir: Path, manifest: dict[str, Any], include_tail: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key in KEYFRAME_KEYS:
        for index, item in enumerate(as_list(manifest.get(key)), 1):
            if isinstance(item, dict):
                row = dict(item)
            else:
                row = {"path": item}
            if not include_tail and is_tail_or_start(row):
                continue
            rows.append(normalize_keyframe(package_dir, row, index))
    return rows


def scan_keyframe_files(package_dir: Path, include_tail: bool) -> list[dict[str, Any]]:
    scan_roots = [package_dir / "keyframes"]
    if package_dir.name.lower() == "keyframes" or not scan_roots[0].exists():
        scan_roots.append(package_dir)

    paths: list[Path] = []
    for root in scan_roots:
        if root.exists():
            paths.extend(path for path in sorted(root.rglob("*")) if path.suffix.lower() in IMAGE_EXTENSIONS)

    rows = []
    for index, path in enumerate(dict.fromkeys(paths), 1):
        name = path.name.lower()
        if not include_tail and any(marker in name for marker in ("tail", "上一段尾帧", "boundary")):
            continue
        rows.append(
            normalize_keyframe(
                package_dir,
                {
                    "path": str(path),
                    "id": path.stem,
                    "label": path.stem,
                    "status": "pending",
                },
                index,
            )
        )
    return rows


def normalize_keyframe(package_dir: Path, item: dict[str, Any], index: int) -> dict[str, Any]:
    path_value = first_value(item, "path", "file", "src", "source", "image_path")
    path = resolve_path(package_dir, path_value)
    shot_id = first_value(item, "shot_id", "shot", "id")
    decision = state_to_decision(first_value(item, "decision", "approval_status", "user_approval", "visual_status", "status"))
    return {
        "keyframe_id": str(first_value(item, "keyframe_id", "image_id", "id", "label") or f"KEYFRAME_{index:03d}"),
        "segment_id": str(first_value(item, "segment_id", "segment") or ""),
        "shot_id": str(shot_id or ""),
        "label": str(first_value(item, "label", "name", "title") or shot_id or (path.stem if path else f"Keyframe {index}")),
        "path": str(path) if path else "",
        "exists": bool(path and path.exists()),
        "decision": decision,
        "note": str(first_value(item, "review_note", "note", "retake_note", "comment") or ""),
        "camera_action": str(first_value(item, "camera_action", "shot_action", "visual_action", "action", "description") or ""),
        "performance": str(first_value(item, "performance", "character_performance", "acting", "role_performance") or ""),
        "prompt_summary": str(first_value(item, "prompt_summary", "prompt", "positive_prompt") or ""),
    }


def build_state(
    package_dir: Path,
    manifest_path: Path | None,
    manifest: dict[str, Any],
    title: str,
    include_tail: bool,
) -> dict[str, Any]:
    keyframes = collect_manifest_keyframes(package_dir, manifest, include_tail)
    if not keyframes:
        keyframes = scan_keyframe_files(package_dir, include_tail)
    return {
        "title": title,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "package_dir": str(package_dir),
        "manifest_path": str(manifest_path) if manifest_path else "",
        "segment_id": manifest.get("segment_id", package_dir.name),
        "scope": manifest.get("active_scope") or manifest.get("scope") or package_dir.name,
        "keyframes": keyframes,
    }


def render_cards(state: dict[str, Any], output_dir: Path) -> str:
    if not state["keyframes"]:
        return '<p class="empty">未找到关键帧图片。请传入段落 manifest，或把图片放在 keyframes/ 文件夹。</p>'

    cards = []
    for index, item in enumerate(state["keyframes"], 1):
        path = Path(item["path"]) if item.get("path") else None
        img = ""
        if path and path.exists():
            img = f'<img src="{html.escape(rel_or_uri(path, output_dir))}" alt="{html.escape(item["label"])}" />'
        else:
            img = '<div class="missing">图片缺失</div>'
        cards.append(
            f"""
            <article class="card" data-index="{index - 1}">
              <div class="image-wrap">{img}</div>
              <div class="card-body">
                <div class="meta">
                  <strong>{html.escape(item["label"])}</strong>
                  <span>{html.escape(item.get("segment_id") or state.get("segment_id") or "")} {html.escape(item.get("shot_id") or "")}</span>
                </div>
                <dl>
                  <dt>画面动作</dt><dd>{html.escape(item.get("camera_action") or "未记录")}</dd>
                  <dt>角色/表演</dt><dd>{html.escape(item.get("performance") or "未记录")}</dd>
                  <dt>提示词摘要</dt><dd>{html.escape(item.get("prompt_summary") or "未记录")}</dd>
                  <dt>文件</dt><dd><code>{html.escape(item.get("path") or "")}</code></dd>
                </dl>
                <div class="controls" role="group" aria-label="decision">
                  <label><input type="radio" name="decision-{index}" value="VISUAL_PASS" /> PASS</label>
                  <label><input type="radio" name="decision-{index}" value="RETAKE_REQUESTED" /> RETAKE</label>
                  <label><input type="radio" name="decision-{index}" value="PENDING" /> PENDING</label>
                </div>
                <textarea placeholder="返修备注 / 验收说明">{html.escape(item.get("note") or "")}</textarea>
              </div>
            </article>
            """
        )
    return "\n".join(cards)


def render_index(state: dict[str, Any], output_dir: Path) -> str:
    state_json = html.escape(json.dumps(state, ensure_ascii=False))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(state["title"])}</title>
  <style>
    body {{ margin: 0; background: #f6f5f0; color: #202a30; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.55; }}
    main {{ max-width: 1280px; margin: 0 auto; padding: 26px 20px 70px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; letter-spacing: 0; }}
    .subtle {{ color: #64717b; }}
    .toolbar {{ position: sticky; top: 0; z-index: 10; display: flex; flex-wrap: wrap; align-items: center; gap: 10px; margin: 18px 0; padding: 12px; border: 1px solid #d9d4c8; border-radius: 8px; background: rgba(255, 253, 250, 0.96); }}
    button {{ border: 1px solid #b9b2a3; border-radius: 8px; padding: 8px 11px; background: #fffdfa; color: #202a30; font: inherit; cursor: pointer; }}
    button.primary {{ background: #0f766e; border-color: #0f766e; color: white; font-weight: 700; }}
    .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); }}
    .card {{ overflow: hidden; border: 1px solid #d9d4c8; border-radius: 8px; background: white; }}
    .image-wrap {{ display: grid; place-items: center; aspect-ratio: 16 / 9; background: #151a1f; }}
    img {{ width: 100%; height: 100%; object-fit: contain; }}
    .missing {{ color: #f8faf9; }}
    .card-body {{ padding: 13px; }}
    .meta {{ display: flex; justify-content: space-between; gap: 10px; margin-bottom: 10px; }}
    .meta span {{ color: #64717b; }}
    dl {{ display: grid; grid-template-columns: 72px minmax(0, 1fr); gap: 6px 9px; margin: 0 0 12px; font-size: 14px; }}
    dt {{ color: #64717b; }}
    dd {{ margin: 0; overflow-wrap: anywhere; }}
    code {{ color: #53616b; font-family: SFMono-Regular, Consolas, "Liberation Mono", monospace; font-size: 12px; }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }}
    label {{ display: inline-flex; align-items: center; gap: 5px; border: 1px solid #d9d4c8; border-radius: 8px; padding: 5px 8px; background: #fffdfa; }}
    textarea {{ width: 100%; min-height: 76px; resize: vertical; border: 1px solid #d9d4c8; border-radius: 8px; padding: 8px; font: inherit; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; border-radius: 8px; padding: 14px; background: #172126; color: #ecf3ef; }}
    .empty {{ padding: 18px; border: 1px solid #d9d4c8; border-radius: 8px; background: #fffdfa; }}
  </style>
</head>
<body>
<main>
  <h1>{html.escape(state["title"])}</h1>
  <div class="subtle">范围：{html.escape(str(state.get("scope") or ""))} | 包：<code>{html.escape(state.get("package_dir") or "")}</code></div>
  <div class="toolbar">
    <button class="primary" type="button" id="save">保存到本浏览器</button>
    <button type="button" id="markPass">全部 PASS</button>
    <button type="button" id="markPending">全部 PENDING</button>
    <button type="button" id="export">导出决策 JSON</button>
    <a href="status_reader.html">打开状态读取页</a>
    <span class="subtle" id="summary"></span>
  </div>
  <section class="grid">{render_cards(state, output_dir)}</section>
  <h2>当前决策 JSON</h2>
  <pre id="jsonPreview"></pre>
</main>
<script id="state" type="application/json">{state_json}</script>
<script>
const initialState = JSON.parse(document.getElementById("state").textContent);
const storageKey = `ai-comic-drama-keyframe-review:${{initialState.package_dir}}:${{initialState.scope}}`;
const cards = [...document.querySelectorAll(".card")];
function applyState(state) {{
  cards.forEach((card, index) => {{
    const item = state.keyframes[index];
    if (!item) return;
    const radio = card.querySelector(`input[value="${{item.decision || "PENDING"}}"]`);
    if (radio) radio.checked = true;
    card.querySelector("textarea").value = item.note || "";
  }});
  refreshPreview();
}}
function collectState() {{
  const state = JSON.parse(JSON.stringify(initialState));
  state.reviewed_at = new Date().toISOString();
  state.keyframes = cards.map((card, index) => {{
    const original = state.keyframes[index] || {{}};
    const checked = card.querySelector("input:checked");
    return {{
      ...original,
      decision: checked ? checked.value : "PENDING",
      note: card.querySelector("textarea").value.trim()
    }};
  }});
  return state;
}}
function refreshPreview() {{
  const state = collectState();
  const counts = state.keyframes.reduce((acc, item) => {{
    acc[item.decision] = (acc[item.decision] || 0) + 1;
    return acc;
  }}, {{}});
  document.getElementById("summary").textContent = `PASS ${{counts.VISUAL_PASS || 0}} / RETAKE ${{counts.RETAKE_REQUESTED || 0}} / PENDING ${{counts.PENDING || 0}}`;
  document.getElementById("jsonPreview").textContent = JSON.stringify(state, null, 2);
}}
function saveState() {{
  const state = collectState();
  localStorage.setItem(storageKey, JSON.stringify(state));
  refreshPreview();
}}
function setAll(decision) {{
  cards.forEach((card) => {{
    const radio = card.querySelector(`input[value="${{decision}}"]`);
    if (radio) radio.checked = true;
  }});
  saveState();
}}
function exportJson() {{
  const state = collectState();
  const blob = new Blob([JSON.stringify(state, null, 2)], {{ type: "application/json" }});
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${{state.segment_id || "keyframes"}}_KEYFRAME_DECISIONS_CONFIRMED.json`;
  link.click();
  URL.revokeObjectURL(link.href);
}}
document.getElementById("save").addEventListener("click", saveState);
document.getElementById("markPass").addEventListener("click", () => setAll("VISUAL_PASS"));
document.getElementById("markPending").addEventListener("click", () => setAll("PENDING"));
document.getElementById("export").addEventListener("click", exportJson);
document.querySelectorAll("input, textarea").forEach((el) => el.addEventListener("input", refreshPreview));
const saved = localStorage.getItem(storageKey);
applyState(saved ? JSON.parse(saved) : initialState);
</script>
</body>
</html>
"""


def render_status_reader(state: dict[str, Any]) -> str:
    state_json = html.escape(json.dumps(state, ensure_ascii=False))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(state["title"])} - 状态读取</title>
  <style>
    body {{ margin: 0; background: #f6f5f0; color: #202a30; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif; line-height: 1.55; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 26px 20px 70px; }}
    button {{ border: 1px solid #0f766e; border-radius: 8px; padding: 8px 11px; background: #0f766e; color: white; font: inherit; cursor: pointer; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; border-radius: 8px; padding: 14px; background: #172126; color: #ecf3ef; }}
    code {{ color: #53616b; }}
  </style>
</head>
<body>
<main>
  <h1>关键帧验收状态读取</h1>
  <p>此页读取同一浏览器本地保存的 PASS / RETAKE / PENDING。把这里的 JSON 保存为项目本地确认记录后，才算可用于正式视频门禁。</p>
  <p>包：<code>{html.escape(state.get("package_dir") or "")}</code></p>
  <button type="button" id="copy">复制 JSON</button>
  <pre id="out"></pre>
</main>
<script id="state" type="application/json">{state_json}</script>
<script>
const initialState = JSON.parse(document.getElementById("state").textContent);
const storageKey = `ai-comic-drama-keyframe-review:${{initialState.package_dir}}:${{initialState.scope}}`;
const stored = localStorage.getItem(storageKey);
const state = stored ? JSON.parse(stored) : initialState;
document.getElementById("out").textContent = JSON.stringify(state, null, 2);
document.getElementById("copy").addEventListener("click", async () => {{
  await navigator.clipboard.writeText(document.getElementById("out").textContent);
  document.getElementById("copy").textContent = "已复制";
}});
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", help="Segment package folder, manifest JSON, or folder containing keyframe images.")
    parser.add_argument("--output", help="Output gallery folder. Defaults to <package>/keyframe_review_gallery.")
    parser.add_argument("--title", default="关键帧验收页")
    parser.add_argument(
        "--include-tail",
        action="store_true",
        help="Include previous-tail/start frames in the review gallery. Default excludes them.",
    )
    args = parser.parse_args()

    package_dir, manifest_path, manifest = load_manifest(Path(args.target))
    output_dir = Path(args.output).expanduser() if args.output else package_dir / "keyframe_review_gallery"
    output_dir.mkdir(parents=True, exist_ok=True)

    state = build_state(package_dir, manifest_path, manifest, args.title, args.include_tail)
    (output_dir / "KEYFRAME_REVIEW_STATE.json").write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    confirmation_template = {
        "confirmed": False,
        "confirmed_at": "",
        "confirmed_by": "user",
        "segment_id": state["segment_id"],
        "gallery_path": str(output_dir / "index.html"),
        "decision_json_path": "",
        "note": "用户提交/导出验收结果后，保存为项目本地 *_KEYFRAME_DECISIONS_CONFIRMED.json，并把 confirmed 改为 true。",
    }
    (output_dir / "KEYFRAME_REVIEW_CONFIRMATION_TEMPLATE.json").write_text(
        json.dumps(confirmation_template, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (output_dir / "index.html").write_text(render_index(state, output_dir), encoding="utf-8")
    (output_dir / "status_reader.html").write_text(render_status_reader(state), encoding="utf-8")
    print((output_dir / "index.html").resolve().as_uri())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
