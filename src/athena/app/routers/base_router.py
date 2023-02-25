from enum import StrEnum

from typing import Any


from fastapi import Request
from fastapi.templating import Jinja2Templates


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


templates = Jinja2Templates(directory="app/templates")


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
    context_request: dict[str, Any] = {},
    headers: dict[str, Any] | None = None
):
    context_request['request'] = request
    return templates.TemplateResponse(
        template_name,
        context_request,
        status_code=status_code,
        headers=headers
    )

templates.env.globals['get_flash_messages'] = get_flash_messages
