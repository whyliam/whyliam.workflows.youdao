# -*- coding: utf-8 -*-
import sys
from workflow import Workflow

reload(sys)
sys.setdefaultencoding('utf8')


def getargs(wf):
    query = sys.argv[1]
    query = query.split(',')
    part = sys.argv[2]
    part = int(part)
    print query[part]
    return 0

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(getargs))