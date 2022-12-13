from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import home_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(
    home_router.router,
    responses={404: {'description': 'not found!'}}
)
