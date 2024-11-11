import shutil
import uuid
import tempfile
from pathlib import Path
from fastapi import UploadFile
import zipfile

def save_uploaded_file(upload_file: UploadFile, upload_dir: Path) -> Path:
    unique_filename = f"{uuid.uuid4()}.gp"
    file_path = upload_dir / unique_filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
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
 