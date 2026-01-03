# inbuilt imports
import os
from sqlmodel import select
from collections import defaultdict
from typing import Annotated, Dict, List
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, UploadFile, File


# custom import
from opendrive.helpers.helper import decode_token
from opendrive.db.config import SessionDependency
from opendrive.helpers.helper import OS_home_directory
from opendrive.helpers.folder_creations import FolderCreations

from opendrive.account.models import User
from opendrive.uploaders.file_models import Folder, FileDataToBeStored



foc = FolderCreations()


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/account/login/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
home = OS_home_directory()
    

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


# def get_user_root_folder(session: SessionDependency, user: User)


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

# Uploaded Files>>>>>  [UploadFile(filename='pidrive (online-video-cutter.com).mp4', size=13258082, headers=Headers({'content-disposition': 'form-data; name="files"; filename="pidrive (online-video-cutter.com).mp4"', 'content-type': 'video/mp4'})), UploadFile(filename='pidrive.mp4', size=69820031, headers=Headers({'content-disposition': 'form-data; name="files"; filename="pidrive.mp4"', 'content-type': 'video/mp4'}))] 



def upload_file_loggedin_user(files: Annotated[list[UploadFile], File()], session: SessionDependency, token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token=token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in to upload files"
        )

    user = get_current_user(session=session, token=token)
    
    stmt = select(Folder).where(user.id == Folder.user_id)
    folder_data = session.exec(stmt).first()

    print("My folder data>>>>>>> ", folder_data)

    file_data: Dict[str, List[str]] = defaultdict(list)

    for file in files:
        print(file.filename, file.size, file.content_type)
        if file.filename is not None:
            file_data['file_name'].append(file.filename)
        if file.size is not None:
            file_data['file_size'].append(str(file.size))
        if file.content_type is not None:
            file_data['mime_type'].append(file.content_type)
            # file_data['stored_path'] = file.filename

    print(file_data) 




    

    
