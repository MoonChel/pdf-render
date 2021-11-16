import pytest
import asyncio

from models.session import engine, session_maker
from models.models import Base, File as FileModel
from models.settings import DATABASE_HOST


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


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
