import logging

from fastapi import APIRouter, HTTPException,Request, Form, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.notice_service import (
    create_notice,
    get_notice_by_slug,
    delete_notice,
    get_all_notices
)
from app.config.database import get_session
from app.schemas.notice import NoticeCreate, NoticeRead

from app.utils.md_renderer import render_markdown
from app.utils.pagination import PaginatedResponse

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
        context={
            "mode": "create",
            "card": None
        }
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
        raise HTTPException(
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
    content_html = render_markdown(notice.content)
    return templates.TemplateResponse(
        request=request,
        name="notice_detail.html",
        context={"card": notice, "content_html": content_html}
    )


@router.get("/{slug}/edit", name="notice_edit_form")
async def edit_notice_form(
    slug: str,
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    notice = await get_notice_by_slug(session=session, slug=slug)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return templates.TemplateResponse(
        request=request,
        name="notice_form.html",
        context={
            "mode": "edit",
            "card": notice
        }
    )

@router.post("/{slug}/edit", name="notice_edit")
async def edit_notice(
    slug: str,
    title: str = Form(..., min_length=1, max_length=200),
    category: str = Form("General"),
    priority: str = Form("normal"),
    content: str = Form(..., min_length=1, max_length=1000),
    pinned: bool = Form(False),
    published: bool = Form(True),
    session: AsyncSession = Depends(get_session)
):
    notice = await get_notice_by_slug(session=session, slug=slug)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    try:
        notice.title = title
        notice.category = category
        notice.priority = priority
        notice.content = content
        notice.pinned = pinned
        notice.published = published
        
        await session.commit()
        
        return RedirectResponse(
            url=router.url_path_for("notice_detail", slug=notice.slug),
            status_code=303
        )
    except Exception as e:
        logger.error(f"Error updating notice: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while updating the notice."
        )
    

@router.post("/{slug}/delete", name="notice_delete")
async def delete_notice_view(
    slug: str,
    session: AsyncSession = Depends(get_session)
):
    notice = await get_notice_by_slug(session=session, slug=slug)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    try:
        await delete_notice(session, notice)
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        logger.error(f"Error deleting notice: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the notice."
        )


@router.get("", response_model=PaginatedResponse[NoticeRead])
async def list_notices(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    items, total = await get_all_notices(session=session, skip=skip, limit=limit)
    
    return PaginatedResponse[NoticeRead].create(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )