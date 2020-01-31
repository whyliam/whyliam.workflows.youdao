# -*- coding: utf-8 -*-

from workflow import Workflow3, web
import sentry_sdk
import os
import json
import uuid
import hashlib
import time
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
    "20": "要翻译的文本过长",
    "30": "无法进行有效的翻译",
    "40": "不支持的语言类型",
    "50": "无效的key",
    "60": "无词典结果，仅在获取词典结果生效",
    "101": "缺少必填的参数，出现这个情况还可能是et的值和实际加密方式不对应",
    "102": "不支持的语言类型",
    "103": "翻译文本过长",
    "104": "不支持的API类型",
    "105": "不支持的签名类型",
    "106": "不支持的响应类型",
    "107": "不支持的传输加密类型",
    "108": "appKey无效，注册账号， 登录后台创建应用和实例并完成绑定，\
        可获得应用ID和密钥等信息，其中应用ID就是appKey（ 注意不是应用密钥）",
    "109": "batchLog格式不正确",
    "110": "无相关服务的有效实例",
    "111": "开发者账号无效",
    "113": "q不能为空",
    "201": "解密失败，可能为DES,BASE64,URLDecode的错误",
    "202": "签名检验失败",
    "203": "访问IP地址不在可访问IP列表",
    "205": "请求的接口与应用的平台类型不一致，如有疑问请参考[入门指南]()",
    "206": "因为时间戳无效导致签名校验失败",
    "207": "重放请求",
    "301": "辞典查询失败",
    "302": "翻译查询失败",
    "303": "服务端的其它异常",
    "401": "账户已经欠费停",
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


def init_sentry():
    # 收集错误信息
    if os.getenv('sentry', 'False').strip():
        sentry_sdk.init(
            "https://4d5a5b1f2e68484da9edd9076b86e9b7@sentry.io/1500348")
        with sentry_sdk.configure_scope() as scope:
            user_id = get_user_id()
            scope.user = {"id": user_id}
            scope.set_tag("version", str(wf.version))


def get_user_id():
    user_id = wf.stored_data('user_id')
    if user_id == None:
        user_id = str(uuid.uuid1())
    wf.store_data('user_id', user_id)
    return user_id


def sentry_message(errorCode, msg):
    if os.getenv('sentry', 'False').strip():
        with sentry_sdk.configure_scope() as scope:
            scope.set_tag("errorCode", errorCode)
        sentry_sdk.capture_message(msg) 


def get_youdao_url(query):
    # 构建有道翻译URL
    import random

    zhiyun_id = os.getenv('zhiyun_id', '').strip()
    zhiyun_key = os.getenv('zhiyun_key', '').strip()
    if zhiyun_id and zhiyun_key:
        url = get_youdao_new_url(query, zhiyun_id, zhiyun_key)
    else:
        youdao_keyfrom = os.getenv('youdao_keyfrom', '').strip()
        youdao_key = os.getenv('youdao_key', '').strip()
        if not youdao_keyfrom or not youdao_key:
            i = random.randrange(0, 11, 1)
            youdao_keyfrom = YOUDAO_DEFAULT_KEYFROM[i]
            youdao_key = YOUDAO_DEFAULT_KEY[i]
        url = get_youdao_old_url(query, youdao_keyfrom, youdao_key)
    wf.logger.debug(url)
    return url


def get_youdao_old_url(query, youdao_keyfrom, youdao_key):
    import urllib

    query = urllib.quote(str(query))
    url = 'http://fanyi.youdao.com/openapi.do?' + \
        'keyfrom=' + str(youdao_keyfrom) + \
        '&key=' + str(youdao_key) + \
        '&type=data&doctype=json&version=1.1&q=' + query
    return url


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


def get_youdao_new_url(query, zhiyun_id, zhiyun_key):
    import urllib
    import hashlib
    import uuid

    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = zhiyun_id + truncate(query) + salt + curtime + zhiyun_key
    sign = encrypt(signStr)

    language = query_language(query)
    if language == "Chinese":
        data_form = 'zh-CHS'
        data_to = 'en'
    elif language == "Korean":
        data_form = 'ko'
        data_to = 'zh-CHS'
    elif language == "Japanese":
        data_form = 'ja'
        data_to = 'zh-CHS'
    else:
        data_form = 'en'
        data_to = 'zh-CHS'

    url = 'https://openapi.youdao.com/api' + \
        '?appKey=' + str(zhiyun_id) + \
        '&salt=' + str(salt) + \
        '&sign=' + str(sign) + \
        '&q=' + urllib.quote(str(query)) + \
        '&from=' + data_form + \
        '&to=' + data_to + \
        '&signType=v3' + \
        '&curtime=' + curtime
    return url


