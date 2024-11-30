import os
from pathlib import Path

# Directory for uploads (static or other files)
UPLOAD_DIR = Path("../files")

# Database file path
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Production environment: Use Railway's mounted volume
    DATABASE_FILE = "/data/files.db"
else:
    # Development environment: Use local SQLite file
    DATABASE_FILE = "./files.db"

# SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"