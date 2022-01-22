#!/usr/bin/env python3
from selenium.webdriver import Firefox
import time
import argparse
import os
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '-o', '--dir', help='output dir')
parser.add_argument(
    '-w', '--wait', help='time to wait transition in seconds.', type=int, default=1)
parser.add_argument('url')
args = parser.parse_args()

urlobj = urllib.parse.urlparse(args.url)
url = urllib.parse.urlunparse((urlobj.scheme, urlobj.netloc, urlobj.path,
                               None, '?start=false&loop=false', None))

os.makedirs(args.dir)

with Firefox() as ff:
    ff.get(url)
    time.sleep(1)

    pages = ff.execute_script('return viewerData.docData[1].map(e=>e[0])')
    for i, page in enumerate(pages):
        svg = ff.execute_script(
            'return document.querySelector(".punch-viewer-svgpage-svgcontainer > svg").outerHTML')

        filename = os.path.join(args.dir, f'{i:05}.svg')
        with open(filename, 'wt', encoding='utf-8') as f:
            f.write(svg)

        ff.find_element_by_css_selector(
            '.punch-viewer-svgpage-svgcontainer').click()
        time.sleep(args.wait)
    ff.close()
