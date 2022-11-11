
from dataclasses import dataclass, field

from fastapi import HTTPException, status


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
