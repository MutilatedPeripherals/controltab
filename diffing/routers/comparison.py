from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request, Body
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from diffing.database import get_db
from diffing.crud import get_tab_file_path
from diffing.utils import save_uploaded_file, extract_gpif, compare_gpif_files
from pathlib import Path
from urllib.parse import urlparse
from diffing.models import SongMetadata

router = APIRouter(prefix="/compare", tags=["comparison"])


@router.post("/{song_id}")
async def compare_tabs(
    song_id: int,
    request: Request,
    user_tab: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    original_gp_filename = get_tab_file_path(db, song_id)
    if not original_gp_filename:
        raise HTTPException(status_code=404, detail="Original tab not found")

    original_gp_path = Path("files") / original_gp_filename
    if not original_gp_path.exists():
        raise HTTPException(status_code=404, detail="Original file not found on disk")

    original_gpif_path = extract_gpif(original_gp_path)
    user_gp_path = save_uploaded_file(user_tab, Path("files"))

    user_gpif_path = extract_gpif(user_gp_path)
    comparison_result = compare_gpif_files(str(original_gpif_path), str(user_gpif_path))

    return JSONResponse(
        content={
            "comparison_result": list(comparison_result),
            "original_file_url": f"{request.base_url}static/{original_gp_filename}",
            "uploaded_file_url": f"{request.base_url}static/{user_gp_path.name}",
        }
    )

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
