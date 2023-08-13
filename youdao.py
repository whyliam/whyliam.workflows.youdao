# -*- coding: utf-8 -*-

from workflow import Workflow3
import os
import json
import uuid
import hashlib
import time
import sys
import random

ERRORCODE_DICT = {
    "20": "要翻译的文本过长",
    "30": "无法进行有效的翻译",
    "40": "不支持的语言类型",
    "50": "无效的key",
    "60": "无词典结果，仅在获取词典结果生效",
    "101": "缺少必填的参数,首先确保必填参数齐全，然后确认参数书写是否正确。",
    "102": "不支持的语言类型",
    "103": "翻译文本过长",
    "104": "不支持的API类型",
    "105": "不支持的签名类型",
    "106": "不支持的响应类型",
    "107": "不支持的传输加密类型",
    "108": "应用ID无效，注册账号，登录后台创建应用并完成绑定，可获得应用ID和应用密钥等信息",
    "109": "batchLog格式不正确",
    "110": "无相关服务的有效应用,应用没有绑定服务应用，可以新建服务应用。注：某些服务的翻译结果发音需要tts服务，需要在控制台创建语音合成服务绑定应用后方能使用。",
    "111": "开发者账号无效",
    "112": "请求服务无效",
    "113": "q不能为空",
    "114": "不支持的图片传输方式",
    "116": "strict字段取值无效，请参考文档填写正确参数值",
    "201": "解密失败，可能为DES,BASE64,URLDecode的错误",
    "202": "签名检验失败,如果确认应用ID和应用密钥的正确性，仍返回202，一般是编码问题。请确保翻译文本 q 为UTF-8编码.",
    "203": "访问IP地址不在可访问IP列表",
    "205": "请求的接口与应用的平台类型不一致，确保接入方式（Android SDK、IOS SDK、API）与创建的应用平台类型一致。如有疑问请参考入门指南",
    "206": "因为时间戳无效导致签名校验失败",
    "207": "重放请求",
    "301": "辞典查询失败",
    "302": "翻译查询失败",
    "303": "服务端的其它异常",
    "304": "会话闲置太久超时",
    "308": "rejectFallback参数错误",
    "309": "domain参数错误",
    "310": "未开通领域翻译服务",
    "401": "账户已经欠费，请进行账户充值",
    "402": "offlinesdk不可用",
    "411": "访问频率受限,请稍后访问",
    "412": "长请求过于频繁，请稍后访问",
    "1001": "无效的OCR类型",
    "1002": "不支持的OCR image类型",
    "1003": "不支持的OCR Language类型",
    "1004": "识别图片过大",
    "1201": "图片base64解密失败",
    "1301": "OCR段落识别失败",
    "1411": "访问频率受限",
    "1412": "超过最大识别字节数",
    "2003": "不支持的语言识别Language类型",
    "2004": "合成字符过长",
    "2005": "不支持的音频文件类型",
    "2006": "不支持的发音类型",
    "2201": "解密失败",
    "2301": "服务的异常",
    "2411": "访问频率受限,请稍后访问",
    "2412": "超过最大请求字符数",
    "3001": "不支持的语音格式",
    "3002": "不支持的语音采样率",
    "3003": "不支持的语音声道",
    "3004": "不支持的语音上传类型",
    "3005": "不支持的语言类型",
    "3006": "不支持的识别类型",
    "3007": "识别音频文件过大",
    "3008": "识别音频时长过长",
    "3009": "不支持的音频文件类型",
    "3010": "不支持的发音类型",
    "3201": "解密失败",
    "3301": "语音识别失败",
    "3302": "语音翻译失败",
    "3303": "服务的异常",
    "3411": "访问频率受限,请稍后访问",
    "3412": "超过最大请求字符数",
    "4001": "不支持的语音识别格式",
    "4002": "不支持的语音识别采样率",
    "4003": "不支持的语音识别声道",
    "4004": "不支持的语音上传类型",
    "4005": "不支持的语言类型",
    "4006": "识别音频文件过大",
    "4007": "识别音频时长过长",
    "4201": "解密失败",
    "4301": "语音识别失败",
    "4303": "服务的异常",
    "4411": "访问频率受限,请稍后访问",
    "4412": "超过最大请求时长",
    "5001": "无效的OCR类型",
    "5002": "不支持的OCR image类型",
    "5003": "不支持的语言类型",
    "5004": "识别图片过大",
    "5005": "不支持的图片类型",
    "5006": "文件为空",
    "5201": "解密错误，图片base64解密失败",
    "5301": "OCR段落识别失败",
    "5411": "访问频率受限",
    "5412": "超过最大识别流量",
    "9001": "不支持的语音格式",
    "9002": "不支持的语音采样率",
    "9003": "不支持的语音声道",
    "9004": "不支持的语音上传类型",
    "9005": "不支持的语音识别 Language类型",
    "9301": "ASR识别失败",
    "9303": "服务器内部错误",
    "9411": "访问频率受限（超过最大调用次数）",
    "9412": "超过最大处理语音长度",
    "10001": "无效的OCR类型",
    "10002": "不支持的OCR image类型",
    "10004": "识别图片过大",
    "10201": "图片base64解密失败",
    "10301": "OCR段落识别失败",
    "10411": "访问频率受限",
    "10412": "超过最大识别流量",
    "11001": "不支持的语音识别格式",
    "11002": "不支持的语音识别采样率",
    "11003": "不支持的语音识别声道",
    "11004": "不支持的语音上传类型",
    "11005": "不支持的语言类型",
    "11006": "识别音频文件过大",
    "11007": "识别音频时长过长，最大支持30s",
    "11201": "解密失败",
    "11301": "语音识别失败",
    "11303": "服务的异常",
    "11411": "访问频率受限,请稍后访问",
    "11412": "超过最大请求时长",
    "12001": "图片尺寸过大",
    "12002": "图片base64解密失败",
    "12003": "引擎服务器返回错误",
    "12004": "图片为空",
    "12005": "不支持的识别图片类型",
    "12006": "图片无匹配结果",
    "13001": "不支持的角度类型",
    "13002": "不支持的文件类型",
    "13003": "表格识别图片过大",
    "13004": "文件为空",
    "13301": "表格识别失败",
    "15001": "需要图片",
    "15002": "图片过大（1M）",
    "15003": "服务调用失败",
    "17001": "需要图片",
    "17002": "图片过大（1M）",
    "17003": "识别类型未找到",
    "17004": "不支持的识别类型",
    "17005": "服务调用失败",
    "500": "有道翻译失败"
}

