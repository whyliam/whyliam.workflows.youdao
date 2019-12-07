# -*- coding: utf-8 -*-
import sys
import os
import ssl
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')


def getargs(wf):
    query = sys.argv[1]
    query = query.split('$%')
    operation = str(sys.argv[2])

    # 是否有更新
    if query[4] == 'update':
        wf.start_update()
    # 是否有错误
    elif query[4] == 'error':
        import webbrowser
        url = "https://blog.naaln.com/2017/04/alfred-youdao-intro/"
        webbrowser.open(url)
        return
    elif query[4] != '':
        return

    if operation == 'search':
        # 查询的单词
        sys.stdout.write(query[0].strip())
    elif operation == 'copy':
        # 翻译的结果
        sys.stdout.write(query[1].strip())
    elif operation == "pronounce":
        # 发音
        if query[2]:
            bashCommand = "say --voice='Samantha' " + query[2]
            os.system(bashCommand)
        if query[3]:
            bashCommand = "say --voice='Ting-Ting' " + query[3]
            os.system(bashCommand)


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'whyliam/whyliam.workflows.youdao',
    })
    sys.exit(wf.run(getargs))
