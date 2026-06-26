from datetime import datetime, UTC

from sqlmodel import SQLModel, Field


class Notice(SQLModel, table=True):

    __tablename__ = "notices"

    id: int | None = Field(
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

    pinned: bool = False

    published: bool = True

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
