import os
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Project information
    PROJECT_NAME: str
    SECRET_KEY: str
    API_PREFIX: str = ""
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    # Database information
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_SERVER: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
    # Token information
    ACCESS_TOKEN_EXPIRE: int
    REFRESH_TOKEN_EXPIRE: int
    SECURITY_ALGORITHM: str
    # Superuser information
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_PHONE_NUMBER: str
    # Server mail infomation
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    # Google OAuth2 information
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_PROJECT_ID: str
    GOOGLE_AUTH_URI: str
    GOOGLE_TOKEN_URI: str
    GOOGLE_AUTH_PROVIDER_X509_CERT_URL: str
    GOOGLE_REDIRECT_URI: str
    GOOGLE_JAVASCRIPT_ORIGIN: str
    # AWS S3 information
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str
    AWS_BUCKET_NAME: str
    # Redis information
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int
    REDIS_EXPIRE: int

    class Config:
        env_file = ".env"


settings = Settings()
