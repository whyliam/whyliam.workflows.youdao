# -*- coding: utf-8 -*-

# 主要备注：
# 1. 该脚本用于与有道翻译API交互，获取翻译结果、发音和释义。
# 2. 使用BeautifulSoup解析HTML内容。
# 3. 记录历史查询到history.log文件中。

from workflow import Workflow3
import os
import json
import uuid
import time
import sys
import requests
from bs4 import BeautifulSoup


ICON_DEFAULT = 'icon.png'
ICON_PHONETIC = 'icon_phonetic.png'
ICON_BASIC = 'icon_basic.png'
ICON_WEB = 'icon_web.png'
ICON_UPDATE = 'icon_update.png'
ICON_ERROR = 'icon_error.png'

def get_user_id():
    # 获取用户ID，如果不存在则生成一个新的ID
    user_id = wf.stored_data('user__id')
    if user_id is None:
        user_id = str(uuid.uuid1())
    wf.store_data('user__id', user_id)
    return user_id

def get_query_language(query):
    # 根据输入的查询内容确定语言类型
    # 检查中文
    import re
    if re.search(r"[\u4e00-\u9fa5]+", query):
        return "eng"
    # 检查韩语
    elif re.search(r"[\uAC00-\uD7A3]+", query):
        return "ko"
    # 检查日语
    elif re.search(r"[\u3040-\u309F\u30A0-\u30FF]+", query):
        return "jap"
    else:
        return "eng"

def get_youdao_url(query):
    # 构建有道翻译的请求URL
    query_language = get_query_language(query)
    url = "http://mobile.youdao.com/dict?le=" + query_language + "&q=" + query
    return url

def get_youdao_response(query):
    # 发送请求并获取有道翻译的响应
    url = get_youdao_url(query)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }  # 添加请求头
    try:
        response = requests.get(url, headers=headers) 
        response.raise_for_status()  # 检查请求是否成功
        return response
    except requests.RequestException:
        return None

def get_youdao_soup(response):
    # 将响应内容解析为BeautifulSoup对象
    if response is None:  # 检查响应是否有效
        return None
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception:
        return None
    return soup

def save_history_data(query, title, arg, ICON_DEFAULT):
    # 将查询历史保存到文件中
    jsonData = '{"title": "%s", "subtitle": "%s", "arg": "%s", "icon": "%s"}\n' % (query, title, arg, ICON_DEFAULT)
    with open('history.log', 'a') as file:
        file.write(jsonData)

def get_history_data():
    # 从历史记录文件中读取最近的查询记录
    with open('history.log', 'r') as file:
        for line in file.readlines()[-1:-10:-1]:
            try:
                line = json.loads(line)
                wf.add_item(
                    title=line['title'], subtitle=line['subtitle'],
                    arg=line['arg'], valid=True, icon=line['icon'])
            except Exception:
                pass

def get_arg_str(query, result, pronounce='', operation='', query_language='eng'):
    arg_array = [str(wf.version), query, result, query_language, pronounce, operation]
    return '$%'.join(arg_array)

def add_translation(query, soup):
    # 翻译结果
    subtitle = '翻译结果'
    fanyi_content = soup.find('div', id='fanyi_contentWrp')  # 查找翻译内容
    if fanyi_content:  # 检查翻译内容是否存在
        translation = fanyi_content.find('p').find_next_sibling('p')  # 获取第二个 <p> 标签内容
        if translation:
            title = str(translation.get_text(strip=True))  # 转换为字符串
            arg = get_arg_str(query, title)
            save_history_data(query, title, arg, ICON_DEFAULT)
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_DEFAULT)

def add_phonetic(query, soup):
    # 发音
    subtitle = '有道发音'
    pronunciations = {}
    for span in soup.find_all('span', class_='phonetic'):
        preceding_text = span.find_previous('span').get_text(strip=True)  # 获取发音前的文本
        pronunciations[preceding_text] = span.get_text(strip=True)  # 将发音存入字典

    title = ' '.join([f"{lang}" for lang, pronunciation in pronunciations.items()])
    
    # 检查发音否为空
    if not title.strip():  # 如果标题为空则不执行 add_item
        return
    arg = get_arg_str(query, title)
    wf.add_item(
        title=title, subtitle=subtitle, arg=arg,
        valid=True, icon=ICON_PHONETIC)

def add_explains(query, soup):
    # 简明释意
    ec_content = soup.find('div', id='ec_contentWrp')  # 查找简明释意内容
    if ec_content:  # 检查内容是否存在
        definitions = [li.get_text(strip=True) for li in ec_content.find_all('li')] 
        for definition in definitions:
            title = definition
            subtitle = '简明释意'
            arg = get_arg_str(query, title)
            save_history_data(query, title, arg, ICON_DEFAULT)
            wf.add_item(
                title=title, subtitle=subtitle, arg=arg,
                valid=True, icon=ICON_BASIC)

def add_badcase(query):
    title = '有道也翻译不出来了'
    subtitle = '尝试一下去网站搜索'
    arg = get_arg_str(query, '')
    wf.add_item(
        title=title, subtitle=subtitle, arg=arg,
        valid=True, icon=ICON_DEFAULT)
    wf.send_feedback()

def main(wf):
    query = wf.args[0].strip()

    if query == "*":
        get_history_data()
    else:
        response = get_youdao_response(query)
        soup = get_youdao_soup(response)
        if soup is None:
            add_badcase(query)
            return
        else:
            add_translation(query, soup)
            add_phonetic(query, soup)
            add_explains(query, soup)
    if not wf._items: 
        add_badcase(query)
        return
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
