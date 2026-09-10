from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings
engine=create_async_engine(settings.database_url,pool_pre_ping=True,pool_size=5,max_overflow=10)
SessionLocal=async_sessionmaker(engine,expire_on_commit=False)
async def get_db():
    async with SessionLocal() as s: yield s
