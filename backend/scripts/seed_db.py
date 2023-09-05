from typing import List
import asyncio
from tempfile import TemporaryDirectory
from pathlib import Path
from fire import Fire
import s3fs
from app.core.config import settings
import upsert_db_sec_documents
import download_sec_pdf
from download_sec_pdf import DEFAULT_CIKS, DEFAULT_FILING_TYPES
import seed_storage_context


def copy_to_s3(dir_path: str, s3_bucket: str = settings.S3_ASSET_BUCKET_NAME):
    """
    Copy all files in dir_path to S3.
    """
    s3 = s3fs.S3FileSystem(
        key=settings.AWS_KEY,
        secret=settings.AWS_SECRET,
        endpoint_url=settings.S3_ENDPOINT_URL,
    )

    if not (settings.RENDER or s3.exists(s3_bucket)):
        s3.mkdir(s3_bucket)

    s3.put(dir_path, s3_bucket, recursive=True)


async def async_seed_db(
    ciks: List[str] = DEFAULT_CIKS, filing_types: List[str] = DEFAULT_FILING_TYPES
):
    with TemporaryDirectory() as temp_dir:
        print("Downloading SEC filings")
        download_sec_pdf.main(
            output_dir=temp_dir,
            ciks=ciks,
            file_types=filing_types,
        )

        print("Copying downloaded SEC filings to S3")
        copy_to_s3(str(Path(temp_dir) / "sec-edgar-filings"))

        print("Upserting records of downloaded SEC filings into database")
        await upsert_db_sec_documents.async_upsert_documents_from_filings(
            url_base=settings.CDN_BASE_URL,
            doc_dir=temp_dir,
        )

        print("Seeding storage context")
        await seed_storage_context.async_main_seed_storage_context()
        print(
            """
Done! 🏁
\t- SEC PDF documents uploaded to the S3 assets bucket ✅
\t- Documents database table has been populated ✅
\t- Vector storage table has been seeded with embeddings ✅
        """.strip()
        )


def seed_db(
    ciks: List[str] = DEFAULT_CIKS, filing_types: List[str] = DEFAULT_FILING_TYPES
):
    asyncio.run(async_seed_db(ciks, filing_types))


if __name__ == "__main__":
    Fire(seed_db)
