"""Check an explicitly supplied HTTP endpoint; exits 1 on mismatch."""
import argparse
import json
import math
import urllib.error
import urllib.request


def check(url, expected=200, required=(), timeout=5):
    request = urllib.request.Request(url, headers={'Accept': 'application/json'})
    try:
        response = urllib.request.urlopen(request, timeout=timeout)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        status = response.code
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
