from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import httpx
import aiofiles
import aiofiles.os
import tempfile
import zipfile
from diffing.script2 import compare_gpif_files
from starlette.responses import JSONResponse

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


@app.get("/knack-records", response_model=None)
async def get_knack_records():
    async with httpx.AsyncClient() as client:
        response = await client.get(KNACK_API_URL, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error retrieving records from Knack")

        response_data = response.json()
        record = response_data["records"][2]

        files_to_download = [
            ("old", record["field_18_raw"]["url"]),
            ("new", record["field_19_raw"]["url"])
        ]

        download_paths = {}

        for field, url in files_to_download:
            async with client.stream("GET", url) as file_response:
                if file_response.status_code != 200:
                    raise HTTPException(status_code=file_response.status_code,
                                        detail=f"Error downloading file from {field}")

                tmp_dir = tempfile.mkdtemp()
                tmp_file_path = f"{tmp_dir}/{field}.gp"

                async with aiofiles.open(tmp_file_path, 'wb') as tmp_file:
                    async for chunk in file_response.aiter_bytes():
                        await tmp_file.write(chunk)

                with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
                    zip_ref.extractall(tmp_dir)

                download_paths[field] = tmp_dir

        return {
            "download_paths": files_to_download,
            "masterbar_diffs":compare_gpif_files(f"{download_paths["old"]}/Content/score.gpif",
                                           f"{download_paths["new"]}/Content/score.gpif")
        }