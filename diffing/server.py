from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import httpx

from diffing.models import KnackResponse
from diffing.script2 import compare_gpif_files

app = FastAPI()

# Define the origins that are allowed to make requests to your API
origins = [
    "*",  # Allow all
]

KNACK_APP_ID = "672a995e272023027ef03c76"
KNACK_API_KEY = ""
KNACK_API_URL = "https://api.knack.com/v1/objects/object_4/records/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict methods if needed, e.g. ["GET", "POST"]
    allow_headers=["*"],  # You can restrict headers if needed
)

headers = {
    "X-Knack-Application-Id": KNACK_APP_ID,
    "X-Knack-REST-API-Key": KNACK_API_KEY,
    "Content-Type": "application/json"
}


@app.get("/")
def read_root():
    x = compare_gpif_files('./complex/scoreA.gpif', './complex/scoreB.gpif')
    return x


@app.get("/knack-records", response_model=KnackResponse)
async def get_knack_records():
    async with httpx.AsyncClient() as client:
        response = await client.get(KNACK_API_URL, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error retrieving records from Knack")
        return response.json()