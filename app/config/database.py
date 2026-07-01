"""异步数据库引擎、连接池与会话管理。"""

from collections.abc import AsyncGenerator

from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import settings

from app.models.notice import Notice
from app.models.user import User
# 创建异步引擎（连接池由 asyncpg 内部维护）
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # 开发时可改为 True 查看 SQL
)

# 会话工厂（每次请求通过 get_session 获取独立会话）
async_session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖注入：为每次请求创建/关闭会话。"""
    async with async_session_factory() as session:
        try:
            yield session
            #await session.commit() 这里不做自动 commit ,避免响应发出后才发现异常
        except Exception:
            await session.rollback()
            raise

async def create_db_and_tables():

    async with engine.begin() as conn:

        await conn.run_sync(
            SQLModel.metadata.create_all
        )
