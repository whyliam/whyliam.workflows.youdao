# -*- coding: utf-8 -*-
import sys
import os
from workflow import Workflow

reload(sys)
sys.setdefaultencoding('utf8')


def getargs(wf):
    query = sys.argv[1]
    query = query.split('$')
    part = int(sys.argv[2])

    if part == 1:
        sys.stdout.write(query[1].strip())
    elif part == 2:
        if query[2]:
            bashCommand = "say --voice='Samantha' " + query[2]
            os.system(bashCommand)
        if query[3]:
            bashCommand = "say --voice='Ting-Ting' " + query[3]
            os.system(bashCommand)
    return 0

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(getargs))
