# builtin imports
from datetime import datetime , timezone, timedelta

def now_utc():
    return datetime.now(timezone.utc)


import os
import uuid
from jose import JWTError, jwt
from sqlmodel import Session, select
from passlib.context import CryptContext
from typing import Any, Dict
from fastapi import Response

# custom imports
from opendrive.db.config import settings
from opendrive.account.models import RefreshToken, User


SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)


# creation of acess tokens
def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None):
    to_encode=data.copy()
    expire = now_utc() + (expires_delta or timedelta(minutes=20))
    to_encode.update({
        "exp": expire
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def create_tokens(session: Session, user: User):
    access_token = create_access_token(data={
        "sub": str(user.id)
    })

    refresh_token_str = str(uuid.uuid4())
    expires_at = now_utc() + timedelta(days=7)
    refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token_str,
        expires_at=expires_at
    )

    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token_str,
        'token_type': "bearer"
    }


def verify_refresh_token(session: Session, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    db_token = session.exec(stmt).first()

    if not db_token or db_token.revoked:
        return None, None
    
    expires_at = db_token.expires_at

    if expires_at.tzinfo is None:
        expires_at=expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now_utc():
        return None, None

    user = session.exec(select(User).where(User.id == db_token.user_id)).first()
    return user, db_token

    # if db_token and not db_token.revoked:
    #     expires_at = db_token.expires_at
    #     if expires_at.tzinfo is None:
    #         expires_at=expires_at.replace(tzinfo=timezone.utc)
    #     if expires_at > now_utc():
    #         stmt1 = select(User).where(User.id == db_token.user_id)
    #         return session.exec(stmt1).first()
    # return None


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return None


# Environment detection
def set_refresh_cookie(response: Response, token: str):

    ENV = os.getenv("ENV", "local").lower()

    # Default values
    secure = False
    samesite = "lax"
    domain = None

    if ENV == "local":
        # for localhost → HTTP only
        secure = False
        samesite = "lax"

    elif ENV == "staging":
        # staging → HTTPS enabled
        secure = True
        samesite = "none"
        domain = os.getenv("COOKIE_DOMAIN")

    elif ENV == "production":
        # prod → HTTPS likely enabled
        secure = True
        samesite = "none"
        domain = os.getenv("COOKIE_DOMAIN")

    response.set_cookie(
        key="refresh_token",
        value=token,
        httponly=True,
        secure=secure,
        samesite=samesite,
        domain=domain,
        max_age=60 * 60 * 24 * 7,  # 7 days
    )


