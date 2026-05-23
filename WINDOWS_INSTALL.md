# ai-comic-drama Windows 安装说明

## 安装位置

把压缩包里的 `ai-comic-drama` 文件夹复制到：

```powershell
$env:USERPROFILE\.codex\skills\ai-comic-drama
```

如果 `.codex\skills` 不存在，可以在 PowerShell 里执行：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
Copy-Item -Recurse -Force ".\ai-comic-drama" "$env:USERPROFILE\.codex\skills\"
```

## 验证

在 PowerShell 里执行：

```powershell
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\check_skill_integrity.py" --strict-toc
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\build_user_manual_browser.py"
```

如果本机没有安装 `py`，可以先在 Codex 桌面里使用内置 Python 验证；普通 PowerShell 使用前仍建议安装 Python 3 并确保 `py` 可用。

第二条命令会生成并输出本地手册页面路径：

```text
$env:USERPROFILE\.codex\skills\ai-comic-drama\references\user-manual-browser.html
```

## 重要规则

- 静态图、角色/场景/道具参考图、关键帧和返修图必须走 `$imagegen` built-in `image_gen`。
- 正式视频上传、查询、下载必须走本地 `dreamina` CLI。
- 进入故事基线、剧本、分镜、关键帧计划或多段规划前，必须先确认 `EPISODE_SPEC` 剧集规格，不能默认3分钟。
- 关键帧验收页可优先用 `$keyframe-review-gallery`；不可用时运行内置 `scripts/build_keyframe_review_gallery.py`。
- 视频提交前必须先生成上传包 viewer，并等待用户明确确认。

## Windows 依赖

- Python 3，PowerShell 中可用 `py` 命令。
- 正式视频阶段需要 `dreamina` CLI 已安装并在 `PATH` 中。
- Codex 内置 `$imagegen` 用于图片生成；不要用 Dreamina/Seedance 生成静态图。
