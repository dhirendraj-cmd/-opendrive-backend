# builtins
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# custom imports
from opendrive.helpers.helper import now_utc



class RefreshToken(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")
    token: str = Field(unique=True, index=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=now_utc)
    revoked: bool = Field(default=False)

    # back populates relationship to user
    user: "User" = Relationship(back_populates="refresh_tokens")