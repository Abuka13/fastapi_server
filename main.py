import contextlib
import sqlite3

from fastapi import FastAPI, Request, Form
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/home", response_class=HTMLResponse)
async def root(request: Request):
    context = "Добро пожаловать на домашнюю страницу"
    return templates.TemplateResponse("home.html", {"request": request, "context" : context})


@app.get("/list", response_class=HTMLResponse)
async def list(request: Request):
    with contextlib.closing(sqlite3.connect('database/database.db')) as connection:
        with connection as cursor:
            rows = cursor.execute("""
                SELECT id, title, description, status FROM todo
                ORDER BY id DESC
                """)
            records: list[tuple] = rows.fetchall()
            todos = [
                {"id": row[0], "title": row[1], "description": row[2], "status": row[3]}
                for row in records
            ]

    return templates.TemplateResponse("list.html", {"request": request, "todos": todos})
@app.get("/create", response_class=HTMLResponse)
async def create_get(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_post(request: Request):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")
    status = True if form.get("status") == "on" else False
    print(f"Received form data: title={title}, description={description}, status={status}")
    with contextlib.closing(sqlite3.connect('database/database.db')) as connection:
        with connection as cursor:
            cursor.execute("""
                INSERT INTO todo (title, description, status) VALUES (?, ?, ?);
                """, (title, description, status))

    return RedirectResponse(url='/list', status_code=301)

