from pathlib import Path
from typing import List, Optional, Tuple
import datetime

import pandas as pd
from pydantic import BaseModel


class Filing(BaseModel):
    file_path: str
    symbol: str
    filing_type: str
    year: int
    quarter: Optional[int] = None
    cik: str
    accession_number: str
    period_of_report_date: datetime.datetime
    filed_as_of_date: datetime.datetime
    date_as_of_change: datetime.datetime


def filing_exists(cik: str, filing_type: str, output_dir: str) -> bool:
    """Checks if a filing exists for a given cik and filing type."""
    data_dir = Path(output_dir) / "sec-edgar-filings"
    filing_dir = data_dir / cik / filing_type
    return filing_dir.exists()


def parse_quarter_from_full_submission_txt(full_submission_txt_file_path: Path) -> int:
    """
    The full-submission.txt file contains a like like the following line:
    <td class="pl" style="border-bottom: 0px;" valign="top"><a class="a" href="javascript:void(0);" onclick="Show.showAR( this, 'defref_dei_DocumentFiscalPeriodFocus', window );">Document Fiscal Period Focus</a></td>
    <td class="text">Q1<span></span>

    This method parses the quarter from that second line
    """
    with open(full_submission_txt_file_path) as f:
        try:
            line = next(f)
            while "Document Fiscal Period Focus</a>" not in line:
                line = next(f)
            quarter_line = next(f)
            quarter_line = quarter_line.split(">")[1].split("<")[0]
            quarter = quarter_line.strip("Q ")
            return int(quarter)
        except StopIteration:
            raise ValueError(
                f"Could not find Document Fiscal Period Focus in file {full_submission_txt_file_path}"
            )


def get_line_with_substring_in_file(file_path: Path, substring: str) -> str:
    """Returns the first line in a file that contains a given substring."""
    with open(file_path) as f:
        for line in f:
            if substring in line:
                return line
    raise ValueError(f"Could not find substring '{substring}' in file {file_path}")


def parse_dates_from_full_submission_txt(
    full_submission_txt_file_path: Path,
) -> Tuple[datetime.datetime, datetime.datetime, datetime.datetime]:
    period_of_report_line = get_line_with_substring_in_file(
        full_submission_txt_file_path, "CONFORMED PERIOD OF REPORT:"
    )
    period_of_report_line = period_of_report_line.split(":")[1].strip()
    # Example value for date format: 20220930
    period_of_report_date = datetime.datetime.strptime(
        period_of_report_line.strip(), "%Y%m%d"
    )

    filed_as_of_date_line = get_line_with_substring_in_file(
        full_submission_txt_file_path, "FILED AS OF DATE:"
    )
    filed_as_of_date_line = filed_as_of_date_line.split(":")[1].strip()
    filed_as_of_date = datetime.datetime.strptime(
        filed_as_of_date_line.strip(), "%Y%m%d"
    )

    date_as_of_change_line = get_line_with_substring_in_file(
        full_submission_txt_file_path, "DATE AS OF CHANGE:"
    )
    date_as_of_change_line = date_as_of_change_line.split(":")[1].strip()
    date_as_of_change = datetime.datetime.strptime(
        date_as_of_change_line.strip(), "%Y%m%d"
    )
    return period_of_report_date, filed_as_of_date, date_as_of_change


def parse_cik_from_full_submission_txt(
    full_submission_txt_file_path: Path,
) -> str:
    cik_line = get_line_with_substring_in_file(
        full_submission_txt_file_path, "CENTRAL INDEX KEY:"
    )
    cik_line = cik_line.split(":")[1].strip()
    return cik_line


def parse_ticker_symbol_from_full_submission_txt(
    full_submission_txt_file_path: Path,
) -> str:
    """
    Very hacky approach to parsing the ticker symbol from the full-submission.txt file.
    The file usually has a line that reads something like "<FILENAME>amzn-20220930.htm"
    We can extract "amzn" from that line.
    """
    ticker_symbol_line = get_line_with_substring_in_file(
        full_submission_txt_file_path, "<FILENAME>"
    )
    ticker_symbol_line = ticker_symbol_line.split("<FILENAME>")[1].strip()
    ticker_symbol = ticker_symbol_line.split("-")[0].strip()
    return ticker_symbol.upper()


def get_available_filings(output_dir: str) -> List[Filing]:
    data_dir = Path(output_dir) / "sec-edgar-filings"
    filings = []
    for cik_dir in data_dir.iterdir():
        for filing_type_dir in cik_dir.iterdir():
            for filing_dir in filing_type_dir.iterdir():
                filing_pdf = filing_dir / "primary-document.pdf"
                full_submission_txt = filing_dir / "full-submission.txt"
                if filing_pdf.exists():
                    filing_type = filing_type_dir.name
                    file_path = str(filing_pdf.absolute())
                    quarter = None
                    assert full_submission_txt.exists()
                    if filing_type == "10-Q":
                        quarter = parse_quarter_from_full_submission_txt(
                            full_submission_txt
                        )
                    (
                        period_of_report_date,
                        filed_as_of_date,
                        date_as_of_change,
                    ) = parse_dates_from_full_submission_txt(full_submission_txt)
                    accession_number = filing_dir.name.strip()
                    cik = parse_cik_from_full_submission_txt(full_submission_txt)
                    symbol = parse_ticker_symbol_from_full_submission_txt(
                        full_submission_txt
                    )
                    filing = Filing(
                        file_path=file_path,
                        symbol=symbol,
                        filing_type=filing_type,
                        year=period_of_report_date.year,
                        quarter=quarter,
                        accession_number=accession_number,
                        cik=cik,
                        period_of_report_date=period_of_report_date,
                        filed_as_of_date=filed_as_of_date,
                        date_as_of_change=date_as_of_change,
                    )
                    filings.append(filing)
    return filings


def get_available_filings_as_df(output_dir: str) -> pd.DataFrame:
    filings = get_available_filings(output_dir)
    return pd.DataFrame([filing.dict() for filing in filings])
