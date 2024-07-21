from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core import constant

engine = create_engine(
    constant.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=100,
    connect_args={"connect_timeout": 10},
)
engine.dialect.supports_sane_rowcount = engine.dialect.supports_sane_multi_rowcount = (
    False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
