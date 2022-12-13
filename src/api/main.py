from fastapi import FastAPI


from api.constants.mapped_prefix import MAPPED_API_ENDPOINT_PREFIX
from api.routers import auth_router, user_router

from database.connection import database

api = FastAPI()


@api.on_event("startup")
async def startup():
    await database.connect()


@api.on_event("shutdown")
async def shutdown():
    await database.disconnect()


api.include_router(
    user_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX['user'],
    tags=['user'],
    responses={404: {'description': 'not found!'}}
)
api.include_router(
    auth_router.router,
    tags=['auth'],
    responses={404: {'description': 'not found!'}}
)
