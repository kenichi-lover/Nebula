from datetime import datetime

from sqlmodel import select

from app.models.notice import Notice

from sqlalchemy.ext.asyncio.session import AsyncSession

from app.schemas.notice import NoticeCreate

from app.utils.slug import generate_slug

async def get_all_notices(
    session: AsyncSession
) -> list[Notice]:

    result = await session.execute(
        select(Notice)
        .where(
            Notice.published.is_(True)
        )
        .order_by(
            Notice.pinned.desc(),
            Notice.created_at.desc()
        )
    )
    return result.scalars().all()


async def get_notice_by_id(
        session: AsyncSession,
        notice_id: int
) -> Notice | None:
    result = await session.execute(
        select(Notice)
        .where(
            Notice.id == notice_id
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
            Notice.slug == slug
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
    await session.delete(notice)
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
            Notice.slug == slug
        )
    )
    return result.scalar_one_or_none()