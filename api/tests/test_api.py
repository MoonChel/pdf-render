import pytest
from io import TextIOWrapper
from httpx import AsyncClient, Request
from api.models.models import File as FileModel


async def mock_zmq():
    return "mock"


@pytest.mark.asyncio
async def test_handlers(
    test_client: AsyncClient,
    pdf_test_file: TextIOWrapper,
    pdf_db_file: FileModel,
    mocker,
):
    mocker.patch("api.zmq_sender.zmq_client.send_string", return_value=mock_zmq())
    mocker.patch("api.zmq_sender.zmq_client.recv_string", return_value=mock_zmq())

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
