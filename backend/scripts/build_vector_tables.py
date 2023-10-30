from fire import Fire
from app.chat.pg_vector import get_vector_store_singleton
import asyncio

async def build_vector_tables():
    vector_store = await get_vector_store_singleton()
    await vector_store.run_setup()


def main_build_vector_tables():
    """
    Script to build the PGVector table if they don't already exist
    """
    asyncio.run(build_vector_tables())

if __name__ == "__main__":
    Fire(main_build_vector_tables)
