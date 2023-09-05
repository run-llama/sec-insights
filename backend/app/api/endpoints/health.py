from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.api import deps

router = APIRouter()


@router.get("/")
async def health(db: AsyncSession = Depends(deps.get_db)) -> Dict[str, str]:
    """
    Health check endpoint.
    """
    await db.execute(text("SELECT 1"))
    return {"status": "alive"}
