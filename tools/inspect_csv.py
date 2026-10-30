"""Read-only CSV inspection; Python standard library only."""
import argparse
import csv
import io
import json
import math
import statistics
from collections import Counter
from pathlib import Path


def inspect(path, encoding=None, delimiter=None, sample=5):
    raw = Path(path).read_bytes()
    if encoding:
        text, used = raw.decode(encoding), encoding
    else:
        for used in ('utf-8-sig', 'cp949', 'utf-16'):
            try:
                text = raw.decode(used)
                break
            except UnicodeError:
                continue
        else:
            raise ValueError('Encoding unknown; pass --encoding explicitly')
    if delimiter is None:
        try:
            delimiter = csv.Sniffer().sniff(text[:65536], delimiters=',;\t|').delimiter
        except csv.Error:
            delimiter = ','
    rows = list(csv.reader(io.StringIO(text), delimiter=delimiter))
    if not rows:
        return {'encoding': used, 'rows': 0, 'columns': [], 'warning': 'empty file'}
    header, data = rows[0], rows[1:]
    columns = []
    for i, name in enumerate(header):
        values = [row[i] if i < len(row) else '' for row in data]
        missing = sum(not value.strip() for value in values)
        present = [value for value in values if value.strip()]
        numbers = []
        for value in present:
            try:
                number = float(value)
                if math.isfinite(number):
                    numbers.append(number)
            except ValueError:
                pass
        item = {'index': i, 'name': name, 'blank_or_absent': missing,
                'numeric_parseable': len(numbers), 'nonblank': len(present),
                'inferred_type': 'empty' if not present else 'numeric' if len(numbers) == len(present) else 'text_or_mixed'}
        if numbers:
            item['numeric_summary'] = {'count': len(numbers), 'min': min(numbers), 'max': max(numbers), 'mean': statistics.mean(numbers)}
        columns.append(item)
    return {'encoding': used, 'delimiter': delimiter, 'rows': len(data),
            'columns': columns, 'duplicate_headers': [k for k,v in Counter(header).items() if v > 1],
            'duplicate_rows': len(data) - len({tuple(row) for row in data}),
            'ragged_row_count': sum(len(row) != len(header) for row in data),
            'samples': data[:sample],
            'notes': ['No source data was changed.', 'NULL/NA are preserved as text; missing counts cover blanks and absent fields only.', 'All rows are loaded into memory; use a separate chunked approach for large files.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--encoding')
    parser.add_argument('--delimiter')
    parser.add_argument('--sample', type=int, default=5)
    args = parser.parse_args()
    try:
        if args.sample < 0:
            parser.error('--sample must be nonnegative')
        print(json.dumps(inspect(args.path, args.encoding, args.delimiter, args.sample), ensure_ascii=False, indent=2))
    except (OSError, ValueError, UnicodeError, csv.Error) as error:
        parser.exit(1, f'Error: {error}\n')
