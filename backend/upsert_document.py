from fire import Fire
from app.schema import Document
from app.db.session import SessionLocal
from app.api import crud
import asyncio

async def upsert_single_document(doc_url: str):
    """
    Upserts a single SEC document into the database using its URL.
    """
    if not doc_url or not doc_url.startswith('http'):
        print("DOC_URL must be an http(s) based url value")
        return
    metadata_map = {}
    doc = Document(url=doc_url, metadata_map=metadata_map)

    async with SessionLocal() as db:
        document = await crud.upsert_document_by_url(db, doc)
        print(f"Upserted document. Database ID:\n{document.id}")


def main_upsert_single_document(doc_url: str):
    """
    Script to upsert a single document by URL. metada_map parameter will be empty dict ({})
    This script is useful when trying to use your own PDF files.
    """
    asyncio.run(upsert_single_document(doc_url))

if __name__ == "__main__":
    Fire(main_upsert_single_document)
