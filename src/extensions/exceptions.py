
from dataclasses import dataclass, field


from fastapi import HTTPException, status, Request
from fastapi.responses import RedirectResponse

from app.routers.base_router import render_template

from serializers.context_serializer import AlertTypeEnum


@dataclass
class BaseAuthHTTPException(HTTPException):
    headers: dict[str, str] = field(
        default_factory=lambda: {'WWW-Authenticate': 'Bearer'}
    )


@dataclass
class GetUserError(BaseAuthHTTPException):
    detail: str = field(default='Could not validate credentials', init=True)
    status_code: status = status.HTTP_401_UNAUTHORIZED


@dataclass
class TokenError(BaseAuthHTTPException):
    detail: str = field(default='Incorrect username or password', init=True)
    status_code: status = status.HTTP_401_UNAUTHORIZED


@dataclass
class LoginError(BaseAuthHTTPException):
    detail: str = field(default='Incorrect username or password', init=True)
    status_code: status = status.HTTP_400_BAD_REQUEST


@dataclass
class InactiveUserError(BaseAuthHTTPException):
    detail: str = field(default='Inactive user', init=True)
    status_code: status = status.HTTP_400_BAD_REQUEST


@dataclass
class UserNotFoundError(HTTPException):
    detail: str = field(default='User not found!', init=True)
    status_code: status = status.HTTP_404_NOT_FOUND


@dataclass
class NothingToPatchError(HTTPException):
    detail: str = field(default='Nothing to patch!', init=True)
    status_code: status = status.HTTP_400_BAD_REQUEST


async def handle_403_http_error(request: Request, exc: HTTPException):
    response = RedirectResponse('/user/login')
    response.headers['X-Unauthorized'] = 'Login before!'
    return response


async def handle_404_http_error(request: Request, exc: HTTPException):
    return await render_template(
        'errors/404_error.html', request, exc.status_code,
        alert_type=AlertTypeEnum.danger, exc=exc
    )
