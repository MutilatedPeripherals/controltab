from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status, Request, Body
from sqlalchemy.orm import Session
from typing import List
from diffing.database import get_db
from diffing.crud import create_song_with_tab, get_song_with_tab, get_all_songs
from diffing.models import Song, SongMetadata
from diffing.utils import save_uploaded_file
from pathlib import Path 
from urllib.parse import urlparse

router = APIRouter(prefix="/songs", tags=["songs"])

@router.get("/", response_model=List[Song])
async def get_songs(db: Session = Depends(get_db)):
    return get_all_songs(db)

@router.get("/{song_id}")
async def get_song(song_id: int, request: Request, db: Session = Depends(get_db)):
    song = get_song_with_tab(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    if song.tab:
        song.tab.filepath = f"{request.base_url}static/{song.tab.filepath}"

    return song


@router.post("/", response_model=Song)
async def create_song(title: str = Form(...), tab_file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not tab_file.filename.endswith(".gp"):
        raise HTTPException(status_code=400, detail="Only .gp files are allowed")
    
    unique_filename = save_uploaded_file(tab_file, Path("files")).name
    return create_song_with_tab(db, title=title, filepath=unique_filename)

@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = get_song_with_tab(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    db.delete(song)
    db.commit()
    return {"message": "Song deleted successfully"}

@router.put("/{song_id}/confirm-changes")
async def confirm_changes(
    song_id: int,
    db: Session = Depends(get_db),
    uploaded_file_url: str = Body(..., embed=True)
):
    song = db.query(SongMetadata).filter(SongMetadata.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    uploaded_path = urlparse(uploaded_file_url).path
    relative_path = Path(uploaded_path).relative_to("/static")

    song.tab.filepath = str(relative_path)
    db.commit()

    return {"message": "Tab updated successfully"}