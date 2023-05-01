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
    url = get_env_var("ATHENA_API_BASE_URL")

    about_section_slug = 'sobre'
    if (about_section := await async_fetch(
        MethodEnum.get, f'{url}/section',
        params={'title_slug': about_section_slug}
    )) and about_section.is_success:
        about_section = about_section.json()[0]
    if (about_subsections := await async_fetch(
        MethodEnum.get, f'{url}/section/{about_section_slug}/subsection',
    )) and about_subsections.is_success:
        about_subsections = about_subsections.json()

    for_devs_section_slug = 'para-desenvolvedores'
    if (for_devs_section := await async_fetch(
        MethodEnum.get, f'{url}/section',
        params={'title_slug': for_devs_section_slug}
    )) and for_devs_section.is_success:
        for_devs_section = for_devs_section.json()[0]
    if (for_devs_subsections := await async_fetch(
        MethodEnum.get, f'{url}/section/{for_devs_section_slug}/subsection',
    )) and for_devs_subsections.is_success:
        for_devs_subsections = for_devs_subsections.json()

    return await async_render_template(
        'index_template.html', request,
        context_request={
            'about_section': about_section,
            'about_subsections': about_subsections,
            'for_devs_section': for_devs_section,
            'for_devs_subsections': for_devs_subsections
        })
