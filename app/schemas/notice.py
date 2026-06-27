from datetime import datetime

from pydantic import BaseModel


class NoticeCreate(BaseModel):

    title: str

    content: str

    category: str = "General"

    priority: str = "normal"

    pinned: bool = False

    published: bool = True


class NoticeRead(BaseModel):

    id: int

    title: str

    slug: str

    content: str

    category: str

    priority: str

    pinned: bool

    published: bool

    created_at: datetime