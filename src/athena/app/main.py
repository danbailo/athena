from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware


from extensions.env_var import get_env_var

from .middlewares.auth_backend_middleware import OAuth2Backend

from .routers import home_router, user_router

from .utils.exception_handler_util import (
    async_403_http_error_exception_handler,
    async_404_http_error_exception_handler,
)

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(SessionMiddleware, secret_key=get_env_var('SECRET_KEY'))
app.add_middleware(AuthenticationMiddleware, backend=OAuth2Backend())

app.add_exception_handler(403, async_403_http_error_exception_handler)
app.add_exception_handler(404, async_404_http_error_exception_handler)

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(home_router.router)
app.include_router(user_router.router)
