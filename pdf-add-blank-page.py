import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from PyPDF2 import PdfFileWriter, PdfFileReader, pdf


def parse_file(file_path: str):
    try:
        return open(file_path, 'rb')
    except FileNotFoundError:
        raise argparse.ArgumentTypeError(
            'file not found for "%s"' % (file_path))


def create_whitemark(width, height):
    c = canvas.Canvas('watermark.pdf')
    c.setFillColor(Color(255, 255, 255, alpha=.8))
    c.rect(0, 0, width, height, fill=True, stroke=False)
    c.save()
    return PdfFileReader('watermark.pdf').getPage(0)


parser = argparse.ArgumentParser()
parser.add_argument('pdf_input', type=parse_file)
parser.add_argument('pdf_output', type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    pdf_input = PdfFileReader(args.pdf_input)
    pdf_output = PdfFileWriter()

    page1 = pdf_input.getPage(0)
    box = page1.mediaBox
    width, height = box.getWidth(), box.getHeight()
    whitemark = create_whitemark(width, height)

    for i in range(pdf_input.getNumPages()):
        page = pdf_input.getPage(i)
        pdf_output.addPage(page)
        transparent_page = pdf.PageObject.createBlankPage(
            width=width, height=height)
        transparent_page.mergePage(page)
        transparent_page.mergePage(whitemark)
        pdf_output.addPage(transparent_page)

    with open(args.pdf_output, 'wb') as f:
        pdf_output.write(f)

    args.pdf_input.close()
