from fastapi import FastAPI


from constants.mapped_prefix import EndPointEnum, MAPPED_API_ENDPOINT_PREFIX

from .database.connection import database

from .routers import auth_router, user_router


api = FastAPI()


@api.on_event("startup")
async def startup():
    await database.connect()


@api.on_event("shutdown")
async def shutdown():
    await database.disconnect()


api.include_router(
    auth_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.auth],
    tags=['auth'],
    responses={404: {'description': 'not found!'}}
)
api.include_router(
    user_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.user],
    tags=['user'],
    responses={404: {'description': 'not found!'}}
)
