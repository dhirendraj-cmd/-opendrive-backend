from pydantic import BaseModel
from sqlmodel import SQLModel
from datetime import datetime


class UploadResultSchema(BaseModel):
    filename: str


class FileDataSchema(SQLModel):
    file_name: str
    file_size: int
    mime_type: str
    stored_path: str


class FileDataToShow(FileDataSchema):
    created_at: datetime
    updated_at: datetime
