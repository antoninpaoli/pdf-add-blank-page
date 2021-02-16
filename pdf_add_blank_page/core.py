from __future__ import annotations

from PyPDF2 import PdfFileWriter, PdfFileReader, pdf

from .strategies import BetweenPageStrategy, EndOfFilePageStrategy


def add_blank_page(file_path: str, strategy: BetweenPageStrategy | EndOfFilePageStrategy, output_path: str | None):
    """Add blank pages at selected positions

    Args:
        file_path (str): PDF file path
        strategy (BetweenPageStrategy|EndOfFilePageStrategy): strategy for adding pages
        output_path (str?): [optional] PDF file output path default to file_path
    """
    assert isinstance(strategy, BetweenPageStrategy) or isinstance(
        strategy, EndOfFilePageStrategy), 'only BetweenPageStrategy or EndOfFilePageStrategy are allowed'
    if not output_path:
        output_path = file_path
    file = open(file_path, 'rb')
    pdf_input = PdfFileReader(file)
    pdf_output = PdfFileWriter()
    strategy.start(pdf_input, pdf_output)
    with open(output_path, 'wb') as f:
        pdf_output.write(f)
    file.close()
