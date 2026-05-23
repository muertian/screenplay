# AI漫剧 Skill 使用手册

适用 skill：`ai-comic-drama`  
适用系统：Windows / macOS / Linux  
当前版本重点：图片必须用 `$imagegen`，视频上传/查询/下载必须用本地 `dreamina` CLI，剧集规格必须先确认；关键帧验收页可用内置 `build_keyframe_review_gallery.py` 兜底生成。

## 1. 安装后怎么用

把 `ai-comic-drama` 文件夹放到 Codex skills 目录：

```powershell
$env:USERPROFILE\.codex\skills\ai-comic-drama
```

在 Codex 里使用时，直接点选或提到：

```text
[$ai-comic-drama](你的技能路径/SKILL.md) 从选题开始做一个类爱死机短剧。
```

或者：

```text
用 $ai-comic-drama 推进当前项目，先读当前运行设置，不要生成图片，不要提交视频。
```

## 2. 正确启动一个项目

推荐第一句：

```text
用 $ai-comic-drama 从选题开始做一个原创成人向科幻寓言短剧。先给我选题池，不要写剧本，不要生成图片，不要提交视频。
```

选定题材后，必须先确认剧集规格：

```text
我选第 2 个题材。先给我剧集规格选项，不要默认 3 分钟。
```

规格选项通常包括：

| 规格      | 适合什么            |
| ------- | --------------- |
| 90秒概念短片 | 快速验证一个强反转       |
| 3分钟黄金样片 | 验证图像和视频链路       |
| 5-7分钟单集 | 更完整的短剧单集        |
| 10分钟+正片 | 更接近成人向动画短片      |
| 自定义     | 由你指定时长、集数、画幅和平台 |

## 3. 标准推进顺序

不要一上来就让它生成全套。推荐按这个顺序推进：

1. 选题池
2. 剧集规格确认
3. 一句话故事
4. 世界观规则
5. 人物设定
6. 单集大纲
7. 15秒视频单元拆分
8. 分镜头脚本
9. 角色/场景/道具锁定表
10. `$imagegen` 参考图任务表
11. `$imagegen` 关键帧
12. 关键帧 review gallery / 人工验收（没有 `$keyframe-review-gallery` 时用内置脚本兜底）
13. Seedance 上传包 viewer
14. 用户明确确认后，才用 `dreamina` CLI 提交视频

## 4. 常用提示词

### 从选题开始

```text
用 $ai-comic-drama 从选题阶段重新开始。给我 10 个原创类爱死机短剧选题，偏成人向科幻寓言。只做选题，不写剧本，不生成图片。
```

### 确认剧集规格

```text
用 $ai-comic-drama 给当前选题做剧集规格菜单。必须包含单集时长、集数、画幅、平台、内容边界、交付深度。等我选择后再继续。
```

### 写故事基线

```text
用 $ai-comic-drama 按已确认的 EPISODE_SPEC 写故事基线。只写一句话故事、主题、角色功能、世界规则和结尾反转，不写完整分镜。
```

### 写分镜

```text
用 $ai-comic-drama 按当前运行设置写分镜。每个正式 15 秒视频单元固定 4 个 SHOT，后续段 SHOT01 必须等上一段真实尾帧。不要生成图片。
```

### 生成图片任务表

```text
用 $ai-comic-drama 生成 $imagegen 图片任务表。角色、场景、道具、关键帧都必须标注 provider 为 $imagegen_builtin_image_gen。不要调用 dreamina。
```

### 准备视频上传包

```text
用 $ai-comic-drama 为当前已验收关键帧准备 Seedance 多模态参考上传包。只生成上传包和 viewer，不提交视频。
```

### 生成关键帧验收页

```text
用 $ai-comic-drama 为当前段落制作关键帧验收网页。优先用 $keyframe-review-gallery；如果不可用，运行 scripts/build_keyframe_review_gallery.py。只展示关键帧图片，保存 PASS/RETAKE/PENDING 决策，不提交视频。
```

### 提交视频前确认

```text
用 $ai-comic-drama 打开上传包 viewer 给我检查。等我明确说“确认提交”后，才允许用 dreamina CLI 提交当前段。
```

## 5. 必须遵守的硬规则

- 不确认 `EPISODE_SPEC`，不能继续完整剧本、分镜、关键帧计划或多段规划。
- 静态图、参考图、关键帧、返修图只能用 `$imagegen`。
- Dreamina/即梦不能用于静态图生成。
- 视频上传、查询、下载必须用本地 `dreamina` CLI。
- 批量生产不包含视频提交、查询、下载、Seedan 处理或尾帧抽取。
- 正式视频提交前，必须先验收当前范围内所有关键帧。
- 关键帧验收网页只是决策 UI，必须把结果保存为项目本地 `*_KEYFRAME_DECISIONS_CONFIRMED.json` 后才算正式通过。
- 正式视频提交前，必须生成并打开上传包 viewer。
- 后续段落的 `SHOT01` 必须来自上一段真实视频尾帧，不能用提示词伪造。
- 旧草稿、失败图、联系表、拼图板、全局缓存图不能直接进入正式 manifest。

## 6. Windows 常用命令

验证 skill：

```powershell
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\check_skill_integrity.py" --strict-toc
```

生成本地网页手册：

```powershell
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\build_user_manual_browser.py"
```

生成上传包 viewer：

```powershell
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\build_upload_package_viewer.py" `
  "<segment-package-or-manifest>" `
  --output "<segment-package>\upload_package_viewer" `
  --title "SXXEXX_SEGXXX 上传包核对"
```

生成关键帧验收页：

```powershell
py "$env:USERPROFILE\.codex\skills\ai-comic-drama\scripts\build_keyframe_review_gallery.py" `
  "<segment-package-or-manifest>" `
  --output "<segment-package>\keyframe_review_gallery" `
  --title "SXXEXX_SEGXXX 关键帧验收"
```

Dreamina 视频提交示例：

```powershell
$prompt = Get-Content "prompts\00_seedance多功能参考提示词.txt" -Raw
dreamina multimodal2video `
  --image="uploads\SXXEXX_SEGXXX\图片1_上一段尾帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片2_SHOT02关键帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片3_SHOT03关键帧.png" `
  --image="uploads\SXXEXX_SEGXXX\图片4_SHOT04关键帧.png" `
  --prompt="$prompt" `
  --duration=15 `
  --ratio=16:9 `
  --video_resolution=720p `
  --model_version=seedance2.0 `
  --poll=30
```

查询/下载：

```powershell
dreamina query_result --submit_id=<submit_id> --download_dir=<download_dir>
```

## 7. 遇到问题怎么办

| 问题                   | 处理                                                                      |
| -------------------- | ----------------------------------------------------------------------- |
| agent 默认写成3分钟        | 让它检查 `EPISODE_SPEC`，未确认就停止                                              |
| agent 想用 Dreamina 生图 | 纠正：静态图只能用 `$imagegen`                                                   |
| agent 想直接提交视频        | 要求先生成 viewer 并等待明确确认                                                    |
| 后续段没有尾帧              | 阻塞视频提交，不能伪造尾帧                                                           |
| 包里有旧图或失败图            | 从当前 manifest 移除，保留为归档                                                   |
| Windows 路径打不开        | 用 PowerShell 的 `$env:USERPROFILE\.codex\skills\ai-comic-drama` 检查实际安装路径 |

## 8. 最短安全启动词

```text
用 $ai-comic-drama 推进当前项目。先读 00_项目设定/03_当前运行设置.md。若 EPISODE_SPEC 未确认，先给规格选项并停止等待我选择。不要生成图片，不要提交视频。
```
