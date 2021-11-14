from typing import Optional
from fastapi import APIRouter, UploadFile, File

from .utils import save_file
from .data_models import UploadDocumentResponse

api = APIRouter(prefix="/api")


@api.post("/document", response_model=UploadDocumentResponse)
async def document_upload(pdf_file: Optional[UploadFile] = File("file")):
    filename = await save_file(pdf_file)

    return UploadDocumentResponse(file_id=1, name=filename)


@api.get("/document/{document_id}")
async def get_document(document_id: int):
    return document_id


@api.get("/document/{document_id}/render")
async def render_document(document_id: int):
    return document_id
