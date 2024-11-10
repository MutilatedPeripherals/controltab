from sqlalchemy.orm import Session, joinedload
from diffing.models import SongMetadata, TabMetadata, Song, Tab
from typing import Optional


def create_song_with_tab(db: Session, title: str, filepath: str):
    new_song = SongMetadata(title=title)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    new_tab = TabMetadata(filepath=filepath, song_id=new_song.id)
    db.add(new_tab)
    db.commit()
    db.refresh(new_song)  

    return new_song  

def get_song_with_tab(db: Session, song_id: int) -> Optional[SongMetadata]:
    return db.query(SongMetadata).options(joinedload(SongMetadata.tab)).filter(SongMetadata.id == song_id).first()


def get_all_songs(db: Session) -> list[Song]:
    songs = db.query(SongMetadata).all()

    song_list = []
    for song in songs:
        song_data = Song(
            id=song.id,
            title=song.title,
            tab=Tab(
                id=song.tab.id,
                filepath=song.tab.filepath, 
                song_id=song.tab.song_id,
                uploaded_at=song.tab.uploaded_at,
            ) if song.tab else None,
        )
        song_list.append(song_data)

    return song_list


def get_tab_file_path(db: Session, song_id: int) -> Optional[str]:
    tab = db.query(TabMetadata).filter(TabMetadata.song_id == song_id).first()
    return tab.filepath if tab else None
