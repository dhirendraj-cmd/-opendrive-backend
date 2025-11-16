# custom imports
from opendrive.helpers.helper import now_utc
from .upload_schemas import FileDataSchema



# builtins imports
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, Relationship



if TYPE_CHECKING:
    from opendrive.account.models import User




class FileDataToBeStored(FileDataSchema, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)

    # back populate to User model
    user: Optional["User"] = Relationship(back_populates="files")


