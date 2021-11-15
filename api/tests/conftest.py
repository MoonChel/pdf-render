import os
import pytest
import asyncio
from fastapi.testclient import TestClient

from httpx import AsyncClient

from api.app import app
from api.settings import _current_dir

from models.settings import DATABASE_HOST
from models.session import engine, session_maker
from models.models import Base, File as FileModel


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
async def prepare_db():
    if DATABASE_HOST not in [
        "localhost",
        "postgres",
        "0.0.0.0",
        # "test_db",
    ]:
        raise Exception("Tests must run on 'test' database")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def pdf_db_file():
    async with session_maker() as session:
        db_file = FileModel(name="test_file.pdf")
        session.add(db_file)
        await session.commit()

        yield db_file

        await session.delete(db_file)
        await session.commit()


@pytest.fixture
async def test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def pdf_test_file():
    pdf_test_path = os.path.join(
        _current_dir,
        "tests",
        "pdf-test.pdf",
    )

    with open(pdf_test_path, "rb") as pdf_file:
        yield pdf_file
