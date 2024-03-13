from fastapi import APIRouter, Response
from app.core.config import settings

# 创建 API 路由器
loader_io_router = APIRouter()

# 定义路由处理函数，处理 GET 请求
@loader_io_router.get("/")
async def get_verification_file() -> str:
    """
    Verification string for loader.io
    """
    # 返回加载器.io的验证字符串
    return Response(settings.LOADER_IO_VERIFICATION_STR, media_type="text/plain")
