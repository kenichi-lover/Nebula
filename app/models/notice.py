from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from app.models.user import User

class Notice(SQLModel, table=True):

    __tablename__ = "notices"

    id:  Optional[int] | None = Field(
        default=None,
        primary_key=True
    )

    title: str = Field(
        max_length=200,
        index=True
    )

    slug: str = Field(
        max_length=200,
        unique=True,
        index=True
    )

    content: str

    category: str = Field(
        default="General",
        max_length=50,
        index=True
    )

    priority: str = Field(
        default="normal",
        max_length=20
    )

    pinned: bool = Field(
        default=False
    )

    published: bool = Field(
        default=True
    )

    is_deleted: bool = Field(
        default=False,
        nullable=False
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )

    # 外键关系
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    author: Optional["User"] = Relationship(back_populates="notices")
