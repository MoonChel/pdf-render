from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .settings import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True)
session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class SessionManager:
    def _init(self, session: AsyncSession) -> None:
        self.session = session


session_manager = SessionManager()


async def shutdown_db():
    session_maker.close_all()
