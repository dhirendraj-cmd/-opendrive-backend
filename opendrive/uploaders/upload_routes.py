# builtin imports
import os
from typing import List
from fastapi import APIRouter, Depends, status

# custom imports
from opendrive.helpers.dependencies import upload_file_loggedin_user
from .upload_schemas import FileDataToShow


upload_router = APIRouter(
    prefix="/upload",
    tags=["Upload Files"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# @upload_router.post("/uploadfiles/", response_model=List[FileDataToShow], status_code=status.HTTP_201_CREATED)
@upload_router.post("/uploadfiles/", status_code=status.HTTP_201_CREATED)
def create_upload_file(uploaded_file: List[FileDataToShow] = Depends(upload_file_loggedin_user)):
    return uploaded_file

