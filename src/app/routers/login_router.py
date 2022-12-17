from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, Response, RedirectResponse

from httpx import HTTPStatusError


from extensions.base_requests import async_fetch, MethodEnum

from serializers.context_serializer import AlertTypeEnum

from .base_router import (
    templates, render_template, render_404_error_template
)

from ..forms.login_form import LoginForm

router = APIRouter()


@router.get('/login', response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        'login_template.html',
        {'request': request}
    )


@router.post('/login', response_class=HTMLResponse)
async def login_user(
    request: Request,
    response: Response,
    form_data: LoginForm = Depends(LoginForm.as_form)
):
    try:
        user_token = await async_fetch(
            MethodEnum.post, 'http://127.0.0.1:8000/auth/token',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data=form_data.dict(by_alias=True)
        )
    except HTTPStatusError:
        return await render_template(
            'login_template.html', request, 401,
            'Incorrect Username or Password', AlertTypeEnum.warning,
        )
    except Exception as err:
        return await render_404_error_template(request, err)
    response.set_cookie(
        key="access_token", value=user_token['access_token'],
        httponly=True
    )
    return RedirectResponse(
        '/home', 302, response.headers
    )


@router.get('/logout')
async def logout():
    response = RedirectResponse(
        '/login', 302
    )
    response.delete_cookie(key='access_token')
    return response
