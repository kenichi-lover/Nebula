from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.config.database  import (
    create_db_and_tables
)
from app.routers.board import (
    router as board_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(board_router)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


@app.get("/", name = "home")
async def dashboard():
    return {"message": "Hello, World!"}

