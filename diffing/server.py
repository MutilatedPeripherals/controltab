from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
import shutil
import zipfile
from pathlib import Path
from sqlalchemy.orm import Session
from typing import List
import tempfile
import uuid
from urllib.parse import urlparse

from diffing.database import SessionLocal, engine, Base
from diffing.models import Song, SongMetadata
from diffing.crud import (
    create_song_with_tab,
    get_song_with_tab,
    get_all_songs,
    get_tab_file_path
)
from diffing.script2 import compare_gpif_files

app = FastAPI()

# CORS configuration
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
Base.metadata.create_all(bind=engine)

@app.get("/songs", response_model=List[Song])
async def get_songs(db: Session = Depends(get_db)):
    songs = get_all_songs(db)
    return songs

@app.get("/songs/{song_id}")
async def get_song(song_id: int, request: Request, db: Session = Depends(get_db)):
    song = get_song_with_tab(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    # Modify the tab filepath to include the full URL for downloading
    if song.tab:
        song.tab.filepath = f"{request.base_url}static/{song.tab.filepath}"

    return song

@app.post("/compare/{song_id}")
async def compare_tabs(
    song_id: int,
    request: Request,
    user_tab: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Get the relative file path from the database and construct the full path
    original_gp_filename = get_tab_file_path(db, song_id)
    if not original_gp_filename:
        raise HTTPException(status_code=404, detail="Original tab not found")

    original_gp_path = UPLOAD_DIR / original_gp_filename  # Construct the full path

    # Verify if the file actually exists at this location
    if not original_gp_path.exists():
        raise HTTPException(status_code=404, detail="Original file not found on disk")

    # Proceed with file processing as before...
    with zipfile.ZipFile(original_gp_path, 'r') as zip_ref:
        temp_original_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_original_dir)
        original_gpif_path = Path(temp_original_dir) / "Content" / "score.gpif"
        if not original_gpif_path.exists():
            raise HTTPException(status_code=400, detail="Original .gp file does not contain score.gpif")

    # Continue with user file extraction and comparison as usual
    unique_filename = f"{uuid.uuid4()}.gp"
    user_gp_path = UPLOAD_DIR / unique_filename
    with user_gp_path.open("wb") as f:
        shutil.copyfileobj(user_tab.file, f)

    with zipfile.ZipFile(user_gp_path, 'r') as zip_ref:
        temp_user_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_user_dir)
        user_gpif_path = Path(temp_user_dir) / "Content" / "score.gpif"
        if not user_gpif_path.exists():
            raise HTTPException(status_code=400, detail="Uploaded .gp file does not contain score.gpif")

    # Compare the two .gpif files
    comparison_result = compare_gpif_files(str(original_gpif_path), str(user_gpif_path))

    # Cleanup temporary directories
    shutil.rmtree(temp_original_dir)
    shutil.rmtree(temp_user_dir)

    original_file_url = f"{request.base_url}static/{original_gp_filename}"
    uploaded_file_url = f"{request.base_url}static/{unique_filename}"

    return JSONResponse(content={
        "comparison_result": list(comparison_result),
        "original_file_url": original_file_url,
        "uploaded_file_url": uploaded_file_url
    })

@app.post("/songs", response_model=Song)
async def create_song(
    title: str = Form(...),
    tab_file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not tab_file.filename.endswith(".gp"):
        raise HTTPException(status_code=400, detail="Only .gp files are allowed")

    # Generate a unique filename for the file to avoid conflicts
    unique_filename = f"{uuid.uuid4()}.gp"
    file_path = UPLOAD_DIR / unique_filename

    # Save the tab file with the unique name
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(tab_file.file, buffer)

    # Create song with tab in the database, store only the relative path
    song = create_song_with_tab(db, title=title, filename=unique_filename, filepath=str(file_path.relative_to(UPLOAD_DIR)))
    
    return song

@app.delete("/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(SongMetadata).filter(SongMetadata.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    if song.tab:
        db.delete(song.tab)
    
    db.delete(song)
    db.commit()
    return {"message": "Song deleted successfully"}

@app.put("/songs/{song_id}/confirm-changes")
async def confirm_changes(
    song_id: int,
    db: Session = Depends(get_db),
    uploaded_file_url: str = Body(..., embed=True)
):
    song = db.query(SongMetadata).filter(SongMetadata.id == song_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    # Parse the provided URL to extract the file path
    uploaded_path = urlparse(uploaded_file_url).path
    relative_path = Path(uploaded_path).relative_to("/static")

    # Store the relative path in the database
    song.tab.filepath = str(relative_path)
    db.commit()

    return {"message": "Tab updated successfully"}
