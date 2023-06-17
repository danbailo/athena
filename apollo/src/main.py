from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles

from pydantic import ValidationError

from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware


from extensions.env_var import get_env_var

from middlewares.auth_backend_middleware import OAuth2Backend

from routers import home_router, user_router, admin_router

from utils.exception_handler_util import (
    async_403_http_error_exception_handler,
    async_404_http_error_exception_handler,
    async_validation_error_exception_handler
)

app = FastAPI(docs_url=None, redoc_url=None)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         'http://localhost',
#         'http://localhost:8001',
#         'https://localhost',
#         'https://localhost:8001',
#         'http://athena-project.dev',
#         'https://athena-project.dev',
#     ],
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*']
# )
# app.add_middleware(HTTPSRedirectMiddleware)

app.add_middleware(SessionMiddleware, secret_key=get_env_var('SECRET_KEY'))
app.add_middleware(AuthenticationMiddleware, backend=OAuth2Backend())

app.add_exception_handler(403, async_403_http_error_exception_handler)
app.add_exception_handler(404, async_404_http_error_exception_handler)
app.add_exception_handler(ValidationError,
                          async_validation_error_exception_handler)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(home_router.router)
app.include_router(admin_router.router)
app.include_router(user_router.router)
