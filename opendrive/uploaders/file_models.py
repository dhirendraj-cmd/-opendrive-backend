# custom imports
from opendrive.helpers.helper import now_utc
from .upload_schemas import FileDataSchema



# builtins imports
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel



if TYPE_CHECKING:
    from opendrive.account.models import User



class Folder(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    folder_key: str = Field(unique=True, index=True)
    display_name: str = Field(default="Pi Drive")
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default=now_utc)
    updated_at: datetime = Field(default=now_utc)

    # back populates
    user: Optional["User"] = Relationship(back_populates="folders")
    files: List["FileDataToBeStored"] = Relationship(back_populates="folder")
    
    



class FileDataToBeStored(FileDataSchema, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    folder_id: int = Field(foreign_key="folder.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    # back populate
    user: Optional["User"] = Relationship(back_populates="files")
    folder: Optional["Folder"] = Relationship(back_populates="files")


