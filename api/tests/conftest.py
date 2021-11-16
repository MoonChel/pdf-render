import os
import pytest
import asyncio
from httpx import AsyncClient

from api.app import app
from api.settings import _current_dir
from models.tests.conftest import pdf_db_file, prepare_db, session


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


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
