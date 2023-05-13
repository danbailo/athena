from enum import StrEnum

from math import ceil

from typing import Any


from fastapi import Request
from fastapi.templating import Jinja2Templates

import regex


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


def url_for_query(request: Request, name: str, **params: str) -> str:
    url = request.url_for(name)
    return url.include_query_params(**params)


def get_last_page(total_itens: int, limit: int):
    return ceil(total_itens/limit)


templates.env.globals['get_flash_messages'] = get_flash_messages
templates.env.globals['get_endpoint'] = get_endpoint
templates.env.globals['get_last_page'] = get_last_page
templates.env.globals['url_for_query'] = url_for_query
templates.env.globals['dir'] = dir
