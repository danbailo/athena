from fastapi import Request
from fastapi.templating import Jinja2Templates


from serializers.context_serializer import AlertTypeEnum, ContextSerializer

templates = Jinja2Templates(directory="app/templates")


async def render_template(
    template_name: str, context_request: Request, status_code: int,
    alert_msg: str | None = None, alert_type: AlertTypeEnum | None = None,
    headers: dict[str, str] | None = None
):
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


async def render_404_error_template(
    context_request: Request, err: Exception | None = None
):
    msg = 'Unexpected error'
    if err:
        msg += f' - {err}'
    return templates.TemplateResponse(
        '404_template.html',
        ContextSerializer(
            request=context_request,
            msg=msg,
            alert_type=AlertTypeEnum.danger
        ).dict(),
        status_code=404
    )
