from jose import jwt, ExpiredSignatureError, JWTError

from pydantic import BaseModel

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, SimpleUser, UnauthenticatedUser
)


from extensions.env_var import get_env_var


class TokenResponseSerializer(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenDataSerializer(BaseModel):
    username: str | None = None


class OAuth2Backend(AuthenticationBackend):
    async def authenticate(self, conn):
        if 'access_token' not in conn.headers.get('cookie', ''):
            return
        auth = conn.headers['cookie'].split('=')[-1].strip('"')
        _, token = auth.split()
        try:
            payload = jwt.decode(
                token, get_env_var('SECRET_KEY'),
                algorithms=[get_env_var('ALGORITHM')]
            )
        except ExpiredSignatureError:
            return\
                AuthCredentials(["not_authenticated"]), UnauthenticatedUser()
        except JWTError:
            return
        username = payload.get("sub")
        return AuthCredentials(["authenticated"]), SimpleUser(username)
