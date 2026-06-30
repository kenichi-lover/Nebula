from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # 登录标识（必须唯一）
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(index=True, unique=True, max_length=255)
    
    # 密码必须存哈希，绝不能存明文
    hashed_password: str = Field(max_length=255)
    
    # 用户资料
    full_name: Optional[str] = Field(default=None, max_length=100)
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    
    # 权限控制
    is_active: bool = Field(default=True)      # 是否可用（软禁启用）
    is_superuser: bool = Field(default=False)    # 管理员
    
    # 时间戳
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
