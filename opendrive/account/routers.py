# custom imports
from opendrive.db.config import SessionDependency
from opendrive.account.services import create_user, authenticate_user
from opendrive.account.models import User, UserCreate, UserOut, RefreshToken, LoginInputSchema
from opendrive.account.utils import create_tokens, verify_refresh_token, set_refresh_cookie
from opendrive.account.dependencies import get_current_user

# built in imports
# from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, Request, status, Response
from sqlmodel import select


router = APIRouter(
    prefix="/account",
    tags=["Account"]
)

# @router.get("/users", response_model=List[UserOut])
# def get_all_users(all_users=Depends(get_all_user)):
#     return all_users


# register user endpoint
@router.post("/register/", response_model=UserOut)
def register_user(session: SessionDependency, user: UserCreate):
    return create_user(session, user)


# user login
@router.post("/login/")
# def login_user(response: Response, session: SessionDependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
def login_user(response: Response, session: SessionDependency, form_data: LoginInputSchema):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!")
    # user has entered correct username and paswword so token creation will start from here
    tokens = create_tokens(session, user)

    set_refresh_cookie(response, tokens["refresh_token"])

    return {"access_token": tokens["access_token"]}


# refresh token
@router.post("/refresh/")
def refresh_token(session: SessionDependency, request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Refresh Token")
    user, db_token = verify_refresh_token(session, token)
    if not user or not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    
    db_token.revoked = True
    session.add(db_token)
    session.commit()

    # creating new access n refrsh token
    tokens = create_tokens(session=session, user=user)

    set_refresh_cookie(response, tokens["refresh_token"])

    return {"access_token": tokens["access_token"]}


# logged in user
@router.get("/me/", response_model=UserOut)
def loggedin_user(user: User = Depends(get_current_user)):
    return user


# logout end point
@router.post("/logout/")
def logout_user(response: Response, session: SessionDependency, request: Request, current_user: User = Depends(get_current_user)):
    
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in"
        )
    
    # get refresh token from cookies
    token = request.cookies.get("refresh_token")

    if token:
        # revoke refrsh token from db
        stmt = select(RefreshToken).where(RefreshToken.token == token)
        db_token = session.exec(stmt).first()

        
        if db_token:
            db_token.revoked = True
            session.add(db_token)
            session.commit()

    response.delete_cookie(key="refresh_token")
    return {
        "message": "Logged Out Successfully!"
    }







