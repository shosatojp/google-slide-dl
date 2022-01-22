#!/usr/bin/env python3
import os
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor, Future
from typing import List


def svg2pdf(svg: str) -> str:
    pdf = svg + '.pdf'
    subprocess.run(
        ['cairosvg', '-f', 'pdf', svg, '-o', pdf],
        check=True
    )
    return pdf


def concatpdf(pdfs: List[str], output: str):
    subprocess.run(
        ['pdftk', *pdfs, 'cat', 'output', output],
        check=True
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('svgs', nargs='+')
    parser.add_argument('output')
    args = parser.parse_args()

    fs: List[Future] = []
    pool = ThreadPoolExecutor(os.cpu_count())
    for svg in args.svgs:
        fs.append(pool.submit(svg2pdf, svg))

    pdfs = []
    for f in fs:
        pdfs.append(f.result())
    concatpdf(pdfs, args.output)

    for pdf in pdfs:
        os.remove(pdf)
