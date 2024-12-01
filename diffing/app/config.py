import os
from pathlib import Path

# Determine the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory for storing files in local development
LOCAL_UPLOAD_DIR = BASE_DIR / "files"

# Set the file storage path based on the environment
if os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production":  # If running in production
    # Use Railway's mounted volume path
    FILE_STORAGE_PATH = Path(os.getenv("FILE_STORAGE_PATH", "/mnt/volume/files"))
else:
    # Use local directory for development
    FILE_STORAGE_PATH = LOCAL_UPLOAD_DIR

# Ensure the directory exists
FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

# Set database URL based on the environment
if os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production":  # If running in production
    # Use PostgreSQL DATABASE_URL for production
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the Railway environment.")
else:
    # In local development, use SQLite
    DATABASE_FILE = FILE_STORAGE_PATH / "database.db"
    DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Debugging: Print paths for confirmation
print(f"File Storage Path: {FILE_STORAGE_PATH}")
print(f"SQLAlchemy Database URL: {SQLALCHEMY_DATABASE_URL}")