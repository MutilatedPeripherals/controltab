import os
from pathlib import Path

UPLOAD_DIR = Path("../files")

if os.getenv("RAILWAY_ENVIRONMENT"):
    DATABASE_FILE = "/data/files.db"
else:
    DATABASE_FILE = "./files.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"