ICON_DEFAULT = 'icon.png'
ICON_PHONETIC = 'icon_phonetic.png'
ICON_BASIC = 'icon_basic.png'
ICON_WEB = 'icon_web.png'
ICON_UPDATE = 'icon_update.png'
ICON_ERROR = 'icon_error.png'

QUERY_LANGUAGE = 'EN2zh-CHS'





def get_user_id():
    user_id = wf.stored_data('user__id')
    if user_id == None:
        user_id = str(uuid.uuid1())
    wf.store_data('user__id', user_id)
    return user_id


def get_youdao_url(query):
    # 构建有道翻译URL
    zhiyun_id = os.getenv('zhiyun_id', '').strip()
    zhiyun_key = os.getenv('zhiyun_key', '').strip()
    if zhiyun_id and zhiyun_key:
        url = get_youdao_new_url(query, zhiyun_id, zhiyun_key)
    else:
        url = ''
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
    import urllib.parse
    import hashlib
    import uuid

    curtime = str(int(time.time()))
    salt = str(uuid.uuid1())
    signStr = zhiyun_id + truncate(query) + salt + curtime + zhiyun_key
    sign = encrypt(signStr)
    data_form, data_to = QUERY_LANGUAGE.split('2')

    url = 'https://openapi.youdao.com/api' + \
        '?appKey=' + str(zhiyun_id) + \
        '&salt=' + str(salt) + \
        '&sign=' + str(sign) + \
        '&q=' + urllib.parse.quote(str(query)) + \
        '&from=' + data_form + \
        '&to=' + data_to + \
        '&signType=v3' + \
        '&curtime=' + curtime
    return url


