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
    # Project information
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    API_PREFIX: str = ""
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    # Database information
    DATABASE_URL: str = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        MYSQL_USER,
        MYSQL_PASSWORD,
        MYSQL_SERVER,
        MYSQL_PORT,
        MYSQL_DATABASE,
    )
    # Token information
    ACCESS_TOKEN_EXPIRE_SECONDS: int = os.getenv("ACCESS_TOKEN_EXPIRE")
    REFRESH_TOKEN_EXPIRE_SECONDS: int = os.getenv("REFRESH_TOKEN_EXPIRE")
    SECURITY_ALGORITHM: str = os.getenv("SECURITY_ALGORITHM")
    # Superuser information
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_EMAIL: str = os.getenv("FIRST_SUPERUSER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    FIRST_SUPERUSER_PHONE_NUMBER: str = os.getenv("FIRST_SUPERUSER_PHONE_NUMBER")
    # Server mail infomation
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_PORT: int = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    # Google OAuth2 information
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_PROJECT_ID: str = os.getenv("GOOGLE_PROJECT_ID")
    GOOGLE_AUTH_URI: str = os.getenv("GOOGLE_AUTH_URI")
    GOOGLE_TOKEN_URI: str = os.getenv("GOOGLE_TOKEN_URI")
    GOOGLE_AUTH_PROVIDER_X509_CERT_URL: str = os.getenv(
        "GOOGLE_AUTH_PROVIDER_X509_CERT_URL"
    )
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI")
    GOOGLE_JAVASCRIPT_ORIGIN: str = os.getenv("GOOGLE_JAVASCRIPT_ORIGINS")
    # AWS S3 information
    AWS_S3_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_REGION: str = os.getenv("AWS_DEFAULT_REGION")
    AWS_S3_BUCKET: str = os.getenv("AWS_BUCKET_NAME")


settings = Settings()
