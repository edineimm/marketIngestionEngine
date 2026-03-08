from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.configs import settings

engine = create_async_engine(settings.DB_URL, echo=True)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)
