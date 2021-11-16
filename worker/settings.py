import os

from dotenv import load_dotenv

load_dotenv()

_current_dir = os.path.dirname(os.path.realpath(__file__))

SOCKET_HOST = os.environ["SOCKET_HOST"]
SOCKET_POST = os.environ["SOCKET_POST"]
SOCKET_URL = f"tcp://*:{SOCKET_POST}"

FILE_FOLDER = os.path.join(_current_dir, "../files")
IMAGE_FOLDER = os.path.join(_current_dir, "../images")
