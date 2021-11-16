import os
import pytest
import asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from api.models.session import session_maker
from api.models.models import File as FileModel

from worker.settings import _current_dir
from worker.render_pdf import render_pdf


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
async def pdf_db_file(event_loop):
    async with session_maker() as session:
        db_file = FileModel(name="pdf-test.pdf")
        session.add(db_file)
        await session.commit()

        yield db_file

        await session.delete(db_file)
        await session.commit()


@pytest.mark.asyncio
async def test_render_pdf(event_loop, pdf_db_file, mocker):
    mocker.patch("worker.settings.FILE_FOLDER", os.path.join(_current_dir, "tests"))

    await render_pdf(str(pdf_db_file.id))

    async with session_maker() as session:
        result = await session.execute(
            select(FileModel)
            .options(joinedload("images"))
            .where(FileModel.id == pdf_db_file.id)
        )

        (db_file,) = result.first()

        assert db_file.processed == True
        assert len(db_file.images) > 0
