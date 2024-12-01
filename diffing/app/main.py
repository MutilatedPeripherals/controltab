from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.auth import authentication
from app.config import FILE_STORAGE_PATH  # Import FILE_STORAGE_PATH
from app.database import initialize_database
from app.routers import bands, songs, comparison, setlists
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

# CORS Middleware to allow requests from the front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://controltab.up.railway.app",  # Deployed Svelte app
        "http://localhost:5173",             # Local Svelte app during development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi(app: FastAPI):
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Configure security scheme for Swagger UI
    openapi_schema['components']['securitySchemes'] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Apply security globally to all endpoints
    for path in openapi_schema.get('paths', {}).values():
        for method in path.values():
            method.setdefault('security', []).append({"bearerAuth": []})
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Use the custom OpenAPI schema
app.openapi = lambda: custom_openapi(app)

# Ensure the directory for static files exists
FILE_STORAGE_PATH.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=FILE_STORAGE_PATH), name="static")

# Include routers
app.include_router(songs.router)
app.include_router(comparison.router)
app.include_router(bands.router)
app.include_router(authentication.router)
app.include_router(setlists.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

# Enforce HTTPS for the Static Files
@app.middleware("http")
async def enforce_https_static(request, call_next):
    if request.url.scheme == "http":
        # Redirect HTTP to HTTPS for static files
        if request.url.path.startswith("/static"):
            url = request.url.replace(scheme="https")
            return RedirectResponse(url=str(url))
    return await call_next(request)
