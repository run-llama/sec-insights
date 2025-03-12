from tqdm import tqdm
from fire import Fire
import asyncio
from app.db.session import SessionLocal
from app.api import crud
from llama_index.core.callbacks import CallbackManager
from app.chat.engine import (
    build_doc_id_to_index_map,
    get_s3_fs,
)


async def async_main_seed_storage_context():
    fs = get_s3_fs()
    async with SessionLocal() as db:
        docs = await crud.fetch_documents(db)
    callback_manager = CallbackManager([])
    for doc in tqdm(docs, desc="Seeding storage with DB documents"):
        await build_doc_id_to_index_map(callback_manager, [doc], fs=fs)


def main_seed_storage_context():
    asyncio.run(async_main_seed_storage_context())


if __name__ == "__main__":
    Fire(main_seed_storage_context)
