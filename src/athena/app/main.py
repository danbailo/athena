from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.authentication import AuthenticationMiddleware


from serializers.auth_serializer import OAuth2Backend

from .routers import home_router, user_router

from .utils.handle_exceptions_util import (
    handle_403_http_error, handle_404_http_error
)

app = FastAPI(docs_url=None, redoc_url=None)

app.add_middleware(AuthenticationMiddleware, backend=OAuth2Backend())

app.add_exception_handler(403, handle_403_http_error)
app.add_exception_handler(404, handle_404_http_error)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(home_router.router)
app.include_router(user_router.router)
