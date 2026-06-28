from datetime import datetime

from pydantic import BaseModel, ConfigDict

class NoticeBase(BaseModel):
    """公共字段，无默认值"""
    title: str
    content: str
    category: str
    priority: str
    pinned: bool
    published: bool

class NoticeCreate(NoticeBase):
    """创建时给默认值"""
    category: str = "General"
    priority: str = "normal"
    pinned: bool = False
    published: bool = True


class NoticeRead(NoticeBase):
    """读取时继承无默认值的基类"""
    id: int
    slug: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class NoticeDetailRead(NoticeRead):
    """详情页继承 Read,追加 updated_at"""
    updated_at: datetime

