from jose import jwt, ExpiredSignatureError, JWTError

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, SimpleUser
)


from extensions.base_requests import async_fetch, MethodEnum
from extensions.env_var import get_env_var

from serializers.auth_serializer import TokenRequestHeaders


class AthenaUser(SimpleUser):
    def __init__(
        self, username: str, name: str, email: str,
        *args, **kwargs
    ) -> None:
        self._username = username
        self._name = name
        self._email = email

    @property
    def username(self) -> str:
        return self._username

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email


class OAuth2Backend(AuthenticationBackend):
    async def authenticate(self, conn):
        if 'access_token' not in conn.headers.get('cookie', ''):
            return
        auth = TokenRequestHeaders(access_token=conn.headers['cookie'])
        _, token = auth.access_token.split()
        try:
            jwt.decode(
                token, get_env_var('SECRET_KEY'),
                algorithms=[get_env_var('ALGORITHM')]
            )
        except (ExpiredSignatureError, JWTError):
            return

        url = get_env_var("ATHENA_API_BASE_URL", raise_exception=True)
        response = await async_fetch(
            MethodEnum.post, f'{url}/auth/user/info', headers=auth
        )
        conn.scope["athena_user_is_admin"] = response['role'] == 'admin'
        return (
            AuthCredentials(['authenticated', response['role']]),
            AthenaUser(**response)
        )
