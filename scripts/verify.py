#!/usr/bin/env python3
"""Validate the actual installable archive. --live also checks Youdao."""
import concurrent.futures
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import zipfile

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    with zipfile.ZipFile(root / 'whyliam.workflows.youdao.alfredworkflow') as archive:
        assert archive.testzip() is None
        assert not any(name.startswith(('requests/', 'workflow/')) or 'history' in name or 'cookie' in name for name in archive.namelist())
        for name in archive.namelist():
            assert archive.read(name) == (root / name).read_bytes(), name + ' is stale'
        archive.extractall(path)
    plist = plistlib.loads((path / 'info.plist').read_bytes())
    assert plist['version'] == (path / 'version').read_text().strip()
    for obj in plist['objects']:
        if obj['type'] in ('alfred.workflow.input.scriptfilter', 'alfred.workflow.action.script'):
            assert obj['config']['scriptargtype'] == 1
            assert '{query}' not in obj['config']['script']

    def run(script, *args):
        result = subprocess.run([sys.executable, str(path / script), *args], cwd=path,
                                env={**os.environ, 'alfred_workflow_data': str(path / 'data')},
                                capture_output=True, text=True, timeout=20, check=True)
        assert not result.stderr, result.stderr
        return result.stdout

    assert not json.loads(run('youdao.py'))['items'][0]['valid']
    query = 'hello; echo SHOULD_NOT_RUN $(id) " $%\n你好'
    payload = json.dumps({'query': query, 'result': query})
    assert run('splitargs.py', payload, 'copy') == query
    from urllib.parse import parse_qs, urlsplit
    assert parse_qs(urlsplit(run('splitargs.py', payload, 'search')).query)['word'] == [query]
    if '--live' in sys.argv:
        cases = [('hello', '喂'), ('你好', 'hello'), ('こんにちは', '你好'),
                 ('안녕하세요', '你好'), ('今天下午我们一起去公园散步。', 'park'),
                 ('hello & goodbye', '再见'), ('今日はいい天気ですね', '天气')]

        def check(case):
            q, expected = case
            items = json.loads(run('youdao.py', q))['items']
            assert any(expected in i['title'] and i['valid'] for i in items), (q, items)
            print('Live query passed:', q, flush=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            list(executor.map(check, cases))
        assert json.loads(run('youdao.py', '*'))['items'][0]['valid']
print('Installable archive validation passed')
