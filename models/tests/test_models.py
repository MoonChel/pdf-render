import pytest

from uuid import UUID
from models.models import File as FileModel


@pytest.mark.asyncio
async def test_save(session):
    db_file = FileModel(name="test.pdf")
    session.add(db_file)
    await session.commit()

    assert isinstance(db_file.id, UUID)
