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

from api.models.models import File, Image
from api.models.session import session_maker

from . import settings

context = zmq.asyncio.Context()
zmq_client = context.socket(zmq.REP)


def get_file_path(filename: str):
    return os.path.join(settings.FILE_FOLDER, filename)


async def render_pdf(file_id: str):
    async with session_maker() as session:
        result = await session.execute(
            select(File).where(File.id == file_id),
        )
        (file,) = result.first()

        images = convert_from_path(
            get_file_path(file.name),
            output_folder=settings.IMAGE_FOLDER,
            fmt="png",
        )

        for image in images:
            db_image = Image(file=file, name=image.filename)
            session.add(db_image)

        await session.execute(
            update(File).where(File.id == file_id).values(processed=True)
        )
        await session.commit()


async def start_zmq_client():
    zmq_client.bind(settings.SOCKET_URL)

    while True:
        file_id = await zmq_client.recv_string()
        await zmq_client.send_string("recieved")

        print(f"New file for processing: {file_id}")

        await render_pdf(file_id)
