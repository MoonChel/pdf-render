import pytest
from io import TextIOWrapper
from httpx import AsyncClient, Request
from models.models import File as FileModel


@pytest.mark.anyio
async def test_handlers(
    test_client: AsyncClient,
    pdf_test_file: TextIOWrapper,
    pdf_db_file: FileModel,
):
    document_id = pdf_db_file.id

    endpoints = [
        Request("post", "/api/document", files={"file": pdf_test_file}),
        Request("get", f"/api/document/{document_id}"),
        Request("get", f"/api/document/{document_id}/images"),
    ]

    for req in endpoints:
        req.url = test_client.base_url.join(req.url)
        resp = await test_client.send(req)

        assert resp.status_code == 200
