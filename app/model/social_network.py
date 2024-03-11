from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import SocialType
from app.model.user import User


class SoicalNetwork(Base):
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    type = Column(Enum(SocialType))
    social_id = Column(String(100), nullable=True)
