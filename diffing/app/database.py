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
    # Ensure the directory for the database exists
    db_dir = os.path.dirname(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))
    if not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    print(f"Database initialized at: {SQLALCHEMY_DATABASE_URL}")
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()