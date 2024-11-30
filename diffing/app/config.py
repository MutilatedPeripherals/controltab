import os
from pathlib import Path

# Determine the base directory
BASE_DIR = Path(__file__).resolve().parent

# Directory for uploaded files (for static or other purposes)
UPLOAD_DIR = BASE_DIR / "files"

# Ensure the `UPLOAD_DIR` exists (for local development)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Set the database path depending on the environment
if os.getenv("RAILWAY_ENVIRONMENT"):
    # In production, use the volume-mounted /data/database.db
    DATABASE_FILE = "/data/database.db"
else:
    # In local development, use ./files/database.db
    DATABASE_FILE = UPLOAD_DIR / "database.db"

# Set the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"