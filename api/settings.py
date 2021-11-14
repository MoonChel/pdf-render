import os

from dotenv import load_dotenv

load_dotenv()

_current_dir = os.path.dirname(os.path.realpath(__file__))

SOCKET_URL = os.environ["CLIENT_SOCKET_URL"]

FILE_FOLDER = os.path.join(_current_dir, "../files")
IMAGE_FOLDER = os.path.join(_current_dir, "../images")
