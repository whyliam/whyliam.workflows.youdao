#!/usr/bin/env python3
"""Publish the verified package in a GitHub tag workflow using its job token."""
import json
import os
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[1]
tag = os.environ['RELEASE_TAG']
assert tag == (root / 'version').read_text().strip(), 'Tag/version mismatch'
repository = os.environ['GITHUB_REPOSITORY']
headers = {'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
           'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}

def request(url, data, content_type='application/json'):
    req = Request(url, data=data, headers={**headers, 'Content-Type': content_type}, method='POST')
    with urlopen(req, timeout=60) as response:
        return json.load(response)

release = request('https://api.github.com/repos/' + repository + '/releases', json.dumps({
    'tag_name': tag, 'name': '有道词典 Workflow ' + tag, 'draft': True,
    'body': '修复中日韩释义、句子翻译、特殊字符查询、Alfred 参数及发音命令注入。历史记录支持并发保护、去重和容量限制。运行时仅依赖 Python 3 标准库。\n\n下载下方 .alfredworkflow 文件，双击导入 Alfred。\n\n已通过回归测试、安装包校验及本机真实接口测试。有道网站接口可能调整或限流。',
    'prerelease': False,
}).encode('utf-8'))
asset = root / 'whyliam.workflows.youdao.alfredworkflow'
request(release['upload_url'].split('{')[0] + '?name=' + quote(asset.name), asset.read_bytes(), 'application/octet-stream')
req = Request(release['url'], data=json.dumps({'draft': False, 'make_latest': 'true'}).encode(),
              headers={**headers, 'Content-Type': 'application/json'}, method='PATCH')
with urlopen(req, timeout=60) as response:
    published = json.load(response)
print(published['html_url'])
