"""Extract page-tagged PDF text locally; no OCR or external calls."""
import argparse


def extract(path):
    from pypdf import PdfReader
    reader = PdfReader(path)
    if reader.is_encrypted and not reader.decrypt(''):
        raise ValueError('Password-protected PDF is not supported')
    for number, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ''
        yield f'\n--- PAGE {number} ---\n{text if text.strip() else "[NO TEXT: scan/image or extraction failure; visual review required]"}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path')
    args = parser.parse_args()
    try:
        for page in extract(args.path):
            print(page)
    except Exception as error:
        parser.exit(1, f'Error: {error}\n')
