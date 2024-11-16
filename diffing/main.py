from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from diffing.auth import authentication
from diffing.config import UPLOAD_DIR
from diffing.database import initialize_database
from diffing.routers import bands, songs, comparison, setlists

app = FastAPI()

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for storing uploaded files
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# Initialize Database
initialize_database()

# Include Routers
app.include_router(songs.router)
app.include_router(comparison.router)
app.include_router(bands.router)
app.include_router(authentication.router)
app.include_router(setlists.router)
