from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from diffing.script2 import compare_gpif_files

app = FastAPI()

# Define the origins that are allowed to make requests to your API
origins = [
    "*",  # Allow all
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict methods if needed, e.g. ["GET", "POST"]
    allow_headers=["*"],  # You can restrict headers if needed
)


@app.get("/")
def read_root():
    x = compare_gpif_files('./complex/scoreA.gpif', './complex/scoreB.gpif')
    return x
