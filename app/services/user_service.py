from datetime import datetime

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.security import hash_password


async def create_user(
    session: AsyncSession,
    username: str,
    email: str,
    password: str,
) -> User:
    """创建新用户，密码自动哈希。
    
    调用方需先检查 username/email 是否已存在。
    """
    hashed_password = hash_password(password)
    
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_username(
    session: AsyncSession,
    username: str,
) -> User | None:
    """通过用户名查找用户（不区分大小写）。"""
    result = await session.execute(
        select(User).where(
            User.username.ilike(username)
        )
    )
    return result.scalar_one_or_none()


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    """通过邮箱查找用户（不区分大小写）。"""
    result = await session.execute(
        select(User).where(
            User.email.ilike(email)
        )
    )
    return result.scalar_one_or_none()


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    """通过 ID 查找用户。"""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def update_user_last_login(
    session: AsyncSession,
    user: User,
) -> User:
    """更新用户最后登录时间。"""
    user.updated_at = datetime.now()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


"""
| 改动                            | 说明                                         |
| ----------------------------- | ------------------------------------------ |
| 加类型注解                         | `session: AsyncSession`, `-> User \| None` |
| `.ilike()` 不区分大小写             | `Admin` 和 `admin` 视为同一用户，避免重复注册            |
| 新增 `get_user_by_id`           | JWT token 里存 user\_id，验证时需要                |
| 新增 `update_user_last_login`   | 记录登录时间，安全审计用                               |
| `updated_at` 用 `timezone.utc` | 和你模型里的 `default_factory` 保持一致              |

"""
