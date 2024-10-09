from sqlalchemy import Column, ForeignKey, Integer, Enum, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import Provider, Role, TypeAccount


class SocialNetwork(Base):
    type = Column(Enum(Provider), nullable=False, index=True)
    social_id = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    access_token = Column(String(500), nullable=False)
    id = Column(Integer, ForeignKey("user.id"), primary_key=True)

    user = relationship("User", back_populates="social_network")
