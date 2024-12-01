from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.auth import authentication
from app.config import FILE_STORAGE_PATH  # Import FILE_STORAGE_PATH
from app.database import initialize_database
from app.routers import bands, songs, comparison, setlists


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory for storing uploaded files
FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
app.mount("/static", StaticFiles(directory=FILE_STORAGE_PATH), name="static")

# Include Routers
app.include_router(songs.router)
app.include_router(comparison.router)
app.include_router(bands.router)
app.include_router(authentication.router)
app.include_router(setlists.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
