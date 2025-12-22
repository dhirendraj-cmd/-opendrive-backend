from pydantic import BaseModel
from sqlmodel import SQLModel
from datetime import datetime


class UploadResultSchema(BaseModel):
    filename: str


class FolderSchema(SQLModel):
    folder_key: str
    display_name: str


class FolderToShow(SQLModel):
    created_at: datetime
    updated_at: datetime


class FileDataSchema(SQLModel):
    file_name: str
    file_size: int
    mime_type: str
    stored_path: str


class FileDataToShow(FileDataSchema):
    folder_key: str
    display_name: str
    created_at: datetime
    updated_at: datetime
