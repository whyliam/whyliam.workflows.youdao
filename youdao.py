#!/usr/bin/env python3
"""Dependency-free Youdao dictionary and translation for Alfred."""
import fcntl
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = 'https://dict.youdao.com/jsonapi_s'
ROOT = Path(__file__).resolve().parent


def get_query_language(query):
    # Kana must take precedence over kanji in Japanese sentences.
    if re.search(r'[\u3040-\u30ff]', query):
        return 'jap'
    if re.search(r'[\uac00-\ud7af\u1100-\u11ff]', query):
        return 'ko'
    return 'eng'


def data_dir():
    return Path(os.environ.get('alfred_workflow_data', str(Path.home() / 'Library/Application Support/Alfred/Workflow Data/whyliam.workflows.youdao')))


def get_youdao_url(query):
    return API + '?' + urlencode({'q': query, 'le': get_query_language(query)})


def fetch(query):
    request = Request(get_youdao_url(query), headers={'User-Agent': 'Youdao-Alfred/4.1.0', 'Accept': 'application/json'})
    with urlopen(request, timeout=10) as response:
        data = json.loads(response.read(4 * 1024 * 1024).decode('utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Invalid API response')
    return data


def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return ''.join(text(v) for v in value)
    if isinstance(value, dict):
        return text(value.get('#text', value.get('i', '')))
    return ''


def make_item(query, result, subtitle='简明释义', icon='icon_basic.png'):
    payload = json.dumps({'query': query, 'result': result}, ensure_ascii=False)
    return {'title': result, 'subtitle': subtitle, 'arg': payload, 'valid': True,
            'icon': {'path': icon}, 'mods': {'ctrl': {'arg': payload, 'valid': True}}}


def parse_results(query, data):
    items = []
    seen = set()

    def add(value, subtitle='简明释义', icon='icon_basic.png'):
        if value and value not in seen:
            seen.add(value)
            items.append(make_item(query, value, subtitle, icon))

    for key in ('ec', 'ce', 'jc', 'cj', 'kc', 'ck'):
        section = data.get(key) or {}
        words = section.get('word', [])
        if isinstance(words, dict):
            words = [words]
        for word in words:
            phones = ' '.join(label + '[' + word[field] + ']' for field, label in
                              [('ukphone', '英'), ('usphone', '美'), ('phone', '')] if word.get(field))
            if phones:
                add(phones, '本机朗读：Shift + 回车', 'icon_phonetic.png')
            for sense in word.get('trs', []):
                for translation in sense.get('tr', []):
                    add(text(translation.get('l', {})).strip())
    translation = data.get('fanyi') or {}
    add(text(translation.get('tran', '')), '翻译结果', 'icon.png')
    # Exact-match web definitions only; related phrases are not translations.
    if not any(i['subtitle'] in ('简明释义', '翻译结果') for i in items):
        for entry in (data.get('web_trans') or {}).get('web-translation', []):
            if entry.get('key', '').casefold() == query.casefold():
                for trans in entry.get('trans', []):
                    add(text(trans.get('value', '')), '网络释义', 'icon_web.png')
    return items


def history(items=None):
    directory = data_dir()
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / 'history.jsonl'
    # Separate lock file keeps read/replace safe across concurrent invocations.
    with (directory / 'history.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        records = []
        source = path if path.exists() else ROOT / 'history.log'
        if source.exists():
            for line in source.read_text(encoding='utf-8', errors='replace').splitlines():
                try:
                    record = json.loads(line)
                    if isinstance(record, dict) and isinstance(record.get('title'), str):
                        payload = record.get('arg')
                        if not isinstance(payload, str):
                            continue
                        if not payload.startswith('{'):
                            parts = payload.split('$%')
                            if len(parts) != 6:
                                continue
                            record = make_item(parts[1], parts[2], record.get('subtitle', '简明释义'))
                        if isinstance(record.get('icon'), str):
                            record['icon'] = {'path': record['icon']}
                        records.append(record)
                except (ValueError, TypeError):
                    continue
        if items is not None:
            for item in items:
                if item['subtitle'] != '本机朗读：Shift + 回车':
                    records = [r for r in records if r.get('arg') != item['arg']]
                    records.append(item)
            temporary = directory / 'history.tmp'
            temporary.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in records[-200:]), encoding='utf-8')
            temporary.replace(path)
        return list(reversed(records[-9:]))


def notice(title, subtitle, query=''):
    item = make_item(query, title, subtitle, 'icon_error.png')
    item['valid'] = False
    return item


def main(args=None):
    args = sys.argv[1:] if args is None else args
    query = args[0].strip() if args else ''
    if not query:
        return {'items': [notice('输入单词或句子', '输入 * 查看最近查询')]}
    if len(query) > 2000:
        return {'items': [notice('查询内容过长', '请控制在 2000 字符以内')]}
    if query == '*':
        try:
            items = history()
            return {'items': items or [notice('暂无查询历史', '先查询一个单词或句子')]}
        except OSError:
            return {'items': [notice('无法读取历史记录', '请检查数据目录权限')]}
    try:
        items = parse_results(query, fetch(query))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
        print('Youdao request failed: ' + str(error), file=sys.stderr)
        return {'items': [notice('查询失败', '网络或接口异常，请稍后重试；Ctrl + 回车打开网页', query)]}
    if not items:
        items = [notice('未找到释义', 'Ctrl + 回车打开有道网页', query)]
    else:
        try:
            history(items)
        except OSError as error:
            print('Could not save history: ' + str(error), file=sys.stderr)
    return {'items': items}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False))
