from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
import jwt
from jwt import decode, PyJWTError
from diffing.models import Band, Token, TokenData
from diffing.database import get_db
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

# Security configuration for Swagger
api_key_scheme = APIKeyHeader(name="Authorization")

# JWT Configuration
SECRET_KEY = "YTqyjx8ja5KiCl2vjgg9XCIujYAAAnjx"  # Replace with a secure, unique key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper function to create a JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Custom login endpoint that issues a token based on access_code
@router.post("/token", response_model=Token)
async def login_for_access_token(access_code: str = Form(...), db: Session = Depends(get_db)):
    band = db.query(Band).filter(Band.access_code == access_code).first()
    if not band:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access code",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token with band ID encoded
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"band_id": band.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to validate the token and retrieve the current band
async def get_current_band(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[Band]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        band_id: int = payload.get("band_id")
        if band_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    # Query the database to retrieve the current band
    band = db.query(Band).filter(Band.id == band_id).first()
    print("alskjdflkjasdflkjasdflkjasdñlfkjalsdkfjaldkjsfadfkl")
    print(band)
    if band is None:
        raise credentials_exception

    return band
