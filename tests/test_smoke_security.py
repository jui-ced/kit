import importlib.util
import os
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('smoke_test', Path(__file__).resolve().parents[1] / 'tools/smoke_test.py')
smoke = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(smoke)


class LocalOnlyTests(unittest.TestCase):
    def test_normalizes_allowed_addresses(self):
        for url, expected in [
            ('http://localhost:8000/health', 'http://127.0.0.1:8000/health'),
            ('http://LOCALHOST/', 'http://127.0.0.1/'),
            ('http://127.0.0.1/', 'http://127.0.0.1/'),
            ('https://[::1]:8443/health', 'https://[::1]:8443/health'),
        ]:
            self.assertEqual(smoke.local_url(url), expected)

    def test_rejects_before_opening_network(self):
        urls = [
            'https://example.com/?data=secret', 'http://192.168.1.1/',
            'http://10.0.0.1/', 'http://169.254.169.254/', 'http://0.0.0.0/',
            'http://localhost.example.com/', 'http://localhost./',
            'http://127.1/', 'http://2130706433/', 'http://0x7f000001/',
            'http://[::ffff:127.0.0.1]/', 'http://127.0.0.1@evil.example/',
            'http://evil.example@127.0.0.1/', 'http://%6cocalhost/',
            'file:///etc/passwd', 'ftp://127.0.0.1/', '//127.0.0.1/',
            'http://127.0.0.1:0/', 'http://127.0.0.1:65536/',
            'http://127.0.0.1:bad/', 'http://127.0.0.1:/',
            'http://127.0.0.1/#fragment', 'http://local\nhost/',
            ' http://127.0.0.1/', 'http://localhost\\@evil.example/',
        ]
        with patch.object(smoke.urllib.request, 'build_opener') as opener:
            for url in urls:
                with self.subTest(url=url), self.assertRaises(ValueError):
                    smoke.check(url)
            opener.assert_not_called()


class Handler(BaseHTTPRequestHandler):
    visits = []

    def do_GET(self):
        type(self).visits.append(self.path)
        if self.path.startswith('/redirect/'):
            self.send_response(int(self.path.rsplit('/', 1)[1]))
            self.send_header('Location', '/destination')
        else:
            self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, *args):
        pass


class NetworkPolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://localhost:%d' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_environment_proxy_is_ignored(self):
        with patch.dict(os.environ, {'http_proxy': 'http://127.0.0.1:1',
                                     'HTTP_PROXY': 'http://127.0.0.1:1',
                                     'no_proxy': '', 'NO_PROXY': ''}):
            self.assertTrue(smoke.check(self.url + '/health', required=['ok'])['ok'])

    def test_redirect_never_reaches_destination(self):
        Handler.visits.clear()
        for code in (300, 301, 302, 303, 304, 307, 308):
            with self.subTest(code=code), self.assertRaises(ValueError):
                smoke.check(self.url + '/redirect/%d' % code, expected=code)
        self.assertNotIn('/destination', Handler.visits)


if __name__ == '__main__':
    unittest.main()
