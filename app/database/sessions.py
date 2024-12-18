from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.configs import settings


async_engine = create_async_engine(
    settings.sqlalchemy_database_uri,
    echo=False,
    pool_size=30,
    max_overflow=50,
    pool_use_lifo=True,
    pool_pre_ping=True,
)


async_session_factory = sessionmaker(
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    bind=async_engine,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
