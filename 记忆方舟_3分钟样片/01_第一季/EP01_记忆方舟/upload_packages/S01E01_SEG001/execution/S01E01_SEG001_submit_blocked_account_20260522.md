# S01E01_SEG001提交阻塞记录

日期：2026-05-22

## 结论

新版 `dreamina` CLI 已安装，但当前登录账号没有 `dreamina_cli` 使用权限。

CLI 返回：

```text
当前账号没有 dreamina_cli 使用权限: current account is not maestro vip
```

## 已确认

- 账户额度检查：`total_credit=225`
- 会员等级：`standard`
- `dreamina list_task` 返回空数组，未发现已创建任务。
- 本次未获得 `submit_id`。
- 未下载视频，未生成尾帧。

## 下一步

需要使用已开通 `maestro vip` / 支持 `dreamina_cli` 权限的账号重新登录，或在即梦网页端完成对应CLI权限开通后再提交。