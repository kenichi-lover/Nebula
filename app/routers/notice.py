import logging

from fastapi import APIRouter, HTTPException, Request, Form, Depends, Query, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.services.notice_service import (
    create_notice,
    get_notice_by_slug,
    delete_notice,
    get_all_notices,
    update_notice
)
from app.config.database import get_session
from app.schemas.notice import NoticeCreate, NoticeRead, NoticeUpdate

from app.utils.md_renderer import render_markdown
from app.utils.pagination import PaginatedResponse
from app.dependencies.auth import require_superuser, get_current_user
from app.models.notice import Notice
from app.models.user import User
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/notice",
    tags=["notice"]
)

templates = Jinja2Templates(
    directory="templates"
)

def check_notice_ownership(notice: Notice, current_user: User):
    """非超级用户只能操作自己的公告"""
    if not current_user.is_superuser and notice.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only manage your own notices."
        )
    
@router.get("/new", name="notice_create_from")
async def new_notice(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        request=request,
        name="notice_form.html",
        context={
            "mode": "create",
            "card": None
        }
    )

@router.post("/new", name="notice_create", response_class=RedirectResponse)
async def create_notice_view(
    request: Request,  # 获取请求上下文，便于在模板中使用
    title: str = Form(..., min_length=1, max_length=200),
    category: str = Form(
        "General",
        regex="^(General|System|Development|Security|Personal)$"# 优化：限制可选值
        ),
    priority: str = Form(
        "normal", 
        regex="^(low|normal|high)$"),  # 优化：限制可选值
    content: str = Form(..., min_length=1, max_length=1000),
    pinned: bool = Form(False),
    published: bool = Form(True),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)  # 未来：登录用户都能发布
):
    try:
        # 验证表单数据(可选，可移至 Pydantic 模型)
        if not title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty."
            )
        notice_data = NoticeCreate(
            title=title,
            category=category,
            priority=priority,
            content=content,
            pinned=pinned,
            published=published
        )
        notice = await create_notice(session, notice_data, author_id=current_user.id)
        # 确保 slug 存在（可选：create_notice 应自动生成）
        if not notice.slug:
            notice.slug = f"{notice.id}-{title.lower().replace(' ', '-')}"
            await session.commit()

        return RedirectResponse(
            url=router.url_path_for("notice_detail", slug=notice.slug),
            status_code=status.HTTP_303_SEE_OTHER
        )
    except Exception as e:
        logger.error(f"Error creating notice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    notice = await get_notice_by_slug(session=session, slug=slug)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    check_notice_ownership(notice, current_user)
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
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = (
        select(Notice)
        .where(Notice.slug == slug)
        .options(selectinload(Notice.author))
    )
    result = await session.execute(statement)
    notice = result.scalar_one_or_none()
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    check_notice_ownership(notice, current_user)

    try:
        notice_data = NoticeUpdate(
            title=title,
            category=category,
            priority=priority,
            content=content,
            pinned=pinned,
            published=published,
        )
        await update_notice(session, notice, notice_data)

        return RedirectResponse(
            url=router.url_path_for("notice_detail", slug=notice.slug),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except Exception as e:
        logger.error(f"Error updating notice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the notice.",
        )
    

@router.post("/{slug}/delete", name="notice_delete")
async def delete_notice_view(
    slug: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    notice = await get_notice_by_slug(session=session, slug=slug)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    check_notice_ownership(notice, current_user)
    try:
        await delete_notice(session, notice)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        logger.error(f"Error deleting notice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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

@router.get("/my", name="my_notices")
async def my_notices(
    request: Request,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_superuser)
):
    statement = (
        select(Notice)
        .where(Notice.user_id == current_user.id)
        .options(selectinload(Notice.author))
        .order_by(Notice.pinned.desc(), Notice.created_at.desc())
    )
    result = await session.execute(statement)
    notices = result.scalars().all()
    total = len(notices)

    return templates.TemplateResponse(
        request=request,
        name="board.html",
        context={
            "cards": notices,
            "total": total,
            "search": "",
            "my_notices": True,
        }
    )
"""
# 现在：只有 superuser 能发布
current_user=Depends(require_superuser)

# 未来：登录用户都能发布
current_user=Depends(get_current_user)

# 未来：特定角色能发布
current_user=Depends(require_role(["author", "admin"]))
"""