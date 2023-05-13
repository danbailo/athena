from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from constants.mapped_api_prefix import (
    EndPointEnum, MAPPED_API_ENDPOINT_PREFIX
)

from .database.connection import database

from .routers import auth_router, admin_router, user_router, section_router

from extensions.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug('started api')
    await database.connect()
    yield
    logger.debug('shutdown api')
    await database.disconnect()


api = FastAPI(lifespan=lifespan)

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
api.include_router(
    section_router.router,
    prefix=MAPPED_API_ENDPOINT_PREFIX[EndPointEnum.section],
    tags=['section']
)
