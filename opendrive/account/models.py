from datetime import timezone, datetime
from typing import Optional, Annotated, List
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


def now_utc():
    return datetime.now(timezone.utc)


class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    username: str = Field(min_length=3, unique=True, index=True)
    is_active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
                            


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserOut(UserBase):
    id: int
    created_at: datetime
    upated_at: datetime
    

class RefreshToken(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    token: str = Field(unique=True, index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=now_utc)
    revoked: bool = Field(default=False)

    # back populates relationship to user
    user: "User" = Relationship(back_populates="refresh_tokens")


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=now_utc)
    upated_at: datetime = Field(default_factory=now_utc)

    # back populate to refresh token
    refresh_tokens: List[RefreshToken] = Relationship(back_populates="user")

    # __table_args__ = (UniqueConstraint("email"), UniqueConstraint("username"))





