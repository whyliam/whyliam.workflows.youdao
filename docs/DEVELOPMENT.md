# 开发与验证

运行时仅使用 Python 3 标准库。入口为 `youdao.py`，Alfred 的复制、网页跳转和本机朗读动作由 `splitargs.py` 处理。Alfred 使用 argv 传入参数，动作数据采用 JSON；朗读通过 `subprocess.run` 和标准输入调用 macOS `say`。

## 接口

通过 HTTPS 调用有道词典网站的 `https://dict.youdao.com/jsonapi_s`，查询参数统一编码，请求超时 10 秒。这是网站接口，并非有稳定性承诺的有道智云 API，可能调整或限流。失败时显示错误并保留网页查询入口。

## 历史数据

历史记录保存在 Alfred 的 `alfred_workflow_data` 目录中；直接运行时使用 `~/Library/Application Support/Alfred/Workflow Data/whyliam.workflows.youdao`。采用 UTF-8 JSON Lines，最多保留 200 条、去重，并通过文件锁和原子替换处理并发。

首次读取兼容旧版 Workflow 目录的 `history.log`，损坏记录会跳过。不再使用旧版 Cookie 和在线单词本功能。安装包不包含 Cookie、历史记录或第三方依赖。

## 本地验证与打包

在仓库根目录执行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/package.py
python3 scripts/verify.py
python3 scripts/verify.py --live
```

`--live` 会实际访问有道，网络或服务故障会导致检查失败。打包使用固定文件时间戳，生成可重复构建的 `.alfredworkflow`；安装包校验会检查文件是否与当前源码一致、参数传递方式和解包后的独立运行。

README 同时作为 Alfred 内的使用说明。修改 README 后，需要同步 `info.plist` 的 `readme` 字段，并重新打包。

## 自动检查与发布

GitHub Actions 会在推送和 PR 时运行回归测试、安装包校验及可重复构建检查。版本标签（如 `4.1.0`）通过检查后自动发布 Release 和安装包。真实接口测试由本机显式执行，不作为离线回归检查。

发布前同步 `version`、`info.plist` 及请求 User-Agent 中的版本，再重新打包并验证。已发布的版本标签保留原样，后续版本使用新标签。
