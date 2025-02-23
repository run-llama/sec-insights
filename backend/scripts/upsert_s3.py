import boto3
from fire import Fire
from app.schema import Document
from app.db.session import SessionLocal
from app.api import crud
import asyncio
import os

s3_client = boto3.client('s3')

BUCKET_NAME = os.getenv('S3_ASSET_BUCKET_NAME')
FOLDER_NAME = "documents"


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
        print(f"Upserted document. Database ID: {document.id}")

async def upsert_all_documents_in_s3():
    """
    Fetches all files in the 'documents' folder in the S3 bucket and upserts them into the database.
    """
    try:
        # List the objects in the 'documents' folder in the S3 bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{FOLDER_NAME}/")

        # Loop through all files and upsert them
        if 'Contents' in response:
            for file in response['Contents']:
                file_key = file['Key']

                if file_key.endswith('/'):
                    continue
                
                doc_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_key}"

                await upsert_single_document(doc_url)
        else:
            print(f"No files found in the folder '{FOLDER_NAME}' in the bucket.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main_upsert_all_documents():
    """
    Script to upsert all documents from S3 into the database.
    """
    asyncio.run(upsert_all_documents_in_s3())

if __name__ == "__main__":
    Fire(main_upsert_all_documents)
