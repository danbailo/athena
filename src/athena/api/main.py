from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from constants.mapped_api_prefix import (
    EndPointEnum, MAPPED_API_ENDPOINT_PREFIX
)

from .database.connection import database

from .routers import auth_router, admin_router, user_router

api = FastAPI()


@api.on_event("startup")
async def startup():
    await database.connect()


@api.on_event("shutdown")
async def shutdown():
    await database.disconnect()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8001",
        "https://localhost",
        "https://localhost:8001",
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

api.include_router(
    admin_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.admin],
    tags=['admin']
)
api.include_router(
    auth_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.auth],
    tags=['auth']
)
api.include_router(
    user_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.user],
    tags=['user']
)
