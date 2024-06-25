from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except:
    config = Config("")

DATABASE_URL = config("DATABASE_URL", Secret)