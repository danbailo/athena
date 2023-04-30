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
    about_section = 'sobre'
    url = get_env_var("ATHENA_API_BASE_URL")
    if (about := await async_fetch(
        MethodEnum.get, f'{url}/section',
        params={'title_slug': about_section}
    )) and about.is_success:
        about = about.json()[0]
    if (about_subsections := await async_fetch(
        MethodEnum.get, f'{url}/section/{about_section}/subsection',
    )) and about_subsections.is_success:
        about_subsections = about_subsections.json()

    return await async_render_template(
        'index_template.html', request,
        context_request={'about': about,
                         'about_subsections': about_subsections}
    )
