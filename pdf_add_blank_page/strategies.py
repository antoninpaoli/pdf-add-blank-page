import os

from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color


def _create_whitemark(width: int, height: int, alpha: float):
    PATH = '.watermark.pdf'
    c = canvas.Canvas(PATH)
    c.setFillColor(Color(255, 255, 255, alpha=alpha))
    c.rect(0, 0, width, height, fill=True, stroke=False)
    c.save()
    whitemark = PdfFileReader(PATH).getPage(0)
    os.remove(PATH)
    return whitemark


class PageStrategy:
    def __init__(self, nb_pages: int):
        self.nb_pages = nb_pages


class BetweenPageStrategy(PageStrategy):
    def __init__(self, nb_pages: int, alpha: float):
        """Create between Page strategie

        Args:
            nb_pages (int): number of blank pages you want between each pdf page
            alpha (float): transparency of the previous page used as background (0=invisible, 1=fully visible)
        """
        assert nb_pages > 0, 'nb copies must be at least 1'
        assert 0 <= alpha <= 1, 'alpha must be in [0,1]'
        PageStrategy.__init__(self, nb_pages)
        self.alpha = alpha

    def start(self, pdf_input: PdfFileReader, pdf_output: PdfFileWriter):
        page1 = pdf_input.getPage(0)
        box = page1.mediaBox
        width, height = box.getWidth(), box.getHeight()
        whitemark = _create_whitemark(width, height, self.alpha)

        for i in range(pdf_input.getNumPages()):
            page = pdf_input.getPage(i)
            pdf_output.addPage(page)
            for _ in range(self.nb_pages):
                transparent_page = pdf.PageObject.createBlankPage(
                    width=width, height=height)
                transparent_page.mergePage(page)
                transparent_page.mergePage(whitemark)
                pdf_output.addPage(transparent_page)


class EndOfFilePageStrategy(PageStrategy):
    def __init__(self, nb_pages: int):
        """Create between at end of file

        Args:
            nb_pages (int): number of blank pages you want between each pdf page
        """
        assert nb_pages > 0, 'nb copies must be at least 1'
        PageStrategy.__init__(self, nb_pages)

    def start(self, pdf_input: PdfFileReader, pdf_output: PdfFileWriter):
        page1 = pdf_input.getPage(0)
        box = page1.mediaBox
        width, height = box.getWidth(), box.getHeight()

        for i in range(pdf_input.getNumPages()):
            page = pdf_input.getPage(i)
            pdf_output.addPage(page)
        for _ in range(self.nb_pages):
            blank_page = pdf.PageObject.createBlankPage(
                width=width, height=height)
            pdf_output.addPage(blank_page)
