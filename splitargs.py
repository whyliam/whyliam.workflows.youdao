# -*- coding: utf-8 -*-
import sys
import os
from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')


def getargs(wf):
    query = sys.argv[1]
    query = query.split('$%')
    part = int(sys.argv[2])

    if query[4]:
        import webbrowser
        new = 2
        url = "https://blog.naaln.com/2017/04/alfred-youdao-intro/"
        webbrowser.open(url, new=new)
        return 0

    if part == 0:
        # 查询的单词
        sys.stdout.write(query[0].strip())
    elif part == 1:
        # 翻过的结果
        sys.stdout.write(query[1].strip())
    elif part == 2:
        # 发音
        if query[2]:
            bashCommand = "say --voice='Samantha' " + query[2]
            os.system(bashCommand)
        if query[3]:
            bashCommand = "say --voice='Ting-Ting' " + query[3]
            os.system(bashCommand)


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(getargs))
