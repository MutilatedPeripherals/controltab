import os
from pathlib import Path

# Directory for uploaded files (for static or other purposes)
UPLOAD_DIR = Path("../files")

# Check the environment and set the database path
if os.getenv("RAILWAY_ENVIRONMENT"):
    DATABASE_FILE = "/data/files.db"  # Ensure this is the correct path
else:
    DATABASE_FILE = "./files.db"

# Set the SQLAlchemy database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILE}"