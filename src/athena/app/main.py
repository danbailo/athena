from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.authentication import AuthenticationMiddleware

from .middlewares.auth_backend_middleware import OAuth2Backend
from .middlewares.flash_message_middleware import FlashMessageMiddleware

from .routers import home_router, user_router

from .utils.exception_handler_util import (
    async_403_http_error_exception_handler,
    async_404_http_error_exception_handler,
)

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(FlashMessageMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=OAuth2Backend())

app.add_exception_handler(403, async_403_http_error_exception_handler)
app.add_exception_handler(404, async_404_http_error_exception_handler)

app.mount('/static', StaticFiles(directory='app/static'), name='static')

app.include_router(home_router.router)
app.include_router(user_router.router)
