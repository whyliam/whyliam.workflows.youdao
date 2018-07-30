# -*- coding: utf-8 -*-

from workflow import Workflow3, ICON_WEB, web
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

YOUDAO_DEFAULT_KEYFROM = ('whyliam-wf-1', 'whyliam-wf-2', 'whyliam-wf-3',
                          'whyliam-wf-4', 'whyliam-wf-5', 'whyliam-wf-6',
                          'whyliam-wf-7', 'whyliam-wf-8', 'whyliam-wf-9',
                          'whyliam-wf-10', 'whyliam-wf-11')

YOUDAO_DEFAULT_KEY = (2002493135, 2002493136, 2002493137,
                      2002493138, 2002493139, 2002493140,
                      2002493141, 2002493142, 2002493143,
                      1947745089, 1947745090)

ERRORCODE_DICT = {
    "101": "缺少必填的参数，出现这个情况还可能是et的值和实际加密方式不对应",
    "102": "不支持的语言类型",
    "103": "翻译文本过长",
    "104": "不支持的API类型",
    "105": "不支持的签名类型",
    "106": "不支持的响应类型",
    "107": "不支持的传输加密类型",
    "108": "appKey无效，注意不是应用密钥",
    "109": "batchLog格式不正确",
    "110": "无相关服务的有效实例",
    "111": "开发者账号无效",
    "113": "q不能为空",
    "201": "解密失败，可能为DES,BASE64,URLDecode的错误",
    "202": "签名检验失败",
    "203": "访问IP地址不在可访问IP列表",
    "205": "请求的接口与应用的平台类型不一致",
    "301": "辞典查询失败",
    "302": "翻译查询失败",
    "303": "服务端的其它异常",
    "401": "账户已经欠费",
    "411": "访问频率受限,请稍后访问",
    "412": "长请求过于频繁，请稍后访问",
    "500": "有道翻译失败"
}

ICON_DEFAULT = 'icon.png'
ICON_PHONETIC = 'icon_phonetic.png'
ICON_BASIC = 'icon_basic.png'
ICON_WEB = 'icon_web.png'
ICON_UPDATE = 'icon_update.png'
ICON_ERROR = 'icon_error.png'


def set_youdao_url(query):
    # 构建有道翻译URL
    import os
    import random

    zhiyun_id = os.getenv('zhiyun_id', '').strip()
    zhiyun_key = os.getenv('zhiyun_key', '').strip()
    if zhiyun_id and zhiyun_key:
        url = set_youdao_new_url_from(query, zhiyun_id, zhiyun_key)
    else:
        youdao_keyfrom = os.getenv('youdao_keyfrom', '').strip()
        youdao_key = os.getenv('youdao_key', '').strip()
        if not youdao_keyfrom or not youdao_key:
            i = random.randrange(0, 11, 1)
            youdao_keyfrom = YOUDAO_DEFAULT_KEYFROM[i]
            youdao_key = YOUDAO_DEFAULT_KEY[i]
        url = set_youdao_old_url_from(query, youdao_keyfrom, youdao_key)
    return url


def set_youdao_old_url_from(query, youdao_keyfrom, youdao_key):
    import urllib

    query = urllib.quote(str(query))
    url = 'http://fanyi.youdao.com/openapi.do?' + \
        'keyfrom=' + str(youdao_keyfrom) + \
        '&key=' + str(youdao_key) + \
        '&type=data&doctype=json&version=1.1&q=' + query
    return url


def set_youdao_new_url_from(query, zhiyun_id, zhiyun_key):
    import urllib
    import hashlib
    import uuid

    salt = uuid.uuid4().hex
    sign = hashlib.md5(zhiyun_id + query + salt + zhiyun_key).hexdigest()
    query = urllib.quote(str(query))

    url = 'https://openapi.youdao.com/api' + \
        '?appKey=' + str(zhiyun_id) + \
        '&salt=' + str(salt) + \
        '&sign=' + str(sign) + \
        '&q=' + query
    return url


def get_web_data(query):
    # 获取翻译数据
    url = set_youdao_url(query)
    try:
        rt = web.get(url).json()
        return rt
    except:
        rt = {}
        rt['errorCode'] = "500"
        return rt
    else:
        rt = {}
        rt['errorCode'] = "500"
        return rt


