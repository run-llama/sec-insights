import asyncio
import asyncpg
from app.core.config import settings

database_url = "postgresql://user:password@db:5432/llama_app_db"

async def check_database_connection(max_attempts: int = 30, sleep_interval: int = 1) -> bool:
    for attempt in range(1, max_attempts + 1):
        print(database_url + "hi")
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
    if await check_database_connection():
        pass

if __name__ == "__main__":
    asyncio.run(main())
