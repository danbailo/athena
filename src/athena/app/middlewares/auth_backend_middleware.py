from jose import jwt, ExpiredSignatureError, JWTError

from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, SimpleUser
)


from extensions.env_var import get_env_var


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
        except (ExpiredSignatureError, JWTError):
            return
        username = payload.get('sub')
        return AuthCredentials(['authenticated']), SimpleUser(username)
