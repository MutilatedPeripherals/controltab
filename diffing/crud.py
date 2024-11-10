from sqlalchemy.orm import Session, joinedload
from diffing.models import SongMetadata, TabMetadata, Song, Tab
from typing import Optional


def create_song_with_tab(db: Session, title: str, filename: str, filepath: str):
    # Create a new SongMetadata entry
    new_song = SongMetadata(title=title)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    # Create a new TabMetadata entry and link it to the song
    new_tab = TabMetadata(filename=filename, filepath=filepath, song_id=new_song.id)
    db.add(new_tab)
    db.commit()
    db.refresh(new_song)  # Refresh the song to include the tab relationship

    return new_song  # Return the song with associated tab

def get_song_with_tab(db: Session, song_id: int) -> Optional[SongMetadata]:
    # Fetch the song and eagerly load the associated tab
    return db.query(SongMetadata).options(joinedload(SongMetadata.tab)).filter(SongMetadata.id == song_id).first()


def get_all_songs(db: Session) -> list[Song]:
    songs = db.query(SongMetadata).all()

    # Convert to Pydantic model
    song_list = []
    for song in songs:
        # Map the SQLAlchemy object to the Pydantic model
        song_data = Song(
            id=song.id,
            title=song.title,
            tab=Tab(
                id=song.tab.id,
                filename=song.tab.filename,
                filepath=song.tab.filepath,
                song_id=song.tab.song_id,
                uploaded_at=song.tab.uploaded_at,
            ) if song.tab else None,
        )
        song_list.append(song_data)

    return song_list


def get_tab_file_path(db: Session, song_id: int) -> Optional[str]:
    # Retrieve the file path of the tab associated with the song
    tab = db.query(TabMetadata).filter(TabMetadata.song_id == song_id).first()
    return tab.filepath if tab else None
