from uuid import UUID
from typing import Optional
from fastapi import APIRouter, UploadFile, File

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from models.models import File as FileModel
from models.session import session_manager

from .utils import save_file
from .zmq_sender import zmq_client

api = APIRouter(prefix="/api")


@api.post("/document")
async def document_upload(file: Optional[UploadFile] = File("file")):
    # save on disk
    filename = await save_file(file)

    # save in db
    db_file = FileModel(name=filename)
    session_manager.session.add(db_file)
    await session_manager.session.commit()

    # send for processing
    await zmq_client.send_string(str(db_file.id))
    recieved = await zmq_client.recv_string()

    return {
        "name": filename,
        "file_id": db_file.id,
        # "in_progress": True,
        "in_progress": bool(recieved),
    }


@api.get("/document/{document_id}")
async def get_document(document_id: UUID):
    result = await session_manager.session.execute(
        select(FileModel).where(FileModel.id == document_id)
    )

    (db_file,) = result.first()

    return {
        "id": db_file.id,
        "name": db_file.name,
        "processed": db_file.processed,
    }


@api.get("/document/{document_id}/images")
async def get_images(document_id: UUID):
    result = await session_manager.session.execute(
        select(FileModel)
        .options(joinedload("images"))
        .where(FileModel.id == document_id)
    )

    (db_file,) = result.first()

    return [
        {
            "id": image.id,
            "url": image.name,
        }
        for image in db_file.images
    ]
