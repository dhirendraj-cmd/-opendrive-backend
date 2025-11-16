# inbuilt imports
import os
import shutil
from typing import Annotated
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, UploadFile, File

# custom import
from opendrive.helpers.helper import decode_token
from opendrive.db.config import SessionDependency
from opendrive.account.models import User


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/account/login/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


def upload_file_loggedin_user(files: Annotated[list[UploadFile], File()], session: SessionDependency, token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token=token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You need to be logged in to upload files"
        )
    
    upload_dir = os.path.join(BASE_DIR, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    save_files: list[dict[str, str]] = []

    for file in files:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "Uploaded File has no filename"
            )
        
        filename = os.path.basename(file.filename)
        save_path = os.path.join(upload_dir, filename)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        safe_name = os.path.basename(file.filename)
        
        save_files.append({"filename": safe_name})

    return save_files

    
