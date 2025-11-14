from pydantic import BaseModel


class UploadResultSchema(BaseModel):
    filename: str

