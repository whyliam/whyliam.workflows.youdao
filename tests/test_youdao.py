import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit
import youdao
import splitargs


class WorkflowTests(unittest.TestCase):
    def test_encoded_query(self):
        q = 'hello & goodbye #你好?'
        self.assertEqual(parse_qs(urlsplit(youdao.get_youdao_url(q)).query)['q'], [q])

    def test_languages(self):
        for q, lang in [('今日はいい天気ですね', 'jap'), ('안녕하세요', 'ko'), ('你好', 'eng')]:
            self.assertEqual(youdao.get_query_language(q), lang)
        self.assertEqual(splitargs.detect_language('Hello, world!'), 'EN')

    def test_all_dictionaries(self):
        for key in ('ec', 'ce', 'jc', 'kc', 'cj', 'ck'):
            data = {key: {'word': [{'trs': [{'tr': [{'l': {'i': ['你好']}}]}]}]}}
            self.assertEqual(youdao.parse_results('test', data)[0]['title'], '你好')

    def test_chinese_fragments(self):
        data = {'ce': {'word': [{'trs': [{'tr': [{'l': {'i': ['', {'#text': 'hello'}, ' ', {'#text': 'world'}]}}]}]}]}}
        self.assertEqual(youdao.parse_results('你好', data)[0]['title'], 'hello world')

    def test_sentence(self):
        self.assertEqual(youdao.parse_results('test', {'fanyi': {'tran': '翻译'}})[0]['title'], '翻译')

    def test_payload_and_speech(self):
        q = 'hello; echo DANGER $(id) " $%\n你好'
        payload = youdao.make_item(q, 'result')['arg']
        self.assertEqual(splitargs.decode(payload), (q, 'result'))
        with patch('splitargs.subprocess.run') as run:
            self.assertEqual(splitargs.main([payload, 'pronounce']), 0)
            self.assertEqual(run.call_args.kwargs['input'], q)
            self.assertNotIn(q, run.call_args.args[0])

    def test_history(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {'alfred_workflow_data': directory}):
            Path(directory, 'history.jsonl').write_text('broken\n')
            for n in range(205):
                youdao.history([youdao.make_item('q"\\\n' + str(n), 'result')])
            self.assertEqual(len(youdao.history()), 9)
            self.assertEqual(len(Path(directory, 'history.jsonl').read_text().splitlines()), 200)
            for line in Path(directory, 'history.jsonl').read_text().splitlines():
                json.loads(line)

    def test_empty_and_failure(self):
        self.assertFalse(youdao.main([])['items'][0]['valid'])
        with patch('youdao.fetch', side_effect=TimeoutError('timeout')):
            self.assertIn('查询失败', youdao.main(['hello'])['items'][0]['title'])

    def test_legacy(self):
        self.assertEqual(splitargs.decode('4$%query$%result$%eng$%$%'), ('query', 'result'))

    def test_web_exact_match(self):
        self.assertEqual(youdao.parse_results('a', {'web_trans': {'web-translation': [{'key': 'another', 'trans': [{'value': '错误'}]}]}}), [])


if __name__ == '__main__':
    unittest.main()

class ActionTests(unittest.TestCase):
    def test_browser_action(self):
        from io import StringIO
        query = '你好 & #test'
        item = youdao.make_item(query, 'hello')
        with patch('sys.stdout', new_callable=StringIO) as output:
            self.assertEqual(splitargs.main([item['mods']['ctrl']['arg'], 'search']), 0)
            self.assertEqual(parse_qs(urlsplit(output.getvalue()).query)['word'], [query])

    def test_copy_action(self):
        from io import StringIO
        with patch('sys.stdout', new_callable=StringIO) as output:
            self.assertEqual(splitargs.main([youdao.make_item('q', 'hello $% "你好"')['arg'], 'copy']), 0)
            self.assertEqual(output.getvalue(), 'hello $% "你好"')
