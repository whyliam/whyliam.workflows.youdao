# -*- coding: utf-8 -*-
import sys
import os
import re
from workflow import Workflow3


def escape_quote(result):
    return result.replace("\'", "\\\'").replace("\"", "\\\"")


def get_args(wf):
    query = sys.argv[1]
    arg_array = query.split('$%')
    command = str(sys.argv[2])

    try:
        version, query, result, query_language, pronounce, operation = arg_array

        # 是否有错误
        if operation == 'error':
            import webbrowser
            url = "https://blog.naaln.com/2017/04/alfred-youdao-intro/"
            webbrowser.open(url)
            return

        # 查询的单词
        if command == 'search':
            sys.stdout.write(query)

        # 翻译的结果
        elif command == 'copy':
            sys.stdout.write(result)

        # 发音
        elif command == "pronounce":
            language = detect_language(query)
            bashCommand = f"say --voice='{get_voice(language)}' {escape_quote(query)}"
            os.system(bashCommand)

    except Exception:
        return


def detect_language(query):
    if re.match(r'^[a-zA-Z]+$', query):
        return 'EN'
    elif re.match(r'^[\u4e00-\u9fa5]+$', query):
        return 'zh-CHS'
    elif re.match(r'^[\uac00-\ud7af]+$', query):
        return 'KO'
    elif re.match(r'^[\u3040-\u309F\u30A0-\u30FF]+$', query):
        return 'JA'
    return 'UNKNOWN'


def get_voice(data_form):
    voices = {
        'EN': 'Samantha',
        'KO': 'Yuna',
        'zh-CHS': 'Ting-Ting',
        'JA': 'Kyoko'
    }
    return voices.get(data_form, 'Ting-Ting')


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(get_args))
