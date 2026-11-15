# 有道词典 Alfred Workflow 4.1.0

输入 `yd 单词或句子` 查询中英、日中、韩中释义及句子翻译。

- 回车：复制所选结果。
- Command + 回车：粘贴所选结果。
- Control + 回车：打开对应语言的有道词典网页；查询失败时也可使用。
- Shift + 回车：使用 macOS 本机语音朗读原文（并非有道音频）。
- `yd *`：显示最近 9 条释义。空查询显示使用提示。
- 选中文字快捷查询：在 Alfred 中自行设置 Workflow 的 Hotkey。

## 安装

从 [最新 Release](https://github.com/whyliam/whyliam.workflows.youdao/releases/latest) 下载 `.alfredworkflow` 文件，双击导入 Alfred。也可使用仓库中的同名文件。
需要支持 Workflow 的 Alfred 和 `/usr/bin/python3`。若系统没有 Python 3，需要先安装 Apple Command Line Tools，或将 Workflow 脚本中的解释器路径改为本机 Python 3 的绝对路径。

运行时仅使用 Python 3 标准库，无需 pip 安装依赖。历史版本自带的第三方库不再参与运行，也不会进入新安装包。

## 接口与数据

通过 HTTPS 调用有道词典网站的 `https://dict.youdao.com/jsonapi_s`，查询参数统一编码，请求超时 10 秒。该网站接口不是有稳定性承诺的有道智云 API，可能调整或限流；失败时显示错误并保留网页查询入口。翻译结果由有道返回，不保证译文准确性。

历史记录保存在 Alfred 的 `alfred_workflow_data` 目录中；直接运行时使用 `~/Library/Application Support/Alfred/Workflow Data/whyliam.workflows.youdao`。采用 UTF-8 JSON Lines，最多保留 200 条、去重，并通过文件锁和原子替换处理并发。首次读取可兼容旧版 Workflow 目录的 `history.log`，损坏记录会跳过。查询原文会发送给有道，释义保存在本机历史中。

不再使用旧版 Cookie 和在线单词本功能。安装包不包含 Cookie、历史记录或第三方依赖。

## 开发与验证

```sh
python3 -m unittest discover -s tests -v
python3 scripts/package.py
python3 scripts/verify.py
python3 scripts/verify.py --live  # 实际访问有道，网络或服务故障会失败
```

4.1.0 修复：中日韩释义漏解析、句子翻译失败、特殊字符查询错误、发音 shell 注入、Alfred 参数注入、历史 JSON 损坏、缺失历史文件异常、空输入异常、英文句子发音语言误判及第三方依赖兼容警告。

MIT License，见 `License`。

GitHub Actions 会在推送和 PR 时运行回归测试、安装包校验及可重复构建检查。版本标签（如 `4.1.0`）通过检查后自动发布 Release 和安装包。真实接口测试由本机显式执行，不作为离线回归检查。
