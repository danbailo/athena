
from dataclasses import dataclass, field


from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError


@dataclass
class BaseAuthHTTPException(HTTPException):
    headers: dict[str, str] = field(
        default_factory=lambda: {'WWW-Authenticate': 'Bearer'}
    )


@dataclass
class GetUserError(BaseAuthHTTPException):
    detail: str = field(default='Não foi possível validar as credenciais',
                        init=True)
    status_code: status = status.HTTP_401_UNAUTHORIZED


@dataclass
class TokenError(BaseAuthHTTPException):
    detail: str = field(default='Usuário ou senha inválidos!', init=True)
    status_code: status = status.HTTP_401_UNAUTHORIZED


@dataclass
class LoginError(BaseAuthHTTPException):
    detail: str = field(default='Usuário ou senha inválidos!', init=True)
    status_code: status = status.HTTP_400_BAD_REQUEST


@dataclass
class InactiveUserError(BaseAuthHTTPException):
    detail: str = field(default='Usuário inativo', init=True)
    status_code: status = status.HTTP_400_BAD_REQUEST


@dataclass
class UserNotFoundError(HTTPException):
    detail: str = field(default='Usuário não encontrado!', init=True)
    status_code: status = status.HTTP_404_NOT_FOUND


@dataclass
class ItemNotFoundError(HTTPException):
    detail: str = field(default='Item não encontrado!', init=True)
    status_code: status = field(default=status.HTTP_404_NOT_FOUND, init=False)


@dataclass
class NothingToPatchError(HTTPException):
    detail: str = field(default='Nada para atualizar!', init=True)
    status_code: status = status.HTTP_400_BAD_REQUEST


@dataclass
class NotAuthorizedError(HTTPException):
    detail: str = field(default='Não autorizado!', init=True)
    status_code: status = status.HTTP_403_FORBIDDEN


@dataclass
class NotPossibleDeleteAdmin(HTTPException):
    detail: str = field(
        default='Não é possível deletar um usuário administrador!', init=True)
    status_code: status = status.HTTP_406_NOT_ACCEPTABLE


async def validation_error_handler(
    request: Request, exc: ValidationError
):
    return JSONResponse(content=jsonable_encoder({'detail': exc.errors()}),
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
