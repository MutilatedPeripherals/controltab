import os
from pathlib import Path

# Define upload directory relative to current environment
UPLOAD_DIR = Path("files")
if os.getenv("RAILWAY_ENVIRONMENT"):  # Check if running in Railway
    DATABASE_FILE = "/data/files.db"  # Use Railway's persistent storage
else:
    DATABASE_FILE = "./files.db"  # Local environment

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"