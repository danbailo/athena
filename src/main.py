from fastapi import FastAPI


from api.constants.mapped_prefix import MAPPED_ENDPOINT_PREFIX
from api.routers import auth_router, user_router

from database.connection import database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    user_router.router,
    prefix=MAPPED_ENDPOINT_PREFIX['user'],
    tags=['user'],
    responses={404: {'description': 'not found!'}}
)
app.include_router(
    auth_router.router,
    tags=['auth'],
    responses={404: {'description': 'not found!'}}
)
