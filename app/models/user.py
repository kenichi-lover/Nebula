from sqlmodel import SQLModel, Field

class Notice(SQLModel, table=True):

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    title: str

    content: str

    priority: str = "low"

    category: str = "General"

    pinned: bool = False
