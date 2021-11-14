import zmq
import zmq.asyncio

from fastapi import FastAPI

from .settings import SOCKET_URL

context = zmq.asyncio.Context()
zmq_client = context.socket(zmq.REQ)


async def startup_zmq_client():
    zmq_client.connect(SOCKET_URL)


async def shutdown_zmq_client():
    zmq_client.close()
    context.destroy()


def init_zmq_client(app: FastAPI):
    app.on_event("startup")(startup_zmq_client)
    app.on_event("shutdown")(shutdown_zmq_client)
