from typing import Union

from fastapi import FastAPI

from diffing.script2 import compare_gpif_files

app = FastAPI()


@app.get("/")
def read_root():
    x = compare_gpif_files('./complex/scoreA.gpif', './complex/scoreB.gpif')
    return {"Hello": f"World {len(x)}"}