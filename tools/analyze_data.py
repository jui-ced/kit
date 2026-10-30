"""Read-only CSV filtering and grouped numeric summaries (standard library)."""
import argparse
import csv
import json
import math
import statistics
from collections import defaultdict


def analyze(path, value, group=None, where=None, encoding='utf-8-sig'):
    groups = defaultdict(lambda: {'rows': 0, 'missing': 0, 'invalid': 0, 'values': []})
    with open(path, encoding=encoding, newline='') as source:
        reader = csv.DictReader(source)
        headers = reader.fieldnames or []
        if not headers or len(set(headers)) != len(headers):
            raise ValueError('CSV needs nonduplicate headers')
        condition = None
        if where:
            key, sep, expected = where.partition('=')
            if not sep:
                raise ValueError('--where must be COLUMN=VALUE')
            condition = (key, expected)
        for column in [value, group, condition[0] if condition else None]:
            if column is not None and column not in headers:
                raise ValueError('Unknown column: ' + column)
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError('Ragged CSV row at line ' + str(reader.line_num))
            if condition and row[condition[0]] != condition[1]:
                continue
            item = groups[row[group] if group else 'ALL']
            item['rows'] += 1
            raw = row[value].strip()
            if not raw:
                item['missing'] += 1
                continue
            try:
                number = float(raw)
                if not math.isfinite(number):
                    raise ValueError('nonfinite')
                item['values'].append(number)
            except ValueError:
                item['invalid'] += 1
    result = []
    for key, item in sorted(groups.items()):
        numbers = item.pop('values')
        result.append(dict(group=key, **item, count=len(numbers),
                           mean=statistics.mean(numbers) if numbers else None,
                           min=min(numbers) if numbers else None,
                           max=max(numbers) if numbers else None))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--value', required=True)
    parser.add_argument('--group')
    parser.add_argument('--where', help='Exact text equality: COLUMN=VALUE')
    parser.add_argument('--encoding', default='utf-8-sig')
    args = parser.parse_args()
    try:
        print(json.dumps(analyze(args.path, args.value, args.group, args.where, args.encoding), ensure_ascii=False, indent=2, allow_nan=False))
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, 'Error: %s\n' % error)
