from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union

class AssetInfo(BaseModel):
    id: str
    application_id: str
    s3: bool
    type: str
    source: Optional[str]
    filename: str
    url: HttpUrl
    thumb_url: Optional[HttpUrl] = None
    size: int
    field_key: str
    checksum: str

class Record(BaseModel):
    id: str
    field_17: int
    field_17_raw: int
    field_16: str
    field_16_raw: str
    field_18: str
    field_18_raw: AssetInfo
    field_19: Optional[str] = None
    field_19_raw: Union[AssetInfo, str, None] = None

class ResponseModel(BaseModel):
    total_pages: int
    current_page: int
    total_records: int
    records: List[Record]
