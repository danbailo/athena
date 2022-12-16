from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import home_router, login_router, logout_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


app.include_router(
    home_router.router,
    prefix='/home',
    responses={404: {'description': 'not found!'}}
)
app.include_router(
    login_router.router,
    prefix='/login',
    responses={404: {'description': 'not found!'}}
)
app.include_router(
    logout_router.router,
    prefix='/logout',
    responses={404: {'description': 'not found!'}}
)
