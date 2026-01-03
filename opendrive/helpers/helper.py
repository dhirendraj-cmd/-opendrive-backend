# builtin imports
import os
from pathlib import Path
from typing import Any, Dict
from fastapi import Response
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime , timezone, timedelta


# custom imports
from opendrive.db.config import settings


SECRET_KEY=settings.SECRET_KEY
ALGORITHM=settings.ALGORITHM
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def now_utc():
    return datetime.now(timezone.utc)

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

def OS_home_directory():
    home = Path.home()
    return str(home)

    

    

