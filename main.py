# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

table_01 = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z']
    },
    index=[11, 22, 33])


def get_main_table():
    # Пример DataFrame
    df = pd.DataFrame({
        'A': [1, 2, 3],
        'B': ['x', 'y', 'z']
    }, index=[11, 22, 33])
    # Получаем HTML-таблицу
    return df.to_html(classes='table table-striped', index=True)


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    table_html = get_main_table()
    return templates.TemplateResponse(
        "main.html",
        {"request": request, "table_html": table_html}
    )
