from pathlib import Path
import re
from lxml import html

from pickler import pickler

ticker_symbol = "TSLA"
default_dir = "sec-edgar-filings"
output_file = "source.html"


def download_if_needed(dir: Path):

    if not dir.exists():
        from sec_edgar_downloader import Downloader

        dl = Downloader()
        dl.get("10-Q", ticker_symbol, after="2019-01-01")


def clean_sgml_junk(dir: Path) -> list[str]:
    """Clean up an EDGAR filing by brute-force extracting all the text nodes of a reasonable length"""
    output: list[str] = []
    punctuation: list[str] = []

    for filing_dir in sorted(dir.rglob("*")):

        filing = filing_dir / "full-submission.txt"
        if filing.exists():
            report = filing.open().read().replace("\n", "")
            p = r"<html>(.*?)</html>"
            if blob := re.search(p, report, re.MULTILINE):
                html_blob = blob.group(1)
                parsed = html.fromstring(html_blob)
                el_with_text = parsed.xpath("//*[text()!='']")
                for el in el_with_text:
                    text = el.text
                    if text and text.strip():
                        picklered, punct = pickler([text.strip()])
                        punctuation.append("".join(punct))
                        el.text = "".join(picklered)
                output.append(
                    html.tostring(parsed, encoding="unicode", pretty_print=True)
                )
    output.append(f"<p>{''.join(punctuation)}")
    return output


if __name__ == "__main__":

    dir = Path(default_dir)
    download_if_needed(dir)
    Path(output_file).open("w").writelines(clean_sgml_junk(dir))
    print("Now run:\n cat source.html | w3m -dump -T text/html -cols 100 > source.txt")
