# builtin imports
import os
from typing import List
from sqlmodel import select
from fastapi import APIRouter, Depends, status

# custom imports
from opendrive.account.models import User
from .upload_schemas import FileDataToShow
from .view_schemas import DriveItemResponse
from opendrive.db.config import SessionDependency
from .file_models import Folder, FileDataToBeStored
from opendrive.helpers.dependencies import upload_file_loggedin_user, get_current_user


upload_router = APIRouter(
    prefix="/upload",
    tags=["Upload Files"]
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# @upload_router.post("/uploadfiles/", response_model=List[FileDataToShow], status_code=status.HTTP_201_CREATED)
@upload_router.post("/uploadfiles/", status_code=status.HTTP_201_CREATED)
def create_upload_file(uploaded_file: List[FileDataToShow] = Depends(upload_file_loggedin_user)):
    return uploaded_file


@upload_router.get('/drive/list/', status_code=status.HTTP_200_OK, response_model=List[DriveItemResponse])
def get_drive_list(db: SessionDependency, user: User = Depends(get_current_user)):
    print("inside drive list")

    items:list = []

    # print("USER>>> ", user)
    print("USERIDD>>> ", user.id)

    # Folders
    stmt = select(Folder).where(Folder.user_id == user.id)
    print("STMT>>>>>>> ", stmt)
    folders = db.exec(stmt).first()
    print("FOLDERS>>>>>>>>>>>>>> ", folders)
    items.append(user)

    return items

    
    




