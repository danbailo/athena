from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse


from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from .base_router import async_render_template

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def home_page(request: Request):
    url = get_env_var("ATHENA_ARES_BASE_URL")
    # TODO: melhorar rotas e respostas da api

    about_section = []
    about_subsections = []
    devs_section = []
    devs_subsections = []

    about_section_slug = 'sobre'
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section',
        params={'title_slug': about_section_slug}
    )) and response.is_success and (about_section := response.json()):
        about_section = about_section[0]
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section/{about_section_slug}/subsection',
    )) and response.is_success:
        about_subsections = response.json()

    devs_section_slug = 'devs'
    if (response := await async_fetch(
        MethodEnum.get, f'{url}/section',
        params={'title_slug': devs_section_slug}
    )) and response.is_success and (devs_section := response.json()):
        devs_section = devs_section[0]
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
