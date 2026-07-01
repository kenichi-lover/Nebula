from fastapi import APIRouter,Depends,Request, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_session
from app.services.notice_service import (
    get_all_notices
)
from app.utils.md_renderer import strip_markdown
 
router = APIRouter()


def _get_author_name(notice) -> str:
    if not notice.author:
        return "未知作者"
    return notice.author.full_name or notice.author.username

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/", name="board")
async def dashboard(
    request: Request,
    search: str | None = Query(None),
    session: AsyncSession = Depends(get_session)
):
    notices, total = await get_all_notices(
        session,
        skip=0,
        limit=100,
        search=search
        )
    cards = []
    for notice in notices:
        cards.append({
            "id": notice.id,
            "title": notice.title,
            "slug": notice.slug,
            "summary": strip_markdown(notice.content, max_length=150),
            "category": notice.category,
            "priority": notice.priority,
            "pinned": notice.pinned,
            "created_at": notice.created_at,
            "author_name": _get_author_name(notice),
        })
    return templates.TemplateResponse(
        request=request,
        name="board.html",
        context={
            "cards": cards,
            "total": total,
            "search": search or ""
        }
    )
