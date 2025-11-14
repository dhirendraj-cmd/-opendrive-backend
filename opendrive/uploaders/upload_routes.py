# builtin imports
import os
import shutil
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, Depends

# custom imports
from opendrive.account.dependencies import upload_file_loggedin_user


upload_router = APIRouter(
    prefix="/upload",
    tags=["Upload Files"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@upload_router.post("/uploadfiles/")
def create_upload_file(uploaded_file = Depends(upload_file_loggedin_user)):
    return uploaded_file





