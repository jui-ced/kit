"""Read-only .xlsx inspection. Formulas are displayed, never calculated."""
import argparse
import json
from pathlib import Path


def inspect(path, sample=5):
    from openpyxl import load_workbook
    workbook = load_workbook(Path(path), read_only=True, data_only=False)
    try:
        result = []
        for sheet in workbook:
            rows = sheet.iter_rows(values_only=True)
            header = next(rows, ())
            preview = []
            for _, row in zip(range(sample), rows):
                preview.append(list(row))
            result.append({'sheet': sheet.title, 'reported_rows': sheet.max_row,
                           'reported_columns': sheet.max_column, 'first_row': list(header), 'samples': preview})
        return {'sheets': result, 'notes': ['Source unchanged. First row is a header candidate only.', 'Dimensions come from workbook metadata and may include formatted empty cells.', 'Formulas are not recalculated; .xls is not supported.']}
    finally:
        workbook.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    parser.add_argument('--sample', type=int, default=5)
    args = parser.parse_args()
    try:
        if args.sample < 0:
            parser.error('--sample must be nonnegative')
        print(json.dumps(inspect(args.path, args.sample), ensure_ascii=False, indent=2, default=str))
    except Exception as error:
        parser.exit(1, f'Error: {error}\n')
