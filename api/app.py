from fastapi import FastAPI

from .handlers import api
from .middlewares import init_db
from .zmq_sender import init_zmq_client

app = FastAPI()

init_db(app)
init_zmq_client(app)

app.include_router(api)
