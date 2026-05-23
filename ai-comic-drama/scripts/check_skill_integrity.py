#!/usr/bin/env python3
"""Check ai-comic-drama skill routing and reference hygiene.

This checker is intentionally lightweight. It validates that the skill stays
loadable, that routed files exist, and that large references remain navigable.
It does not validate project-specific production packages; use
check_keyframe_multiref_package.py for segment packages.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TOC_HEADINGS = {"## Contents", "## 目录", "## Table of Contents"}
MAX_SKILL_LINES = 180
LONG_REFERENCE_LINES = 120

REQUIRED_PATHS = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/run-settings.md",
    "references/output-templates.md",
    "references/story-and-shot-templates.md",
    "references/imagegen-staging.md",
    "references/asset-package-tables.md",
    "references/continuity-locks.md",
    "references/mimo-audio-handoff.md",
    "references/seedance-2-handoff.md",
    "references/delivery-qc-templates.md",
    "references/quality-gates.md",
    "references/official-usage-guide.md",
    "references/user-manual-prompts.md",
    "references/user-manual-browser.html",
    "references/style-options.md",
    "scripts/build_keyframe_review_gallery.py",
    "scripts/build_user_manual_browser.py",
    "scripts/build_upload_package_viewer.py",
    "scripts/check_keyframe_multiref_package.py",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_count(text: str) -> int:
    return len(text.splitlines())


def has_toc(text: str) -> bool:
    first_lines = text.splitlines()[:60]
    return any(line.strip() in TOC_HEADINGS for line in first_lines)


def collect_routed_paths(text: str) -> set[str]:
    """Collect simple backtick/markdown references to skill-local files."""
    paths: set[str] = set()
    for match in re.finditer(r"`((?:references|scripts|agents)/[^`]+)`", text):
        candidate = match.group(1)
        if Path(candidate).suffix in {".md", ".py", ".yaml", ".yml", ".json"}:
            paths.add(candidate.replace("\\", "/"))
    for match in re.finditer(r"\]\(((?:references|scripts|agents)/[^)]+)\)", text):
        candidate = match.group(1)
        if Path(candidate).suffix in {".md", ".py", ".yaml", ".yml", ".json"}:
            paths.add(candidate.replace("\\", "/"))
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-toc",
        action="store_true",
        help="treat long reference files without a top-level contents section as errors",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUIRED_PATHS:
        if not (SKILL_ROOT / relative).exists():
            errors.append(f"missing required file: {relative}")

    skill_path = SKILL_ROOT / "SKILL.md"
    if skill_path.exists():
        skill_text = read_text(skill_path)
        if not skill_text.startswith("---"):
            errors.append("SKILL.md is missing YAML frontmatter")
        for field in ("name:", "description:"):
            if field not in skill_text.split("---", 2)[1]:
                errors.append(f"SKILL.md frontmatter missing {field}")
        skill_lines = line_count(skill_text)
        if skill_lines > MAX_SKILL_LINES:
            warnings.append(f"SKILL.md is {skill_lines} lines; target is <= {MAX_SKILL_LINES}")

        routed_paths = collect_routed_paths(skill_text)
        for relative in sorted(routed_paths):
            if not (SKILL_ROOT / relative).exists():
                errors.append(f"SKILL.md references missing path: {relative}")

        for expected in ("references/imagegen-staging.md", "references/asset-package-tables.md"):
            if expected not in routed_paths:
                errors.append(f"SKILL.md load map should route to {expected}")

    for router_name in ("references/output-templates.md",):
        router = SKILL_ROOT / router_name
        if router.exists():
            for relative in sorted(collect_routed_paths(read_text(router))):
                if not (SKILL_ROOT / relative).exists():
                    errors.append(f"{router_name} references missing path: {relative}")

    references_dir = SKILL_ROOT / "references"
    if references_dir.exists():
        for path in sorted(references_dir.glob("*.md")):
            text = read_text(path)
            lines = line_count(text)
            if lines >= LONG_REFERENCE_LINES and not has_toc(text):
                message = f"{path.relative_to(SKILL_ROOT)} is {lines} lines and has no Contents/目录 near top"
                if args.strict_toc:
                    errors.append(message)
                else:
                    warnings.append(message)

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARN: {message}")

    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"OK: skill integrity checks passed with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
