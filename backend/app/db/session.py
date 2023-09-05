from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=4,  # Number of connections to keep open in the pool
    max_overflow=4,  # Number of connections that can be opened beyond the pool_size
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_timeout=120,  # Raise an exception after 2 minutes if no connection is available from the pool
)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
