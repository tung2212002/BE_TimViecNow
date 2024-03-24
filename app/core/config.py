import os
from pydantic_settings import BaseSettings
from typing import List

from app.core.constant import (
    MYSQL_SERVER,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_DATABASE,
)


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    API_PREFIX: str = ""
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    DATABASE_URL: str = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        MYSQL_USER,
        MYSQL_PASSWORD,
        MYSQL_SERVER,
        MYSQL_PORT,
        MYSQL_DATABASE,
    )
    ACCESS_TOKEN_EXPIRE_SECONDS: int = os.getenv("ACCESS_TOKEN_EXPIRE")
    REFRESH_TOKEN_EXPIRE_SECONDS: int = os.getenv("REFRESH_TOKEN_EXPIRE")
    SECURITY_ALGORITHM: str = os.getenv("SECURITY_ALGORITHM")
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    FIRST_SUPERUSER_PHONE_NUMBER: str = os.getenv("FIRST_SUPERUSER_PHONE_NUMBER")


settings = Settings()
