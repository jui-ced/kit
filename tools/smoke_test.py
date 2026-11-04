"""Check a loopback-only HTTP(S) endpoint; no proxies or redirects."""
import argparse
import json
import math
import urllib.error
import urllib.request
from urllib.parse import urlsplit, urlunsplit


def local_url(url):
    if any(ord(char) <= 32 or ord(char) == 127 for char in url):
        raise ValueError('URL must not contain whitespace or control characters')
    parts = urlsplit(url)
    if parts.scheme not in ('http', 'https'):
        raise ValueError('Only HTTP(S) is allowed')
    if parts.username is not None or parts.password is not None or parts.fragment:
        raise ValueError('Credentials and fragments are not allowed')
    host = parts.hostname
    if host not in ('localhost', '127.0.0.1', '::1'):
        raise ValueError('Only localhost, 127.0.0.1 and [::1] are allowed')
    port = parts.port  # Reject malformed or out-of-range ports before connecting.
    if port == 0 or parts.netloc.endswith(':'):
        raise ValueError('Port must be between 1 and 65535')
    # Pin localhost to a numeric loopback address; do not resolve hostnames.
    authority = '[::1]' if host == '::1' else '127.0.0.1'
    if port is not None:
        authority += ':' + str(port)
    return urlunsplit((parts.scheme, authority, parts.path, parts.query, ''))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        fp.close()
        raise ValueError('Redirects are blocked; use the final loopback URL directly')


def check(url, expected=200, required=(), timeout=5):
    url = local_url(url)
    if not math.isfinite(timeout) or timeout <= 0:
        raise ValueError('Timeout must be finite and positive')
    request = urllib.request.Request(url, headers={'Accept': 'application/json'})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        response = opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        status = response.code
        if 300 <= status < 400:
            raise ValueError('Redirect responses are blocked')
        body = response.read(1024 * 1024 + 1)
    if status != expected:
        raise ValueError('Expected HTTP %d; got %d' % (expected, status))
    if len(body) > 1024 * 1024:
        raise ValueError('Response exceeds 1 MiB')
    if required:
        data = json.loads(body)
        if not isinstance(data, dict) or any(key not in data or data[key] is None for key in required):
            raise ValueError('Missing/null required JSON fields')
    return {'ok': True, 'status': status}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('url')
    parser.add_argument('--status', type=int, default=200)
    parser.add_argument('--required', nargs='+', default=[])
    parser.add_argument('--timeout', type=float, default=5)
    args = parser.parse_args()
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('--timeout must be finite and positive')
    try:
        print(json.dumps(check(args.url, args.status, args.required, args.timeout)))
    except (OSError, ValueError) as error:
        parser.exit(1, 'Error: %s\n' % error)
