from pydantic import BaseModel


class UploadDocumentResponse(BaseModel):
    # or uuid.uuid4
    file_id: int
    name: str
