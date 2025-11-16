from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship



from opendrive.uploaders.file_models import FileDataToBeStored
from opendrive.helpers.helper import now_utc



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


class LoginInputSchema(SQLModel):
    username: str
    password: str
    

class RefreshToken(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
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
    refresh_tokens: List[RefreshToken] = Relationship(back_populates="user", sa_relationship_kwargs={
        "cascade": "all, delete"
    })

    # back populate to Upload Files model
    files: List[FileDataToBeStored] = Relationship(back_populates="user", sa_relationship_kwargs={
        "cascade": "all, delete"
    })





