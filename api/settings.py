import os

from dotenv import load_dotenv

load_dotenv()

_current_dir = os.path.dirname(os.path.realpath(__file__))

SOCKET_HOST = os.environ["SOCKET_HOST"]
SOCKET_POST = os.environ["SOCKET_POST"]
SOCKET_URL = f"tcp://{SOCKET_HOST}:{SOCKET_POST}"

FILE_FOLDER = os.path.join(_current_dir, "../files")
IMAGE_FOLDER = os.path.join(_current_dir, "../images")

# database
DATABASE_HOST = os.environ["DATABASE_HOST"]

POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_PORT = os.environ["POSTGRES_PORT"]

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
