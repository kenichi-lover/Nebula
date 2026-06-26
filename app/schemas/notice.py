from pydantic import BaseModel


class NoticeCreate(BaseModel):

    title: str

    content: str

    category: str = "General"

    priority: str = "normal"


class NoticeRead(BaseModel):

    id: int

    title: str

    slug: str

    content: str

    category: str

    priority: str

    pinned: bool
