from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from diffing.database import Base
from typing import Optional

# SQLAlchemy Models
class SongMetadata(Base):
    __tablename__ = "song_metadata"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    tab = relationship("TabMetadata", uselist=False, back_populates="song", cascade="all, delete")

class TabMetadata(Base):
    __tablename__ = "tab_metadata"
    id = Column(Integer, primary_key=True, index=True)
    filepath = Column(String, nullable=False)
    song_id = Column(Integer, ForeignKey("song_metadata.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    song = relationship("SongMetadata", back_populates="tab")

# Pydantic Schemas
class SongBase(BaseModel):
    title: str

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int
    tab: Optional["Tab"]

    class Config:
        orm_mode = True

class Tab(BaseModel):
    id: int
    filepath: str
    song_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
