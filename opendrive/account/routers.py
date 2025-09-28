# custom imports
from opendrive.db.config import SessionDependency
from opendrive.account.services import create_user, authenticate_user
from opendrive.account.models import User, UserCreate, UserOut
from opendrive.account.utils import create_tokens, verify_refresh_token
from opendrive.account.dependencies import get_current_user, get_all_user

# built in imports
from typing import Annotated, List
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Query, Depends, Request, status


router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

@router.get("/users", response_model=List[UserOut])
def get_all_users(all_users=Depends(get_all_user)):
    return all_users


# register user endpoint
@router.post("/register", response_model=UserOut)
def register_user(session: SessionDependency, user: UserCreate):
    return create_user(session, user)


# user login
@router.post("/login")
def login_user(session: SessionDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!")
    # user has entered correct username and paswword so token creation will start from here
    tokens = create_tokens(session, user)
    response = JSONResponse(
        content={
            "access_token": tokens["access_token"]
        }
    )
    response.set_cookie("refresh_token", tokens["refresh_token"], httponly=True, secure=True, samesite="lax", max_age=60*60*24*7)
    return response


# refresh token
@router.post("/refresh")
def refresh_token(session: SessionDependency, request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Refresh Token")
    user = verify_refresh_token(session, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return create_tokens(session, user)


# logged in user
@router.get("/me", response_model=UserOut)
def loggedin_user(user = Depends(get_current_user)):
    return user







