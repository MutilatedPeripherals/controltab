# models.py
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from diffing.database import Base

class FileData(BaseModel):
    url: str

class Tab(BaseModel):
    id: int
    name: str
    oldFile: FileData
    newFile: FileData


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    filepath = Column(String)  # Path or URL to file
    song_name = Column(String)  # New column for the song name
    uploaded_at = Column(DateTime, default=datetime.utcnow)

# Pydantic model for the response
class Tab(BaseModel):
    id: int
    filename: str
    song_name: str
    filepath: str  # This could be a URL in production
    uploaded_at: datetime

    class Config:
        orm_mode = True  # Enables ORM to Pydantic model conversion