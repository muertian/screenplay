# S01E01_SEG001 即梦网页端人工上传包

用途：把已经通过验收的 `S01E01_SEG001` 直接拿到即梦网页端手动上传生成 15 秒视频。

重要说明：

- 本文件夹是“网页端人工上传辅助包”，不是 CLI 正式提交包。
- 原 CLI 路线因当前账号缺少 `dreamina_cli / maestro vip` 权限被阻塞。
- 本包只整理素材、顺序、提示词和检查清单；不会自动提交、查询或下载视频。
- 图片和提示词来自已确认的 SEG001 上传包，未重新生成、未替换锁定资产。

## 文件夹结构

| 路径 | 用途 |
|---|---|
| `01_images_upload_in_order/` | 按网页端上传顺序排好的 7 张图片 |
| `02_prompt/COPY_THIS_PROMPT_TO_JIMENG.txt` | 复制到即梦网页端的最终提示词 |
| `03_reference_notes/01_UPLOAD_ORDER.md` | 上传顺序和每张图的用途 |
| `03_reference_notes/02_WEB_UPLOAD_STEPS.md` | 网页端操作步骤 |
| `03_reference_notes/03_OMITTED_REFERENCES.md` | 没上传的参考图和原因 |
| `04_source_audit/` | 原 CLI 包 manifest、viewer 确认记录，仅用于追溯 |

## 推荐网页端设置

| 项目 | 选择 |
|---|---|
| 功能 | 视频生成 / 全能参考 / 多模态参考 / 智能多帧，按网页端实际名称选择最接近项 |
| 模型 | Seedance 2.0 |
| 画幅 | 16:9 |
| 时长 | 15 秒 |
| 清晰度 | 720p 或网页端默认可用项 |
| 音频 | 本包不上传音频 |
| 上传图片数 | 7 张，严格按 `01-07` 顺序 |

## 快速使用

1. 打开 `01_images_upload_in_order/`。
2. 按文件名前缀 `01` 到 `07` 依次上传图片。
3. 打开 `02_prompt/COPY_THIS_PROMPT_TO_JIMENG.txt`，全选复制到即梦提示词输入框。
4. 生成前再核对：16:9、15秒、Seedance 2.0、无字幕、无文字信息。
5. 生成后把视频保存到项目的 `manual_web_outputs/S01E01_SEG001/`，再做质检和下一段尾帧提取。
