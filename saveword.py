# -*- coding: utf-8 -*-
import sys
import os
import re
import json
import cookielib
import urllib2
import urllib
import hashlib
import logging

from workflow import Workflow3

reload(sys)
sys.setdefaultencoding('utf8')


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        result.headers = headers
        return result


cookie_filename = 'youdao_cookie'
fake_header = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'),
    ('Content-Type', 'application/x-www-form-urlencoded'),
    ('Cache-Control', 'no-cache'),
    ('Accept', '*/*'),
    ('Connection', 'Keep-Alive'),
]


class SaveWord(object):

    def __init__(self, username, password, localfile, word):

        self.username = username
        self.password = password
        self.localfile = localfile
        self.word = word
        self.cj = cookielib.LWPCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load(cookie_filename, ignore_discard=True,
                         ignore_expires=True)
        self.opener = urllib2.build_opener(
            SmartRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = fake_header

    def loginToYoudao(self):
        self.cj.clear()
        first_page = self.opener.open(
            'https://account.youdao.com/login?back_url=http://dict.youdao.com&service=dict')
        login_data = urllib.urlencode({
            'app': 'web',
            'tp': 'urstoken',
            'cf': '7',
            'fr': '1',
            'ru': 'http://dict.youdao.com',
            'product': 'DICT',
            'type': '1',
            'um': 'true',
            'username': self.username,
            'password': self.password,
            'savelogin': '1',
        })
        response = self.opener.open(
            'https://logindict.youdao.com/login/acc/login', login_data)
        if response.headers.get('Set-Cookie') != None:
            if response.headers.get('Set-Cookie').find(self.username) > -1:
                self.cj.save(cookie_filename, ignore_discard=True,
                             ignore_expires=True)
                return True
            else:
                return False
        else:
            return False

    def syncToYoudao(self):
        post_data = urllib.urlencode({
            'word': self.word.get('word'),
            'phonetic': self.word.get('phonetic'),
            'desc': self.word.get('trans'),
            'tags': self.word.get('tags'),
        })
        self.opener.addheaders = fake_header + [
            ('Referer', 'http://dict.youdao.com/wordbook/wordlist'),
        ]
        response = self.opener.open(
            'http://dict.youdao.com/wordbook/wordlist?action=add', post_data)
        return response.headers.get('Location') == 'http://dict.youdao.com/wordbook/wordlist'

    def generateWordBook(self, source_xml):
        item = self.word
        item_xml = '<item>'
        for i in item:
            value = '<![CDATA[' + item[i] + ']]>' if i in ["trans",
                                                           "phonetic"] else item[i]
            item_xml = item_xml + '<' + i + '>' + value + '</' + i + '>\n'
        item_xml = item_xml + '</item>\n'

        source_xml = re.sub('<item>(?:(?!<\/item>)[\s\S])*<word>' + item.get(
            "word") + '<\/word>[\s\S]*?<\/item>\n', '', source_xml)
        if source_xml.find('</wordbook>') > -1:
            source_xml = source_xml.replace('</wordbook>', '') + item_xml
        else:
            source_xml = '<wordbook>\n' + item_xml
        return source_xml + '</wordbook>'

    def saveLocal(self):
        try:
            source_xml = ''
            if os.path.exists(self.localfile):
                f = open(self.localfile, 'r')
                source_xml = f.read()
                f.close()
            f = open(self.localfile, 'w')
            f.write(self.generateWordBook(source_xml))
            f.close()
        except Exception, e:
            return e
        return 0

    def save(self, wf):
        if self.syncToYoudao() or (self.loginToYoudao() and self.syncToYoudao()):
            sys.stdout.write('成功保存至线上单词本')
        else:
            result = self.saveLocal()
            sys.stdout.write('帐号出错，临时保存至本地单词本')


if __name__ == '__main__':
    params = sys.argv[1].split('$%')
    version = params[0]
    query = params[1]
    result = params[2]

    username = os.getenv('username', '').strip()
    password = os.getenv('password', '').strip()
    filepath = os.getenv('filepath', '').strip()
    if filepath is None:
        filepath = os.path.join(
            os.environ['HOME'], 'Documents/Alfred-youdao-wordbook.xml')
    else:
        filepath = os.path.expanduser(filepath)

    m2 = hashlib.md5()
    m2.update(password)
    password_md5 = m2.hexdigest()

    item = {
        "word": query,
        "trans": result,
        # "phonetic":
        "tags": "Alfred",
        "progress": "-1",
    }

    saver = SaveWord(username, password_md5, filepath, item)

    wf = Workflow3()
    sys.exit(wf.run(saver.save))
