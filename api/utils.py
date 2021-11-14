import os
import uuid
import aiofiles
from fastapi import File

from .settings import FILE_FOLDER


def gen_filename(filename: str):
    return str(uuid.uuid4()) + "_" + filename


def get_file_path(filename: str):
    return os.path.join(FILE_FOLDER, filename)


async def save_file(file: File) -> str:
    filename = gen_filename(file.filename)
    file_path = get_file_path(filename)

    async with aiofiles.open(file_path, "wb") as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    return filename
