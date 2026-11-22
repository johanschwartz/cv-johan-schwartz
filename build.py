#!/usr/bin/env python3
"""Builds "Johan Schwartz - CV.pdf" from README.md.

Needs:
  - pandoc            https://pandoc.org/installing.html
  - Python 3 with Playwright:
        pip install playwright
        python -m playwright install chromium

Run from anywhere:
    python build.py
"""
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "README.md"
HTML = ROOT / "cv.html"
PDF = ROOT / "Johan Schwartz - CV.pdf"


def main() -> int:
    # 1. Markdown -> HTML. --section-divs wraps each role in a <section>,
    #    which style.css uses to keep every role on a single page.
    subprocess.run(
        [
            "pandoc", str(SOURCE),
            "-f", "markdown", "-t", "html5", "-s", "--section-divs",
            "--metadata", "pagetitle=Johan Schwartz - CV",
            "-c", "style.css",
            "-o", str(HTML),
        ],
        cwd=ROOT,
        check=True,
    )

    # 2. HTML -> PDF with headless Chromium, using the page size in style.css.
    try:
        with sync_playwright() as p:
            # Unhinted text. With Chromium's default font hinting on Linux, lines
            # wrap differently and the CV runs to three pages.
            browser = p.chromium.launch(args=["--font-render-hinting=none"])
            page = browser.new_page()
            page.goto(HTML.as_uri())
            page.wait_for_load_state("networkidle")
            page.pdf(path=str(PDF), format="A4", print_background=True,
                     prefer_css_page_size=True)
            browser.close()
    finally:
        HTML.unlink(missing_ok=True)

    print(f"Built {PDF.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
