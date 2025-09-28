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
async def create_upload_file(uploaded_file = Depends(upload_file_loggedin_user)):
    return uploaded_file
    
# async def create_upload_file(files: Annotated[list[UploadFile], File()]):
    # save_files = []
    # if not os.path.exists(os.path.join(BASE_DIR, "uploads")):
    #     os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

    # for file in files:
    #     file_path = os.path.join(BASE_DIR, "uploads")
    #     save_path = f"{file_path}/{file.filename}"
    #     with open(save_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    #     save_files.append({"filename": file.filename})

    # return save_files
