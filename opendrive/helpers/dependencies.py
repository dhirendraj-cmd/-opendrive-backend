# inbuilt imports
import os
# import shutil, traceback
from typing import Annotated
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, UploadFile, File


# custom import
from opendrive.helpers.helper import decode_token
from opendrive.db.config import SessionDependency
from opendrive.account.models import User
# from opendrive.uploaders.file_models import FileDataToBeStored
from opendrive.helpers.helper import OS_home_directory
# from opendrive.helpers.file_creations import FileCreation
from opendrive.helpers.folder_creations import FolderCreations

foc = FolderCreations()


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/account/login/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
home = OS_home_directory()

# def get_all_user(session: SessionDependency):
#     all_users = session.exec(select(User)).all()
#     return all_users

    

def get_current_user(session: SessionDependency, token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    stmt = select(User).where(User.id == int(user_id))
    user = session.exec(stmt).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    
    return user


# def save_file_data_in_db(db: SessionDependency, file_name: str, file_size: int, mime_type: str, stored_path: str, user_id: int):
#     file_data = FileDataToBeStored(
#         file_name=file_name,
#         file_size=file_size,
#         mime_type=mime_type,
#         stored_path=stored_path,
#         user_id=user_id
#     )

#     db.add(file_data)
#     db.commit()
#     db.refresh(file_data)

#     return file_data




def upload_file_loggedin_user(files: Annotated[list[UploadFile], File()], session: SessionDependency, token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token=token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in to upload files"
        )

    user = get_current_user(session=session, token=token)
    print("user.id>>>>>> ", user.id)

    folder_path  = foc.create_directories_per_user(user_id=str(user.id))

    print("My folder path >>> ", folder_path)



    

    
