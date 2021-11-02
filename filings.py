from pathlib import Path
import re
from lxml import etree

ticker_symbol = "TSLA"
default_dir = "sec-edgar-filings"
output_dir = "."
output_file = "source.txt"


def download_if_needed(dir: Path):

    if not dir.exists():
        from sec_edgar_downloader import Downloader

        dl = Downloader()
        dl.get("10-Q", ticker_symbol)


def clean_sgml_junk(dir: Path) -> list[str]:
    """Clean up an EDGAR filing by brute-force extracting all the text nodes of a reasonable length"""
    output: list[str] = []
    min_node_length = 5

    for filing_dir in dir.rglob("*"):

        filing = filing_dir / "full-submission.txt"
        if filing.exists():
            report = filing.open().read().replace("\n", "")
            p = r"<XBRL>(.*?)</XBRL>"
            if blob := re.search(p, report, re.MULTILINE):
                xml = blob.group(1).encode("utf-8")
                tree = etree.fromstring(xml)
                text_nodes = tree.xpath(
                    "//x:html//x:*/text()",  # Extract only HTML content, not GAAP junk
                    namespaces={"x": "http://www.w3.org/1999/xhtml"},
                )
                for node in text_nodes:
                    if len(node) > min_node_length:
                        output.append(node + "\n")
    return output


if __name__ == "__main__":

    dir = Path(default_dir)
    download_if_needed(dir)
    Path(output_file).open("w").writelines(clean_sgml_junk(dir))
