from fastapi import APIRouter,Depends,Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_session
from app.services.notice_service import (
    get_all_notices
)

router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get("/")
async def dashboard(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    cards = await get_all_notices(session)
    return templates.TemplateResponse(
        request=request,
        name="board.html",
        context={
            "cards": cards
        }
    )
