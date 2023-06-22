from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from .base_router import async_render_template, init_section, init_subsection

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    url = get_env_var('ATHENA_ARES_BASE_URL')

    about_section = await init_section('Sobre')
    about_subsections = await init_subsection()

    devs_section = await init_section('Devs')
    devs_subsections = await init_subsection()

    about_section_slug = 'sobre'
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section/{about_section_slug}'
    )) and response.is_success:
        about_section = response.json()
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section/{about_section_slug}/subsection',
    )) and response.is_success:
        about_subsections = response.json()

    devs_section_slug = 'devs'
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section/{devs_section_slug}'
    )) and response.is_success:
        devs_section = response.json()
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section/{devs_section_slug}/subsection',
    )) and response.is_success:
        devs_subsections = response.json()

    return await async_render_template(
        'index_template.html', request,
        context_request={
            'about_section': about_section,
            'about_subsections': about_subsections,
            'devs_section': devs_section,
            'devs_subsections': devs_subsections
        })
