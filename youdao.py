# -*- coding: utf-8 -*-

import re
import urllib
from workflow import Workflow, ICON_WEB, web
import sys

reload(sys)
sys.setdefaultencoding('utf8')

apikey = 1331254833
keyfrom = 'whyliam'
ICON_DEFAULT = 'icon.png'
ICON_BASIC = 'icon_basic.png'
ICON_WEB = 'icon_web.png'


def get_web_data(query):
    query = urllib.quote(str(query))
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=' + keyfrom + \
        '&key=' + str(apikey) + \
        '&type=data&doctype=json&version=1.1&q=' + query
    return web.get(url).json()


def main(wf):

    query = wf.args[0].strip().replace("\\", "")

    if not query:
        wf.add_item('有道翻译')
        wf.send_feedback()
        return 0

    s = get_web_data(query)

    # '翻译结果'
    title = s["translation"]
    title = ''.join(title).encode("UTF-8")
    url = u'http://dict.youdao.com/search?q=' + query

    if title != query:
        subtitle = '翻译结果'
        arg = url + "," + title
        wf.add_item(
            title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_DEFAULT)

        if u'basic' in s.keys():
            # '发音'
            title = "[" + s["basic"]["phonetic"] + "]"
            if s["basic"]["us-phonetic"]:
                title += (" [美: " + s["basic"]["us-phonetic"] + "]")
            if s["basic"]["uk-phonetic"]:
                title += (" [英: " + s["basic"]["uk-phonetic"] + "]")
            subtitle = '发音'
            arg = url + "," + title
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_DEFAULT)

            # '简明释意'
            for be in range(len(s["basic"]["explains"])):
                title = s["basic"]["explains"][be]
                subtitle = '简明释意'
                arg = url + "," + title
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_BASIC)

        # '网络翻译'
        if u'web' in s.keys():
            for w in range(len(s["web"])):
                title = s["web"][w]["key"]
                title = ''.join(title).encode("UTF-8")
                subtitle = '网络翻译: ' + s["web"][w]["key"]
                arg = url + "," + title
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_WEB)

    else:
        title = '有道也翻译不出来了'
        subtitle = '尝试一下去网站搜索'
        arg = url + "," + title
        wf.add_item(
            title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_DEFAULT)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'liszd/whyliam.workflows.youdao',
        'frequency': 7
    })

    sys.exit(wf.run(main))
    if wf.update_available:
        wf.start_update()
