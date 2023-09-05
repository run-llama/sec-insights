from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal


async def get_db() -> Generator[AsyncSession, None, None]:
    async with SessionLocal() as db:
        yield db
