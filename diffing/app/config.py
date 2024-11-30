import os
from pathlib import Path

# Determine the base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Directory for storing files (e.g., uploads or local database)
UPLOAD_DIR = BASE_DIR / "files"

# Ensure the `UPLOAD_DIR` exists in local development
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Set the database file path based on the environment
if os.getenv("RAILWAY_ENVIRONMENT"):  # Railway-specific environment variable
    # In production, use the volume-mounted path (persistent storage)
    DATABASE_FILE = "../data/database.db"
else:
    # In local development, store the SQLite database locally
    DATABASE_FILE = UPLOAD_DIR / "database.db"

# Construct the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Debugging: Print the resolved database path (optional)
print(f"Database path resolved to: {DATABASE_FILE}")
