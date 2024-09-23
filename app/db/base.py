import sys
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from typing import Generator


from app.core.config import settings
from app.core.loggers import logger


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
