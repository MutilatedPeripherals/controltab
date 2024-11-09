from sqlalchemy.orm import Session
from diffing.models import FileMetadata

def create_file_metadata(db: Session, filename: str, filepath: str, song_name: str):
    db_file = FileMetadata(filename=filename, filepath=filepath, song_name=song_name)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file_metadata(db: Session, file_id: int):
    return db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

def get_all_tabs(db: Session):
    return db.query(FileMetadata).all()

def get_original_file_path_by_id(db: Session, file_id: int):
    file_metadata = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()
    return file_metadata.filepath if file_metadata else None