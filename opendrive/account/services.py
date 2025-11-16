from sqlmodel import Session, select
from fastapi import HTTPException, status
from opendrive.helpers.helper import hash_password, verify_password
from opendrive.account.models import User, UserCreate


def create_user(session: Session, user: UserCreate):
    # check for existing email
    exisitng_email = select(User).where(User.email == user.email)

    if session.exec(exisitng_email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # check for existing username
    username_exists = select(User).where(User.username == user.username)

    if session.exec(username_exists).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken"
        )
    
    new_user = User(
        name=user.name,
        email=user.email,
        username=user.username,
        is_active=True,
        hashed_password=hash_password(user.password),
        is_verified=False
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
    

def authenticate_user(session: Session, username: str, password: str):
    stmt = select(User).where(User.username == username)
    user = session.exec(stmt).first()

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


