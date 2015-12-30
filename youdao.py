# -*- coding: utf-8 -*-

import re
import urllib
from workflow import Workflow, ICON_WEB, web
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')

apikey = 1185055258
keyfrom = 'imgxqb'
ICON_DEFAULT = 'icon.png'
ICON_PHONETIC = 'icon_phonetic.png'
ICON_BASIC = 'icon_basic.png'
ICON_WEB = 'icon_web.png'


def get_web_data(query):
    query = urllib.quote(str(query))
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom=' + keyfrom + \
        '&key=' + str(apikey) + \
        '&type=data&doctype=json&version=1.1&q=' + query
    return web.get(url).json()

def get_phonetic_args(s):
    result = {}
    if u'basic' in s.keys():
        if s["basic"].get("us-phonetic"):
            result["us"] = "[" + s["basic"]["us-phonetic"] + "]"
        if s["basic"].get("uk-phonetic"):
            result["uk"] = "[" + s["basic"]["uk-phonetic"] + "]"
    return result

def main(wf):
    query = wf.args[0].strip().replace("\\", "")
    extra_args = {}
    
    if not query:
        wf.add_item('有道翻译')
        wf.send_feedback()
        return 0

    s = get_web_data(query)
    extra_args.update(get_phonetic_args(s))
    
    if s.get("errorCode") == 0:
        # '翻译结果'
        title = s["translation"]
        title = ''.join(title)
        # url = u'http://dict.youdao.com/search?q=' + query
        tran = 'EtC'
        if not isinstance(query, unicode):
            query = query.decode('utf8')
        if re.search(ur"[\u4e00-\u9fa5]+", query):
            tran = 'CtE'
        subtitle = '翻译结果'

        arg = [query, title, query, ' ', json.dumps(extra_args)] if tran == 'EtC' else [
            query, title, title, ' ', json.dumps(extra_args)]
        arg = '$'.join(arg)
        wf.add_item(
            title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_DEFAULT)

        if u'basic' in s.keys():
            # '发音'
            if s["basic"].get("phonetic"):
                title = ""
                if s["basic"].get("us-phonetic"):
                    title += (" [美: " + s["basic"]["us-phonetic"] + "]")
                if s["basic"].get("uk-phonetic"):
                    title += (" [英: " + s["basic"]["uk-phonetic"] + "]")
                title = title if title else "[" + s["basic"]["phonetic"] + "]"
                subtitle = '有道发音'
                arg = [query, title, query, ' ', json.dumps(extra_args)] if tran == 'EtC' else [
                    query, title, ' ', query, json.dumps(extra_args)]
                arg = '$'.join(arg)
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_PHONETIC)

            # '简明释意'
            for be in range(len(s["basic"]["explains"])):
                title = s["basic"]["explains"][be]
                subtitle = '简明释意'
                arg = [query, title, query, ' ', json.dumps(extra_args)] if tran == 'EtC' else [
                    query, title, title, ' ', json.dumps(extra_args)]
                arg = '$'.join(arg)
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_BASIC)

        # '网络翻译'
        if u'web' in s.keys():
            for w in range(len(s["web"])):
                title = s["web"][w]["value"]
                title = ', '.join(title)
                subtitle = '网络翻译: ' + s["web"][w]["key"]

                if tran == 'EtC':
                    key = ''.join(s["web"][w]["key"])
                    arg = [query, title, key, ' ', json.dumps(extra_args)]
                else:
                    value = ' '.join(s["web"][w]["value"])
                    arg = [query, title, value, ' ', json.dumps(extra_args)]

                arg = '$'.join(arg)
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_WEB)

    else:
        title = '有道也翻译不出来了'
        subtitle = '尝试一下去网站搜索'
        arg = [query, ' ', ' ', ' ', json.dumps(extra_args)]
        arg = '$'.join(arg)
        wf.add_item(
            title=title, subtitle=subtitle, arg=arg, valid=True, icon=ICON_DEFAULT)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'kaiye/workflows-youdao',
        'frequency': 7
    })

    sys.exit(wf.run(main))
    if wf.update_available:
        wf.start_update()
