from pathlib import Path
from typing import List, Optional

import pdfkit
from file_utils import filing_exists
from fire import Fire
from sec_edgar_downloader import Downloader
from distutils.spawn import find_executable
from tqdm.contrib.itertools import product
from app.core.config import settings

DEFAULT_OUTPUT_DIR = "data/"
# You can lookup the CIK for a company here: https://www.sec.gov/edgar/searchedgar/companysearch
DEFAULT_CIKS = [
    # AAPL
    "320193",
    # MSFT
    "789019",
    # AMZN
    "0001018724",
    # GOOGL
    "1652044",
    # META
    "1326801",
    # TSLA
    "1318605",
    # NVDA
    "1045810",
    # NFLX
    "1065280",
    # PYPL
    "0001633917",
    # PFE (Pfizer)
    "78003",
    # AZNCF (AstraZeneca)
    "901832",
    # LLY (Eli Lilly)
    "59478",
    # MRNA (Moderna)
    "1682852",
    # JNJ (Johnson & Johnson)
    "200406",
]
DEFAULT_FILING_TYPES = [
    "10-K",
    "10-Q",
]


def _download_filing(
    cik: str, filing_type: str, output_dir: str, limit=None, before=None, after=None
):
    dl = Downloader(settings.SEC_EDGAR_COMPANY_NAME, settings.SEC_EDGAR_EMAIL, output_dir)
    dl.get(filing_type, cik, limit=limit, before=before, after=after, download_details=True)


def _convert_to_pdf(output_dir: str):
    """Converts all html files in a directory to pdf files."""

    # NOTE: directory structure is assumed to be:
    # output_dir
    # ├── sec-edgar-filings
    # │   ├── AAPL
    # │   │   ├── 10-K
    # │   │   │   ├── 0000320193-20-000096
    # │   │   │   │   ├── primary-document.html
    # │   │   │   │   ├── primary-document.pdf   <-- this is what we want

    data_dir = Path(output_dir) / "sec-edgar-filings"

    for cik_dir in data_dir.iterdir():
        for filing_type_dir in cik_dir.iterdir():
            for filing_dir in filing_type_dir.iterdir():
                filing_doc = filing_dir / "primary-document.html"
                filing_pdf = filing_dir / "primary-document.pdf"
                if filing_doc.exists() and not filing_pdf.exists():
                    print("- Converting {}".format(filing_doc))
                    input_path = str(filing_doc.absolute())
                    output_path = str(filing_pdf.absolute())
                    try:
                        pdfkit.from_file(input_path, output_path, verbose=True)
                    except Exception as e:
                        print(f"Error converting {input_path} to {output_path}: {e}")


def main(
    output_dir: str = DEFAULT_OUTPUT_DIR,
    ciks: List[str] = DEFAULT_CIKS,
    file_types: List[str] = DEFAULT_FILING_TYPES,
    before: Optional[str] = None,
    after: Optional[str] = None,
    limit: Optional[int] = 3,
    convert_to_pdf: bool = True,
):
    print('Downloading filings to "{}"'.format(Path(output_dir).absolute()))
    print("File Types: {}".format(file_types))
    if convert_to_pdf:
        if find_executable("wkhtmltopdf") is None:
            raise Exception(
                "ERROR: wkhtmltopdf (https://wkhtmltopdf.org/) not found, "
                "please install it to convert html to pdf "
                "`sudo apt-get install wkhtmltopdf`"
            )
    for symbol, file_type in product(ciks, file_types):
        try:
            if filing_exists(symbol, file_type, output_dir):
                print(f"- Filing for {symbol} {file_type} already exists, skipping")
            else:
                print(f"- Downloading filing for {symbol} {file_type}")
                _download_filing(symbol, file_type, output_dir, limit, before, after)
        except Exception as e:
            print(
                f"Error downloading filing for symbol={symbol} & file_type={file_type}: {e}"
            )

    if convert_to_pdf:
        print("Converting html files to pdf files")
        _convert_to_pdf(output_dir)


if __name__ == "__main__":
    Fire(main)
