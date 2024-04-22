from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)

from fastapi import FastAPI
from dotenv import load_dotenv
from os.path import dirname, join
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.base import engine, get_db
from app.db.base_class import Base
from app.db.init_db import init_db
from app.storage.s3 import s3_service

from app.api import api_router

Base.metadata.create_all(bind=engine)
init_db(next(get_db()))

app = FastAPI(title="TVNow", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

app.include_router(api_router)
