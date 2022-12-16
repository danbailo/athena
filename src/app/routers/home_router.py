from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from .base_router import render_template

router = APIRouter()


@router.get('', response_class=HTMLResponse)
async def home(request: Request):
    return await render_template('home_template.html', request, 200)
