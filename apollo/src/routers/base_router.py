from enum import StrEnum

from math import ceil

from typing import Any


from fastapi import Request
from fastapi.templating import Jinja2Templates

import regex


from extensions.env_var import get_env_var
from extensions.base_requests import _fetch, MethodEnum
from extensions.logger import logger


class AlertTypeEnum(StrEnum):
    primary = 'primary'
    secondary = 'secondary'
    success = 'success'
    danger = 'danger'
    warning = 'warning'
    info = 'info'
    light = 'light'
    dark = 'dark'


templates = Jinja2Templates(directory='templates')


async def flash(
    request: Request,
    message: str,
    alert_type: AlertTypeEnum = 'primary'
):
    if not request.session.get('athena-flash-messages'):
        request.session['athena-flash-messages'] = []
    request.session['athena-flash-messages'].append(
        {'message': message, 'alert_type': alert_type}
    )


def get_flash_messages(request: Request):
    logger.debug(request.session)
    return request.session.pop('athena-flash-messages')\
        if request.session.get('athena-flash-messages') else []


async def async_render_template(
    template_name: str, request: Request, status_code: int = 200,
    context_request: dict[str, Any] = None,
    headers: dict[str, Any] | None = None
):
    if context_request is None:
        context_request = {}
    context_request['request'] = request
    return templates.TemplateResponse(
        template_name,
        context_request,
        status_code=status_code,
        headers=headers
    )


def get_endpoint(request: Request):
    if match := regex.search(r'(\b\/\w+)', str(request.url), regex.I):
        return match[0]
    return ''


def url_for_query(
    request: Request,
    route: str,
    path_params: dict[str, any] | None = None,
    **query_params: str
) -> str:
    if path_params is None:
        path_params = {}
    url = request.url_for(route, **path_params)
    return url.include_query_params(**query_params)


def get_last_page(total_itens: int, limit: int):
    return ceil(total_itens/limit)


def url_for_path(request: Request, route: str, **path_params: str):
    return request.url_for(route, **path_params).path


def get_nav_visible_sections():
    url = get_env_var('ATHENA_ARES_BASE_URL')
    if (response := _fetch(
        MethodEnum.get, f'{url}/section', params={'is_visible': True}
    )) and response.is_success:
        sections = response.json()
    else:
        sections = []
    return filter(lambda x: x['visible'] is True, sections)


templates.env.globals['get_flash_messages'] = get_flash_messages
templates.env.globals['get_endpoint'] = get_endpoint
templates.env.globals['get_last_page'] = get_last_page
templates.env.globals['url_for_query'] = url_for_query
templates.env.globals['dir'] = dir
templates.env.globals['url_for_path'] = url_for_path
templates.env.globals['get_nav_visible_sections'] = get_nav_visible_sections
