import os
from pathlib import Path

# Configure database path based on environment
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Use Railway's persistent volume path
    DATABASE_FILE = "/data/files.db"
else:
    # Local environment
    DATABASE_FILE = "./files.db"

# Construct SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Directory for uploads (if needed)
UPLOAD_DIR = Path("files")