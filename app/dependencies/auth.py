from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.models.user import User
from app.services.user_service import get_user_by_id
from app.utils.jwt import decode_access_token

# auto_error=False：没有 Header 时不自动报错，让我们自己处理
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,  # 用于读取 Cookie
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> User:
    
    """从 JWT token 获取当前登录用户。"""
    token = None
    if credentials:
        token = credentials.credentials
    else:
        token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    payload = decode_access_token(token)
    user_id = int(payload.get("sub"))
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    return user
    


async def require_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """要求当前用户必须是管理员。"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user