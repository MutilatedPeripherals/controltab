import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine the base directory of the project
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent  # Move up to the `diffing` directory

# Directory for storing files in local development (fallback)
LOCAL_UPLOAD_DIR = BASE_DIR / "files"
LOCAL_DATABASE_DIR = PROJECT_ROOT / "database"  # Place the database outside `app`

# Set the file storage path based on the environment or .env variable
if os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production":  # If running in production
    # Use Railway's mounted volume path
    FILE_STORAGE_PATH = Path(os.getenv("FILE_STORAGE_PATH", "/mnt/volume/files"))
    DATABASE_PATH = FILE_STORAGE_PATH  # Use the same path as FILE_STORAGE_PATH for production
else:
    # Use FILE_STORAGE_PATH from the .env file if set, otherwise fallback to LOCAL_UPLOAD_DIR
    FILE_STORAGE_PATH = Path(os.getenv("FILE_STORAGE_PATH", LOCAL_UPLOAD_DIR))
    DATABASE_PATH = LOCAL_DATABASE_DIR  # Use a separate directory for the database locally

# Ensure the directories exist
FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)
DATABASE_PATH.mkdir(parents=True, exist_ok=True)

# Set database URL based on the environment
if os.getenv("RAILWAY_ENVIRONMENT_NAME") == "production":  # If running in production
    # Use PostgreSQL DATABASE_URL for production
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the Railway environment.")
else:
    # In local development, use SQLite
    DATABASE_FILE = DATABASE_PATH / "database.db"  # Store the database in the `diffing/database` directory
    DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Debugging: Print paths for confirmation
print(f"File Storage Path: {FILE_STORAGE_PATH}")
print(f"Database Path: {DATABASE_PATH}")
print(f"SQLAlchemy Database URL: {SQLALCHEMY_DATABASE_URL}")