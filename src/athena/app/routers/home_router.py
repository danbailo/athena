from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from constants.mapped_prefix import EndPointEnum, MAPPED_API_ENDPOINT_PREFIX

from .base_router import async_render_template

router = APIRouter(prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.home])


@router.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    return await async_render_template('home_template.html', request)