def fetch_translation(query):
    # 获取翻译数据
    url = get_youdao_url(query)
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
            try:
                line = json.loads(line)
                wf.add_item(
                    title=line['title'], subtitle=line['subtitle'],
                    arg=line['arg'], valid=True, icon=line['icon'])
            except Exception as e:
                pass


def is_expired():
    # 检查更新
    if wf.update_available:
        arg = ['', '', '', '', 'update']
        arg = '$%'.join(arg)
        wf.add_item(
            title='马上更新', subtitle='有新版本更新', arg=arg,
            valid=True, icon=ICON_UPDATE)

        arg = ['', '', '', '', 'not_update']
        arg = '$%'.join(arg)
        wf.add_item(
            title='暂不更新', subtitle='有新版本更新', arg=arg,
            valid=True, icon=ICON_ERROR)
        wf.send_feedback()
        return True
    return False


def query_language(query):
    import re
    # 检查中文
    if re.search(ur"[\u4e00-\u9fa5]+", query):
        return "Chinese"
    # 检查韩语
    if re.search(ur"[\uAC00-\uD7A3]+", query):
        return "Korean"
    # 检查日语
    if re.search(ur"[\u0800-\u4e00]+", query):
        return "Japanese"
    return "Default"

def add_translation(query, isChinese, rt):
    # 翻译结果
    subtitle = '翻译结果'
    translations = rt["translation"]
    for title in translations:
        if isChinese:
            arg = [query, title, title, '', '']
        else:
            arg = [query, title, query, '', '']
        arg = '$%'.join(arg)

        save_history_data(query, title, arg, ICON_DEFAULT)

        wf.add_item(
            title=title, subtitle=subtitle, arg=arg,
            valid=True, icon=ICON_DEFAULT)


def add_phonetic(query, isChinese, rt):
    # 发音
    if u'basic' in rt.keys():
        if rt["basic"] is not None:
            if rt["basic"].get("phonetic"):
                title = ""
                if rt["basic"].get("us-phonetic"):
                    title += ("[美: " + rt["basic"]["us-phonetic"] + "] ")
                if rt["basic"].get("uk-phonetic"):
                    title += ("[英: " + rt["basic"]["uk-phonetic"] + "] ")
                title = title if title else "[" + rt["basic"]["phonetic"] + "]"
                subtitle = '有道发音'
                if isChinese:
                    arg = [query, title, '', query, ''] 
                else:
                    arg = [query, title, query, '', '']
                arg = '$%'.join(arg)
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg,
                    valid=True, icon=ICON_PHONETIC)


def add_explains(query, isChinese, rt):
    # 简明释意
    if u'basic' in rt.keys():
        if rt["basic"] is not None:
            for i in range(len(rt["basic"]["explains"])):
                title = rt["basic"]["explains"][i]
                subtitle = '简明释意'
                if isChinese:
                    arg = [query, title, '', title, '']
                else:
                    arg = [query, title, query, '', '']
                arg = '$%'.join(arg)
                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg,
                    valid=True, icon=ICON_PHONETIC)


def add_web_translation(query, isChinese, rt):
  # 网络翻译
    if u'web' in rt.keys():
        if rt["web"] is not None:
            for i in range(len(rt["web"])):
                titles = rt["web"][i]["value"]
                for title in titles:
                    subtitle = '网络翻译: ' + rt["web"][i]["key"]

                    if isChinese:
                        value = ' '.join(rt["web"][i]["value"])
                        arg = [query, title, title, '', '']
                    else:
                        key = ''.join(rt["web"][i]["key"])
                        arg = [query, title, key, '', '']

                    arg = '$%'.join(arg)
                    wf.add_item(
                        title=title, subtitle=subtitle,
                        arg=arg, valid=True, icon=ICON_WEB)


def main(wf):
    if is_expired():
        return

    query = wf.args[0].strip()
    if not isinstance(query, unicode):
        query = query.decode('utf8')

    if query == "*":
        get_history_data()
    else:
        rt = fetch_translation(query)
        errorCode = str(rt.get("errorCode"))

        if ERRORCODE_DICT.has_key(errorCode):
            if errorCode == "500":
                sentry_message(errorCode, ERRORCODE_DICT[errorCode])
            arg = ['', '', '', '', 'error']
            arg = '$%'.join(arg)
            wf.add_item(
                title=errorCode+" "+ERRORCODE_DICT[errorCode],
                subtitle='', arg=arg,
                valid=True, icon=ICON_ERROR)

        elif errorCode == "0":
            isChinese = True if query_language(query) == "Chinese" else False
            add_translation(query, isChinese, rt)
            add_phonetic(query, isChinese, rt)
            add_explains(query, isChinese, rt)
            add_web_translation(query, isChinese, rt)

        else:
            sentry_message(errorCode, '有道也翻译不出来了')
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
        'github_slug': 'whyliam/whyliam.workflows.youdao',
        'frequency': 7
    })
    init_sentry()
    sys.exit(wf.run(main))
