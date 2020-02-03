# -*- coding: utf-8 -*-
import sys
import os
import ssl
import re
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')


def escape_quote(result):
    return result.replace("\'", "\\\'").replace("\"", "\\\"")


def get_args(wf):
    query = sys.argv[1]
    arg_array = query.split('$%')
    command = str(sys.argv[2])

    try:
        version = arg_array[0]
        query = arg_array[1]
        result = arg_array[2]
        query_language = arg_array[3]
        pronounce = arg_array[4]
        operation = arg_array[5]

        # 是否有更新
        if operation == 'update_now':
            wf.start_update()
            return
        elif operation == 'update_with_url':
            import webbrowser
            url = "https://github.com/whyliam/whyliam.workflows.youdao/releases"
            webbrowser.open(url)
            return
        elif operation == 'update_next_time':
            return

        # 是否有错误
        elif operation == 'error':
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
            if ('2') in query_language:
                data_form, data_to = query_language.split('2')
            else:
                data_form = query_language
                data_to = ''

            if data_form == 'EN':
                if pronounce == '':
                    pronounce = query
                bashCommand = "say --voice='Samantha' " + \
                    escape_quote(pronounce)
                os.system(bashCommand)

            elif data_form == 'KO':
                if pronounce == '':
                    pronounce = query
                bashCommand = "say --voice='Yuna' " + escape_quote(pronounce)
                os.system(bashCommand)

            elif data_form == 'zh-CHS':
                if pronounce == '':
                    pronounce = query
                bashCommand = "say --voice='Ting-Ting' " + \
                    escape_quote(pronounce)
                os.system(bashCommand)

            elif data_form == 'JA':
                if pronounce == '':
                    pronounce = query
                bashCommand = "say --voice='Kyoko' " + escape_quote(pronounce)
                os.system(bashCommand)

            elif data_to == 'EN':
                if pronounce == '':
                    pronounce = result
                bashCommand = "say --voice='Samantha' " + \
                    escape_quote(pronounce)
                os.system(bashCommand)

    except Exception as e:
        return


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'whyliam/whyliam.workflows.youdao',
        'frequency': 0
    })
    sys.exit(wf.run(get_args))
