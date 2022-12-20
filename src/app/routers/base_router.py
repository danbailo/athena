from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates


from serializers.context_serializer import AlertTypeEnum, ContextSerializer

templates = Jinja2Templates(directory="app/templates")


async def async_render_template(
    template_name: str, context_request: Request, status_code: int,
    alert_msg: str = '', alert_type: AlertTypeEnum | None = None,
    exc: HTTPException | None = None, headers: dict[str, str] | None = None
):
    if exc:
        alert_msg += getattr(exc, 'detail', None) or str(exc)
    return templates.TemplateResponse(
        template_name,
        ContextSerializer(
            request=context_request,
            msg=alert_msg,
            alert_type=alert_type
        ).dict(),
        status_code=status_code,
        headers=headers
    )
