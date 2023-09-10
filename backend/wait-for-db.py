import asyncio
import asyncpg
from app.core.config import settings


async def check_database_connection(database_url: str, max_attempts: int = 30, sleep_interval: int = 1) -> bool:
    database_url = database_url.replace("postgresql+asyncpg://","postgresql://")
    for attempt in range(1, max_attempts + 1):
        try:
            await asyncpg.connect(database_url)
            print(f"Connected to the database on attempt {attempt}.")
            return True
        except Exception as e:
            print(f"Attempt {attempt}: Database is not yet available. Error: {e}")
            if attempt == max_attempts:
                print("Max attempts reached. Exiting.")
                return False
            await asyncio.sleep(sleep_interval)

async def main():
    if await check_database_connection(database_url=settings.DATABASE_URL):
        pass

if __name__ == "__main__":
    asyncio.run(main())
