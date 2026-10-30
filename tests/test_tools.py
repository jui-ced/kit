import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'tools' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CSVTests(unittest.TestCase):
    def test_missing_duplicate_and_source_preservation(self):
        path = ROOT / 'examples/sample.csv'
        before = path.read_bytes()
        result = load('inspect_csv').inspect(path)
        self.assertEqual(result['rows'], 5)
        self.assertEqual(result['duplicate_rows'], 1)
        self.assertEqual(result['columns'][1]['blank_or_absent'], 1)
        self.assertEqual(result['columns'][1]['numeric_parseable'], 3)
        self.assertEqual(path.read_bytes(), before)

    def test_encoding_ragged_duplicate_headers_and_nonfinite(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'data.csv'
            path.write_bytes('항목,항목\n가,NaN\n나\n'.encode('cp949'))
            result = load('inspect_csv').inspect(path)
            self.assertEqual(result['encoding'], 'cp949')
            self.assertEqual(result['duplicate_headers'], ['항목'])
            self.assertEqual(result['ragged_row_count'], 1)
            self.assertEqual(result['columns'][1]['numeric_parseable'], 0)

    def test_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'empty.csv'
            path.write_text('')
            self.assertEqual(load('inspect_csv').inspect(path)['rows'], 0)


class DocumentTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec('openpyxl'), 'optional dependency: openpyxl')
    def test_xlsx_formula_preserved(self):
        from openpyxl import Workbook
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'data.xlsx'
            book = Workbook()
            book.active.append(['value'])
            book.active.append(['=1+1'])
            book.save(path)
            result = load('inspect_excel').inspect(path)
            self.assertEqual(result['sheets'][0]['samples'], [['=1+1']])

    @unittest.skipUnless(importlib.util.find_spec('pypdf'), 'optional dependency: pypdf')
    def test_pdf_page_labels_and_empty_page(self):
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'blank.pdf'
            writer = PdfWriter()
            writer.add_blank_page(width=100, height=100)
            with path.open('wb') as output:
                writer.write(output)
            pages = list(load('extract_pdf').extract(path))
            self.assertIn('PAGE 1', pages[0])
            self.assertIn('NO TEXT', pages[0])


if __name__ == '__main__':
    unittest.main()
