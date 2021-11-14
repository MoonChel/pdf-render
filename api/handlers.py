from typing import Optional
from fastapi import APIRouter, UploadFile, File

from models.models import File as FileModel
from models.session import session_manager

from .utils import save_file
from .data_models import UploadDocumentResponse
from .zmq_sender import zmq_client

api = APIRouter(prefix="/api")


@api.post("/document", response_model=UploadDocumentResponse)
async def document_upload(pdf_file: Optional[UploadFile] = File("file")):
    # save on disk
    filename = await save_file(pdf_file)

    # save in db
    db_file = FileModel(name=filename)
    session_manager.session.add(db_file)

    # send for processing
    zmq_client.send(db_file.id)

    return UploadDocumentResponse(file_id=db_file.id, name=filename)


@api.get("/document/{document_id}")
async def get_document(document_id: int):
    result = session_manager.session.execute(FileModel).where(
        FileModel.id == document_id
    )

    db_file = result.first()

    return {
        "id": db_file.id,
        "name": db_file.name,
        "processed": db_file.processed,
    }


@api.get("/document/{document_id}/images")
async def get_images(document_id: int):
    result = session_manager.session.execute(FileModel).where(
        FileModel.id == document_id
    )

    db_file = result.first()

    return [
        {
            "id": image.id,
            "url": image.name,
        }
        for image in db_file.images
    ]
