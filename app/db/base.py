import sys
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from typing import Generator, Annotated
from fastapi import Depends
from sqlalchemy.orm.session import Session


from app.core.config import settings
from app.core import constant
from app.core.loggers import logger

# engine = create_engine(
#     constant.DATABASE_URL,
#     pool_pre_ping=True,
#     pool_size=20,
#     max_overflow=100,
#     connect_args={"connect_timeout": 10},
# )
# engine.dialect.supports_sane_rowcount = engine.dialect.supports_sane_multi_rowcount = (
#     False
# )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def create_engine_and_session(url: str) -> Engine:
    try:
        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=100,
            connect_args={"connect_timeout": 10},
        )
    except Exception as e:
        logger.error(f"Failed to connect to Database: {e}")
        sys.exit(1)

    else:
        engine.dialect.supports_sane_rowcount = (
            engine.dialect.supports_sane_multi_rowcount
        ) = False
        db_session = sessionmaker(
            engine,
            expire_on_commit=False,
        )
        return engine, db_session


MYSQL_URL = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"

engine, SessionLocal = create_engine_and_session(MYSQL_URL)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
        logger.info("Close connection to database")


CurrentSession = Annotated[Session, Depends(get_db)]
# def get_db() -> Generator:


# def create_async_engine_and_session(url: str) -> Engine:
#     try:
#         engine = create_async_engine(
#             url,
#             pool_pre_ping=True,
#             pool_size=20,
#             max_overflow=100,
#             connect_args={"connect_timeout": 10},
#         )
#     except Exception as e:
#         logger.error(f"Failed to connect to Database: {e}")
#         sys.exit(1)

#     else:
#         engine.dialect.supports_sane_rowcount = (
#             engine.dialect.supports_sane_multi_rowcount
#         ) = False
#         db_session = async_sessionmaker(
#             engine,
#             expire_on_commit=False,
#             class_=AsyncSession,
#         )
#         return engine, db_session


# MYSQL_URL = f"mysql+aiomysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"

# async_engine, async_session = create_async_engine_and_session(MYSQL_URL)


# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session() as session:
#         try:
#             yield session
#         except Exception as e:
#             await session.rollback()
#             raise e
#         finally:
#             await session.close()


# CurrentSession = Annotated[AsyncSession, Depends(get_db)]
