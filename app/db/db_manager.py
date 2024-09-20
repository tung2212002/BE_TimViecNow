# from sqlalchemy import create_engine, Engine
# from sqlalchemy.ext.asyncio import AsyncEngine
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.orm import sessionmaker, scoped_session, Session
# from sqlalchemy.orm import Session


# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import Session


# from app.core.config import settings
# from app.core import constant


# class DBManager:
#     def __init__(self):
#         self.engine: AsyncEngine | None = None
#         self.sessio_maker = None
#         self.session = None

#     def init_db(self):
#         self.engine = create_async_engine(
#             constant.DATABASE_ASYNC_URL,
#             pool_size=100,
#             max_overflow=0,
#             pool_pre_ping=False,
#         )
#         self.session = sessionmaker(
#             autocommit=False, autoflush=False, bind=self.engine
#         )
#         self.session = async_scoped_session(self.session_maker, scopefunc=current_task)


# db_manager = DBManager()
