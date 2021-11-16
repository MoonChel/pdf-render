from fastapi import Request, FastAPI
from .models.session import session_maker, session_manager, shutdown_db


def init_db(app: FastAPI):
    app.on_event("shutdown")(shutdown_db)
    app.middleware("http")(db_middleware)


async def db_middleware(request: Request, call_next):
    async with session_maker() as session:
        session_manager._init(session)
        response = await call_next(request)

    return response
