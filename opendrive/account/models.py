# builtin imports
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


# custom imports
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
    updated_at: datetime


class LoginInputSchema(SQLModel):
    username: str
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    # back populate to refresh token
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user", sa_relationship_kwargs={
        "cascade": "all, delete"
    })

    # back populate to Upload Files model
    files: List["FileDataToBeStored"] = Relationship(back_populates="user", sa_relationship_kwargs={
        "cascade": "all, delete"
    })

    folders: List["Folder"] = Relationship(back_populates="user", sa_relationship_kwargs={
        "cascade": "all, delete"
    })





