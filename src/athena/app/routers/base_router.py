from typing import Any


from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates


from serializers.context_serializer import (
    AlertTypeEnum, DefaultContextSerializer
)

templates = Jinja2Templates(directory="app/templates")


async def async_render_template(
    template_name: str, request: Request, status_code: int = 200,
    alert_msg: str = '', alert_type: AlertTypeEnum | None = None,
    exc: HTTPException | str | None = None,
    context_request: dict[str, Any] = {},
    headers: dict[str, Any] | None = None
):
    context_request['request'] = request
    if exc:
        alert_msg += getattr(exc, 'detail', None) or str(exc)
    context_request.update(
        DefaultContextSerializer(
            msg=alert_msg, alert_type=alert_type
        ).dict()
    )
    return templates.TemplateResponse(
        template_name,
        context_request,
        status_code=status_code,
        headers=headers
    )
