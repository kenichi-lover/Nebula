import logging

from fastapi import APIRouter, HTTPException,Request, Form, Depends    
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.notice_service import (
    create_notice,
    get_notice_by_slug
)
from app.config.database import get_session
from app.schemas.notice import NoticeCreate

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notice",
    tags=["notice"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/new", name="notice_create_from")
async def new_notice(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="notice_form.html",
        context={}
    )

@router.post("/new", name="notice_create")
async def create_notice_view(
    title: str = Form(..., min_length=1, max_length=200),
    category: str = Form("General"),
    priority: str = Form("normal"),
    content: str = Form(..., min_length=1, max_length=1000),
    pinned: bool = Form(False),
    published: bool = Form(True),
    session: AsyncSession = Depends(get_session)
):
    try:
        notice_data = NoticeCreate(
            title=title,
            category=category,
            priority=priority,
            content=content,
            pinned=pinned,
            published=published
        )
        notice = await create_notice(session, notice_data)
        return RedirectResponse(
            url=router.url_path_for("notice_detail", slug=notice.slug),
            status_code=303
        )
    except Exception as e:
        logger.error(f"Error creating notice: {e}")
        return HTTPException(
            status_code=500,
            detail="An error occurred while creating the notice."
        ) 



@router.get("/{slug}", name="notice_detail")
async def notice_detail(
    slug: str,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    # Implementation for fetching and displaying a specific notice
    notice = await get_notice_by_slug(session=session, slug=slug)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return templates.TemplateResponse(
        request=request,
        name="notice_detail.html",
        context={"card": notice}
    )