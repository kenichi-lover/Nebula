from sqlmodel import SQLModel
from .notice import Notice
from .user import User

__all__ = ["SQLModel", "User", "Notice"]
# 以后有新模型继续加这里