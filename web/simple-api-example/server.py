"""Local preview server: GET /health, GET /api/summary?values=10,20,30."""
import argparse
import json
import math
import statistics
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/':
            body = (Path(__file__).resolve().parents[1] / 'simple-dashboard-example/index.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if url.path == '/health':
            self.reply(200, {'ok': True})
            return
        if url.path != '/api/summary':
            self.reply(404, {'error': 'Not found'})
            return
        try:
            raw = parse_qs(url.query).get('values', [''])[0]
            if not raw or len(raw) > 10000:
                raise ValueError('Enter comma-separated numbers (maximum 10000 characters)')
            values = [float(item.strip()) for item in raw.split(',')]
            if not all(math.isfinite(value) for value in values):
                raise ValueError('Only finite numbers are accepted')
            self.reply(200, {'count': len(values), 'mean': statistics.mean(values), 'min': min(values), 'max': max(values)})
        except ValueError as error:
            self.reply(400, {'error': str(error)})

    def reply(self, status, data):
        body = json.dumps(data, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), Handler) as server:
        print('Preview on %s:%d (Ctrl+C to stop)' % server.server_address, flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
