from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.db.base_class import Base


class Blacklist(Base):
    token = Column(String(500), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
