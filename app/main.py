from fastapi import FastAPI
from dotenv import load_dotenv
from os.path import dirname, join
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.base import engine, get_db
from app.db.base_class import Base
from app.db.init_db import init_db

from app.api import api_router

Base.metadata.create_all(bind=engine)
# AttributeError: 'generator' object has no attribute 'query'
init_db(next(get_db()))
# fix


app = FastAPI(title="DATN", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

app.include_router(api_router)
