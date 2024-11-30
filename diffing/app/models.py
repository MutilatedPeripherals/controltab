from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from typing import Optional
import enum
import uuid

# SQLAlchemy Models
class SongMetadata(Base):
    __tablename__ = "song_metadata"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    band_id = Column(Integer, ForeignKey("bands.id"), nullable=False)
    tab = relationship("TabMetadata", uselist=False, back_populates="song", cascade="all, delete")
    band = relationship("Band", back_populates="songs")
    setlist_items = relationship("SetlistItem", back_populates="song") 

class TabMetadata(Base):
    __tablename__ = "tab_metadata"
    id = Column(Integer, primary_key=True, index=True)
    filepath = Column(String, nullable=False)
    song_id = Column(Integer, ForeignKey("song_metadata.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    song = relationship("SongMetadata", back_populates="tab")

class Band(Base):
    __tablename__ = "bands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    access_code = Column(String, unique=True, nullable=False)
    songs = relationship("SongMetadata", back_populates="band")

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

class BandBase(BaseModel):
    name: str

class BandCreate(BandBase):
    pass 

class BandSchema(BandBase): 
    id: int
    access_code: str 

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    band_id: int | None = None

class LoginRequest(BaseModel):
    access_code: str
    
class SetlistItemType(str, enum.Enum):
    SONG = "song"
    SAMPLE = "sample"
    BREAK = "break"
    SPEECH = "speech"


class SetlistItem(Base):
    __tablename__ = "setlist_items"

    id: str = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    type: SetlistItemType = Column(Enum(SetlistItemType), nullable=False)
    title: Optional[str] = Column(String, nullable=True)
    notes: Optional[str] = Column(Text, nullable=True)
    song_id: Optional[int] = Column(Integer, ForeignKey("song_metadata.id"), nullable=True)
    order: int = Column(Integer, nullable=False)

    song = relationship("SongMetadata", back_populates="setlist_items")

    def __repr__(self):
        return f"<SetlistItem(id={self.id}, type={self.type}, title={self.title}, song_id={self.song_id}, notes={self.notes}, order={self.order})>"

class SetlistItemBase(BaseModel):
    type: SetlistItemType
    title: Optional[str] = None
    notes: Optional[str] = None
    song_id: Optional[int] = None
    order: int  


class SetlistItemCreate(SetlistItemBase):
    pass

class SetlistItemSchema(BaseModel):
    id: Optional[str] = None
    type: SetlistItemType
    title: Optional[str] = None
    notes: Optional[str] = None
    song_id: Optional[int] = None
    order: int 

    class Config:
        from_attributes = True 