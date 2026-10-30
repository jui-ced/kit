import importlib.util
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DataTests(unittest.TestCase):
    def test_group_filter_and_missing(self):
        analyze = load('tools/analyze_data.py').analyze
        groups = {r['group']: r for r in analyze(ROOT / 'examples/sample.csv', 'value', 'status')}
        self.assertAlmostEqual(groups['ok']['mean'], 70 / 3)
        self.assertEqual(groups['unknown']['missing'], 1)
        self.assertEqual(groups['review']['invalid'], 1)
        self.assertEqual(analyze(ROOT / 'examples/sample.csv', 'value', where='id=A')[0]['mean'], 10)
        self.assertEqual(analyze(ROOT / 'examples/sample.csv', 'value', where='id=Z'), [])

    def test_bad_csv_and_nonfinite(self):
        analyze = load('tools/analyze_data.py').analyze
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'data.csv'
            for content in ['', 'x,x\n1,2', 'x,y\n1', 'x,y\n1,2,3']:
                path.write_text(content, encoding='utf-8')
                with self.assertRaises(ValueError):
                    analyze(path, 'x')
            path.write_text('x\nNaN\nInfinity\n-2', encoding='utf-8')
            row = analyze(path, 'x')[0]
            self.assertEqual((row['invalid'], row['mean']), (2, -2))

    def test_json_validation(self):
        validate = load('tools/validate_json.py').validate
        self.assertTrue(validate('[{"id":0}]', ['id'], True)['valid'])
        self.assertEqual(validate('[]', ['id'], True)['records_checked'], 0)
        for text in ['{"id":null}', '{}', '{"id":1,"id":2}', '{"id":NaN}', '{', '[]']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                validate(text, ['id'])

    def test_cli_exit_and_output(self):
        command = [sys.executable, str(ROOT / 'tools/validate_json.py'), str(ROOT / 'examples/sample.json'), '--each', '--required']
        run = subprocess.run(command + ['id'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['records_checked'], 3)
        run = subprocess.run(command + ['value'], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1)
        self.assertIn('null', run.stderr)


class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = load('web/simple-api-example/server.py').Handler
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://127.0.0.1:%d' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_summary_and_dashboard(self):
        import urllib.request
        with urllib.request.urlopen(self.url + '/api/summary?values=-10,20,30') as response:
            data = json.load(response)
        self.assertEqual(data['count'], 3)
        self.assertAlmostEqual(data['mean'], 40 / 3)
        self.assertEqual((data['min'], data['max']), (-10, 30))
        with urllib.request.urlopen(self.url + '/') as response:
            self.assertIn(b'id="form"', response.read())

    def test_smoke_and_errors(self):
        check = load('tools/smoke_test.py').check
        self.assertTrue(check(self.url + '/health', required=['ok'])['ok'])
        for value in ['', 'bad', 'NaN', 'Infinity', '1,,2']:
            self.assertEqual(check(self.url + '/api/summary?values=' + value, 400, ['error'])['status'], 400)
        self.assertEqual(check(self.url + '/missing', 404)['status'], 404)
        with self.assertRaises(ValueError):
            check(self.url + '/missing')
        with self.assertRaises(ValueError):
            check(self.url + '/health', required=['missing'])


if __name__ == '__main__':
    unittest.main()
