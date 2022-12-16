from fastapi import APIRouter, Request


from serializers.context_serializer import AlertTypeEnum, ContextSerializer


from .base_router import templates

router = APIRouter()


@router.get('')
async def logout(request: Request):
    response = templates.TemplateResponse(
        'login_template.html',
        ContextSerializer(
            request=request,
            msg='Successfully logged out!',
            alert_type=AlertTypeEnum.success
        ).dict(),
        status_code=302
    )
    response.delete_cookie(key='access_token')
    return response
