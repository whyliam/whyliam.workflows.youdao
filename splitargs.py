#!/usr/bin/env python3
"""Alfred actions: structured arguments and shell-free speech."""
import json
import re
import subprocess
import sys
from urllib.parse import urlencode
from youdao import get_query_language


def detect_language(query):
    if re.search(r'[\u3040-\u30ff]', query):
        return 'JA'
    if re.search(r'[\uac00-\ud7af\u1100-\u11ff]', query):
        return 'KO'
    if re.search(r'[\u3400-\u9fff]', query):
        return 'zh-CHS'
    return 'EN'


def get_voice(language):
    return {'EN': 'Samantha', 'KO': 'Yuna', 'zh-CHS': 'Ting-Ting', 'JA': 'Kyoko'}[language]


def decode(payload):
    try:
        data = json.loads(payload)
        if isinstance(data, dict) and all(isinstance(data.get(k), str) for k in ('query', 'result')):
            return data['query'], data['result']
    except ValueError:
        pass
    # Read history produced by version 4.0.0.
    parts = payload.split('$%')
    if len(parts) == 6:
        return parts[1], parts[2]
    raise ValueError('Invalid action argument')


def main(args=None):
    args = sys.argv[1:] if args is None else args
    try:
        payload, command = args
        query, result = decode(payload)
        if command == 'search':
            sys.stdout.write("https://dict.youdao.com/result?" + urlencode({"word": query, "lang": {"eng": "en", "jap": "ja", "ko": "ko"}[get_query_language(query)]}))
        elif command == 'copy':
            sys.stdout.write(result)
        elif command == 'pronounce':
            # stdin also prevents leading dashes being treated as say options.
            subprocess.run(['/usr/bin/say', '-v', get_voice(detect_language(query))], input=query, text=True, check=True, timeout=60)
        else:
            raise ValueError('Unknown action')
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
