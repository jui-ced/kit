"""Create synthetic XLSX/PDF examples without overwriting existing files."""
from pathlib import Path
from openpyxl import Workbook
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

folder = Path(__file__).resolve().parent
xlsx = folder / 'sample.xlsx'
pdf = folder / 'sample.pdf'
if xlsx.exists() or pdf.exists():
    raise SystemExit('Samples already exist; existing files were not changed.')
book = Workbook()
sheet = book.active
sheet.title = 'Data'
sheet.append(['id', 'value'])
sheet.append(['A', 10])
sheet.append(['B', None])
book.create_sheet('Notes').append(['Synthetic example only'])
book.save(xlsx)
writer = PdfWriter()
page = writer.add_blank_page(width=612, height=792)
font = DictionaryObject({NameObject('/Type'): NameObject('/Font'), NameObject('/Subtype'): NameObject('/Type1'), NameObject('/BaseFont'): NameObject('/Helvetica')})
page[NameObject('/Resources')] = DictionaryObject({NameObject('/Font'): DictionaryObject({NameObject('/F1'): writer._add_object(font)})})
stream = DecodedStreamObject()
stream.set_data(b'BT /F1 12 Tf 72 720 Td (Synthetic sample page 1) Tj ET')
page[NameObject('/Contents')] = writer._add_object(stream)
writer.add_blank_page(width=612, height=792)
with pdf.open('wb') as output:
    writer.write(output)
print('Created synthetic sample.xlsx and sample.pdf')
