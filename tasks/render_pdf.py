import os
import zmq
import zmq.asyncio
from sqlalchemy import select, update

from pdf2image import convert_from_path
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
)

from models.models import File, Image
from models.session import session_maker

from . import settings

context = zmq.asyncio.Context()
zmq_client = context.socket(zmq.REP)


def get_file_path(filename: str):
    return os.path.join(settings.FILE_FOLDER, filename)


async def start_zmq_client():
    zmq_client.bind(settings.SOCKET_URL)

    async with session_maker() as session:
        while True:
            file_id = await zmq_client.recv()
            print(f"New file for processing: {file_id}")

            result = await session.execute(select(File).where(File.id == file_id))
            file = result.first()

            images = convert_from_path(get_file_path(file.name))

            for image in images:
                db_image = Image(
                    file=file,
                    name=image.name,
                )
                session.add(db_image)

            await session.execute(
                update(File).where(File.id == file_id).values(processed=True)
            )
            await session.commit()
