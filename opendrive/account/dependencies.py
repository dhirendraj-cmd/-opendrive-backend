# inbuilt imports
import os
import shutil
from typing import Annotated
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, UploadFile, File

# custom import
from opendrive.account.utils import decode_token
from opendrive.db.config import SessionDependency
from opendrive.account.models import User, RefreshToken


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="account/login")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_all_user(session: SessionDependency):
    all_users = session.exec(select(User)).all()
    return all_users
    

def get_current_user(session: SessionDependency, token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    stmt = select(User).where(User.id == int(payload.get("sub")))
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
    
    save_files = []
    if not os.path.exists(os.path.join(BASE_DIR, "uploads")):
        os.makedirs(os.path.join(BASE_DIR, "uploads"), exist_ok=True)

    for file in files:
        file_path = os.path.join(BASE_DIR, "uploads")
        save_path = f"{file_path}/{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        save_files.append({"filename": file.filename})

    return save_files

    
