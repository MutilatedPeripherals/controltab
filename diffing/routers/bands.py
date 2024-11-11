from fastapi import APIRouter, Depends, HTTPException, status
from diffing.auth.authentication import get_current_band
from diffing.models import Band, BandCreate, BandSchema  # Import necessary schemas
from sqlalchemy.orm import Session
from diffing.database import get_db
from diffing.utils import generate_access_code

router = APIRouter(prefix="/bands", tags=["bands"])

@router.get("/{band_id}", response_model=BandSchema)
async def get_band(band_id: int, db: Session = Depends(get_db), band: Band = Depends(get_current_band)):
    band_data = db.query(Band).filter(Band.id == band_id).first()
    
    if band_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Band not found"
        )
    
    return band_data

@router.post("/", response_model=BandSchema, status_code=status.HTTP_201_CREATED)
async def create_band(band: BandCreate, db: Session = Depends(get_db)):
    # Check if a band with the same name already exists
    existing_band = db.query(Band).filter(Band.name == band.name).first()
    if existing_band:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A band with this name already exists"
        )
    
    # Generate a unique access code and check if it is already taken
    access_code = generate_access_code()
    while db.query(Band).filter(Band.access_code == access_code).first():
        access_code = generate_access_code()  # Regenerate if code is already in use

    # Create a new Band instance with the generated access code
    new_band = Band(name=band.name, access_code=access_code)
    
    # Add and commit the new band to the database
    db.add(new_band)
    db.commit()
    db.refresh(new_band)  # Refresh to get the new band's ID
    
    return new_band