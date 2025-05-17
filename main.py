from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pathlib import Path
from temp import get_main_table

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    df_summary = get_main_table()
    table_html = df_summary.to_html(classes="table table-striped", index=False, border=0)
    return templates.TemplateResponse("main.html", {"request": request, "table": table_html})
