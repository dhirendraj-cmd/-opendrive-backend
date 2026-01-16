from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class DriveItemType(str, Enum):
    FILE = "file"
    FOLDER = "folder"


class DriveItemSchema(BaseModel):
    id: int
    type: DriveItemType
    name: str
    folder_key: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    # parent_folder_key: Optional[str] = None


class DriveItemResponse(DriveItemSchema):
    created_at: datetime
    updated_at: datetime

