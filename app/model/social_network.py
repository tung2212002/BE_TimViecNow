from sqlalchemy import Column, ForeignKey, Integer, Enum, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import Provider, Role, TypeAccount


class SocialNetwork(Base):
    type = Column(Enum(Provider), nullable=False, index=True)
    social_id = Column(String(50), nullable=False)
    full_name = Column(String(50), nullable=True)
    phone_number = Column(String(10), nullable=True)
    avatar = Column(String(255), nullable=True)
    email = Column(String(50), nullable=False)
    access_token = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), default=Role.SOCIAL_NETWORK)
    is_verified = Column(Boolean, default=False)
    type_account = Column(Enum(TypeAccount), default=TypeAccount.NORMAL)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates="social_network")
