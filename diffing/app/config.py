import os
from pathlib import Path

# Determine the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory for storing files (e.g., uploads or local database) in local development
UPLOAD_DIR = BASE_DIR / "files"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists locally

# Set the database file path or service URL based on the environment
if os.getenv("RAILWAY_ENVIRONMENT"):  # Detect if running in Railway
    # In production, use the private SQLite service's networking URL
    DATABASE_URL = "sqlite://sqlite3.railway.internal:5432/database.db"
else:
    # In local development, store the SQLite database locally
    DATABASE_FILE = UPLOAD_DIR / "database.db"
    DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Debugging: Print the resolved database URL (optional)
print(f"SQLAlchemy Database URL: {SQLALCHEMY_DATABASE_URL}")