def fetch_translation(query):
    from urllib import request

    # 获取翻译数据
    url = get_youdao_url(query)
    if url == '':
        rt = {}
        rt['errorCode'] = "108"
        return rt
    try:
        data = request.urlopen(url).read()
        rt = json.loads(data)
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

def get_query_language(query):
    import re
    global QUERY_LANGUAGE
    # 检查中文
    if re.search(r"[\u4e00-\u9fa5]+", query):
        QUERY_LANGUAGE = "zh-CHS2EN"
    # 检查韩语
    elif re.search(r"[\uAC00-\uD7A3]+", query):
        QUERY_LANGUAGE = "KO2zh-CHS"
    # 检查日语
    elif re.search(r"[\u0800-\u4e00]+", query):
        QUERY_LANGUAGE = "JA2zh-CHS"


def get_arg_str(query, result, pronounce='', operation='', query_language=''):
    if query_language == '':
        query_language = QUERY_LANGUAGE
    arg_array = [str(wf.version), query, result,
                 query_language, pronounce, operation]
    return '$%'.join(arg_array)


# def get_l(query, rt):
#     if u'l' in rt.keys():
#         if rt["l"] is not None:
#             QUERY_LANGUAGE = rt["l"]


def add_translation(query, rt):
    # 翻译结果
    subtitle = '翻译结果'
    translations = rt["translation"]
    for title in translations:
        arg = get_arg_str(query, title)
        save_history_data(query, title, arg, ICON_DEFAULT)

        wf.add_item(
            title=title, subtitle=subtitle, arg=arg,
            valid=True, icon=ICON_DEFAULT)


def add_phonetic(query, rt):
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
                data_form, data_to = QUERY_LANGUAGE.split('2')
                arg = get_arg_str(query, title, pronounce=query,
                                  query_language=data_form)

                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg,
                    valid=True, icon=ICON_PHONETIC)


def add_explains(query, rt):
    # 简明释意
    if u'basic' in rt.keys():
        if rt["basic"] is not None:
            for i in range(len(rt["basic"]["explains"])):
                title = rt["basic"]["explains"][i]
                subtitle = '简明释意'
                arg = get_arg_str(query, title)

                wf.add_item(
                    title=title, subtitle=subtitle, arg=arg,
                    valid=True, icon=ICON_PHONETIC)


def add_web_translation(query, rt):
  # 网络翻译
    if u'web' in rt.keys():
        if rt["web"] is not None:
            for i in range(len(rt["web"])):
                values = rt["web"][i]["value"]
                for value in values:
                    title = value
                    key = rt["web"][i]["key"]
                    subtitle = '网络翻译: ' + key

                    if QUERY_LANGUAGE.split('2')[1] == 'EN':
                        arg = get_arg_str(query, title, pronounce=value)
                    else:
                        arg = get_arg_str(query, title, pronounce=key)

                    wf.add_item(
                        title=title, subtitle=subtitle,
                        arg=arg, valid=True, icon=ICON_WEB)


def main(wf):
    query = wf.args[0].strip()

    if query == "*":
        get_history_data()
    else:
        get_query_language(query)
        rt = fetch_translation(query)
        errorCode = str(rt.get("errorCode"))

        if errorCode in ERRORCODE_DICT:
            arg = get_arg_str('', '', operation='error')
            wf.add_item(
                title=errorCode + " " + ERRORCODE_DICT[errorCode],
                subtitle='', arg=arg,
                valid=True, icon=ICON_ERROR)

        elif errorCode == "0":
            # get_l(query, rt)
            add_translation(query, rt)
            add_phonetic(query, rt)
            add_explains(query, rt)
            add_web_translation(query, rt)

        else:
            title = '有道也翻译不出来了'
            subtitle = '尝试一下去网站搜索'
            arg = get_arg_str(query, '')
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_DEFAULT)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
