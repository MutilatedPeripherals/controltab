from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import SQLALCHEMY_DATABASE_URL
import os

# SQLAlchemy engine configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Session maker for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()

def initialize_database():
    """Initialize the database and create tables."""
    db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
    print(f"Initializing database at: {db_path}")
    if not os.path.exists(db_path):
        print("Database file does not exist. Creating new database.")
    else:
        print("Database file already exists.")
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()