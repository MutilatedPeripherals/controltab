from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from diffing.models import SetlistItem, SetlistItemCreate, SetlistItemType, SetlistItem as SetlistItemSchema
from diffing.database import get_db

router = APIRouter(prefix="/setlist_items", tags=["setlist_items"])

# Get a specific setlist item by ID
@router.get("/{item_id}", response_model=SetlistItemSchema)
async def get_setlist_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(SetlistItem).filter(SetlistItem.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setlist item not found"
        )
    return item

# Get all setlist items (optionally filtered by type)
@router.get("/", response_model=List[SetlistItemSchema])
async def list_setlist_items(type: SetlistItemType = None, db: Session = Depends(get_db)):
    query = db.query(SetlistItem)
    if type:
        query = query.filter(SetlistItem.type == type)
    items = query.all()
    return items

# Create a new setlist item
@router.post("/", response_model=SetlistItemSchema, status_code=status.HTTP_201_CREATED)
async def create_setlist_item(setlist_item: SetlistItemCreate, db: Session = Depends(get_db)):
    # Additional validation based on type
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

    # Create and save the setlist item
    new_item = SetlistItem(**setlist_item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# Update an existing setlist item
@router.put("/{item_id}", response_model=SetlistItemSchema)
async def update_setlist_item(item_id: int, updates: SetlistItemCreate, db: Session = Depends(get_db)):
    item = db.query(SetlistItem).filter(SetlistItem.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Setlist item not found"
        )

    # Update fields based on the provided data
    if updates.type == SetlistItemType.SONG:
        item.song_id = updates.song_id or item.song_id
    else:
        item.title = updates.title or item.title

    item.notes = updates.notes if updates.notes is not None else item.notes
    db.commit()
    db.refresh(item)
    return item

@router.get("/first", response_model=SetlistItemSchema)
async def get_first_setlist_item(db: Session = Depends(get_db)):
    item = db.query(SetlistItem).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No setlist items found"
        )
    return item