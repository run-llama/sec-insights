from fastapi import APIRouter, Response
from app.core.config import settings

loader_io_router = APIRouter()


@loader_io_router.get("/")
async def get_verification_file() -> str:
    """
    Verification string for loader.io
    """
    return Response(settings.LOADER_IO_VERIFICATION_STR, media_type="text/plain")
