#!/usr/bin/env python3
import re
import sys
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import time
import argparse
import os
import urllib.parse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "-o", "--dir", help="output directory. title of slide is used if omitted."
)
parser.add_argument(
    "-w", "--wait", help="time to wait transition in seconds.", type=int, default=1
)
parser.add_argument("url")
args = parser.parse_args()

urlobj = urllib.parse.urlparse(args.url)
url = urllib.parse.urlunparse(
    (urlobj.scheme, urlobj.netloc, urlobj.path, None, "?start=false&loop=false", None)
)

with Firefox() as ff:
    ff.get(url)
    time.sleep(1)

    el_title = ff.find_element(By.CSS_SELECTOR, "meta[itemprop=name]")
    title = el_title.get_attribute("content")
    print(title, file=sys.stderr)

    # create output directory
    dir = args.dir or re.sub(r'[<>:"/\\|?*]', "_", title)
    os.makedirs(dir, exist_ok=True)

    # get pages
    pages = ff.execute_script("return viewerData.docData[1].map(e=>e[0])")
    for i, page in enumerate(pages):
        print(f"{i+1}/{len(pages)}", file=sys.stderr)

        svg = ff.execute_script(
            'return document.querySelector(".punch-viewer-svgpage-svgcontainer > svg").outerHTML'
        )

        svgpath = os.path.join(dir, f"{i:05}.svg")
        with open(svgpath, "wt", encoding="utf-8") as f:
            f.write(svg)

        ff.find_element(By.CSS_SELECTOR, ".punch-viewer-svgpage-svgcontainer").click()
        time.sleep(args.wait)
    ff.close()
