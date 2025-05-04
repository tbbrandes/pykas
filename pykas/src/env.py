import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from pykas/config/.env
dotenv_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path)

NODE_HOST = os.getenv("NODE_HOST")
NODE_PORT = os.getenv("NODE_PORT")
TLS_SECURE_RAW = os.getenv("TLS_SECURE")

if TLS_SECURE_RAW is None:
    raise ValueError("TLS_SECURE must be set in the .env file (True/False)")

if TLS_SECURE_RAW not in ("True", "true", "False", "false"):
    raise ValueError("TLS_SECURE must be either 'True' or 'False' (case-insensitive)")

TLS_SECURE = TLS_SECURE_RAW.lower() == "true"

if not NODE_HOST or not NODE_PORT:
    raise EnvironmentError("NODE_HOST and NODE_PORT must be set in the .env file.")
