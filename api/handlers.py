from uuid import UUID
from typing import Optional
from fastapi import APIRouter, UploadFile, File

from models.models import File as FileModel, Image as ImageModel
from models.session import session_manager
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .utils import save_file
from .data_models import UploadDocumentResponse
from .zmq_sender import zmq_client

api = APIRouter(prefix="/api")


@api.post("/document", response_model=UploadDocumentResponse)
async def document_upload(file: Optional[UploadFile] = File("file")):
    # save on disk
    filename = await save_file(file)

    # save in db
    db_file = FileModel(name=filename)
    session_manager.session.add(db_file)
    await session_manager.session.commit()

    # send for processing
    # zmq_client.send(db_file.id)

    return UploadDocumentResponse(file_id=db_file.id, name=filename)


@api.get("/document/{document_id}")
async def get_document(document_id: UUID):
    result = await session_manager.session.execute(
        select(FileModel).where(FileModel.id == document_id)
    )

    db_file = result.first()
    if db_file:
        (db_file,) = db_file

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

    db_file = result.first()
    if db_file:
        (db_file,) = db_file

    return [
        {
            "id": image.id,
            "url": image.name,
        }
        for image in db_file.images
    ]
