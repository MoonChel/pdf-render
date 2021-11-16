import os
import pytest
import asyncio
from httpx import AsyncClient

from api.app import app
from api.settings import _current_dir

from api.models.session import engine, session_maker
from api.models.models import Base, File as FileModel
from api.settings import DATABASE_HOST


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()

    yield loop

    loop.close()


@pytest.fixture
async def session(event_loop):
    async with session_maker() as session:
        yield session


@pytest.fixture(autouse=True)
async def prepare_db(event_loop):
    if DATABASE_HOST not in [
        "localhost",
        "postgres",
        "0.0.0.0",
        "test_db",
    ]:
        raise Exception(
            f"Tests must run on 'test' database, instead of '{DATABASE_HOST}'"
        )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def pdf_db_file(session):
    db_file = FileModel(name="pdf-test.pdf")
    session.add(db_file)
    await session.commit()

    yield db_file

    await session.delete(db_file)
    await session.commit()


@pytest.fixture
async def test_client(event_loop):
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
