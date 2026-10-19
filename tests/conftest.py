"""Фикстуры для тестов: клиент и чистая БД."""

import os

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def _use_test_database(tmp_path):
    """Указывает на отдельный SQLite-файл до инициализации движка."""
    os.environ["APP_DATABASE_URL"] = f"sqlite+aiosqlite:///{tmp_path / 'test_edtech.db'}"


@pytest.fixture
async def client():
    """AsyncClient поверх ASGITransport + пустая БД на каждый тест."""
    from src.database import engine
    from src.edtech.models import Base
    from src.main import app

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
