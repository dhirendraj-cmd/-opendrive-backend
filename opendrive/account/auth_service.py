import uuid
from datetime import timedelta, timezone

from sqlmodel import Session, select
from opendrive.account.models import User
from opendrive.account.token_models import RefreshToken
from opendrive.helpers.helper import create_access_token, now_utc


def create_tokens(session: Session, user: User):
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

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
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }


def verify_refresh_token(session: Session, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    db_token = session.exec(stmt).first()

    if not db_token or db_token.revoked:
        return None, None

    expires_at = db_token.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at <= now_utc():
        return None, None

    user = session.get(User, db_token.user_id)
    return user, db_token
