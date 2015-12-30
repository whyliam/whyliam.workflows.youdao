# -*- coding: utf-8 -*-
import sys,os
import re
import json
from workflow import Workflow

reload(sys)
sys.setdefaultencoding('utf8')

def generate_word_item(item):
    xml = '<item>'
    for i in item:
        value = '<![CDATA[' + item[i] + ']]>' if i in ["trans", "phonetic"] else item[i]
        xml = xml + '<' + i + '>' + value + '</' + i + '>\n'
    return xml + '</item>\n'

def generate_word_book(source_xml, item):
    item_xml = generate_word_item(item)
    source_xml = re.sub('<item>(?:(?!<\/item>)[\s\S])*<word>'+ item.get("word") +'<\/word>[\s\S]*?<\/item>\n', '', source_xml)
    if source_xml.find('</wordbook>') > -1:
        source_xml = source_xml.replace('</wordbook>','') + item_xml
    else:
        source_xml = '<wordbook>\n' + item_xml
    return source_xml + '</wordbook>'

def save_word(wf):
    params = sys.argv[1].split('$')
    extra_args = json.loads(params[4])
    phonetic_type = sys.argv[2] if sys.argv[2] in ["uk","us"] else "uk"
    phonetic = extra_args.get(phonetic_type) if extra_args.get(phonetic_type) else ''

    item = {
        "word" : params[0],
        "trans" : params[1],
        "phonetic" : phonetic,
        "tags" : "Alfred",
        "progress" : "-1",
    }
    print item
    if len(sys.argv) > 3:
        filepath = sys.argv[3]
    else:
        filepath = os.path.join(os.environ['HOME'] , 'Documents/Alfred-youdao-wordbook.xml')
    try:
        source_xml = ''
        if os.path.exists(filepath):
            f = open(filepath,'r')
            source_xml = f.read()
            f.close()
        f = open(filepath,'w')
        f.write(generate_word_book(source_xml, item))
        f.close()
    except Exception,e:
        print Exception,':',e
    return 0

if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(save_word))