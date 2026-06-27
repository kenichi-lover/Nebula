from fastapi import APIRouter,Request, Form, Depends    
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.notice_service import (
    create_notice
)
from app.config.database import get_session
from app.schemas.notice import NoticeCreate

router = APIRouter(
    prefix="/notice",
    tags=["notice"]
)

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/new", name="notice_create")
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
    title: str = Form(...),
    category: str = Form(...),
    priority: str = Form(...),
    content: str = Form(...),
    pinned: bool = Form(False),
    session: AsyncSession = Depends(get_session)
):
    notice_data = NoticeCreate(
        title=title,
        category=category,
        priority=priority,
        content=content,
        pinned=pinned
    )
    await create_notice(session, notice_data)
    return RedirectResponse(url="/", status_code=303)