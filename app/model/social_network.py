from sqlalchemy import Column, ForeignKey, Integer, Enum

from app.db.base_class import Base
from app.hepler.enum import SocialType


class SoicalNetwork(Base):
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    type = Column(Enum(SocialType), nullable=False, index=True)
