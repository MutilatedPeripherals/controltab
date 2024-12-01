from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import SQLALCHEMY_DATABASE_URL
import os

# Determine connection arguments based on the database type
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else None

# SQLAlchemy engine configuration
if connect_args:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args=connect_args  # Pass this only if not None
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Omit connect_args entirely for PostgreSQL

# Session maker for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()

def initialize_database():
    """Initialize the database and create tables."""
    if "sqlite" in SQLALCHEMY_DATABASE_URL:
        # SQLite-specific logic
        db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
        absolute_path = os.path.abspath(db_path)
        print(f"Resolved database path: {absolute_path}")
        print(f"Initializing database at: {db_path}")
        if not os.path.exists(db_path):
            print("Database file does not exist. Creating new database.")
        else:
            print("Database file already exists.")

    # Create all tables using the engine
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
