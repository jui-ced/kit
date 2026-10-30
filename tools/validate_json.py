"""Strict JSON syntax and top-level required-field checks; not JSON Schema."""
import argparse
import json
from pathlib import Path


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('Nonstandard JSON constant: ' + value)


def validate(text, required=(), each=False):
    data = json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
    if each and not isinstance(data, list):
        raise ValueError('--each requires an array')
    records = data if each else [data]
    if required or each:
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                raise ValueError('Record %d must be an object' % index)
            for key in required:
                if key not in record or record[key] is None:
                    raise ValueError('Record %d: missing/null field %s' % (index, key))
    return {'valid': True, 'records_checked': len(records)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--required', nargs='+', default=[])
    parser.add_argument('--each', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(validate(Path(args.path).read_text(encoding='utf-8-sig'), args.required, args.each)))
    except (OSError, ValueError) as error:
        parser.exit(1, 'Error: %s\n' % error)
