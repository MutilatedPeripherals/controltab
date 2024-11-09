from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, Request
import httpx
import aiofiles
import aiofiles.os
import tempfile
import zipfile
from diffing.script2 import compare_gpif_files
from starlette.responses import JSONResponse
from typing import List
from diffing.models import Tab
from diffing.crud import create_file_metadata, get_file_metadata
from diffing.database import SessionLocal, engine, Base
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
from fastapi.staticfiles import StaticFiles
from diffing.crud import get_all_tabs
from diffing.crud import get_original_file_path_by_id

app = FastAPI()

# Define the origins that are allowed to make requests to your API
origins = [
    "*",  # Allow all
]



UPLOAD_DIR = Path("files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict methods if needed, e.g. ["GET", "POST"]
    allow_headers=["*"],  # You can restrict headers if needed
)

app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# Directory for storing uploaded files
UPLOAD_DIR = Path("files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    x = compare_gpif_files('./complex/scoreA.gpif', './complex/scoreB.gpif')
    return x

@app.post("/compare/{tab_id}")
async def compare_tabs(
    tab_id: int,  
    user_tab: UploadFile = File(...),  
    db: Session = Depends(get_db)
):
    # Retrieve the path of the original .gp file from the database
    original_metadata = get_file_metadata(db, tab_id)
    if not original_metadata:
        raise HTTPException(status_code=404, detail="Original tab not found")
    original_gp_path = original_metadata.filepath

    try:
        # Step 1: Extract `score.gpif` from the original .gp file
        with zipfile.ZipFile(original_gp_path, 'r') as zip_ref:
            temp_original_dir = tempfile.mkdtemp()
            zip_ref.extractall(temp_original_dir)
            original_gpif_path = Path(temp_original_dir) / "Content" / "score.gpif"
            if not original_gpif_path.exists():
                raise HTTPException(status_code=400, detail="Original .gp file does not contain score.gpif")

        # Step 2: Save and extract `score.gpif` from the uploaded .gp file
        user_gp_path = UPLOAD_DIR / user_tab.filename
        with user_gp_path.open("wb") as f:
            f.write(await user_tab.read())

        with zipfile.ZipFile(user_gp_path, 'r') as zip_ref:
            temp_user_dir = tempfile.mkdtemp()
            zip_ref.extractall(temp_user_dir)
            user_gpif_path = Path(temp_user_dir) / "Content" / "score.gpif"
            if not user_gpif_path.exists():
                raise HTTPException(status_code=400, detail="Uploaded .gp file does not contain score.gpif")

        # Step 3: Compare the two `score.gpif` files
        comparison_result = compare_gpif_files(str(original_gpif_path), str(user_gpif_path))

        # Convert comparison_result to a JSON-serializable format if needed
        if isinstance(comparison_result, set):
            comparison_result = list(comparison_result)

        return JSONResponse(content={"comparison_result": comparison_result})

    finally:
        # Cleanup: Remove temporary files
        if user_gp_path.exists():
            user_gp_path.unlink()  # Delete the uploaded .gp file
        shutil.rmtree(temp_original_dir, ignore_errors=True)  # Remove extracted original directory
        shutil.rmtree(temp_user_dir, ignore_errors=True)  # Remove extracted user directory

Base.metadata.create_all(bind=engine)

@app.post("/upload")
async def upload_tab(
    song_name: str = Form(...), 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".gp"):
        raise HTTPException(status_code=400, detail="Only .gp files are allowed")

    filename = f"{song_name}.gp"
    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Save metadata to the database, including song_name
    db_file = create_file_metadata(db, filename=filename, filepath=str(file_path), song_name=song_name)
    return {"id": db_file.id, "filename": db_file.filename, "path": db_file.filepath}

@app.get("/files/{file_id}")
async def download_file(file_id: int, request: Request, db: Session = Depends(get_db)):
    db_file = get_file_metadata(db, file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = Path(db_file.filepath)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    # Construct the full URL for accessing the file through /static
    full_url = f"{request.base_url}static/{db_file.filename}"

    return {"filename": db_file.filename, "content_url": full_url}

@app.get("/tabs", response_model=list[Tab])
async def get_tabs(db: Session = Depends(get_db)):
    tabs = get_all_tabs(db)
    return tabs