def save_history_data(query, title, arg, ICON_DEFAULT):
    jsonData = '{"title": "%s", "subtitle": "%s", "arg": "%s", \
        "icon": "%s"}\n' % (query, title, arg, ICON_DEFAULT)
    with open('history.log', 'a') as file:
        file.write(jsonData)


def get_history_data():
    with open('history.log', 'r') as file:
        for line in file.readlines()[-1:-10:-1]:
            line = json.loads(line)
            wf.add_item(
                title=line['title'], subtitle=line['subtitle'],
                arg=line['arg'], valid=True, icon=line['icon'])


def check_Update():
    # 检查更新
    if wf.update_available:
        arg = ['', '', '', '', 'error']
        arg = '$%'.join(arg)
        wf.add_item(
            title='有新版本更新', subtitle='', arg=arg,
            valid=True, icon=ICON_UPDATE)
    else:
        wf.add_item('有道翻译')


def check_English(query):
    # 检查英文翻译中文
    import re

    if re.search(ur"[\u4e00-\u9fa5]+", query):
        return False
    return True


def get_translation(query, isEnglish, rt):
    # 翻译结果
    subtitle = '翻译结果'
    translations = rt["translation"]
    for title in translations:
        arg = [query, title, query, '', ''] if isEnglish else [
            query, title, title, '', '']
        arg = '$%'.join(arg)

        save_history_data(query, title, arg, ICON_DEFAULT)

        wf.add_item(
            title=title, subtitle=subtitle, arg=arg,
            valid=True, icon=ICON_DEFAULT)


def get_phonetic(query, isEnglish, rt):
    # 发音
    if u'basic' in rt.keys():
        if rt["basic"].get("phonetic"):
            title = ""
            if rt["basic"].get("us-phonetic"):
                title += ("[美: " + rt["basic"]["us-phonetic"] + "] ")
            if rt["basic"].get("uk-phonetic"):
                title += ("[英: " + rt["basic"]["uk-phonetic"] + "] ")
            title = title if title else "[" + rt["basic"]["phonetic"] + "]"
            subtitle = '有道发音'
            arg = [query, title, query, '', ''] if isEnglish else [
                query, title, '', query, '']
            arg = '$%'.join(arg)
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_PHONETIC)


def get_explains(query, isEnglish, rt):
    # 简明释意
    if u'basic' in rt.keys():
        for i in range(len(rt["basic"]["explains"])):
            title = rt["basic"]["explains"][i]
            subtitle = '简明释意'
            arg = [query, title, query, '', ''] if isEnglish else [
                query, title, '', title, '']
            arg = '$%'.join(arg)
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_PHONETIC)


def get_web_translation(query, isEnglish, rt):
  # 网络翻译
    if u'web' in rt.keys():
        for i in range(len(rt["web"])):
            titles = rt["web"][i]["value"]
            for title in titles:
                subtitle = '网络翻译: ' + rt["web"][i]["key"]

                if isEnglish:
                    key = ''.join(rt["web"][i]["key"])
                    arg = [query, title, key, '', '']
                else:
                    value = ' '.join(rt["web"][i]["value"])
                    arg = [query, title, title, '', '']

                arg = '$%'.join(arg)
                wf.add_item(
                    title=title, subtitle=subtitle,
                    arg=arg, valid=True, icon=ICON_WEB)


def main(wf):
    query = wf.args[0].strip().replace("\\", "")
    if not isinstance(query, unicode):
        query = query.decode('utf8')

    if not query:
        check_Update()
        wf.send_feedback()

    if query == "*":
        get_history_data()
    else:
        rt = get_web_data(query)
        errorCode = str(rt.get("errorCode"))

        if ERRORCODE_DICT.has_key(errorCode):
            arg = ['', '', '', '', 'error']
            arg = '$%'.join(arg)
            wf.add_item(
                title=errorCode+" "+ERRORCODE_DICT[errorCode],
                subtitle='', arg=arg,
                valid=True, icon=ICON_ERROR)

        elif errorCode == "0":
            isEnglish = check_English(query)
            get_translation(query, isEnglish, rt)
            get_phonetic(query, isEnglish, rt)
            get_explains(query, isEnglish, rt)
            get_web_translation(query, isEnglish, rt)

        else:
            title = '有道也翻译不出来了'
            subtitle = '尝试一下去网站搜索'
            arg = [query, ' ', ' ', ' ']
            arg = '$%'.join(arg)
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_DEFAULT)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'liszd/whyliam.workflows.youdao',
        'frequency': 7
    })
    sys.exit(wf.run(main))
