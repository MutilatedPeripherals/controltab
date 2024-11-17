from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from diffing.models import SetlistItem, SetlistItemCreate, SetlistItemSchema, SetlistItemType
from diffing.database import get_db

router = APIRouter(prefix="/setlist_items", tags=["setlist_items"])

@router.get("/", response_model=List[SetlistItemSchema])
async def list_setlist_items(type: SetlistItemType = None, db: Session = Depends(get_db)):
    query = db.query(SetlistItem)
    if type:
        query = query.filter(SetlistItem.type == type)
    items = query.all()
    return [SetlistItemSchema.from_orm(item) for item in items]

@router.post("/", response_model=SetlistItemSchema, status_code=status.HTTP_201_CREATED)
async def create_setlist_item(setlist_item: SetlistItemCreate, db: Session = Depends(get_db)):
    if setlist_item.type == SetlistItemType.SONG and not setlist_item.song_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="song_id is required for type 'song'"
        )
    if setlist_item.type != SetlistItemType.SONG and not setlist_item.title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="title is required for non-song items"
        )

    new_item = SetlistItem(**setlist_item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return SetlistItemSchema.from_orm(new_item)

@router.put("/setlist", response_model=List[SetlistItemSchema])
def update_setlist(
    new_setlist: List[SetlistItemSchema], 
    db: Session = Depends(get_db)
):
    # Validate new setlist items
    for item in new_setlist:
        if item.type == "song" and not item.song_id:
            raise HTTPException(status_code=400, detail="Missing songId for song type")
        if item.type != "song" and not item.title:
            raise HTTPException(status_code=400, detail="Missing title for non-song type")

    # Get existing items from DB
    existing_items = db.query(SetlistItem).all()
    existing_ids = {item.id for item in existing_items if item.id}
    new_ids = {item.id for item in new_setlist if item.id}

    # Remove stale items
    stale_ids = existing_ids - new_ids
    if stale_ids:
        db.query(SetlistItem).filter(SetlistItem.id.in_(stale_ids)).delete()

    # Update or create items
    for item_data in new_setlist:
        if item_data.id and item_data.id in existing_ids:
            # Update existing item
            db_item = db.query(SetlistItem).filter(SetlistItem.id == item_data.id).first()
            for key, value in item_data.dict(exclude_unset=True).items():
                setattr(db_item, key, value)
        else:
            # Create new item
            new_db_item = SetlistItem(**item_data.dict())
            db.add(new_db_item)

    db.commit()

    # Return updated setlist
    return db.query(SetlistItem).all()