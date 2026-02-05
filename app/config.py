import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")

    CHAT_ROOMS = [
        "Introductions",
        "Moonies",
        "Daily Chit-Chat",
        "Posts",
        "Connections",
    ]
