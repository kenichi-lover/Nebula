from datetime import datetime
from typing import Sequence

from sqlmodel import select, func, or_

from app.models.notice import Notice

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.schemas.notice import NoticeCreate

from app.utils.slug import generate_slug

async def get_all_notices(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
) -> tuple[Sequence[Notice], int]:
    """
    返回: (当前页数据列表, 总条数)
    """
    # 基础过滤条件
    base_where = [
        Notice.published.is_(True),
        Notice.is_deleted.is_(False)
    ]

    if search:
        keyword = f"%{search}%"
        base_where.append(
            Notice.title.ilike(keyword) |
            Notice.content.ilike(keyword)
        )

    count_stmt = (
        select(func.count())
        .select_from(Notice)
        .where(*base_where)
    )
    total = await session.execute(count_stmt)
    total_count = total.scalar_one() or 0

    stmt = (
        select(Notice)
        .where(*base_where)
        .order_by(Notice.pinned.desc(), Notice.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    result = await session.execute(stmt)
    items = result.scalars().all()
    return items, total_count

async def get_notice_by_id(
        session: AsyncSession,
        notice_id: int
) -> Notice | None:
    result = await session.execute(
        select(Notice)
        .where(
            Notice.id == notice_id,
            Notice.is_deleted.is_(False)
        )
    )
    return result.scalar_one_or_none()

async def get_notice_by_slug(
        session: AsyncSession,
        slug: str
) -> Notice | None:
    result = await session.execute(
        select(Notice)
        .where(
            Notice.slug == slug,
            Notice.is_deleted.is_(False)
        )
    )
    return result.scalar_one_or_none()


async def update_notice(
        session: AsyncSession,
        notice: Notice
) -> Notice:
    notice.updated_at = datetime.now()
    session.add(notice)
    await session.commit()
    await session.refresh(notice)
    return notice

async def delete_notice(
        session: AsyncSession,
        notice: Notice
) -> None:
    notice.is_deleted = True
    notice.updated_at = datetime.now()
    await session.commit()


async def create_notice(
        session: AsyncSession,
        data: NoticeCreate
) -> Notice:
    slug = generate_slug(data.title)
    existing_notice = await get_notice_by_slug(session, slug)
    if existing_notice:
        slug = f"{slug}-{int(datetime.now().timestamp())}"
    notice = Notice(
        title=data.title,
        slug=slug,
        content=data.content,
        published=data.published,
        pinned=data.pinned,
        category=data.category,
        priority=data.priority
)
    session.add(notice)
    await session.commit()
    await session.refresh(notice)
    return notice

async def get_notices_by_slug(
    session: AsyncSession,
    slug: str
) -> Notice | None:
    result = await session.execute(
        select(Notice)
        .where(
            Notice.slug == slug,
            Notice.is_deleted.is_(False)
        )
    )
    return result.scalar_one_or_none()


