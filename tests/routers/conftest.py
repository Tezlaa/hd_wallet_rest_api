import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client(event_loop, async_db_session):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as aclient:
        yield aclient
