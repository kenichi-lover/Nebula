from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.config.database  import (
    create_db_and_tables
)

from app.routers.board import (
    router as board_router
)

from app.routers.notice import (
    router as notice_router
)

from app.routers.auth import (
    router as auth_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(board_router)
app.include_router(notice_router)
app.include_router(auth_router)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)
