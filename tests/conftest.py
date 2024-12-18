import asyncio

import pytest
import pytest_asyncio

from app.database.async_base import Base
from app.database.sessions import async_engine, async_session_factory


@pytest_asyncio.fixture(scope="function")
async def database():
    # Drop and recreate the schema for the test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Drop the schema after the test
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_db_session(database):
    async with async_session_factory() as async_db_session:
        yield async_db_session
