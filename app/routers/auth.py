from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.schemas.user import UserCreate, UserLogin, UserRead, TokenResponse
from app.services import user_service
from app.utils.jwt import create_access_token
from app.utils.security import verify_password
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    """用户注册。默认 is_active=True, is_superuser=False。"""
    # 检查用户名
    existing = await user_service.get_user_by_username(session, data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    
    # 检查邮箱
    existing = await user_service.get_user_by_email(session, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    user = await user_service.create_user(
        session=session,
        username=data.username,
        email=data.email,
        password=data.password,
    )
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,   # 用于设置 Cookie
    data: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    """用户登录，返回 JWT token。"""
    user = await user_service.get_user_by_username(session, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # 在生产环境中应设置为 True
        max_age=3600,  # 1 hour
        path="/",
        samesite="lax",
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )

@router.post("/logout")
async def logout(response: Response):
    """登出，清除 Cookie。"""
    response.delete_cookie(key="access_token")
    return {"message": "Logged out"}

@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """获取当前登录用户信息。"""
    return current_user