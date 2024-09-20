# from os.path import dirname, join
# from dotenv import load_dotenv

# dotenv_path = join(dirname(dirname(__file__)), ".env")
# load_dotenv(dotenv_path)
from app.core.config import settings
from fastapi import FastAPI
from dotenv import load_dotenv
from os.path import dirname, join
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.db.base import engine, get_db
from app.db.base_class import Base
from app.db.init_db import init_db
from app.storage.s3 import s3_service
from app.storage.redis import redis_dependency
from app.core.loggers import get_logger, setup_logging
from app.core import loggers

from app.api import api_router

logger = get_logger(__name__)


def enable_logging():
    setup_logging()
    logger.success(msg="Logging setup successfully")


async def check_sync_engine():
    logger.debug(msg="Checking sync engine")
    # do something with sync engine


async def check_async_engine():
    logger.debug(msg="Checking async engine")
    # do something with async engine


async def setup_redis():
    logger.debug(msg="Setting up Redis")
    # do something with Redis


async def setup_s3():
    logger.debug(msg="Setting up S3")
    # do something with S3


async def disable_all_connections():
    logger.debug(msg="Disabling all connections with MySQL")
    # do something with MySQL


async def disable_all_redis_connections():
    logger.debug(msg="Disabling all connections with Redis")
    # do something with Redis


async def disable_all_s3_connections():
    logger.debug(msg="Disabling all connections with S3")
    # do something with S3


@asynccontextmanager
async def lifespan(app: FastAPI):
    enable_logging()
    logger.info(msg="Starting application")
    await setup_redis()
    await setup_s3()
    await check_sync_engine()
    await check_async_engine()
    # Startup event
    print("Redis connection opened")
    init_db(next(get_db()))
    await redis_dependency.init()
    yield
    # Shutdown event
    print("Redis connection closed")
    await disable_all_connections()
    await disable_all_redis_connections()
    await redis_dependency.close()
    await disable_all_s3_connections()
    logger.info(msg="Shutting down application")


# Base.metadata.create_all(bind=engine)

app = FastAPI(
    debug=settings.DEBUG,
    title="TVNow",
    description="TVNow API",
    version="0.0.1",
    openapi_url=(
        f"{settings.API_PREFIX}/openapi.json" if settings.ENABLE_OPENAPI else None
    ),
    redoc_url=None,
    docs_url="/docs" if settings.ENABLE_OPENAPI else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGIN,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app.__main__:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
        reload_delay=10,
        reload_dirs=["app"],
        reload_includes=[".env", "*.py"],
        log_level=settings.LOG_LEVEL,
        log_config=loggers.LOGGING_CONFIG,
        date_header=False,
        server_header=False,
    )
