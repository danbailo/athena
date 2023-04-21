from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from constants.mapped_api_prefix import (
    EndPointEnum, MAPPED_API_ENDPOINT_PREFIX
)

from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from .base_router import async_render_template

router = APIRouter(prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.home])


@router.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    if (section := await async_fetch(
        MethodEnum.get, f'{get_env_var("ATHENA_API_BASE_URL")}/section',
        params={'title_slug': 'my-first-section'}
    )) and section.json():
        section = section.json()[0]
    else:
        section = {'title': 'My First Section', 'body': 'lorem ipsum'}
    return await async_render_template(
        'index_template.html', request,
        context_request={'section': section}
    )
