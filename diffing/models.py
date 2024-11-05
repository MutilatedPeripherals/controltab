from pydantic import BaseModel
from typing import List, Optional

class Asset(BaseModel):
    id: str
    application_id: str
    s3: bool
    type: str
    filename: str
    url: str
    thumb_url: Optional[str]
    size: int
    field_key: str
    checksum: str

class Record(BaseModel):
    id: str
    field_17: int
    field_16: str
    field_18_raw: Asset
    field_19_raw: Optional[Asset]

class KnackResponse(BaseModel):
    total_pages: int
    current_page: int
    total_records: int
    records: List[Record]
