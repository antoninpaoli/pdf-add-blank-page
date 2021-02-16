from __future__ import annotations
from io import BytesIO

import requests

from PyPDF2 import PdfFileWriter, PdfFileReader
from requests import request

from .strategies import BetweenPageStrategy, EndOfFilePageStrategy
from .constants import BASE_URL


def add_blank_page(file_path: str, strategy: BetweenPageStrategy | EndOfFilePageStrategy, output_path: str=None):
    """Add blank pages at selected positions

    Args:
        file_path (str|BytesIO): PDF file path or PDF file
        strategy (BetweenPageStrategy|EndOfFilePageStrategy): strategy for adding pages
        output_path (str?): [optional] PDF file output path default to file_path
    """
    assert isinstance(strategy, BetweenPageStrategy) or isinstance(
        strategy, EndOfFilePageStrategy), 'only BetweenPageStrategy or EndOfFilePageStrategy are allowed'
    if not output_path:
        output_path = file_path
    file = open(file_path, 'rb') if isinstance(file_path, str) else file_path
    pdf_input = PdfFileReader(file)
    pdf_output = PdfFileWriter()
    strategy.start(pdf_input, pdf_output)
    if isinstance(output_path, str):
        with open(output_path, 'wb') as f:
            pdf_output.write(f)
    else:
        pdf_output.write(output_path)
    file.close()


def add_blank_page_remotely(file_path: str | BytesIO, strategy: BetweenPageStrategy | EndOfFilePageStrategy, output_path: str | BytesIO = None):
    """Add blank pages at selected positions (remotely)

    Args:
        file_path (str|BytesIO): PDF file path or PDF file
        strategy (BetweenPageStrategy|EndOfFilePageStrategy): strategy for adding pages
        output_path (str?): [optional] PDF file output path default to file_path
    """
    assert isinstance(strategy, BetweenPageStrategy) or isinstance(
        strategy, EndOfFilePageStrategy), 'only BetweenPageStrategy or EndOfFilePageStrategy are allowed'
    if not output_path:
        output_path = file_path

    file = open(file_path, 'rb') if isinstance(file_path, str) else file_path

    r = requests.post(strategy.toUrl(), files={'file': file}, stream=True)

    if not r.ok:
        raise Exception(r.content)

    if isinstance(output_path, str):
        with open(output_path, 'wb') as f:
            f.write(r.content)
    else:
        output_path.write(r.content)
    file.close()
