import asyncio
from app.db.session import SessionLocal
from sqlalchemy.sql import text


async def check_database_connection(max_attempts: int = 30, sleep_interval: int = 1) -> None:
    for attempt in range(1, max_attempts + 1):
        try:
            async with SessionLocal() as db:
                await db.execute(text("SELECT 1"))
                print(f"Connected to the database on attempt {attempt}.")
                return
        except Exception as e:
            print(f"Attempt {attempt}: Database is not yet available. Error: {e}")
            if attempt == max_attempts:
                raise ValueError(
                    f"Couldn't connect to database after {max_attempts} attempts."
                ) from e
            await asyncio.sleep(sleep_interval)
