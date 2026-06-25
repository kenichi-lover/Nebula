from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

demo_cards = [
    {
        "title":"Technical Weekly Meeting",
        "content":"All staff tech meeting at 3PM",
        "priority":"high",
        "category":"Tech",
        "time":"09:00"
    },
    {
        "title":"Security Drill Notice",
        "content":"Friday 14:00 Fire Drill",
        "priority":"medium"
    }
]

@app.get("/", name = "home")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "board.html",
        context = {
            "cards": demo_cards
        }
    )