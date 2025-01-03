import secrets
import shutil
import string
import tempfile
import uuid
import zipfile
from pathlib import Path
from app.config import FILE_STORAGE_PATH

from fastapi import UploadFile


def generate_access_code(length: int = 10) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def save_uploaded_file(upload_file: UploadFile, upload_dir: Path = FILE_STORAGE_PATH) -> Path:
    # Ensure the upload directory exists
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate a unique filename with .gp extension
    unique_filename = f"{uuid.uuid4()}.gp"
    file_path = upload_dir / unique_filename
    
    # Save the uploaded file to the specified directory
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
        print(f"File saved to: {file_path}")
    return file_path
def extract_gpif(gp_path: Path) -> Path:
    with zipfile.ZipFile(gp_path, 'r') as zip_ref:
        temp_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_dir)
        gpif_path = Path(temp_dir) / "Content" / "score.gpif"
        if not gpif_path.exists():
            raise ValueError("File does not contain score.gpif")
    return gpif_path

def compare_gpif_files(original_gpif_path: str, user_gpif_path: str):
    # Implement comparison logic here, possibly returning a list or JSON structure
    return []