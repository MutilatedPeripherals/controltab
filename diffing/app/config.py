import os
from pathlib import Path

# Determine the base directory
BASE_DIR = Path(__file__).resolve().parent

# Directory for uploaded files (for static or other purposes)
UPLOAD_DIR = BASE_DIR / "files"

# Ensure the `UPLOAD_DIR` exists
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Set the database path depending on the environment
if os.getenv("RAILWAY_ENVIRONMENT"):
    DATABASE_FILE = "/data/files.db"  # Ensure the volume is mounted to /data in Railway
else:
    DATABASE_FILE = UPLOAD_DIR / "files.db"

# Set the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"