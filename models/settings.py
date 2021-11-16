import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.environ["DATABASE_HOST"]

POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
