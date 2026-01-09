# inbuilt imports
import os
import shutil
import traceback
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


def save_file_data_in_db(db: SessionDependency, file_name: str, file_size: int, mime_type: str, stored_path: str, user_id: int, folder_id: int):
    saved_data = FileDataToBeStored(
        file_name=file_name,
        file_size=file_size,
        mime_type=mime_type,
        stored_path=stored_path,
        user_id=user_id,
        folder_id=folder_id
    )

    db.add(saved_data)
    db.commit()
    db.refresh(saved_data)

    return saved_data



def upload_file_loggedin_user(files: Annotated[list[UploadFile], File()], session: SessionDependency, token: Annotated[str, Depends(oauth2_bearer)]):
    parent_folder_type = ""
    child_folder_type = ""
    storing_path: str = ""

    # token retrieval
    payload = decode_token(token=token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in to upload files"
        )

    user = get_current_user(session=session, token=token)
    
    stmt = select(Folder).where(user.id == Folder.user_id)
    folder_data = session.exec(stmt).first()

    # Dictionary to track results for all files
    all_file_results: Dict[str, List[str]] = defaultdict(list)

    file_data: Dict[str, List[str]] = defaultdict(list)

    for file in files:
        if not file.filename:
            continue
        
        if file.content_type is not None:
            parent_folder_type = file.content_type.split('/')[0]
            child_folder_type = file.content_type.split('/')[1]

        if file.size is not None:
            file_data['size'].append(str(file.size))

        # folder data check
        if folder_data:
            user_id = str(folder_data.user_id)
            file_data['user_id'].append(user_id)
            file_data['folder_key'].append(folder_data.folder_key)
            file_data['display_name'].append(folder_data.display_name)

            per_user_upload = foc.create_upload_dir_per_user(user_id=str(folder_data.user_id), folder_key=folder_data.folder_key, display_name=folder_data.display_name, parent_folder_type=parent_folder_type, child_folder_type=child_folder_type)

            print("per_user_upload>>>>>>> ", per_user_upload)
            
            storing_path = os.path.join(per_user_upload, file.filename)

            file_data['stored_path'].append(storing_path)

            try:
                with open(storing_path, "wb+") as file_obj:
                    file.file.seek(0)
                    shutil.copyfileobj(file.file, file_obj)
                
                # save file data in db
                save_file_data_in_db(
                    db=session,
                    file_name=file.filename, 
                    file_size=file.size, 
                    mime_type=str(file.content_type), 
                    stored_path=str(storing_path), 
                    user_id=user.id,
                    folder_id=folder_data.id
                )
                
                # all_file_results.append({"filename": file.filename, "status": "success"})
                all_file_results['filename'].append(file.filename)
                all_file_results['status'].append("success")

            except Exception as err:
                print(f"Error is >>. ", err)
                traceback.print_exc()

    return {"uploaded_files": all_file_results}





    

    
