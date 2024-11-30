import os
from pathlib import Path

# Determine the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory for storing files (e.g., uploads or local database) in local development
UPLOAD_DIR = BASE_DIR / "files"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists locally

# Set database URL based on the environment
if os.getenv("RAILWAY_ENVIRONMENT"):  # Detect if running in Railway
    # Use PostgreSQL DATABASE_URL for production
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not set in the Railway environment.")
else:
    # In local development, use SQLite
    DATABASE_FILE = UPLOAD_DIR / "database.db"
    DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Debugging: Print the resolved database URL
print(f"SQLAlchemy Database URL: {SQLALCHEMY_DATABASE_URL}")