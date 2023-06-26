from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from .base_router import async_render_template

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    url = get_env_var('ATHENA_ARES_BASE_URL')
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section', params={'is_visible': True}
    )) and response.is_success:
        sections = response.json()
    else:
        sections = []
    return await async_render_template(
        'index_template.html', request,
        context_request={'sections': sections})
