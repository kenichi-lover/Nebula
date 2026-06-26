from sqlmodel import select

from app.models.notice import Notice


async def get_all_notices(
    session
):

    result = await session.execute(
        select(Notice)
        .where(
            Notice.published == True
        )
        .order_by(
            Notice.pinned.desc(),
            Notice.created_at.desc()
        )
    )

    return result.scalars().all()
