from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from constants.mapped_prefix import MAPPED_API_ENDPOINT_PREFIX

from .routers import home_router, login_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(
    home_router.router,
    prefix='/home',
    responses={404: {'description': 'not found!'}}
)
app.include_router(
    login_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX['user'],
    responses={404: {'description': 'not found!'}}
)
