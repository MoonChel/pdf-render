import pytest
import asyncio
from models.tests.conftest import prepare_db, pdf_db_file, session


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()
