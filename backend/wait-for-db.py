import os
import asyncio
import asyncpg
import time

database_url = os.environ.get("DATABASE_URL")
database_url = "postgresql://user:password@db:5432/llama_app_db"
max_attempts = 30
sleep_interval = 1

async def check_database_connection():
    print(database_url)
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
                return True
            await asyncio.sleep(sleep_interval)

async def main():
    if await check_database_connection():
        pass

if __name__ == "__main__":
    asyncio.run(main())
