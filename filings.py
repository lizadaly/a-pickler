from pathlib import Path
import re
from lxml import etree

ticker_symbol = "TSLA"
default_dir = "sec-edgar-filings"


def download_if_needed(dir: Path):

    if not dir.exists():
        from sec_edgar_downloader import Downloader

        dl = Downloader()
        dl.get("10-Q", ticker_symbol)


def clean_sgml_junk(dir: Path):
    for filing_dir in dir.rglob("*"):

        filing = filing_dir / "full-submission.txt"
        if filing.exists():
            report = filing.open().read().replace("\n", "")
            p = r"<XBRL>(.*?)</XBRL>"
            if blob := re.search(p, report, re.MULTILINE):
                xml = blob.group(1).encode("utf-8")
                tree = etree.fromstring(xml)
                text_nodes = tree.xpath(
                    "//x:html//text()",
                    namespaces={"x": "http://www.w3.org/1999/xhtml"},
                )
                for node in text_nodes:
                    if len(node) > 5:
                        print(node)


if __name__ == "__main__":

    dir = Path(default_dir)
    download_if_needed(dir)
    clean_sgml_junk(dir)
