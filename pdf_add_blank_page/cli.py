import argparse

from .core import add_blank_page
from .strategies import EndOfFilePageStrategy, BetweenPageStrategy


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('pdf_input', type=str)
    parser.add_argument('--pdf-output', type=str, default=None)
    parser.add_argument('--alpha', type=float, default=.7)
    parser.add_argument('--nb-pages', type=int, default=1)
    parser.add_argument('--end-of-file', type=bool, default=False)

    args = parser.parse_args()
    strategy = BetweenPageStrategy(args.nb_pages, args.alpha)
    if args.end_of_file:
        strategy = EndOfFilePageStrategy(args.nb_pages)
    add_blank_page(args.pdf_input, strategy, args.pdf_output)
