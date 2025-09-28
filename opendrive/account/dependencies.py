# inbuilt imports
from typing import Annotated
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# custom import
from opendrive.account.utils import decode_token
from opendrive.db.config import SessionDependency
from opendrive.account.models import User, RefreshToken


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="account/login")


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
    
