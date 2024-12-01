from sqlalchemy.orm import Session, joinedload
from app.models import SongMetadata, TabMetadata, Song, Tab
from typing import Optional

def create_song_with_tab(db: Session, title: str, filepath: str, band_id: int) -> SongMetadata:
    new_song = SongMetadata(title=title, band_id=band_id)
    db.add(new_song)
    db.commit()
    db.refresh(new_song) 

    new_tab = TabMetadata(filepath=filepath, song_id=new_song.id)
    db.add(new_tab)
    db.commit()
    db.refresh(new_tab) 

    return new_song

def get_song_with_tab(db: Session, song_id: int) -> Optional[SongMetadata]:
    return db.query(SongMetadata).options(joinedload(SongMetadata.tab)).filter(SongMetadata.id == song_id).first()

def get_all_songs(db: Session, band_id: int):
    return db.query(SongMetadata).filter(SongMetadata.band_id == band_id).all()

def get_tab_file_path(db: Session, song_id: int) -> Optional[str]:
    tab = db.query(TabMetadata).filter(TabMetadata.song_id == song_id).first()
    return tab.filepath if tab else None
